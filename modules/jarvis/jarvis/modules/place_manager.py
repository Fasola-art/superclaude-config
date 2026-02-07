"""
장소 즐겨찾기 및 예약 DB 관리
"""
import json
from typing import List, Dict, Any, Optional

from ..memory import DatabaseManager


class PlaceManager(DatabaseManager):
    """장소 즐겨찾기 및 예약 관리"""

    def save_place(self, place: Dict[str, Any], bookmark: bool = True) -> int:
        """장소 저장 (upsert)"""
        query = """
            INSERT INTO places (name, category, address, lat, lng, rating, price_level,
                                google_place_id, phone, website, tags, is_bookmarked)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(google_place_id) DO UPDATE SET
                rating = excluded.rating,
                is_bookmarked = excluded.is_bookmarked,
                updated_at = CURRENT_TIMESTAMP
        """
        tags_json = json.dumps(place.get("tags")) if place.get("tags") else None
        cursor = self.execute(query, (
            place["name"], place.get("category", "other"), place.get("address"),
            place.get("lat"), place.get("lng"), place.get("rating"),
            place.get("price_level"), place.get("google_place_id"),
            place.get("phone"), place.get("website"), tags_json,
            1 if bookmark else 0,
        ))
        return cursor.lastrowid

    def get_bookmarks(self, category: str = None) -> List[Dict[str, Any]]:
        """즐겨찾기 조회"""
        query = "SELECT * FROM places WHERE is_bookmarked = 1"
        params: list = []
        if category:
            query += " AND category = ?"
            params.append(category)
        query += " ORDER BY rating DESC, visit_count DESC"
        cursor = self.execute(query, tuple(params))
        return [dict(row) for row in cursor.fetchall()]

    def record_visit(self, place_id: int) -> None:
        """방문 기록"""
        query = """
            UPDATE places
            SET visit_count = visit_count + 1, last_visited_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.execute(query, (place_id,))

    def add_reservation(self, place_id: int, title: str, reserved_date: str,
                        reserved_time: str = None, party_size: int = 2,
                        booking_url: str = None, notes: str = None) -> int:
        """예약 추가"""
        query = """
            INSERT INTO reservations (place_id, title, reserved_date, reserved_time,
                                      party_size, booking_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute(query, (
            place_id, title, reserved_date, reserved_time,
            party_size, booking_url, notes,
        ))
        return cursor.lastrowid

    def get_reservations(self, status: str = None,
                         upcoming_only: bool = True) -> List[Dict[str, Any]]:
        """예약 조회"""
        query = """
            SELECT r.*, p.name as place_name, p.address, p.phone
            FROM reservations r
            LEFT JOIN places p ON r.place_id = p.id
        """
        conditions: list = []
        params: list = []
        if status:
            conditions.append("r.status = ?")
            params.append(status)
        if upcoming_only:
            conditions.append("r.reserved_date >= DATE('now')")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY r.reserved_date, r.reserved_time"
        cursor = self.execute(query, tuple(params))
        return [dict(row) for row in cursor.fetchall()]

    def update_reservation_status(self, reservation_id: int, status: str) -> None:
        """예약 상태 변경"""
        query = "UPDATE reservations SET status = ? WHERE id = ?"
        self.execute(query, (status, reservation_id))

    def remove_bookmark(self, place_id: int) -> None:
        """즐겨찾기 해제"""
        query = "UPDATE places SET is_bookmarked = 0 WHERE id = ?"
        self.execute(query, (place_id,))
