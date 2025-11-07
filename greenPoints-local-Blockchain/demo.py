#!/usr/bin/env python3
"""
Green Points Blockchain - Demo Simulation
Demonstrates the complete blockchain system with simulated users and tasks
"""

import time
from blockchain import Blockchain
from wallet import UserManager
from tasks import TaskManager, TaskCategory
from transaction import Transaction


def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def simulate_green_points_blockchain():
    """Run a complete simulation of the green points blockchain system"""
    
    print("\n" + "🌱"*40)
    print("GREEN POINTS BLOCKCHAIN - SIMULATION")
    print("🌱"*40)
    
    # Initialize system
    print_section("INITIALIZING BLOCKCHAIN SYSTEM")
    blockchain = Blockchain(difficulty=2)
    user_manager = UserManager()
    task_manager = TaskManager()
    print("✓ Blockchain initialized")
    print("✓ User manager initialized")
    print("✓ Task manager initialized with default tasks")
    
    # Create users
    print_section("CREATING USERS")
    users = [
        ("alice", "alice@greenpoints.com"),
        ("bob", "bob@greenpoints.com"),
        ("charlie", "charlie@greenpoints.com"),
        ("diana", "diana@greenpoints.com")
    ]
    
    wallets = {}
    for username, email in users:
        wallet = user_manager.create_wallet(username, email)
        wallets[username] = wallet
    
    # Display initial state
    print_section("INITIAL USER BALANCES")
    user_manager.display_all_users(blockchain)
    
    # Display available tasks
    print_section("AVAILABLE GREEN TASKS")
    task_manager.display_all_tasks()
    
    # Simulate task completions
    print_section("SIMULATING TASK COMPLETIONS")
    
    # Alice completes tasks
    print("\n👤 Alice's activities:")
    tasks = task_manager.get_all_tasks()
    alice_tasks = [
        (tasks[0], "Recycled 7kg of paper at local center"),
        (tasks[2], "Planted oak tree in community park"),
        (tasks[4], "Biked to work Mon-Fri")
    ]
    
    for task, evidence in alice_tasks:
        completion = task_manager.complete_task(
            task.task_id, 
            wallets["alice"].address, 
            evidence
        )
        if completion.status.value == "verified":
            tx = Transaction(
                sender="SYSTEM",
                recipient=wallets["alice"].address,
                amount=task.reward_points,
                transaction_type="task_reward",
                task_id=task.task_id,
                task_name=task.name
            )
            blockchain.add_transaction(tx.to_dict())
    
    # Bob completes tasks
    print("\n👤 Bob's activities:")
    bob_tasks = [
        (tasks[1], "Collected 5kg of plastic bottles"),
        (tasks[3], "Used subway for entire week"),
        (tasks[7], "Started kitchen composting system")
    ]
    
    for task, evidence in bob_tasks:
        completion = task_manager.complete_task(
            task.task_id,
            wallets["bob"].address,
            evidence
        )
        if completion.status.value == "verified":
            tx = Transaction(
                sender="SYSTEM",
                recipient=wallets["bob"].address,
                amount=task.reward_points,
                transaction_type="task_reward",
                task_id=task.task_id,
                task_name=task.name
            )
            blockchain.add_transaction(tx.to_dict())
    
    # Charlie completes tasks
    print("\n👤 Charlie's activities:")
    charlie_tasks = [
        (tasks[6], "Installed 15 LED bulbs at home"),
        (tasks[9], "Installed low-flow shower heads"),
        (tasks[11], "Attended climate change workshop")
    ]
    
    for task, evidence in charlie_tasks:
        completion = task_manager.complete_task(
            task.task_id,
            wallets["charlie"].address,
            evidence
        )
        if completion.status.value == "verified":
            tx = Transaction(
                sender="SYSTEM",
                recipient=wallets["charlie"].address,
                amount=task.reward_points,
                transaction_type="task_reward",
                task_id=task.task_id,
                task_name=task.name
            )
            blockchain.add_transaction(tx.to_dict())
    
    # Diana completes tasks
    print("\n👤 Diana's activities:")
    diana_tasks = [
        (tasks[8], "Zero waste shopping for 10 days"),
        (tasks[10], "Organized neighborhood cleanup"),
    ]
    
    for task, evidence in diana_tasks:
        completion = task_manager.complete_task(
            task.task_id,
            wallets["diana"].address,
            evidence
        )
        if completion.status.value == "verified":
            tx = Transaction(
                sender="SYSTEM",
                recipient=wallets["diana"].address,
                amount=task.reward_points,
                transaction_type="task_reward",
                task_id=task.task_id,
                task_name=task.name
            )
            blockchain.add_transaction(tx.to_dict())
    
    # Mine first block
    print_section("MINING BLOCK #1")
    print(f"Pending transactions: {len(blockchain.pending_transactions)}")
    block1 = blockchain.mine_pending_transactions(wallets["alice"].address)
    print(f"✓ Block mined by Alice")
    
    # Update task completions
    for tx in block1.transactions:
        if tx.get("type") == "task_reward" and tx.get("task_id"):
            for completion in task_manager.completions:
                if (completion.task_id == tx["task_id"] and 
                    completion.user_address == tx["to"] and
                    completion.status.value == "verified"):
                    completion.mark_rewarded(tx.get("transaction_id", ""))
    
    # Show balances after mining
    print_section("BALANCES AFTER BLOCK #1")
    for username in ["alice", "bob", "charlie", "diana"]:
        balance = blockchain.get_balance(wallets[username].address)
        print(f"{username.capitalize()}: {balance} GP")
    
    # Simulate transfers
    print_section("SIMULATING GREEN POINTS TRANSFERS")
    
    # Alice transfers to Bob
    tx1 = Transaction(
        sender=wallets["alice"].address,
        recipient=wallets["bob"].address,
        amount=50,
        transaction_type="transfer"
    )
    blockchain.add_transaction(tx1.to_dict())
    print(f"✓ Alice -> Bob: 50 GP")
    
    # Charlie transfers to Diana
    tx2 = Transaction(
        sender=wallets["charlie"].address,
        recipient=wallets["diana"].address,
        amount=30,
        transaction_type="transfer"
    )
    blockchain.add_transaction(tx2.to_dict())
    print(f"✓ Charlie -> Diana: 30 GP")
    
    # Mine second block
    print_section("MINING BLOCK #2")
    print(f"Pending transactions: {len(blockchain.pending_transactions)}")
    block2 = blockchain.mine_pending_transactions(wallets["bob"].address)
    print(f"✓ Block mined by Bob")
    
    # Show final balances
    print_section("FINAL BALANCES")
    for username in ["alice", "bob", "charlie", "diana"]:
        balance = blockchain.get_balance(wallets[username].address)
        print(f"{username.capitalize()}: {balance} GP")
    
    # Display blockchain
    print_section("COMPLETE BLOCKCHAIN")
    blockchain.display_chain()
    
    # Validate blockchain
    print_section("BLOCKCHAIN VALIDATION")
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        print("✓ Blockchain is VALID ✓")
        print("All blocks are properly linked and hashed correctly!")
    else:
        print("✗ Blockchain is INVALID")
    
    # Display leaderboard
    print_section("GREEN POINTS LEADERBOARD")
    task_manager.display_leaderboard(blockchain)
    
    # Display statistics
    print_section("SYSTEM STATISTICS")
    print(f"Total Users: {user_manager.get_user_count()}")
    print(f"Total Tasks Available: {len(task_manager.tasks)}")
    print(f"Tasks Completed: {len(task_manager.completions)}")
    print(f"Tasks Rewarded: {len(task_manager.get_verified_completions(rewarded=True))}")
    print(f"Blockchain Length: {len(blockchain.chain)} blocks")
    print(f"Mining Difficulty: {blockchain.difficulty}")
    
    # Calculate total GP
    total_gp = sum(blockchain.get_balance(wallet.address) 
                   for wallet in user_manager.get_all_wallets())
    print(f"Total GP in Circulation: {total_gp}")
    
    # Show transaction history for Alice
    print_section("ALICE'S TRANSACTION HISTORY")
    history = blockchain.get_transaction_history(wallets["alice"].address)
    for tx in history:
        print(f"Block #{tx['block_index']}: {tx['from']} -> {tx['to']}: {tx['amount']} GP")
        if 'task_name' in tx:
            print(f"  Task: {tx['task_name']}")
        print()
    
    # Success message
    print("\n" + "🎉"*40)
    print("SIMULATION COMPLETED SUCCESSFULLY!")
    print("🎉"*40)
    print("\nThe Green Points Blockchain is working perfectly!")
    print("All blocks are validated and the system is ready for use.")
    print("\nTo interact with the system, run: python cli.py")
    print("\n")


if __name__ == "__main__":
    simulate_green_points_blockchain()
