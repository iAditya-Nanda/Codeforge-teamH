"""
Centralized Admin System for Green Points Blockchain
Provides administrative controls for managing the system
"""

import json
import time
from typing import Dict, List, Optional
from blockchain import Blockchain
from wallet_centralized import UserManager, UserType
from tasks import TaskManager, Task, TaskCategory
from database import DatabaseSync


class AdminSystem:
    """
    Centralized administration system for managing the blockchain
    """
    
    def __init__(self, blockchain: Blockchain, user_manager: UserManager, 
                 task_manager: TaskManager, db_sync: Optional[DatabaseSync] = None):
        self.blockchain = blockchain
        self.user_manager = user_manager
        self.task_manager = task_manager
        self.db_sync = db_sync
        self.admin_actions_log = []
    
    def log_action(self, action: str, details: str, admin_id: Optional[int] = None):
        """Log an administrative action"""
        log_entry = {
            "timestamp": time.time(),
            "action": action,
            "details": details,
            "admin_id": admin_id
        }
        self.admin_actions_log.append(log_entry)
    
    # ============ USER MANAGEMENT ============
    
    def create_user_manual(self, user_id: int, username: str, user_type: str,
                          email: str = None, phone: str = None, admin_id: int = None) -> str:
        """
        Manually create a user (admin function)
        
        Returns:
            JSON response
        """
        wallet = self.user_manager.create_wallet_from_db(
            user_id, username, user_type, email, phone
        )
        
        if wallet:
            self.log_action("create_user", f"Created user: {username} ({user_type})", admin_id)
            return json.dumps({
                "success": True,
                "message": f"User {username} created",
                "user": wallet.to_dict()
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "error": "User already exists or creation failed"
            }, indent=2)
    
    def grant_bonus_gp(self, user_id: int, amount: float, reason: str = "Admin bonus",
                      admin_id: int = None) -> str:
        """
        Grant bonus GP to a user (admin function)
        
        Returns:
            JSON response
        """
        wallet = self.user_manager.get_wallet_by_user_id(user_id)
        
        if not wallet:
            return json.dumps({"success": False, "error": "User not found"})
        
        from transaction import Transaction
        tx = Transaction(
            sender="ADMIN",
            recipient=wallet.address,
            amount=amount,
            transaction_type="task_reward",
            metadata={"admin_bonus": True, "reason": reason}
        )
        
        self.blockchain.add_transaction(tx.to_dict())
        self.log_action("grant_bonus", f"Granted {amount} GP to {wallet.username}: {reason}", admin_id)
        
        return json.dumps({
            "success": True,
            "message": f"Granted {amount} GP to {wallet.username}",
            "pending_mining": True
        }, indent=2)
    
    def adjust_user_reward_points(self, user_id: int, amount: float, 
                                  admin_id: int = None) -> str:
        """
        Adjust user's reward points balance (admin function)
        
        Returns:
            JSON response
        """
        wallet = self.user_manager.get_wallet_by_user_id(user_id)
        
        if not wallet:
            return json.dumps({"success": False, "error": "User not found"})
        
        old_balance = wallet.reward_points
        wallet.reward_points += amount
        
        self.log_action("adjust_rewards", 
                       f"Adjusted {wallet.username}'s reward points by {amount} (from {old_balance} to {wallet.reward_points})",
                       admin_id)
        
        return json.dumps({
            "success": True,
            "message": "Reward points adjusted",
            "old_balance": old_balance,
            "adjustment": amount,
            "new_balance": wallet.reward_points
        }, indent=2)
    
    # ============ TASK MANAGEMENT ============
    
    def create_task(self, name: str, description: str, reward_points: float,
                   category: str, difficulty: str = "medium",
                   verification_required: bool = False, admin_id: int = None) -> str:
        """
        Create a new task (admin function)
        
        Returns:
            JSON response
        """
        try:
            category_enum = TaskCategory(category.lower())
        except ValueError:
            return json.dumps({
                "success": False,
                "error": f"Invalid category: {category}"
            })
        
        task = Task(name, description, reward_points, category_enum, 
                   difficulty, verification_required)
        
        if self.task_manager.add_task(task):
            self.log_action("create_task", f"Created task: {name} ({reward_points} GP)", admin_id)
            return json.dumps({
                "success": True,
                "message": "Task created successfully",
                "task": task.to_dict()
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "error": "Task creation failed"
            })
    
    def verify_task_completion(self, completion_id: str, admin_id: int = None) -> str:
        """
        Manually verify a task completion (admin function)
        
        Returns:
            JSON response
        """
        verified = self.task_manager.verify_completion(completion_id)
        
        if verified:
            self.log_action("verify_task", f"Verified completion: {completion_id}", admin_id)
            return json.dumps({
                "success": True,
                "message": "Task completion verified"
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "error": "Completion not found"
            })
    
    # ============ BLOCKCHAIN MANAGEMENT ============
    
    def force_mine_block(self, miner_address: str = "ADMIN", admin_id: int = None) -> str:
        """
        Force mine a block (admin function)
        
        Returns:
            JSON response
        """
        if len(self.blockchain.pending_transactions) == 0:
            return json.dumps({
                "success": False,
                "error": "No pending transactions"
            })
        
        block = self.blockchain.mine_pending_transactions(miner_address)
        self.log_action("force_mine", f"Forced mining of block #{block.index}", admin_id)
        
        # Update task completions
        for tx in block.transactions:
            if tx.get("type") == "task_reward" and tx.get("task_id"):
                for completion in self.task_manager.completions:
                    if (completion.task_id == tx["task_id"] and 
                        completion.user_address == tx["to"] and
                        completion.status.value == "verified"):
                        completion.mark_rewarded(tx.get("transaction_id", ""))
        
        return json.dumps({
            "success": True,
            "message": f"Block #{block.index} mined",
            "block": block.to_dict()
        }, indent=2)
    
    def adjust_mining_difficulty(self, new_difficulty: int, admin_id: int = None) -> str:
        """
        Adjust blockchain mining difficulty (admin function)
        
        Returns:
            JSON response
        """
        old_difficulty = self.blockchain.difficulty
        self.blockchain.difficulty = new_difficulty
        
        self.log_action("adjust_difficulty", 
                       f"Changed difficulty from {old_difficulty} to {new_difficulty}",
                       admin_id)
        
        return json.dumps({
            "success": True,
            "message": "Mining difficulty adjusted",
            "old_difficulty": old_difficulty,
            "new_difficulty": new_difficulty
        }, indent=2)
    
    def adjust_mining_reward(self, new_reward: float, admin_id: int = None) -> str:
        """
        Adjust mining reward (admin function)
        
        Returns:
            JSON response
        """
        old_reward = self.blockchain.mining_reward
        self.blockchain.mining_reward = new_reward
        
        self.log_action("adjust_reward", 
                       f"Changed mining reward from {old_reward} to {new_reward}",
                       admin_id)
        
        return json.dumps({
            "success": True,
            "message": "Mining reward adjusted",
            "old_reward": old_reward,
            "new_reward": new_reward
        }, indent=2)
    
    # ============ DATABASE SYNC ============
    
    def sync_database(self, admin_id: int = None) -> str:
        """
        Manually trigger database sync (admin function)
        
        Returns:
            JSON response
        """
        if not self.db_sync:
            return json.dumps({
                "success": False,
                "error": "Database sync not configured"
            })
        
        total, synced = self.db_sync.sync_to_blockchain(self.user_manager)
        self.log_action("db_sync", f"Synced {synced} users from database", admin_id)
        
        return json.dumps({
            "success": True,
            "message": "Database sync completed",
            "total_new_users": total,
            "synced": synced
        }, indent=2)
    
    # ============ REPORTING ============
    
    def get_admin_dashboard(self) -> str:
        """
        Get admin dashboard with system overview
        
        Returns:
            JSON response with comprehensive stats
        """
        total_gp = sum(self.blockchain.get_balance(w.address) 
                      for w in self.user_manager.get_all_wallets())
        
        total_reward_points = sum(w.reward_points 
                                 for w in self.user_manager.get_all_wallets())
        
        dashboard = {
            "system_health": {
                "blockchain_valid": self.blockchain.is_chain_valid(),
                "chain_length": len(self.blockchain.chain),
                "pending_transactions": len(self.blockchain.pending_transactions)
            },
            "users": {
                "total": self.user_manager.get_user_count(),
                "tourists": len(self.user_manager.get_wallets_by_type(UserType.TOURIST)),
                "regular_users": len(self.user_manager.get_wallets_by_type(UserType.USER)),
                "businesses": len(self.user_manager.get_wallets_by_type(UserType.BUSINESS))
            },
            "economy": {
                "total_gp_circulation": total_gp,
                "total_reward_points": total_reward_points,
                "mining_reward": self.blockchain.mining_reward,
                "mining_difficulty": self.blockchain.difficulty
            },
            "tasks": {
                "total_tasks": len(self.task_manager.tasks),
                "total_completions": len(self.task_manager.completions),
                "pending_verification": len([c for c in self.task_manager.completions 
                                            if c.status.value == "pending"]),
                "rewarded": len(self.task_manager.get_verified_completions(rewarded=True))
            },
            "recent_admin_actions": self.admin_actions_log[-10:]  # Last 10 actions
        }
        
        return json.dumps({
            "success": True,
            "dashboard": dashboard,
            "timestamp": time.time()
        }, indent=2)
    
    def get_action_log(self, limit: int = 50) -> str:
        """
        Get admin action log
        
        Returns:
            JSON response with action history
        """
        return json.dumps({
            "success": True,
            "total_actions": len(self.admin_actions_log),
            "actions": self.admin_actions_log[-limit:]
        }, indent=2)
    
    def export_system_data(self) -> str:
        """
        Export complete system data for backup
        
        Returns:
            JSON string with all system data
        """
        export_data = {
            "export_timestamp": time.time(),
            "blockchain": {
                "chain": [block.to_dict() for block in self.blockchain.chain],
                "pending": self.blockchain.pending_transactions,
                "difficulty": self.blockchain.difficulty,
                "mining_reward": self.blockchain.mining_reward
            },
            "users": [wallet.to_dict() for wallet in self.user_manager.get_all_wallets()],
            "tasks": [task.to_dict() for task in self.task_manager.get_all_tasks()],
            "completions": [c.to_dict() for c in self.task_manager.completions],
            "admin_log": self.admin_actions_log
        }
        
        self.log_action("export_data", "Exported complete system data")
        
        return json.dumps(export_data, indent=2)
    
    def save_system_backup(self, filename: str = "blockchain_backup.json") -> str:
        """
        Save complete system backup to file
        
        Returns:
            JSON response
        """
        data = self.export_system_data()
        
        try:
            with open(filename, 'w') as f:
                f.write(data)
            
            return json.dumps({
                "success": True,
                "message": f"System backup saved to {filename}",
                "filename": filename
            }, indent=2)
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })
