"""
Enhanced Wallet and User Management for Centralized Green Points System
Supports 3 user types: Tourist, User, Business
"""

import json
import hashlib
import time
from typing import Dict, List, Optional
from enum import Enum


class UserType(Enum):
    """Types of users in the system"""
    TOURIST = "tourist"
    USER = "user"
    BUSINESS = "business"


class Wallet:
    """Represents a user's wallet in the Green Points system"""
    
    def __init__(self, user_id: int, username: str, user_type: UserType, 
                 email: Optional[str] = None, phone: Optional[str] = None):
        """
        Initialize a wallet
        
        Args:
            user_id: Unique user ID from SQL database
            username: User's username
            user_type: Type of user (TOURIST, USER, BUSINESS)
            email: Optional email address
            phone: Optional phone number
        """
        self.user_id = user_id
        self.username = username
        self.user_type = user_type
        self.email = email
        self.phone = phone
        self.address = self.generate_address(user_id, username)
        self.created_at = time.time()
        self.reward_points = 0  # Points that can be redeemed for rewards
        self.metadata = {
            "total_tasks_completed": 0,
            "total_gp_earned": 0,
            "total_gp_spent": 0,
            "rank": 0
        }
    
    def generate_address(self, user_id: int, username: str) -> str:
        """
        Generate a unique address for the wallet
        
        Args:
            user_id: User ID from database
            username: Username
        
        Returns:
            Unique wallet address
        """
        address_string = f"{user_id}_{username}_{time.time()}"
        return hashlib.sha256(address_string.encode()).hexdigest()[:20]
    
    def convert_gp_to_rewards(self, gp_amount: float, conversion_rate: float = 0.1) -> float:
        """
        Convert Green Points to reward points
        
        Args:
            gp_amount: Amount of GP to convert
            conversion_rate: Conversion rate (default: 0.1 means 10 GP = 1 RP)
        
        Returns:
            Amount of reward points earned
        """
        reward_points = gp_amount * conversion_rate
        self.reward_points += reward_points
        return reward_points
    
    def get_multiplier(self) -> float:
        """Get GP earning multiplier based on user type"""
        multipliers = {
            UserType.TOURIST: 1.5,  # Tourists get 50% bonus
            UserType.USER: 1.0,     # Regular users get standard rate
            UserType.BUSINESS: 0.8  # Businesses get 80% (they also earn from customers)
        }
        return multipliers.get(self.user_type, 1.0)
    
    def to_dict(self) -> Dict:
        """Convert wallet to dictionary format"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "user_type": self.user_type.value,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "reward_points": self.reward_points,
            "created_at": self.created_at,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert wallet to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def __str__(self) -> str:
        return f"Wallet({self.username}, {self.user_type.value}, {self.address})"
    
    def __repr__(self) -> str:
        return self.__str__()


class UserManager:
    """Manages all users and their wallets - Centralized System"""
    
    def __init__(self):
        self.wallets: Dict[str, Wallet] = {}  # address -> Wallet
        self.user_id_to_address: Dict[int, str] = {}  # user_id -> address
        self.username_to_address: Dict[str, str] = {}  # username -> address
        self.leaderboard_cache = []
        self.leaderboard_last_updated = 0
    
    def create_wallet_from_db(self, user_id: int, username: str, user_type: str,
                             email: Optional[str] = None, phone: Optional[str] = None) -> Optional[Wallet]:
        """
        Create a new wallet from database user data
        
        Args:
            user_id: User ID from SQL database
            username: Username
            user_type: User type as string ('tourist', 'user', 'business')
            email: Optional email
            phone: Optional phone
        
        Returns:
            The created wallet or None if user already exists
        """
        if user_id in self.user_id_to_address:
            print(f"User ID '{user_id}' already exists in blockchain")
            return self.wallets[self.user_id_to_address[user_id]]
        
        # Convert string to UserType enum
        try:
            user_type_enum = UserType(user_type.lower())
        except ValueError:
            print(f"Invalid user type: {user_type}. Defaulting to USER")
            user_type_enum = UserType.USER
        
        wallet = Wallet(user_id, username, user_type_enum, email, phone)
        self.wallets[wallet.address] = wallet
        self.user_id_to_address[user_id] = wallet.address
        self.username_to_address[username] = wallet.address
        
        print(f"✓ Wallet created for {user_type_enum.value}: '{username}' (ID: {user_id})")
        return wallet
    
    def sync_users_from_db(self, db_users: List[Dict]) -> int:
        """
        Sync multiple users from database
        
        Args:
            db_users: List of user dictionaries from database
                     Each dict should have: user_id, username, user_type, email, phone
        
        Returns:
            Number of users synced
        """
        synced = 0
        for user_data in db_users:
            wallet = self.create_wallet_from_db(
                user_id=user_data.get('user_id') or user_data.get('id'),
                username=user_data.get('username'),
                user_type=user_data.get('user_type', 'user'),
                email=user_data.get('email'),
                phone=user_data.get('phone')
            )
            if wallet:
                synced += 1
        
        print(f"\n✓ Synced {synced} users from database to blockchain")
        return synced
    
    def get_wallet_by_user_id(self, user_id: int) -> Optional[Wallet]:
        """Get wallet by database user ID"""
        address = self.user_id_to_address.get(user_id)
        if address:
            return self.wallets.get(address)
        return None
    
    def get_wallet_by_username(self, username: str) -> Optional[Wallet]:
        """Get wallet by username"""
        address = self.username_to_address.get(username)
        if address:
            return self.wallets.get(address)
        return None
    
    def get_wallet_by_address(self, address: str) -> Optional[Wallet]:
        """Get wallet by blockchain address"""
        return self.wallets.get(address)
    
    def get_all_wallets(self) -> List[Wallet]:
        """Get all wallets in the system"""
        return list(self.wallets.values())
    
    def get_wallets_by_type(self, user_type: UserType) -> List[Wallet]:
        """Get all wallets of a specific user type"""
        return [w for w in self.wallets.values() if w.user_type == user_type]
    
    def get_user_count(self) -> int:
        """Get total number of users"""
        return len(self.wallets)
    
    def get_leaderboard(self, blockchain, limit: int = 10, force_refresh: bool = False) -> List[Dict]:
        """
        Get leaderboard of top GP holders
        
        Args:
            blockchain: Blockchain instance to get balances
            limit: Number of top users to return
            force_refresh: Force refresh of leaderboard cache
        
        Returns:
            List of user dictionaries with rankings
        """
        # Cache leaderboard for 5 minutes
        if not force_refresh and time.time() - self.leaderboard_last_updated < 300:
            return self.leaderboard_cache[:limit]
        
        leaderboard = []
        for wallet in self.wallets.values():
            balance = blockchain.get_balance(wallet.address)
            leaderboard.append({
                "rank": 0,  # Will be set after sorting
                "user_id": wallet.user_id,
                "username": wallet.username,
                "user_type": wallet.user_type.value,
                "address": wallet.address,
                "gp_balance": balance,
                "reward_points": wallet.reward_points,
                "tasks_completed": wallet.metadata.get("total_tasks_completed", 0),
                "total_gp_earned": wallet.metadata.get("total_gp_earned", 0)
            })
        
        # Sort by GP balance
        leaderboard.sort(key=lambda x: x["gp_balance"], reverse=True)
        
        # Assign ranks
        for i, user in enumerate(leaderboard, 1):
            user["rank"] = i
            # Update wallet metadata
            wallet = self.get_wallet_by_user_id(user["user_id"])
            if wallet:
                wallet.metadata["rank"] = i
        
        self.leaderboard_cache = leaderboard
        self.leaderboard_last_updated = time.time()
        
        return leaderboard[:limit]
    
    def get_leaderboard_json(self, blockchain, limit: int = 10) -> str:
        """Get leaderboard as JSON string"""
        leaderboard = self.get_leaderboard(blockchain, limit)
        return json.dumps({
            "success": True,
            "timestamp": time.time(),
            "total_users": self.get_user_count(),
            "leaderboard": leaderboard
        }, indent=2)
    
    def get_user_stats_json(self, user_id: int, blockchain) -> str:
        """
        Get detailed stats for a user as JSON
        
        Args:
            user_id: Database user ID
            blockchain: Blockchain instance
        
        Returns:
            JSON string with user statistics
        """
        wallet = self.get_wallet_by_user_id(user_id)
        
        if not wallet:
            return json.dumps({
                "success": False,
                "error": "User not found"
            })
        
        balance = blockchain.get_balance(wallet.address)
        tx_history = blockchain.get_transaction_history(wallet.address)
        
        # Get user's rank
        leaderboard = self.get_leaderboard(blockchain, limit=1000)
        rank = next((u["rank"] for u in leaderboard if u["user_id"] == user_id), 0)
        
        stats = {
            "success": True,
            "user": {
                "user_id": wallet.user_id,
                "username": wallet.username,
                "user_type": wallet.user_type.value,
                "email": wallet.email,
                "phone": wallet.phone,
                "address": wallet.address
            },
            "balances": {
                "gp_balance": balance,
                "reward_points": wallet.reward_points,
                "gp_multiplier": wallet.get_multiplier()
            },
            "statistics": {
                "rank": rank,
                "total_tasks_completed": wallet.metadata.get("total_tasks_completed", 0),
                "total_gp_earned": wallet.metadata.get("total_gp_earned", 0),
                "total_gp_spent": wallet.metadata.get("total_gp_spent", 0),
                "total_transactions": len(tx_history)
            },
            "recent_transactions": tx_history[-10:]  # Last 10 transactions
        }
        
        return json.dumps(stats, indent=2)
    
    def get_all_users_json(self, blockchain=None) -> str:
        """Get all users as JSON"""
        users = []
        for wallet in self.wallets.values():
            user_data = wallet.to_dict()
            if blockchain:
                user_data["gp_balance"] = blockchain.get_balance(wallet.address)
            users.append(user_data)
        
        return json.dumps({
            "success": True,
            "total_users": len(users),
            "users": users
        }, indent=2)
    
    def display_all_users(self, blockchain=None) -> None:
        """Display all users and their balances"""
        print("\n" + "="*80)
        print("USER DIRECTORY - CENTRALIZED BLOCKCHAIN SYSTEM")
        print("="*80)
        
        # Group by user type
        for user_type in UserType:
            wallets = self.get_wallets_by_type(user_type)
            if wallets:
                print(f"\n📊 {user_type.value.upper()}S ({len(wallets)})")
                print("-" * 80)
                
                for wallet in wallets:
                    print(f"ID: {wallet.user_id} | Username: {wallet.username}")
                    print(f"Address: {wallet.address}")
                    if wallet.email:
                        print(f"Email: {wallet.email}")
                    
                    if blockchain:
                        balance = blockchain.get_balance(wallet.address)
                        print(f"GP Balance: {balance} (x{wallet.get_multiplier()} multiplier)")
                        print(f"Reward Points: {wallet.reward_points}")
                    
                    print(f"Tasks Completed: {wallet.metadata.get('total_tasks_completed', 0)}")
                    print("-" * 80)
    
    def save_to_file(self, filename: str = "blockchain_users.json") -> None:
        """Save all wallets to a JSON file"""
        data = {
            "wallets": [wallet.to_dict() for wallet in self.wallets.values()],
            "timestamp": time.time(),
            "total_users": self.get_user_count()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Users saved to {filename}")
    
    def load_from_file(self, filename: str = "blockchain_users.json") -> bool:
        """Load wallets from a JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for wallet_data in data["wallets"]:
                user_type = UserType(wallet_data["user_type"])
                wallet = Wallet(
                    wallet_data["user_id"],
                    wallet_data["username"],
                    user_type,
                    wallet_data.get("email"),
                    wallet_data.get("phone")
                )
                wallet.address = wallet_data["address"]
                wallet.created_at = wallet_data["created_at"]
                wallet.reward_points = wallet_data.get("reward_points", 0)
                wallet.metadata = wallet_data.get("metadata", {})
                
                self.wallets[wallet.address] = wallet
                self.user_id_to_address[wallet.user_id] = wallet.address
                self.username_to_address[wallet.username] = wallet.address
            
            print(f"✓ Loaded {len(self.wallets)} users from {filename}")
            return True
        
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except Exception as e:
            print(f"Error loading users: {e}")
            return False
