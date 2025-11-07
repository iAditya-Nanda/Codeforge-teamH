#!/usr/bin/env python3
"""
Centralized Green Points Blockchain - Demo with JSON API
Demonstrates the complete system with 3 user types, database sync, and JSON outputs
"""

import json
import time
from blockchain import Blockchain
from wallet_centralized import UserManager, UserType
from tasks import TaskManager
from api import BlockchainAPI
from database import DatabaseSync, simulate_user_signup, auto_sync_new_signups
from admin import AdminSystem


def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_json_response(title, json_str):
    """Print a JSON response nicely"""
    print(f"\n📋 {title}")
    print("-" * 80)
    print(json_str)
    print()


def demo_centralized_blockchain():
    """Run complete demonstration of centralized blockchain system"""
    
    print("\n" + "🌱"*40)
    print("CENTRALIZED GREEN POINTS BLOCKCHAIN SYSTEM")
    print("With 3 User Types, SQL Database, and JSON API")
    print("🌱"*40)
    
    # ============ INITIALIZATION ============
    print_section("STEP 1: INITIALIZING SYSTEM")
    
    blockchain = Blockchain(difficulty=2)
    user_manager = UserManager()
    task_manager = TaskManager()
    
    print("✓ Blockchain initialized")
    print("✓ User manager initialized")
    print("✓ Task manager initialized")
    
    # Initialize database
    db = DatabaseSync("greenpoints_demo.db")
    db.connect()
    db.create_tables()
    print("✓ Database connected and tables created")
    
    # Initialize API and Admin
    api = BlockchainAPI(blockchain, user_manager, task_manager)
    admin = AdminSystem(blockchain, user_manager, task_manager, db)
    print("✓ API layer initialized")
    print("✓ Admin system initialized")
    
    # ============ DATABASE SIGNUP SIMULATION ============
    print_section("STEP 2: SIMULATING USER SIGNUPS IN DATABASE")
    
    # Simulate user signups (as they would happen in your app)
    signups = [
        ("tourist_alice", "tourist", "alice@tour.com", "+1111111111"),
        ("tourist_bob", "tourist", "bob@tour.com", "+1111111112"),
        ("user_charlie", "user", "charlie@greenpoints.com", "+1111111113"),
        ("user_diana", "user", "diana@greenpoints.com", "+1111111114"),
        ("business_echo", "business", "echo@business.com", "+1111111115"),
        ("business_frank", "business", "frank@business.com", "+1111111116"),
    ]
    
    user_ids = []
    for username, user_type, email, phone in signups:
        user_id = simulate_user_signup(db, username, user_type, email, phone)
        if user_id:
            user_ids.append(user_id)
    
    print(f"\n✓ {len(user_ids)} users signed up in database")
    
    # ============ SYNC TO BLOCKCHAIN ============
    print_section("STEP 3: SYNCING DATABASE USERS TO BLOCKCHAIN")
    
    synced = auto_sync_new_signups(db, user_manager)
    print(f"✓ {synced} users synced to blockchain with unique addresses")
    
    # ============ API DEMO: GET ALL USERS ============
    print_section("STEP 4: API DEMO - GET ALL USERS (JSON)")
    
    all_users_json = api.get_all_users()
    print_json_response("GET /api/users", all_users_json)
    
    # ============ API DEMO: GET USERS BY TYPE ============
    print_section("STEP 5: API DEMO - GET USERS BY TYPE")
    
    tourists_json = api.get_users_by_type("tourist")
    print_json_response("GET /api/users/type/tourist", tourists_json)
    
    # ============ TASK COMPLETION ============
    print_section("STEP 6: USERS COMPLETING TASKS")
    
    # Get some tasks
    tasks = task_manager.get_all_tasks()
    
    # Tourist Alice completes tasks (1.5x multiplier)
    print("👤 Tourist Alice (1.5x GP multiplier):")
    response1 = api.complete_task(user_ids[0], tasks[0].task_id, "Recycled 10kg paper")
    print_json_response("POST /api/tasks/complete", response1)
    
    # Regular User Charlie completes task (1.0x multiplier)
    print("👤 User Charlie (1.0x GP multiplier):")
    response2 = api.complete_task(user_ids[2], tasks[1].task_id, "Recycled 5kg plastic")
    print_json_response("POST /api/tasks/complete", response2)
    
    # Business Echo completes task (0.8x multiplier)
    print("👤 Business Echo (0.8x GP multiplier):")
    response3 = api.complete_task(user_ids[4], tasks[3].task_id, "Staff used public transport")
    print_json_response("POST /api/tasks/complete", response3)
    
    # More completions
    api.complete_task(user_ids[1], tasks[2].task_id, "Planted 3 trees")
    api.complete_task(user_ids[3], tasks[4].task_id, "Biked to work daily")
    api.complete_task(user_ids[5], tasks[6].task_id, "Installed LED bulbs in store")
    
    # ============ MINING ============
    print_section("STEP 7: MINING BLOCK")
    
    mine_response = api.mine_block(user_ids[2])  # Charlie mines
    print_json_response("POST /api/blockchain/mine", mine_response)
    
    # ============ LEADERBOARD ============
    print_section("STEP 8: LEADERBOARD - TOP GP HOLDERS")
    
    leaderboard_json = api.get_leaderboard(limit=10)
    print_json_response("GET /api/leaderboard?limit=10", leaderboard_json)
    
    # ============ USER STATS ============
    print_section("STEP 9: DETAILED USER STATISTICS")
    
    stats_json = api.get_user_stats(user_ids[0])  # Alice's stats
    print_json_response(f"GET /api/users/{user_ids[0]}/stats", stats_json)
    
    # ============ GP TO REWARD POINTS CONVERSION ============
    print_section("STEP 10: CONVERTING GP TO REWARD POINTS")
    
    # Alice converts 50 GP to reward points
    convert_response = api.convert_gp_to_rewards(user_ids[0], 50)
    print_json_response("POST /api/rewards/convert", convert_response)
    
    # Mine the conversion transaction
    api.mine_block(user_ids[1])
    
    # Check reward balance
    reward_balance = api.get_reward_balance(user_ids[0])
    print_json_response(f"GET /api/rewards/{user_ids[0]}", reward_balance)
    
    # ============ LEADERBOARD BY TYPE ============
    print_section("STEP 11: LEADERBOARD BY USER TYPE")
    
    tourist_leaderboard = api.get_leaderboard_by_type("tourist", limit=5)
    print_json_response("GET /api/leaderboard/tourist?limit=5", tourist_leaderboard)
    
    # ============ ADMIN ACTIONS ============
    print_section("STEP 12: ADMIN ACTIONS")
    
    # Grant bonus GP
    print("🔧 Admin grants bonus GP:")
    bonus_response = admin.grant_bonus_gp(user_ids[3], 100, "Early adopter bonus", admin_id=1)
    print_json_response("Admin: Grant Bonus GP", bonus_response)
    
    # Mine the bonus
    api.mine_block(user_ids[0])
    
    # Create custom task
    print("🔧 Admin creates custom task:")
    task_response = admin.create_task(
        "Beach Cleanup Event",
        "Participate in organized beach cleanup",
        150,
        "community",
        "medium",
        True,
        admin_id=1
    )
    print_json_response("Admin: Create Task", task_response)
    
    # ============ ADMIN DASHBOARD ============
    print_section("STEP 13: ADMIN DASHBOARD")
    
    dashboard = admin.get_admin_dashboard()
    print_json_response("Admin Dashboard", dashboard)
    
    # ============ SYSTEM STATS ============
    print_section("STEP 14: COMPLETE SYSTEM STATISTICS")
    
    system_stats = api.get_system_stats()
    print_json_response("GET /api/stats", system_stats)
    
    # ============ BLOCKCHAIN STATE ============
    print_section("STEP 15: BLOCKCHAIN STATE")
    
    blockchain_state = api.get_blockchain_state()
    print_json_response("GET /api/blockchain/state", blockchain_state)
    
    # ============ SAVE BACKUP ============
    print_section("STEP 16: SYSTEM BACKUP")
    
    backup_response = admin.save_system_backup("blockchain_backup_demo.json")
    print_json_response("Admin: Save Backup", backup_response)
    
    # Also save users
    user_manager.save_to_file("blockchain_users_demo.json")
    
    # ============ FINAL SUMMARY ============
    print_section("DEMONSTRATION COMPLETE - SUMMARY")
    
    print("✅ System Features Demonstrated:")
    print("   1. ✓ SQL Database integration with auto-sync")
    print("   2. ✓ 3 User types (Tourist, User, Business) with different multipliers")
    print("   3. ✓ JSON API for all operations")
    print("   4. ✓ Task completion with automatic rewards")
    print("   5. ✓ Blockchain mining")
    print("   6. ✓ GP Leaderboard (overall and by type)")
    print("   7. ✓ GP to Reward Points conversion")
    print("   8. ✓ Admin controls and dashboard")
    print("   9. ✓ User statistics and transaction history")
    print("   10. ✓ System backup and export")
    
    print("\n📊 Final Statistics:")
    stats_data = json.loads(system_stats)
    print(f"   Total Users: {stats_data['data']['users']['total_users']}")
    print(f"   - Tourists: {stats_data['data']['users']['by_type']['tourists']}")
    print(f"   - Regular Users: {stats_data['data']['users']['by_type']['users']}")
    print(f"   - Businesses: {stats_data['data']['users']['by_type']['businesses']}")
    print(f"   Blockchain Length: {stats_data['data']['blockchain']['chain_length']} blocks")
    print(f"   Total GP in Circulation: {stats_data['data']['economy']['total_gp_in_circulation']}")
    print(f"   Tasks Completed: {stats_data['data']['tasks']['total_completions']}")
    
    print("\n🌱 Green Points Blockchain is ready for your frontend!")
    print("   All endpoints return JSON for easy integration")
    print("   Users are auto-synced from your SQL database")
    print("   Leaderboard and stats available for display")
    
    # Close database
    db.close()
    
    print("\n" + "🎉"*40)
    print("DEMONSTRATION COMPLETE!")
    print("Check the generated JSON files for API response examples")
    print("🎉"*40 + "\n")


if __name__ == "__main__":
    demo_centralized_blockchain()
