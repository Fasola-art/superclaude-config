#!/bin/bash
# React/Next.js 파일 수정 시 규칙 상기

# 현재 작업 파일 확인
FILE="$1"

if [[ "$FILE" == *.tsx ]] || [[ "$FILE" == *.jsx ]]; then
    echo "📋 React 규칙 체크리스트:"
    echo "  🔴 Promise.all 사용 (순차 await 금지)"
    echo "  🔴 Barrel import 금지 (직접 import)"
    echo "  🟠 Server Component 기본 ('use client' 최소화)"
    echo "  🟡 next/image 사용 (<img> 금지)"
fi
