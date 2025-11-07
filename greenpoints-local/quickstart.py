#!/usr/bin/env python3
"""
Green Points Blockchain - Quick Start Guide
This script provides a quick interactive introduction to the blockchain
"""

import sys


def print_header():
    print("\n" + "="*80)
    print("🌱 GREEN POINTS BLOCKCHAIN - QUICK START GUIDE 🌱")
    print("="*80 + "\n")


def print_what_is_it():
    print("📚 WHAT IS THIS?")
    print("-" * 80)
    print("""
This is a fully functional blockchain implementation running locally on your
laptop. It's designed to reward environmental actions with Green Points (GP).

Key Features:
  ✓ Complete blockchain with proof-of-work mining
  ✓ Cryptographic hashing (SHA-256)
  ✓ Task-based reward system
  ✓ User wallets and transfers
  ✓ Transparent transaction history
  ✓ Chain validation
""")


def print_how_to_use():
    print("\n🚀 HOW TO USE")
    print("-" * 80)
    print("""
1. RUN THE DEMO (Recommended for first-time users):
   python3 demo.py
   
   This shows a complete simulation with:
   - 4 users (Alice, Bob, Charlie, Diana)
   - Multiple task completions
   - Block mining
   - Transfers between users
   - Complete blockchain visualization

2. USE THE INTERACTIVE CLI:
   python3 cli.py
   
   This gives you full control to:
   - Create your own users
   - Complete tasks
   - Mine blocks
   - Transfer green points
   - View blockchain state
   - Check balances and history

3. USE AS A PYTHON MODULE:
   Import the components in your own scripts:
   
   from blockchain import Blockchain
   from wallet import UserManager
   from tasks import TaskManager
   
   Then build your own applications!
""")


def print_sample_workflow():
    print("\n💡 SAMPLE WORKFLOW")
    print("-" * 80)
    print("""
Here's a typical user journey:

1. CREATE ACCOUNT
   → User creates a wallet with unique address

2. COMPLETE A GREEN TASK
   → User completes "Recycle Paper" (50 GP)
   → Transaction added to pending pool

3. MINE A BLOCK
   → Miner processes pending transactions
   → User receives 50 GP
   → Miner receives 10 GP mining reward

4. TRANSFER POINTS
   → User can transfer GP to other users
   → Transactions are immutable once mined

5. VIEW BLOCKCHAIN
   → See complete transaction history
   → Verify blockchain integrity
   → Check leaderboard
""")


def print_green_tasks():
    print("\n📋 AVAILABLE GREEN TASKS")
    print("-" * 80)
    print("""
Sample tasks you can complete:

🔄 Recycling
   • Recycle Paper (50 GP)
   • Recycle Plastic (45 GP)

🌳 Environment
   • Plant a Tree (100 GP)
   • Community Cleanup (85 GP)

⚡ Energy
   • LED Bulb Installation (60 GP)
   • Save Electricity (120 GP)

🚲 Transportation
   • Bike to Work (80 GP)
   • Use Public Transport (75 GP)

And more! View all tasks with: python3 cli.py
""")


def print_blockchain_concepts():
    print("\n🔗 BLOCKCHAIN CONCEPTS")
    print("-" * 80)
    print("""
BLOCKS:
  Each block contains:
  - Multiple transactions
  - Hash of previous block (creates the chain)
  - Nonce (proof-of-work)
  - Timestamp

MINING:
  Miners find a nonce that makes the block hash start with zeros
  Difficulty: 2 (hash must start with "00...")
  Reward: 10 GP per block

TRANSACTIONS:
  - Task Rewards: SYSTEM → User (earn GP for tasks)
  - Transfers: User → User (send GP to others)
  - Mining Rewards: SYSTEM → Miner (reward for mining)

VALIDATION:
  Every block is cryptographically linked
  Tampering with one block invalidates entire chain
  Anyone can verify the blockchain
""")


def print_commands():
    print("\n⌨️  QUICK COMMANDS")
    print("-" * 80)
    print("""
# See the system in action
python3 demo.py

# Interactive mode
python3 cli.py

# View this guide
python3 quickstart.py

# Check Python version (requires 3.7+)
python3 --version
""")


def print_project_structure():
    print("\n📁 PROJECT FILES")
    print("-" * 80)
    print("""
blockchain.py    - Core blockchain implementation
transaction.py   - Transaction management
wallet.py        - User wallet system
tasks.py         - Green task definitions
cli.py          - Interactive command-line interface
demo.py         - Automated demonstration
README.md       - Detailed documentation
quickstart.py   - This guide!
""")


def print_footer():
    print("\n" + "="*80)
    print("Ready to start? Run: python3 demo.py")
    print("="*80 + "\n")


def main():
    print_header()
    
    sections = [
        ("1", "What is this?", print_what_is_it),
        ("2", "How to use", print_how_to_use),
        ("3", "Sample workflow", print_sample_workflow),
        ("4", "Green tasks", print_green_tasks),
        ("5", "Blockchain concepts", print_blockchain_concepts),
        ("6", "Quick commands", print_commands),
        ("7", "Project structure", print_project_structure),
    ]
    
    if len(sys.argv) > 1:
        # Show specific section
        try:
            section_num = sys.argv[1]
            for num, title, func in sections:
                if num == section_num:
                    func()
                    return
            print(f"Invalid section number. Use 1-{len(sections)}")
        except:
            pass
    
    # Show all sections
    for _, _, func in sections:
        func()
    
    print_footer()


if __name__ == "__main__":
    main()
