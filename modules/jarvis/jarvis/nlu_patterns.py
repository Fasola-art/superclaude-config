"""
NLU 패턴 정의 - 인텐트, 우선순위, 장소 카테고리
"""

INTENT_PATTERNS = {
    "add_task": [
        r"할\s*일\s*추가", r"task\s*add", r"todo", r"해야\s*할",
    ],
    "add_event": [
        r"일정\s*추가", r"event\s*add", r"calendar",
    ],
    "list_tasks": [
        r"할\s*일\s*목록", r"task\s*list", r"할\s*일\s*보여",
    ],
    "list_events": [
        r"일정\s*목록", r"event\s*list", r"일정\s*보여",
    ],
    "search_place": [
        r"놀러\s*갈\s*곳", r"맛집\s*추천", r"카페\s*추천",
        r"갈\s*만한\s*곳", r"주말\s*나들이", r"관광지",
        r"액티비티", r"숙소\s*추천", r"place\s*search",
    ],
    "add_reservation": [
        r"예약\s*추가", r"예약\s*잡", r"reservation", r"booking",
    ],
    "list_reservations": [
        r"예약\s*목록", r"예약\s*보여", r"예약\s*확인",
    ],
    "bookmark_place": [
        r"즐겨찾기", r"저장\s*해", r"북마크", r"bookmark",
    ],
}

PRIORITY_PATTERNS = {
    "high": [r"긴급", r"중요", r"urgent", r"high"],
    "medium": [r"보통", r"medium"],
    "low": [r"나중에", r"low"],
}

PLACE_CATEGORIES = {
    "restaurant": [r"맛집", r"식당", r"밥"],
    "cafe": [r"카페", r"커피"],
    "attraction": [r"관광", r"여행", r"놀러"],
    "activity": [r"액티비티", r"체험"],
    "accommodation": [r"숙소", r"펜션", r"호텔"],
}

REGION_PATTERN = r"(서울|경기|인천|부산|제주|강원|대전|대구|광주|울산|세종|충[남북]|전[남북]|경[남북])\s*([\w]*)"

DATE_KEYWORDS = r"오늘|내일|주말|이번\s*주\s*토|today|tomorrow|weekend"
