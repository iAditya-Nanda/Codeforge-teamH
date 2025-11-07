"""
Wallet and User Management for Green Points Blockchain
"""

import json
import hashlib
import time
from typing import Dict, List, Optional


class Wallet:
    """Represents a user's wallet in the Green Points system"""
    
    def __init__(self, username: str, email: Optional[str] = None):
        """
        Initialize a wallet
        
        Args:
            username: User's username
            email: Optional email address
        """
        self.username = username
        self.email = email
        self.address = self.generate_address(username)
        self.created_at = time.time()
        self.metadata = {}
    
    def generate_address(self, username: str) -> str:
        """
        Generate a unique address for the wallet
        
        Args:
            username: Username to generate address from
        
        Returns:
            Unique wallet address
        """
        address_string = f"{username}_{time.time()}"
        return hashlib.sha256(address_string.encode()).hexdigest()[:20]
    
    def to_dict(self) -> Dict:
        """Convert wallet to dictionary format"""
        return {
            "username": self.username,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at,
            "metadata": self.metadata
        }
    
    def __str__(self) -> str:
        return f"Wallet({self.username}, {self.address})"
    
    def __repr__(self) -> str:
        return self.__str__()


class UserManager:
    """Manages all users and their wallets"""
    
    def __init__(self):
        self.wallets: Dict[str, Wallet] = {}  # address -> Wallet
        self.username_to_address: Dict[str, str] = {}  # username -> address
    
    def create_wallet(self, username: str, email: Optional[str] = None) -> Optional[Wallet]:
        """
        Create a new wallet for a user
        
        Args:
            username: Username for the new wallet
            email: Optional email address
        
        Returns:
            The created wallet or None if username exists
        """
        if username in self.username_to_address:
            print(f"Username '{username}' already exists")
            return None
        
        wallet = Wallet(username, email)
        self.wallets[wallet.address] = wallet
        self.username_to_address[username] = wallet.address
        
        print(f"✓ Wallet created for '{username}'")
        print(f"  Address: {wallet.address}")
        return wallet
    
    def get_wallet_by_username(self, username: str) -> Optional[Wallet]:
        """
        Get wallet by username
        
        Args:
            username: Username to look up
        
        Returns:
            Wallet object or None
        """
        address = self.username_to_address.get(username)
        if address:
            return self.wallets.get(address)
        return None
    
    def get_wallet_by_address(self, address: str) -> Optional[Wallet]:
        """
        Get wallet by address
        
        Args:
            address: Address to look up
        
        Returns:
            Wallet object or None
        """
        return self.wallets.get(address)
    
    def get_address(self, username: str) -> Optional[str]:
        """
        Get address for a username
        
        Args:
            username: Username to get address for
        
        Returns:
            Address or None
        """
        return self.username_to_address.get(username)
    
    def get_all_wallets(self) -> List[Wallet]:
        """Get all wallets in the system"""
        return list(self.wallets.values())
    
    def get_user_count(self) -> int:
        """Get total number of users"""
        return len(self.wallets)
    
    def display_all_users(self, blockchain=None) -> None:
        """
        Display all users and their balances
        
        Args:
            blockchain: Optional blockchain instance to get balances
        """
        print("\n" + "="*80)
        print("USER DIRECTORY")
        print("="*80)
        print(f"Total Users: {self.get_user_count()}\n")
        
        for wallet in self.wallets.values():
            print(f"Username: {wallet.username}")
            print(f"Address: {wallet.address}")
            if wallet.email:
                print(f"Email: {wallet.email}")
            
            if blockchain:
                balance = blockchain.get_balance(wallet.address)
                print(f"Balance: {balance} GP")
            
            print(f"Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(wallet.created_at))}")
            print("-" * 80)
    
    def save_to_file(self, filename: str = "wallets.json") -> None:
        """
        Save all wallets to a JSON file
        
        Args:
            filename: Name of file to save to
        """
        data = {
            "wallets": [wallet.to_dict() for wallet in self.wallets.values()],
            "timestamp": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Wallets saved to {filename}")
    
    def load_from_file(self, filename: str = "wallets.json") -> bool:
        """
        Load wallets from a JSON file
        
        Args:
            filename: Name of file to load from
        
        Returns:
            True if loaded successfully
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for wallet_data in data["wallets"]:
                wallet = Wallet(wallet_data["username"], wallet_data.get("email"))
                wallet.address = wallet_data["address"]
                wallet.created_at = wallet_data["created_at"]
                wallet.metadata = wallet_data.get("metadata", {})
                
                self.wallets[wallet.address] = wallet
                self.username_to_address[wallet.username] = wallet.address
            
            print(f"Loaded {len(self.wallets)} wallets from {filename}")
            return True
        
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except Exception as e:
            print(f"Error loading wallets: {e}")
            return False
