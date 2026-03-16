# SQL Trading 데이터 수집기 래퍼 스크립트 (Windows PowerShell)

# PostgreSQL PATH 추가
$pgPaths = @(
    "C:\Program Files\PostgreSQL\16\bin",
    "C:\Program Files\PostgreSQL\15\bin",
    "C:\Program Files\PostgreSQL\14\bin"
)
foreach ($p in $pgPaths) {
    if (Test-Path $p) {
        $env:PATH = "$p;$env:PATH"
        break
    }
}

# 로그 디렉토리
$logDir = "$env:USERPROFILE\.claude\logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# 실행
$collectorDir = "$env:USERPROFILE\.claude\modules\sql-trading\collectors"
Set-Location $collectorDir
python realtime_collector.py --quiet

# 타임스탬프 기록
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path "$logDir\sql-trading-collector.log" -Value "$timestamp - 수집 완료"
