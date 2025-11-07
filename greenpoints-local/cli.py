#!/usr/bin/env python3
"""
Green Points Blockchain - Command Line Interface
Interactive CLI for managing the green points blockchain system
"""

import sys
from blockchain import Blockchain
from wallet import UserManager
from tasks import TaskManager, TaskCategory
from transaction import Transaction


class GreenPointsCLI:
    """Command-line interface for Green Points Blockchain"""
    
    def __init__(self):
        self.blockchain = Blockchain(difficulty=2)
        self.user_manager = UserManager()
        self.task_manager = TaskManager()
        self.running = True
    
    def display_banner(self):
        """Display welcome banner"""
        print("\n" + "="*80)
        print("🌱 GREEN POINTS BLOCKCHAIN SYSTEM 🌱")
        print("="*80)
        print("A blockchain-based reward system for environmental actions")
        print("="*80 + "\n")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "─"*80)
        print("MAIN MENU")
        print("─"*80)
        print("👤 USER MANAGEMENT")
        print("  1. Create new user")
        print("  2. View all users")
        print("  3. Check user balance")
        print("\n📋 TASK MANAGEMENT")
        print("  4. View all tasks")
        print("  5. Complete a task")
        print("  6. View my completed tasks")
        print("\n⛏️  BLOCKCHAIN OPERATIONS")
        print("  7. Mine pending transactions")
        print("  8. View blockchain")
        print("  9. Validate blockchain")
        print("  10. View transaction history")
        print("\n📊 STATISTICS")
        print("  11. View leaderboard")
        print("  12. System statistics")
        print("\n🔧 OTHER")
        print("  13. Transfer green points")
        print("  0. Exit")
        print("─"*80)
    
    def create_user(self):
        """Create a new user"""
        print("\n--- CREATE NEW USER ---")
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty")
            return
        
        email = input("Enter email (optional): ").strip()
        email = email if email else None
        
        wallet = self.user_manager.create_wallet(username, email)
        if wallet:
            print(f"\n✓ Welcome, {username}!")
            print(f"Your wallet address: {wallet.address}")
    
    def view_all_users(self):
        """Display all users"""
        self.user_manager.display_all_users(self.blockchain)
    
    def check_balance(self):
        """Check balance for a user"""
        print("\n--- CHECK BALANCE ---")
        username = input("Enter username: ").strip()
        
        wallet = self.user_manager.get_wallet_by_username(username)
        if not wallet:
            print(f"User '{username}' not found")
            return
        
        balance = self.blockchain.get_balance(wallet.address)
        print(f"\n💰 {username}'s Balance: {balance} GP")
        print(f"Address: {wallet.address}")
    
    def view_all_tasks(self):
        """Display all available tasks"""
        self.task_manager.display_all_tasks()
    
    def complete_task(self):
        """Complete a task"""
        print("\n--- COMPLETE A TASK ---")
        username = input("Enter your username: ").strip()
        
        wallet = self.user_manager.get_wallet_by_username(username)
        if not wallet:
            print(f"User '{username}' not found")
            return
        
        # Show tasks
        tasks = self.task_manager.get_all_tasks()
        print("\nAvailable Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.name} - {task.reward_points} GP ({task.difficulty})")
        
        try:
            choice = int(input("\nSelect task number: "))
            if 1 <= choice <= len(tasks):
                task = tasks[choice - 1]
                evidence = input("Enter evidence/notes (optional): ").strip()
                evidence = evidence if evidence else None
                
                completion = self.task_manager.complete_task(
                    task.task_id, wallet.address, evidence
                )
                
                if completion and completion.status.value == "verified":
                    # Create transaction
                    tx = Transaction(
                        sender="SYSTEM",
                        recipient=wallet.address,
                        amount=task.reward_points,
                        transaction_type="task_reward",
                        task_id=task.task_id,
                        task_name=task.name
                    )
                    self.blockchain.add_transaction(tx.to_dict())
                    print(f"\n✓ Transaction added to pending pool")
                    print(f"Mine a block to receive your {task.reward_points} GP!")
            else:
                print("Invalid task number")
        except ValueError:
            print("Invalid input")
    
    def view_my_tasks(self):
        """View user's completed tasks"""
        print("\n--- MY COMPLETED TASKS ---")
        username = input("Enter your username: ").strip()
        
        wallet = self.user_manager.get_wallet_by_username(username)
        if not wallet:
            print(f"User '{username}' not found")
            return
        
        completions = self.task_manager.get_user_completions(wallet.address)
        
        if not completions:
            print("\nNo tasks completed yet")
            return
        
        print(f"\n{username}'s Completed Tasks:")
        print("-" * 80)
        for completion in completions:
            task = self.task_manager.get_task(completion.task_id)
            if task:
                print(f"Task: {task.name}")
                print(f"Reward: {task.reward_points} GP")
                print(f"Status: {completion.status.value}")
                print(f"Completed: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(completion.completed_at))}")
                print("-" * 80)
    
    def mine_block(self):
        """Mine pending transactions"""
        print("\n--- MINE BLOCK ---")
        username = input("Enter your username (miner): ").strip()
        
        wallet = self.user_manager.get_wallet_by_username(username)
        if not wallet:
            print(f"User '{username}' not found")
            return
        
        if len(self.blockchain.pending_transactions) == 0:
            print("\nNo pending transactions to mine")
            return
        
        print(f"\nPending transactions: {len(self.blockchain.pending_transactions)}")
        print(f"Mining reward: {self.blockchain.mining_reward} GP")
        
        confirm = input("\nStart mining? (y/n): ").strip().lower()
        if confirm == 'y':
            block = self.blockchain.mine_pending_transactions(wallet.address)
            print(f"\n✓ Block #{block.index} mined successfully!")
            print(f"You earned {self.blockchain.mining_reward} GP for mining")
            
            # Update task completions
            for tx in block.transactions:
                if tx.get("type") == "task_reward" and tx.get("task_id"):
                    for completion in self.task_manager.completions:
                        if (completion.task_id == tx["task_id"] and 
                            completion.user_address == tx["to"] and
                            completion.status.value == "verified"):
                            completion.mark_rewarded(tx.get("transaction_id", ""))
    
    def view_blockchain(self):
        """Display the blockchain"""
        self.blockchain.display_chain()
    
    def validate_blockchain(self):
        """Validate the blockchain"""
        print("\n--- BLOCKCHAIN VALIDATION ---")
        is_valid = self.blockchain.is_chain_valid()
        if is_valid:
            print("✓ Blockchain is VALID")
        else:
            print("✗ Blockchain is INVALID")
    
    def view_transaction_history(self):
        """View transaction history for a user"""
        print("\n--- TRANSACTION HISTORY ---")
        username = input("Enter username: ").strip()
        
        wallet = self.user_manager.get_wallet_by_username(username)
        if not wallet:
            print(f"User '{username}' not found")
            return
        
        history = self.blockchain.get_transaction_history(wallet.address)
        
        if not history:
            print(f"\nNo transactions found for {username}")
            return
        
        print(f"\nTransaction History for {username}:")
        print("="*80)
        for tx in history:
            print(f"Block: #{tx['block_index']}")
            print(f"From: {tx['from']}")
            print(f"To: {tx['to']}")
            print(f"Amount: {tx['amount']} GP")
            print(f"Type: {tx.get('type', 'transfer')}")
            if 'task_name' in tx:
                print(f"Task: {tx['task_name']}")
            print("-" * 80)
    
    def view_leaderboard(self):
        """View the leaderboard"""
        self.task_manager.display_leaderboard(self.blockchain)
    
    def view_statistics(self):
        """Display system statistics"""
        print("\n" + "="*80)
        print("SYSTEM STATISTICS")
        print("="*80)
        print(f"Total Users: {self.user_manager.get_user_count()}")
        print(f"Total Tasks Available: {len(self.task_manager.tasks)}")
        print(f"Tasks Completed: {len(self.task_manager.completions)}")
        print(f"Blockchain Length: {len(self.blockchain.chain)} blocks")
        print(f"Pending Transactions: {len(self.blockchain.pending_transactions)}")
        print(f"Mining Difficulty: {self.blockchain.difficulty}")
        print(f"Mining Reward: {self.blockchain.mining_reward} GP")
        
        # Calculate total green points in circulation
        total_gp = 0
        for wallet in self.user_manager.get_all_wallets():
            total_gp += self.blockchain.get_balance(wallet.address)
        print(f"Total GP in Circulation: {total_gp}")
        print("="*80)
    
    def transfer_points(self):
        """Transfer green points between users"""
        print("\n--- TRANSFER GREEN POINTS ---")
        sender_username = input("Your username (sender): ").strip()
        
        sender_wallet = self.user_manager.get_wallet_by_username(sender_username)
        if not sender_wallet:
            print(f"User '{sender_username}' not found")
            return
        
        sender_balance = self.blockchain.get_balance(sender_wallet.address)
        print(f"Your balance: {sender_balance} GP")
        
        recipient_username = input("Recipient username: ").strip()
        recipient_wallet = self.user_manager.get_wallet_by_username(recipient_username)
        if not recipient_wallet:
            print(f"User '{recipient_username}' not found")
            return
        
        try:
            amount = float(input("Amount to transfer: "))
            if amount <= 0:
                print("Amount must be positive")
                return
            
            if amount > sender_balance:
                print(f"Insufficient balance. You have {sender_balance} GP")
                return
            
            tx = Transaction(
                sender=sender_wallet.address,
                recipient=recipient_wallet.address,
                amount=amount,
                transaction_type="transfer"
            )
            
            if self.blockchain.add_transaction(tx.to_dict()):
                print(f"\n✓ Transaction added to pending pool")
                print(f"Mine a block to complete the transfer")
        except ValueError:
            print("Invalid amount")
    
    def run(self):
        """Run the CLI"""
        self.display_banner()
        
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.create_user()
            elif choice == "2":
                self.view_all_users()
            elif choice == "3":
                self.check_balance()
            elif choice == "4":
                self.view_all_tasks()
            elif choice == "5":
                self.complete_task()
            elif choice == "6":
                self.view_my_tasks()
            elif choice == "7":
                self.mine_block()
            elif choice == "8":
                self.view_blockchain()
            elif choice == "9":
                self.validate_blockchain()
            elif choice == "10":
                self.view_transaction_history()
            elif choice == "11":
                self.view_leaderboard()
            elif choice == "12":
                self.view_statistics()
            elif choice == "13":
                self.transfer_points()
            elif choice == "0":
                print("\n👋 Thank you for using Green Points Blockchain!")
                print("Keep making the world greener! 🌱\n")
                self.running = False
            else:
                print("\n❌ Invalid choice. Please try again.")
            
            if self.running and choice != "0":
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    import time
    cli = GreenPointsCLI()
    cli.run()
