#!/usr/bin/env python3
"""
Weather Monitor Tests
"""

from .monitor import WeatherMonitor


def test_get_current_weather():
    """현재 날씨 조회 테스트"""
    monitor = WeatherMonitor()
    weather = monitor.get_current_weather("Seoul")

    if "error" in weather:
        print(f"⚠️  날씨 조회 실패: {weather['error']}")
        return

    print(f"✅ 현재 날씨: {weather['weather_desc']}")
    print(f"   온도: {weather['temp_c']}°C (체감: {weather['feels_like_c']}°C)")
    print(f"   습도: {weather['humidity']}%")


def test_get_forecast():
    """일기 예보 테스트"""
    monitor = WeatherMonitor()
    forecasts = monitor.get_forecast("Seoul", days=3)

    if forecasts and "error" in forecasts[0]:
        print(f"⚠️  예보 조회 실패: {forecasts[0]['error']}")
        return

    print(f"✅ 3일 예보:")
    for fc in forecasts:
        print(f"   {fc['date']}: {fc['min_temp_c']}~{fc['max_temp_c']}°C")


def test_should_bring_umbrella():
    """우산 필요 여부 테스트"""
    monitor = WeatherMonitor()
    need_umbrella, reason = monitor.should_bring_umbrella("Seoul")

    if need_umbrella:
        print(f"☔ {reason}")
    else:
        print(f"☀️  {reason}")


if __name__ == "__main__":
    print("=== Weather Monitor Tests ===\n")
    test_get_current_weather()
    print()
    test_get_forecast()
    print()
    test_should_bring_umbrella()
    print("\n🎉 테스트 완료")
