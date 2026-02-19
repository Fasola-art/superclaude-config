#!/bin/bash
# Oracle Cloud ARM 인스턴스 자동 생성 스크립트
# "Out of capacity" 에러 시 자동 재시도
set -euo pipefail

# === 설정 ===
COMPARTMENT_ID=""           # 실행 시 자동 조회
DISPLAY_NAME="sql-trading"
SHAPE="VM.Standard.A1.Flex"
OCPUS=2
MEMORY_GB=12
BOOT_VOLUME_GB=100
SSH_KEY_FILE="$HOME/.ssh/id_oracle.pub"
RETRY_INTERVAL=60           # 재시도 간격 (초)
MAX_RETRIES=1440            # 최대 재시도 (24시간)
IMAGE_ID=""                 # 자동 조회

export SUPPRESS_LABEL_WARNING=True

echo "=== Oracle Cloud ARM 인스턴스 자동 생성 ==="
echo "Shape: $SHAPE ($OCPUS OCPU, ${MEMORY_GB}GB RAM)"
echo ""

# 1. 인증 확인
echo "[1/4] OCI CLI 인증 확인..."
if ! oci iam region list --output json > /dev/null 2>&1; then
    echo "❌ OCI CLI 인증 실패"
    echo "  → OCI 콘솔에서 API 키를 등록했는지 확인하세요"
    echo "  → ~/.oci/config 설정을 확인하세요"
    exit 1
fi
echo "✅ 인증 성공"

# 2. Compartment 조회 (root compartment = tenancy)
echo "[2/4] Compartment 조회..."
TENANCY_ID=$(grep tenancy ~/.oci/config | head -1 | cut -d= -f2)
COMPARTMENT_ID="$TENANCY_ID"
echo "✅ Compartment: root (tenancy)"

# 3. AD (Availability Domain) 조회
echo "[3/4] Availability Domain 조회..."
AD_NAME=$(oci iam availability-domain list \
    --compartment-id "$COMPARTMENT_ID" \
    --query 'data[0].name' \
    --raw-output 2>/dev/null)
if [ -z "$AD_NAME" ]; then
    echo "❌ AD 조회 실패"
    exit 1
fi
echo "✅ AD: $AD_NAME"

# 4. Oracle Linux ARM 이미지 조회
echo "[4/4] ARM 이미지 조회..."
IMAGE_ID=$(oci compute image list \
    --compartment-id "$COMPARTMENT_ID" \
    --operating-system "Oracle Linux" \
    --operating-system-version "8" \
    --shape "$SHAPE" \
    --sort-by TIMECREATED \
    --sort-order DESC \
    --query 'data[0].id' \
    --raw-output 2>/dev/null)
if [ -z "$IMAGE_ID" ] || [ "$IMAGE_ID" = "None" ]; then
    # Ubuntu 시도
    IMAGE_ID=$(oci compute image list \
        --compartment-id "$COMPARTMENT_ID" \
        --operating-system "Canonical Ubuntu" \
        --operating-system-version "22.04" \
        --shape "$SHAPE" \
        --sort-by TIMECREATED \
        --sort-order DESC \
        --query 'data[0].id' \
        --raw-output 2>/dev/null)
fi
if [ -z "$IMAGE_ID" ] || [ "$IMAGE_ID" = "None" ]; then
    echo "❌ ARM 이미지를 찾을 수 없습니다"
    exit 1
fi
echo "✅ Image: $IMAGE_ID"

# 5. VCN + Subnet 조회 또는 생성
echo ""
echo "네트워크 설정 확인..."
VCN_ID=$(oci network vcn list \
    --compartment-id "$COMPARTMENT_ID" \
    --query 'data[0].id' \
    --raw-output 2>/dev/null)

if [ -z "$VCN_ID" ] || [ "$VCN_ID" = "None" ]; then
    echo "VCN 생성 중..."
    VCN_ID=$(oci network vcn create \
        --compartment-id "$COMPARTMENT_ID" \
        --cidr-block "10.0.0.0/16" \
        --display-name "sql-trading-vcn" \
        --dns-label "sqltrade" \
        --query 'data.id' \
        --raw-output 2>/dev/null)

    # Internet Gateway 생성
    IG_ID=$(oci network internet-gateway create \
        --compartment-id "$COMPARTMENT_ID" \
        --vcn-id "$VCN_ID" \
        --is-enabled true \
        --display-name "sql-trading-ig" \
        --query 'data.id' \
        --raw-output 2>/dev/null)

    # Route Table 업데이트
    RT_ID=$(oci network route-table list \
        --compartment-id "$COMPARTMENT_ID" \
        --vcn-id "$VCN_ID" \
        --query 'data[0].id' \
        --raw-output 2>/dev/null)

    oci network route-table update \
        --rt-id "$RT_ID" \
        --route-rules "[{\"cidrBlock\":\"0.0.0.0/0\",\"networkEntityId\":\"$IG_ID\"}]" \
        --force > /dev/null 2>&1

    # Security List 업데이트 (80, 443, 22 포트)
    SL_ID=$(oci network security-list list \
        --compartment-id "$COMPARTMENT_ID" \
        --vcn-id "$VCN_ID" \
        --query 'data[0].id' \
        --raw-output 2>/dev/null)

    oci network security-list update \
        --security-list-id "$SL_ID" \
        --ingress-security-rules '[
            {"source":"0.0.0.0/0","protocol":"6","tcpOptions":{"destinationPortRange":{"min":22,"max":22}}},
            {"source":"0.0.0.0/0","protocol":"6","tcpOptions":{"destinationPortRange":{"min":80,"max":80}}},
            {"source":"0.0.0.0/0","protocol":"6","tcpOptions":{"destinationPortRange":{"min":443,"max":443}}}
        ]' \
        --egress-security-rules '[{"destination":"0.0.0.0/0","protocol":"all"}]' \
        --force > /dev/null 2>&1

    # Subnet 생성
    SUBNET_ID=$(oci network subnet create \
        --compartment-id "$COMPARTMENT_ID" \
        --vcn-id "$VCN_ID" \
        --cidr-block "10.0.0.0/24" \
        --display-name "sql-trading-subnet" \
        --dns-label "subnet1" \
        --query 'data.id' \
        --raw-output 2>/dev/null)

    echo "✅ VCN + Subnet 생성 완료"
