"""
Core Blockchain Implementation for Green Points Reward System
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: float, transactions: List[Dict], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """
        Mine the block using proof-of-work
        
        Args:
            difficulty: Number of leading zeros required in hash
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary format"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    """The main blockchain class managing the chain and transactions"""
    
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
        self.mining_reward = 10  # Green points reward for mining
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the first block in the chain"""
        genesis_block = Block(0, time.time(), [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict) -> bool:
        """
        Add a transaction to the pending transactions pool
        
        Args:
            transaction: Dictionary containing transaction details
        
        Returns:
            True if transaction was added successfully
        """
        # Validate required fields
        required_fields = ["from", "to", "amount"]
        if not all(field in transaction for field in required_fields):
            print("Transaction missing required fields")
            return False
        
        if transaction["amount"] <= 0:
            print("Transaction amount must be positive")
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, miner_address: str) -> Block:
        """
        Mine all pending transactions into a new block
        
        Args:
            miner_address: Address of the miner to receive the reward
        
        Returns:
            The newly mined block
        """
        # Create reward transaction for miner
        reward_transaction = {
            "from": "SYSTEM",
            "to": miner_address,
            "amount": self.mining_reward,
            "type": "mining_reward",
            "timestamp": time.time()
        }
        
        # Create new block with pending transactions
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions + [reward_transaction],
            previous_hash=self.get_latest_block().hash
        )
        
        print(f"\nMining block {block.index}...")
        block.mine_block(self.difficulty)
        
        self.chain.append(block)
        self.pending_transactions = []  # Clear pending transactions
        
        return block
    
    def get_balance(self, address: str) -> float:
        """
        Calculate the balance of an address by going through all transactions
        
        Args:
            address: The address to check balance for
        
        Returns:
            The current balance
        """
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["from"] == address:
                    balance -= transaction["amount"]
                if transaction["to"] == address:
                    balance += transaction["amount"]
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain
        
        Returns:
            True if the blockchain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            
            # Check if previous hash reference is correct
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
            
            # Check if block meets difficulty requirement
            if not current_block.hash.startswith("0" * self.difficulty):
                print(f"Block {i} not properly mined")
                return False
        
        return True
    
    def get_transaction_history(self, address: str) -> List[Dict]:
        """
        Get all transactions involving a specific address
        
        Args:
            address: The address to get history for
        
        Returns:
            List of transactions
        """
        history = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["from"] == address or transaction["to"] == address:
                    history.append({
                        **transaction,
                        "block_index": block.index,
                        "block_hash": block.hash
                    })
        
        return history
    
    def display_chain(self) -> None:
        """Display the entire blockchain in a readable format"""
        print("\n" + "="*80)
        print("BLOCKCHAIN STATE")
        print("="*80)
        print(f"Chain Length: {len(self.chain)}")
        print(f"Difficulty: {self.difficulty}")
        print(f"Pending Transactions: {len(self.pending_transactions)}")
        print("="*80)
        
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Nonce: {block.nonce}")
            print(f"Transactions ({len(block.transactions)}):")
            for tx in block.transactions:
                print(f"  - {tx['from']} -> {tx['to']}: {tx['amount']} GP", end="")
                if "task_id" in tx:
                    print(f" [Task: {tx['task_id']}]", end="")
                print()
            print("-" * 80)
