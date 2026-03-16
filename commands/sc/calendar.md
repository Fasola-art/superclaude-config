---
description: "경제 지표 발표 일정 | Economic indicator release calendar"
---

# /calendar Command

Retrieve and organize economic indicator release schedules for the next month.

## Execution

1. **Today/Tomorrow Key Indicators** - Urgent alerts
2. **This Week Schedule** - Weekly summary
3. **30-Day Calendar** - Markdown table generation

## Tracked Indicators

### CRITICAL (Market-moving)
- **CPI/Core CPI** - Mid-month
- **Non-Farm Payrolls (NFP)** - First Friday monthly
- **FOMC Statement** - 8 times annually
- **GDP** - Quarterly
- **PCE Price Index** - End of month

### HIGH
- Unemployment rate, jobless claims
- Consumer sentiment, retail sales
- ISM Manufacturing/Services PMI

### MEDIUM
- Housing starts, industrial production

## Usage

```
/calendar        # 30-day calendar
/calendar week   # This week only
/calendar today  # Today's schedule
```

## Execution Script

```bash
python3 ~/.claude/scripts/scheduled_collectors.py calendar
```

## Output Location
`~/.claude/modules/trading/data_sources/calendar/calendar_YYYYMMDD.md`

## FOMC 2026 Schedule
| Month | Meeting Dates | Statement Release |
|-------|---------------|-------------------|
| Jan   | 27-28         | 28th 14:00 ET     |
| Mar   | 17-18         | 18th 14:00 ET     |
| May   | 5-6           | 6th 14:00 ET      |
| Jun   | 16-17         | 17th 14:00 ET     |
| Jul   | 28-29         | 29th 14:00 ET     |
| Sep   | 15-16         | 16th 14:00 ET     |
| Nov   | 3-4           | 4th 14:00 ET      |
| Dec   | 15-16         | 16th 14:00 ET     |