else
    echo "✅ 기존 VCN 사용: $VCN_ID"
    SUBNET_ID=$(oci network subnet list \
        --compartment-id "$COMPARTMENT_ID" \
        --vcn-id "$VCN_ID" \
        --query 'data[0].id' \
        --raw-output 2>/dev/null)

    if [ -z "$SUBNET_ID" ] || [ "$SUBNET_ID" = "None" ]; then
        echo "Subnet 생성 중..."
        SUBNET_ID=$(oci network subnet create \
            --compartment-id "$COMPARTMENT_ID" \
            --vcn-id "$VCN_ID" \
            --cidr-block "10.0.0.0/24" \
            --display-name "sql-trading-subnet" \
            --query 'data.id' \
            --raw-output 2>/dev/null)
    fi
fi
echo "✅ Subnet: $SUBNET_ID"

# 6. SSH 키 읽기
SSH_KEY=$(cat "$SSH_KEY_FILE")

# 7. 인스턴스 생성 (자동 재시도)
echo ""
echo "========================================="
echo "  인스턴스 생성 시작 (자동 재시도 모드)"
echo "  Ctrl+C로 중단 가능"
echo "========================================="
echo ""

ATTEMPT=0
while [ $ATTEMPT -lt $MAX_RETRIES ]; do
    ATTEMPT=$((ATTEMPT + 1))
    TIMESTAMP=$(date '+%H:%M:%S')

    echo "[$TIMESTAMP] 시도 #$ATTEMPT/$MAX_RETRIES..."

    RESULT=$(oci compute instance launch \
        --compartment-id "$COMPARTMENT_ID" \
        --availability-domain "$AD_NAME" \
        --shape "$SHAPE" \
        --shape-config "{\"ocpus\":$OCPUS,\"memoryInGBs\":$MEMORY_GB}" \
        --display-name "$DISPLAY_NAME" \
        --image-id "$IMAGE_ID" \
        --subnet-id "$SUBNET_ID" \
        --assign-public-ip true \
        --boot-volume-size-in-gbs "$BOOT_VOLUME_GB" \
        --ssh-authorized-keys-file "$SSH_KEY_FILE" \
        --query 'data.id' \
        --raw-output 2>&1) || true

    # 성공 확인 (OCID 형식이면 성공)
    if [[ "$RESULT" == ocid1.instance.* ]]; then
        echo ""
        echo "========================================="
        echo "  ✅ 인스턴스 생성 성공!"
        echo "========================================="
        echo "Instance ID: $RESULT"
        echo ""

        # IP 주소 대기
        echo "Public IP 할당 대기 중..."
        sleep 30

        INSTANCE_ID="$RESULT"
        VNIC_ID=$(oci compute instance list-vnics \
            --instance-id "$INSTANCE_ID" \
            --query 'data[0].id' \
            --raw-output 2>/dev/null) || true

        if [ -n "$VNIC_ID" ] && [ "$VNIC_ID" != "None" ]; then
            PUBLIC_IP=$(oci network vnic get \
                --vnic-id "$VNIC_ID" \
                --query 'data."public-ip"' \
                --raw-output 2>/dev/null) || true
        fi

        if [ -n "${PUBLIC_IP:-}" ] && [ "${PUBLIC_IP}" != "None" ]; then
            echo "Public IP: $PUBLIC_IP"
            echo ""
            echo "SSH 접속:"
            echo "  ssh -i ~/.ssh/id_oracle opc@$PUBLIC_IP"
            echo ""
            echo "접속 정보를 저장합니다..."
            cat > "$HOME/.claude/modules/sql-trading/deploy/.server-info" <<EOF
INSTANCE_ID=$INSTANCE_ID
PUBLIC_IP=$PUBLIC_IP
SSH_USER=opc
SSH_KEY=~/.ssh/id_oracle
EOF
            echo "✅ ~/.claude/modules/sql-trading/deploy/.server-info 에 저장됨"
        else
            echo "Public IP 아직 할당 안됨 - 잠시 후 확인:"
            echo "  oci compute instance list-vnics --instance-id $INSTANCE_ID"
        fi

        exit 0
    fi

    # 용량 부족 에러 확인
    if echo "$RESULT" | grep -q "Out of capacity\|Out of host capacity\|InternalError\|LimitExceeded"; then
        echo "  → 용량 부족, ${RETRY_INTERVAL}초 후 재시도..."
    else
        echo "  → 예상치 못한 에러:"
        echo "$RESULT" | head -5
        echo "  → ${RETRY_INTERVAL}초 후 재시도..."
    fi

    sleep $RETRY_INTERVAL
done

echo "❌ 최대 재시도 횟수 초과 ($MAX_RETRIES회)"
exit 1
