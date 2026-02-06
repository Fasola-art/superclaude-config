# Weather Monitor

wttr.in API를 사용한 날씨 모니터

## 사용법

```python
from modules.weather import WeatherMonitor

monitor = WeatherMonitor()

# 현재 날씨
weather = monitor.get_current_weather("Seoul")
print(f"온도: {weather['temp_c']}°C")
print(f"날씨: {weather['weather_desc']}")

# 3일 예보
forecasts = monitor.get_forecast("Seoul", days=3)
for fc in forecasts:
    print(f"{fc['date']}: {fc['min_temp_c']}~{fc['max_temp_c']}°C")

# 우산 필요 여부
need_umbrella, reason = monitor.should_bring_umbrella("Seoul")
if need_umbrella:
    print(f"☔ {reason}")
else:
    print(f"☀️ {reason}")
```

## API

- 무료 API (wttr.in)
- API 키 불필요
- 전세계 도시 지원
