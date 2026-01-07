"""Implementasi Database SQLite3

Menggunakan SQLite3 untuk penyimpanan data, tidak perlu install database server terpisah
"""
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from pathlib import Path

logger = logging.getLogger(__name__)


class SQLiteDatabase:
    """Class Manajemen Database SQLite"""

    def __init__(self, db_path: str = "tgbot_verify.db"):
        """Inisialisasi koneksi database"""
        self.db_path = Path(db_path)
        logger.info(f"Inisialisasi Database SQLite: {self.db_path.absolute()}")
        self.init_database()

    def get_connection(self):
        """Mendapatkan koneksi database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Membuat hasil bisa diakses berdasarkan nama kolom
        return conn

    def init_database(self):
        """Inisialisasi struktur tabel database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Tabel user
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    balance INTEGER DEFAULT 1000000000,
                    is_blocked INTEGER DEFAULT 0,
                    invited_by INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_checkin TEXT
                )
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON users(username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_invited_by ON users(invited_by)")

            # Tabel record invitation
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS invitations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inviter_id INTEGER NOT NULL,
                    invitee_id INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (inviter_id) REFERENCES users(user_id),
                    FOREIGN KEY (invitee_id) REFERENCES users(user_id)
                )
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_inviter ON invitations(inviter_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_invitee ON invitations(invitee_id)")

            # Tabel record verifikasi
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS verifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    verification_type TEXT NOT NULL,
                    verification_url TEXT,
                    verification_id TEXT,
                    status TEXT NOT NULL,
                    result TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_ver_user_id ON verifications(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_ver_type ON verifications(verification_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_ver_created ON verifications(created_at)")

            # Tabel card key
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS card_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_code TEXT UNIQUE NOT NULL,
                    balance INTEGER NOT NULL,
                    max_uses INTEGER DEFAULT 1,
                    current_uses INTEGER DEFAULT 0,
                    expire_at TEXT,
                    created_by INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_key_code ON card_keys(key_code)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_by ON card_keys(created_by)")

            # Tabel usage card key
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS card_key_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_code TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    used_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_key_code ON card_key_usage(key_code)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_user_id ON card_key_usage(user_id)")

            conn.commit()
            logger.info("Inisialisasi tabel database SQLite selesai")

        except Exception as e:
            logger.error(f"Gagal inisialisasi database: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def create_user(
        self, user_id: int, username: str, full_name: str, invited_by: Optional[int] = None
    ) -> bool:
        """Membuat user baru"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (user_id, username, full_name, invited_by, created_at)
                VALUES (?, ?, ?, ?, datetime('now'))
                """,
                (user_id, username, full_name, invited_by),
            )

            if invited_by:
                cursor.execute(
                    "UPDATE users SET balance = balance + 2 WHERE user_id = ?",
                    (invited_by,),
                )

                cursor.execute(
                    """
                    INSERT INTO invitations (inviter_id, invitee_id, created_at)
                    VALUES (?, ?, datetime('now'))
                    """,
                    (invited_by, user_id),
                )

            conn.commit()
            return True

        except sqlite3.IntegrityError:
            conn.rollback()
            return False
        except Exception as e:
            logger.error(f"Gagal membuat user: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Mendapatkan info user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None

        finally:
            cursor.close()
            conn.close()

    def user_exists(self, user_id: int) -> bool:
        """Cek apakah user exists"""
        return self.get_user(user_id) is not None

    def is_user_blocked(self, user_id: int) -> bool:
        """Cek apakah user diblacklist"""
        user = self.get_user(user_id)
        return user and user["is_blocked"] == 1

    def block_user(self, user_id: int) -> bool:
        """Blacklist user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE users SET is_blocked = 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Gagal blacklist user: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def unblock_user(self, user_id: int) -> bool:
        """Unblacklist user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE users SET is_blocked = 0 WHERE user_id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Gagal unblacklist: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_blacklist(self) -> List[Dict]:
        """Mendapatkan daftar blacklist"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE is_blocked = 1")
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def add_balance(self, user_id: int, amount: int) -> bool:
        """Tambah token user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, user_id),
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Gagal tambah token: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def deduct_balance(self, user_id: int, amount: int) -> bool:
        """Kurangi token user"""
        user = self.get_user(user_id)
        if not user or user["balance"] < amount:
            return False

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET balance = balance - ? WHERE user_id = ?",
                (amount, user_id),
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Gagal kurangi token: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def can_checkin(self, user_id: int) -> bool:
        """Cek apakah user bisa checkin hari ini"""
        user = self.get_user(user_id)
        if not user:
            return False

        last_checkin = user.get("last_checkin")
        if not last_checkin:
            return True

        try:
            last_date = datetime.fromisoformat(last_checkin).date()
            today = datetime.now().date()
            return last_date < today
        except:
            return True

    def checkin(self, user_id: int) -> bool:
        """User checkin"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Cek apakah bisa checkin
            if not self.can_checkin(user_id):
                return False

            cursor.execute(
                """
                UPDATE users
                SET balance = balance + 1, last_checkin = datetime('now')
                WHERE user_id = ?
                """,
                (user_id,),
            )
            conn.commit()
            
            success = cursor.rowcount > 0
            return success
            
        except Exception as e:
            logger.error(f"Gagal checkin: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def add_verification(
        self, user_id: int, verification_type: str, verification_url: str,
        status: str, result: str = "", verification_id: str = ""
    ) -> bool:
        """Tambah record verifikasi"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO verifications
                (user_id, verification_type, verification_url, verification_id, status, result, created_at)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """,
                (user_id, verification_type, verification_url, verification_id, status, result),
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Gagal tambah record verifikasi: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user_verifications(self, user_id: int) -> List[Dict]:
        """Mendapatkan record verifikasi user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM verifications
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def create_card_key(
        self, key_code: str, balance: int, created_by: int,
        max_uses: int = 1, expire_days: Optional[int] = None
    ) -> bool:
        """Membuat card key"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            expire_at = None
            if expire_days:
                expire_at = (datetime.now() + timedelta(days=expire_days)).isoformat()

            cursor.execute(
                """
                INSERT INTO card_keys (key_code, balance, max_uses, created_by, created_at, expire_at)
                VALUES (?, ?, ?, ?, datetime('now'), ?)
                """,
                (key_code, balance, max_uses, created_by, expire_at),
            )
            conn.commit()
            return True

        except sqlite3.IntegrityError:
            logger.error(f"Card key sudah ada: {key_code}")
            conn.rollback()
            return False
        except Exception as e:
            logger.error(f"Gagal membuat card key: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def use_card_key(self, key_code: str, user_id: int) -> Optional[int]:
        """Gunakan card key, return jumlah token yang didapat"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Query card key
            cursor.execute(
                "SELECT * FROM card_keys WHERE key_code = ?",
                (key_code,),
            )
            row = cursor.fetchone()

            if not row:
                return None

            card = dict(row)

            # Cek apakah expired
            if card["expire_at"]:
                try:
                    expire_time = datetime.fromisoformat(card["expire_at"])
                    if datetime.now() > expire_time:
                        return -2
                except:
                    pass

            # Cek jumlah penggunaan
            if card["current_uses"] >= card["max_uses"]:
                return -1

            # Cek apakah user sudah pernah pakai card key ini
            cursor.execute(
                "SELECT COUNT(*) as count FROM card_key_usage WHERE key_code = ? AND user_id = ?",
                (key_code, user_id),
            )
            count = cursor.fetchone()[0]
            if count > 0:
                return -3

            # Update jumlah penggunaan
            cursor.execute(
                "UPDATE card_keys SET current_uses = current_uses + 1 WHERE key_code = ?",
                (key_code,),
            )

            # Catat record penggunaan
            cursor.execute(
                "INSERT INTO card_key_usage (key_code, user_id, used_at) VALUES (?, ?, datetime('now'))",
                (key_code, user_id),
            )

            # Tambah token user
            cursor.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (card["balance"], user_id),
            )

            conn.commit()
            return card["balance"]

        except Exception as e:
            logger.error(f"Gagal gunakan card key: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def get_card_key_info(self, key_code: str) -> Optional[Dict]:
        """Mendapatkan info card key"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM card_keys WHERE key_code = ?", (key_code,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_all_card_keys(self, created_by: Optional[int] = None) -> List[Dict]:
        """Mendapatkan semua card key (bisa filter by creator)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if created_by:
                cursor.execute(
                    "SELECT * FROM card_keys WHERE created_by = ? ORDER BY created_at DESC",
                    (created_by,),
                )
            else:
                cursor.execute("SELECT * FROM card_keys ORDER BY created_at DESC")
            
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_all_user_ids(self) -> List[int]:
        """Mendapatkan semua user ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT user_id FROM users")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            cursor.close()
            conn.close()

    def get_all_users(self) -> List[Dict]:
        """Mendapatkan semua user dengan detail lengkap"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT user_id, username, full_name, balance, is_blocked, created_at "
                "FROM users ORDER BY created_at DESC"
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()


# Alias untuk global instance
Database = SQLiteDatabase
