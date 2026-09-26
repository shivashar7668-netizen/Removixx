"""
Removix Activity Tracker Module
-------------------------------
Tracks processed files, storage usage, and user activity history using local SQLite.
All statistics and recent file history are persisted in data/activity.db.
"""

import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DB_DIR / "activity.db"


def _get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the activity database schema without inserting any fake or demo data."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL,          -- 'Image', 'PDF', 'Video'
                file_size_bytes INTEGER NOT NULL,
                tool_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                download_path TEXT
            )
            """
        )
        conn.commit()


def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def format_date(dt_str: str) -> str:
    try:
        dt = datetime.datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        try:
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return dt_str
    return dt.strftime("%b %d, %Y, %I:%M %p")


def log_file(
    file_name: str,
    file_type: str,
    file_size_bytes: int,
    tool_name: str,
    download_path: Optional[str] = None,
) -> int:
    """Logs a completed file operation into the activity database."""
    init_db()
    with _get_connection() as conn:
        cursor = conn.cursor()
        # Prevent immediate duplicate logging within 30 seconds for the same download_path
        if download_path:
            cursor.execute(
                """
                SELECT id FROM activity_log 
                WHERE download_path = ? AND created_at >= datetime('now', '-30 seconds')
                """,
                (download_path,),
            )
            existing = cursor.fetchone()
            if existing:
                return existing[0]

        cursor.execute(
            """
            INSERT INTO activity_log (file_name, file_type, file_size_bytes, tool_name, created_at, download_path)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                file_name,
                file_type,
                max(1, int(file_size_bytes)),
                tool_name,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                download_path,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_recent_files(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves the most recently processed files."""
    init_db()
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, file_name, file_type, file_size_bytes, tool_name, created_at, download_path
            FROM activity_log
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        results = []
        for r in rows:
            results.append(
                {
                    "id": r["id"],
                    "name": r["file_name"],
                    "type": r["file_type"],
                    "size_bytes": r["file_size_bytes"],
                    "size": format_file_size(r["file_size_bytes"]),
                    "tool": r["tool_name"],
                    "created_at": r["created_at"],
                    "date": format_date(r["created_at"]),
                    "has_download": bool(r["download_path"] and Path(r["download_path"]).exists()),
                }
            )
        return results


def delete_file_record(file_id: int) -> bool:
    """Deletes an activity record by ID."""
    init_db()
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activity_log WHERE id = ?", (file_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_file_record(file_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single file record by ID."""
    init_db()
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, file_name, file_type, file_size_bytes, tool_name, created_at, download_path
            FROM activity_log
            WHERE id = ?
            """,
            (file_id,),
        )
        r = cursor.fetchone()
        if not r:
            return None
        return {
            "id": r["id"],
            "name": r["file_name"],
            "type": r["file_type"],
            "size_bytes": r["file_size_bytes"],
            "size": format_file_size(r["file_size_bytes"]),
            "tool": r["tool_name"],
            "created_at": r["created_at"],
            "date": format_date(r["created_at"]),
            "download_path": r["download_path"],
            "has_download": bool(r["download_path"] and Path(r["download_path"]).exists()),
        }


def get_stats(period: str = "month") -> Dict[str, Any]:
    """
    Computes activity statistics for the specified timeframe.
    period: 'week', 'month', or 'all'
    """
    init_db()
    now = datetime.datetime.now()
    if period == "week":
        cutoff = (now - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        prev_cutoff = (now - datetime.timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")
    elif period == "all":
        cutoff = "1970-01-01 00:00:00"
        prev_cutoff = "1970-01-01 00:00:00"
    else:  # month default
        cutoff = (now - datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        prev_cutoff = (now - datetime.timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")

    with _get_connection() as conn:
        cursor = conn.cursor()

        # Current period counts
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_count,
                COALESCE(SUM(file_size_bytes), 0) as total_bytes,
                COALESCE(SUM(CASE WHEN file_type = 'Image' THEN 1 ELSE 0 END), 0) as images_count,
                COALESCE(SUM(CASE WHEN file_type = 'PDF' THEN 1 ELSE 0 END), 0) as pdfs_count,
                COALESCE(SUM(CASE WHEN file_type = 'Video' THEN 1 ELSE 0 END), 0) as videos_count
            FROM activity_log
            WHERE created_at >= ?
            """,
            (cutoff,),
        )
        curr = cursor.fetchone()

        # Previous period counts for percentage comparison
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_count,
                COALESCE(SUM(CASE WHEN file_type = 'Image' THEN 1 ELSE 0 END), 0) as images_count,
                COALESCE(SUM(CASE WHEN file_type = 'PDF' THEN 1 ELSE 0 END), 0) as pdfs_count
            FROM activity_log
            WHERE created_at >= ? AND created_at < ?
            """,
            (prev_cutoff, cutoff),
        )
        prev = cursor.fetchone()

        total_files = curr["total_count"] if curr else 0
        total_bytes = curr["total_bytes"] if curr else 0
        images_count = curr["images_count"] if curr else 0
        pdfs_count = curr["pdfs_count"] if curr else 0
        videos_count = curr["videos_count"] if curr else 0

        # Calculate actual storage in MB
        if total_bytes <= 0:
            storage_mb = 0
        elif total_bytes < 10 * 1024 * 1024:
            storage_mb = round(total_bytes / (1024 * 1024), 1)
        else:
            storage_mb = round(total_bytes / (1024 * 1024))

        storage_quota_mb = 500
        storage_pct = min(100, round((storage_mb / storage_quota_mb) * 100)) if storage_quota_mb else 0

        # Calculate real percentage changes
        prev_files = prev["total_count"] if prev and prev["total_count"] else 0
        if prev_files > 0:
            files_change = round(((total_files - prev_files) / prev_files) * 100)
        elif total_files > 0:
            files_change = 100
        else:
            files_change = 0

        prev_images = prev["images_count"] if prev and prev["images_count"] else 0
        if prev_images > 0:
            images_change = round(((images_count - prev_images) / prev_images) * 100)
        elif images_count > 0:
            images_change = 100
        else:
            images_change = 0

        prev_pdfs = prev["pdfs_count"] if prev and prev["pdfs_count"] else 0
        if prev_pdfs > 0:
            pdfs_change = round(((pdfs_count - prev_pdfs) / prev_pdfs) * 100)
        elif pdfs_count > 0:
            pdfs_change = 100
        else:
            pdfs_change = 0

        return {
            "period": period,
            "files_processed": total_files,
            "files_change": files_change,
            "files_change_dir": "up" if files_change > 0 else ("down" if files_change < 0 else "neutral"),
            "storage_used_mb": storage_mb,
            "storage_quota_mb": storage_quota_mb,
            "storage_pct": storage_pct,
            "images_processed": images_count,
            "images_change": images_change,
            "images_change_dir": "up" if images_change > 0 else ("down" if images_change < 0 else "neutral"),
            "pdf_files": pdfs_count,
            "pdf_change": pdfs_change,
            "pdf_change_dir": "up" if pdfs_change > 0 else ("down" if pdfs_change < 0 else "neutral"),
            "video_files": videos_count,
        }


# Auto initialize on module import
init_db()
