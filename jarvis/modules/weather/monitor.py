#!/usr/bin/env python3
"""
Weather Monitor using wttr.in
"""

from __future__ import annotations

import json
from typing import Optional
from urllib.request import urlopen


class WeatherMonitor:
    """날씨 모니터 (wttr.in API 사용)"""

    BASE_URL = "https://wttr.in"
    DEFAULT_LOCATION = "Gangnam,Seoul,Korea"  # 신사동 기준

    def get_current_weather(self, city: str | None = None) -> dict[str, str]:
        city = city or self.DEFAULT_LOCATION
        url = f"{self.BASE_URL}/{city}?format=j1"
        try:
            with urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                current = data["current_condition"][0]
                return {
                    "temp_c": current["temp_C"],
                    "feels_like_c": current["FeelsLikeC"],
                    "humidity": current["humidity"],
                    "weather_desc": current["weatherDesc"][0]["value"],
                    "precipitation_mm": current["precipMM"],
                }
        except Exception as e:
            return {"error": str(e)}

    def get_forecast(self, city: str | None = None, days: int = 3) -> list[dict[str, str]]:
        """일기 예보 조회"""
        city = city or self.DEFAULT_LOCATION
        url = f"{self.BASE_URL}/{city}?format=j1"
        try:
            with urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                forecasts = []
                for day in data["weather"][:days]:
                    forecasts.append(
                        {
                            "date": day["date"],
                            "max_temp_c": day["maxtempC"],
                            "min_temp_c": day["mintempC"],
                            "avg_temp_c": day["avgtempC"],
                            "total_snow_cm": day["totalSnow_cm"],
                            "sun_hour": day["sunHour"],
                            "uv_index": day["uvIndex"],
                        }
                    )
                return forecasts
        except Exception as e:
            return [{"error": str(e)}]

    def should_bring_umbrella(self, city: str | None = None) -> tuple[bool, str]:
        """우산 필요 여부 판단"""
        weather = self.get_current_weather(city or self.DEFAULT_LOCATION)
        if "error" in weather:
            return False, f"날씨 정보 조회 실패: {weather['error']}"

        precip = float(weather.get("precipitation_mm", "0"))
        desc = weather.get("weather_desc", "").lower()

        if precip > 0 or "rain" in desc or "drizzle" in desc or "shower" in desc:
            return True, f"우산 필요 (강수량: {precip}mm, 날씨: {weather['weather_desc']})"

        return False, f"우산 불필요 (날씨: {weather['weather_desc']})"
