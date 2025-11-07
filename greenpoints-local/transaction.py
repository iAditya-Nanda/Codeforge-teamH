"""
Transaction Management for Green Points Blockchain
"""

import time
import hashlib
import json
from typing import Dict, Optional


class Transaction:
    """Represents a transaction in the Green Points system"""
    
    def __init__(self, sender: str, recipient: str, amount: float, 
                 transaction_type: str = "transfer", task_id: Optional[str] = None,
                 task_name: Optional[str] = None, metadata: Optional[Dict] = None):
        """
        Initialize a transaction
        
        Args:
            sender: Address sending green points
            recipient: Address receiving green points
            amount: Amount of green points
            transaction_type: Type of transaction (transfer, task_reward, mining_reward)
            task_id: Optional task identifier
            task_name: Optional task name
            metadata: Optional additional metadata
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.transaction_type = transaction_type
        self.task_id = task_id
        self.task_name = task_name
        self.metadata = metadata or {}
        self.timestamp = time.time()
        self.transaction_id = self.generate_transaction_id()
    
    def generate_transaction_id(self) -> str:
        """Generate a unique transaction ID"""
        tx_string = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "type": self.transaction_type
        }, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary format"""
        tx_dict = {
            "transaction_id": self.transaction_id,
            "from": self.sender,
            "to": self.recipient,
            "amount": self.amount,
            "type": self.transaction_type,
            "timestamp": self.timestamp
        }
        
        if self.task_id:
            tx_dict["task_id"] = self.task_id
        if self.task_name:
            tx_dict["task_name"] = self.task_name
        if self.metadata:
            tx_dict["metadata"] = self.metadata
        
        return tx_dict
    
    def is_valid(self) -> bool:
        """
        Validate the transaction
        
        Returns:
            True if transaction is valid
        """
        if self.amount <= 0:
            return False
        
        if not self.sender or not self.recipient:
            return False
        
        if self.transaction_type not in ["transfer", "task_reward", "mining_reward"]:
            return False
        
        return True
    
    def __str__(self) -> str:
        """String representation of transaction"""
        return f"Transaction({self.sender} -> {self.recipient}: {self.amount} GP)"
    
    def __repr__(self) -> str:
        return self.__str__()


class TransactionPool:
    """Manages pending transactions"""
    
    def __init__(self):
        self.pending_transactions = []
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """
        Add a transaction to the pool
        
        Args:
            transaction: Transaction to add
        
        Returns:
            True if transaction was added successfully
        """
        if not transaction.is_valid():
            print(f"Invalid transaction: {transaction}")
            return False
        
        self.pending_transactions.append(transaction)
        print(f"Transaction added to pool: {transaction.transaction_id}")
        return True
    
    def get_transactions(self, limit: Optional[int] = None) -> list:
        """
        Get pending transactions
        
        Args:
            limit: Maximum number of transactions to return
        
        Returns:
            List of transaction dictionaries
        """
        transactions = [tx.to_dict() for tx in self.pending_transactions]
        if limit:
            return transactions[:limit]
        return transactions
    
    def clear(self) -> None:
        """Clear all pending transactions"""
        self.pending_transactions = []
    
    def remove_transaction(self, transaction_id: str) -> bool:
        """
        Remove a transaction from the pool
        
        Args:
            transaction_id: ID of transaction to remove
        
        Returns:
            True if transaction was removed
        """
        for i, tx in enumerate(self.pending_transactions):
            if tx.transaction_id == transaction_id:
                self.pending_transactions.pop(i)
                return True
        return False
    
    def get_count(self) -> int:
        """Get number of pending transactions"""
        return len(self.pending_transactions)
