"""
Database Schema and Integration for Green Points Blockchain
SQLite database for user management synced with blockchain
Only USER and BUSINESS roles - Users earn GP, Businesses issue rewards
"""

import sqlite3
import json
import time
from typing import Optional, Dict, List, Tuple
from enum import Enum


class UserRole(Enum):
    """User roles in the system"""
    USER = "user"  # Regular users who earn GP
    BUSINESS = "business"  # Businesses that issue rewards via QR codes


class Database:
    """Handles all database operations"""
    
    def __init__(self, db_path: str = "greenpoints.db"):
        self.db_path = db_path
        self.conn = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = self.conn.cursor()
        
        # Users table - synced with blockchain wallets
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                role TEXT NOT NULL CHECK(role IN ('user', 'business')),
                wallet_address TEXT UNIQUE NOT NULL,
                created_at REAL NOT NULL,
                is_active INTEGER DEFAULT 1,
                metadata TEXT DEFAULT '{}',
                CONSTRAINT contact_required CHECK (email IS NOT NULL OR phone IS NOT NULL)
            )
        """)
        
        # QR Codes table (for business rewards)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qr_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                qr_code TEXT UNIQUE NOT NULL,
                business_id INTEGER NOT NULL,
                business_name TEXT NOT NULL,
                reward_amount REAL NOT NULL,
                service_description TEXT,
                created_at REAL NOT NULL,
                expires_at REAL,
                is_used INTEGER DEFAULT 0,
                used_by INTEGER,
                used_at REAL,
                transaction_id TEXT,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (business_id) REFERENCES users(id),
                FOREIGN KEY (used_by) REFERENCES users(id)
            )
        """)
        
        # Task completions pending verification
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pending_verifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_type TEXT NOT NULL,
                evidence TEXT,
                image_path TEXT,
                location TEXT,
                latitude REAL,
                longitude REAL,
                submitted_at REAL NOT NULL,
                verified_at REAL,
                verified_by TEXT,
                status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
                rejection_reason TEXT,
                reward_amount REAL,
                transaction_id TEXT,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Leaderboard cache (for performance)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard_cache (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                total_gp REAL NOT NULL,
                tasks_completed INTEGER NOT NULL,
                rank INTEGER,
                last_updated REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        self.conn.commit()
        print("✓ Database initialized successfully")
    
    def create_user(self, name: str, email: Optional[str], phone: Optional[str], 
                   role: str, wallet_address: str) -> Optional[int]:
        """
        Create a new user in the database
        
        Args:
            name: User's full name
            email: User's email (optional if phone provided)
            phone: User's phone (optional if email provided)
            role: 'user' or 'business'
            wallet_address: Blockchain wallet address
        
        Returns:
            User ID if successful, None otherwise
        """
        if not email and not phone:
            print("Error: Either email or phone is required")
            return None
        
        if role not in ['user', 'business']:
            print(f"Error: Invalid role '{role}'")
            return None
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (name, email, phone, role, wallet_address, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email, phone, role, wallet_address, time.time()))
            
            self.conn.commit()
            user_id = cursor.lastrowid
            print(f"✓ User created: {name} (ID: {user_id}, Role: {role})")
            return user_id
        
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_phone(self, phone: str) -> Optional[Dict]:
        """Get user by phone"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_wallet(self, wallet_address: str) -> Optional[Dict]:
        """Get user by wallet address"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE wallet_address = ?", (wallet_address,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_users(self, role: Optional[str] = None) -> List[Dict]:
        """Get all users, optionally filtered by role"""
        cursor = self.conn.cursor()
        if role:
            cursor.execute("SELECT * FROM users WHERE role = ? AND is_active = 1 ORDER BY created_at DESC", (role,))
        else:
            cursor.execute("SELECT * FROM users WHERE is_active = 1 ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def create_qr_code(self, business_id: int, reward_amount: float, 
                       qr_code: str, service_description: str = "",
                       expires_in_hours: Optional[int] = None) -> Optional[int]:
        """Create a QR code for business reward"""
        cursor = self.conn.cursor()
        
        # Get business name
        business = self.get_user_by_id(business_id)
        if not business or business['role'] != 'business':
            print("Error: Invalid business ID")
            return None
        
        expires_at = None
        if expires_in_hours:
            expires_at = time.time() + (expires_in_hours * 3600)
        
        try:
            cursor.execute("""
                INSERT INTO qr_codes (qr_code, business_id, business_name, reward_amount, 
                                     service_description, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (qr_code, business_id, business['name'], reward_amount, 
                  service_description, time.time(), expires_at))
            
            self.conn.commit()
            return cursor.lastrowid
        
        except sqlite3.IntegrityError:
            print("Error: QR code already exists")
            return None
    
    def get_qr_code(self, qr_code: str) -> Optional[Dict]:
        """Get QR code details"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM qr_codes WHERE qr_code = ?", (qr_code,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def validate_qr_code(self, qr_code: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Validate if QR code can be used
        
        Returns:
            (is_valid, message, qr_data)
        """
        qr_data = self.get_qr_code(qr_code)
        
        if not qr_data:
            return False, "QR code not found", None
        
        if qr_data['is_used']:
            return False, f"QR code already used on {time.strftime('%Y-%m-%d %H:%M', time.localtime(qr_data['used_at']))}", qr_data
        
        if qr_data['expires_at'] and time.time() > qr_data['expires_at']:
            return False, "QR code expired", qr_data
        
        return True, "Valid QR code", qr_data
    
    def use_qr_code(self, qr_code: str, user_id: int, transaction_id: str) -> bool:
        """Mark QR code as used"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE qr_codes 
            SET is_used = 1, used_by = ?, used_at = ?, transaction_id = ?
            WHERE qr_code = ? AND is_used = 0
        """, (user_id, time.time(), transaction_id, qr_code))
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def submit_verification(self, user_id: int, task_type: str, evidence: str,
                          reward_amount: float, image_path: Optional[str] = None,
                          location: Optional[str] = None, 
                          latitude: Optional[float] = None,
                          longitude: Optional[float] = None,
                          metadata: Dict = None) -> Optional[int]:
        """Submit a task for verification"""
        cursor = self.conn.cursor()
        
        metadata_json = json.dumps(metadata or {})
        
        cursor.execute("""
            INSERT INTO pending_verifications 
            (user_id, task_type, evidence, image_path, location, latitude, longitude,
             submitted_at, reward_amount, metadata, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (user_id, task_type, evidence, image_path, location, latitude, longitude,
              time.time(), reward_amount, metadata_json))
        
        self.conn.commit()
        verification_id = cursor.lastrowid
        print(f"✓ Verification submitted (ID: {verification_id})")
        return verification_id
    
    def get_pending_verifications(self) -> List[Dict]:
        """Get all pending verifications"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT v.*, u.name as user_name, u.email as user_email, u.phone as user_phone
            FROM pending_verifications v
            JOIN users u ON v.user_id = u.id
            WHERE v.status = 'pending'
            ORDER BY v.submitted_at ASC
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_verification_by_id(self, verification_id: int) -> Optional[Dict]:
        """Get verification by ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT v.*, u.name as user_name, u.email as user_email
            FROM pending_verifications v
            JOIN users u ON v.user_id = u.id
            WHERE v.id = ?
        """, (verification_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def approve_verification(self, verification_id: int, verified_by: str, 
                            transaction_id: str) -> bool:
        """Approve a verification request"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE pending_verifications
            SET status = 'approved', verified_at = ?, verified_by = ?, transaction_id = ?
            WHERE id = ? AND status = 'pending'
        """, (time.time(), verified_by, transaction_id, verification_id))
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def reject_verification(self, verification_id: int, verified_by: str, 
                           reason: str) -> bool:
        """Reject a verification request"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE pending_verifications
            SET status = 'rejected', verified_at = ?, verified_by = ?, rejection_reason = ?
            WHERE id = ? AND status = 'pending'
        """, (time.time(), verified_by, reason, verification_id))
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def update_leaderboard_cache(self, user_id: int, name: str, total_gp: float, 
                                tasks_completed: int):
        """Update leaderboard cache for a user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO leaderboard_cache 
            (user_id, name, total_gp, tasks_completed, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, name, total_gp, tasks_completed, time.time()))
        
        self.conn.commit()
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get leaderboard data"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                ROW_NUMBER() OVER (ORDER BY total_gp DESC) as rank,
                user_id, name, total_gp, tasks_completed
            FROM leaderboard_cache
            WHERE total_gp > 0
            ORDER BY total_gp DESC
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def rebuild_leaderboard(self, blockchain):
        """Rebuild entire leaderboard from blockchain data"""
        users = self.get_all_users(role='user')
        
        for user in users:
            balance = blockchain.get_balance(user['wallet_address'])
            # Count approved verifications as tasks completed
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as count FROM pending_verifications
                WHERE user_id = ? AND status = 'approved'
            """, (user['id'],))
            tasks_completed = cursor.fetchone()['count']
            
            # Add QR code redemptions
            cursor.execute("""
                SELECT COUNT(*) as count FROM qr_codes
                WHERE used_by = ?
            """, (user['id'],))
            tasks_completed += cursor.fetchone()['count']
            
            self.update_leaderboard_cache(user['id'], user['name'], balance, tasks_completed)
        
        print("✓ Leaderboard rebuilt")
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get statistics for a user"""
        cursor = self.conn.cursor()
        
        # Get verification stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_submissions,
                SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
            FROM pending_verifications
            WHERE user_id = ?
        """, (user_id,))
        
        stats = dict(cursor.fetchone())
        
        # Get QR code usage
        cursor.execute("""
            SELECT COUNT(*) as qr_codes_scanned
            FROM qr_codes
            WHERE used_by = ?
        """, (user_id,))
        
        stats.update(dict(cursor.fetchone()))
        
        # Get business stats if business
        user = self.get_user_by_id(user_id)
        if user and user['role'] == 'business':
            cursor.execute("""
                SELECT 
                    COUNT(*) as qr_codes_generated,
                    SUM(CASE WHEN is_used = 1 THEN 1 ELSE 0 END) as qr_codes_redeemed,
                    SUM(CASE WHEN is_used = 1 THEN reward_amount ELSE 0 END) as total_gp_distributed
                FROM qr_codes
                WHERE business_id = ?
            """, (user_id,))
            stats.update(dict(cursor.fetchone()))
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
