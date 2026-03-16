---
name: market
description: Display today's economic outlook report. Generate new report if none exists.
license: MIT
---

Display today's economic outlook report.

## Execution Steps

1. Check for latest outlook file
2. Generate new report if not found
3. Output outlook content

## Execution Script

```powershell
cd C:/Users/MSI/.claude/modules/trading

# Today's date
$TODAY = Get-Date -Format yyyy-MM-dd

# Check outlook file
$OUTLOOK_FILE = "reports/daily/outlook_${TODAY}.json"

if (Test-Path $OUTLOOK_FILE) {
    Write-Host "=== Economic Outlook ($TODAY) ==="
    python -c "
import json
with open('$OUTLOOK_FILE', 'r') as f:
    data = json.load(f)
print(data.get('text', 'No outlook available'))
print()
print(f\"\"\"Generated: {data.get('timestamp', 'N/A')}\"\"\")
print(f\"\"\"Cost: \${data.get('cost', 0):.4f}\"\"\")
"
} else {
    Write-Host "No outlook for today. Generating..."
    $env:ANTHROPIC_API_KEY = (Get-Content C:/Users/MSI/.claude/credentials/api-keys.json | ConvertFrom-Json).'anthropic'
    python reports/market_outlook.py
}
```

## Output Example

```
=== Economic Outlook (2026-01-29) ===

## Market Status
Stock market slightly weak. VIX at 16.91, moderate volatility...

## Key Points
1. Bond market volatility decline slowing
2. SOFR continues sideways
3. Yield curve normalization progressing

## Tomorrow's Outlook
Volatility expansion expected due to PCE, GDP releases...
```
