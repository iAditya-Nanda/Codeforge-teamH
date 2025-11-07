"""
One-time script to sync existing users from your database to the blockchain

This script:
1. Connects to YOUR existing database (MySQL/PostgreSQL/etc.)
2. Fetches all users
3. Creates blockchain wallets for them
4. Stores wallet addresses back in YOUR database
"""

import requests

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================

# Green Points API URL
API_URL = "http://localhost:5000/api"

# Example for MySQL - uncomment and configure
# import mysql.connector
# YOUR_DB = mysql.connector.connect(
#     host="localhost",
#     user="your_username",
#     password="your_password",
#     database="your_database"
# )

# Example for PostgreSQL - uncomment and configure
# import psycopg2
# YOUR_DB = psycopg2.connect(
#     host="localhost",
#     database="your_database",
#     user="your_username",
#     password="your_password"
# )

# Example for SQLite - uncomment and configure
# import sqlite3
# YOUR_DB = sqlite3.connect("your_database.db")

# ============================================
# SYNC FUNCTION
# ============================================

def sync_existing_users():
    """
    Sync all users from your database to the blockchain
    """
    
    # STEP 1: Connect to YOUR database
    # Uncomment the database connection above first!
    
    # Example: YOUR_DB = mysql.connector.connect(...)
    # cursor = YOUR_DB.cursor(dictionary=True)
    
    print("🔄 Starting user sync to blockchain...\n")
    
    # STEP 2: Fetch all users from YOUR database
    # Modify this query to match YOUR database schema
    
    # Example query:
    # cursor.execute("SELECT id, name, email, phone FROM users")
    # users = cursor.fetchall()
    
    # FOR TESTING: Using dummy data
    # Replace this with actual database query
    users = [
        {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "phone": "+1111111111"},
        {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "phone": "+2222222222"},
        {"id": 3, "name": "Carol White", "email": "carol@example.com", "phone": "+3333333333"},
    ]
    
    print(f"Found {len(users)} users to sync\n")
    
    # STEP 3: Sync each user to blockchain
    synced = 0
    failed = 0
    
    for user in users:
        try:
            # Call blockchain API to create wallet
            response = requests.post(f"{API_URL}/sync-user", json={
                "name": user['name'],
                "email": user.get('email'),
                "phone": user.get('phone')
            })
            
            result = response.json()
            
            if result['success']:
                wallet_address = result['data']['wallet_address']
                blockchain_user_id = result['data']['user_id']
                
                # STEP 4: Update YOUR database with wallet address
                # Uncomment and modify to match YOUR database schema
                
                # Example for MySQL/PostgreSQL:
                # update_cursor = YOUR_DB.cursor()
                # update_cursor.execute(
                #     "UPDATE users SET wallet_address = %s, blockchain_user_id = %s WHERE id = %s",
                #     (wallet_address, blockchain_user_id, user['id'])
                # )
                # YOUR_DB.commit()
                
                print(f"✅ Synced: {user['name']}")
                print(f"   Wallet: {wallet_address}")
                print(f"   Blockchain ID: {blockchain_user_id}\n")
                synced += 1
            else:
                print(f"❌ Failed: {user['name']} - {result.get('message', 'Unknown error')}\n")
                failed += 1
                
        except Exception as e:
            print(f"❌ Error syncing {user['name']}: {e}\n")
            failed += 1
    
    # STEP 5: Summary
    print("\n" + "="*60)
    print("📊 Sync Summary")
    print("="*60)
    print(f"✅ Successfully synced: {synced}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Total: {len(users)}\n")
    
    # Close database connection
    # YOUR_DB.close()

# ============================================
# ALTERNATIVE: Sync on signup (webhook)
# ============================================

def sync_on_signup_example():
    """
    Example code to add to your existing signup function
    
    This shows how to sync users automatically when they sign up
    """
    
    example_code = '''
# In your existing signup endpoint/function:

def signup_user(name, email, phone, password):
    # 1. Create user in YOUR database (your existing code)
    user = your_database.create_user(
        name=name,
        email=email,
        phone=phone,
        password=hash_password(password)
    )
    
    # 2. NEW: Sync to blockchain
    try:
        response = requests.post('http://localhost:5000/api/sync-user', json={
            'name': name,
            'email': email,
            'phone': phone
        })
        
        result = response.json()
        
        if result['success']:
            # Save wallet address to your database
            your_database.update_user(user.id, {
                'wallet_address': result['data']['wallet_address'],
                'blockchain_user_id': result['data']['user_id']
            })
            
    except Exception as e:
        # Log error but don't fail signup
        print(f"Blockchain sync failed: {e}")
        # You can retry later or add to a queue
    
    return user
'''
    
    print("="*60)
    print("📝 Code Example: Sync on Signup")
    print("="*60)
    print(example_code)
    print()

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("🌟 Green Points Blockchain - User Sync Tool")
    print("="*60 + "\n")
    
    print("Choose an option:")
    print("1. Sync existing users (one-time)")
    print("2. Show webhook example (sync on signup)")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        confirm = input("\n⚠️  This will sync users from your database. Continue? (yes/no): ").strip().lower()
        if confirm == "yes":
            try:
                sync_existing_users()
            except requests.exceptions.ConnectionError:
                print("\n❌ ERROR: Could not connect to blockchain API!")
                print("Make sure the server is running: python server.py\n")
            except Exception as e:
                print(f"\n❌ ERROR: {e}\n")
        else:
            print("\n❌ Cancelled\n")
    
    elif choice == "2":
        sync_on_signup_example()
    
    else:
        print("\n❌ Invalid choice\n")
