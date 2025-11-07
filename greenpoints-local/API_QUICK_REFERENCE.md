# 🚀 Quick API Reference - Green Points Blockchain

## For Frontend Developers

### 📦 Import and Initialize

```python
from blockchain import Blockchain
from wallet_centralized import UserManager
from tasks import TaskManager
from api import BlockchainAPI
from database import DatabaseSync

# Initialize (do this once at app startup)
blockchain = Blockchain(difficulty=2)
user_manager = UserManager()
task_manager = TaskManager()
api = BlockchainAPI(blockchain, user_manager, task_manager)

# Connect database
db = DatabaseSync("greenpoints.db")
db.connect()
db.create_tables()
```

---

## 🔥 Most Used API Calls

### 1. User Signs Up (Your App → Database → Blockchain)

```python
# Step 1: Add to your database
user_id = db.add_user(
    username="john_doe",
    user_type="tourist",  # or "user" or "business"
    email="john@example.com",
    phone="+1234567890"
)

# Step 2: Sync to blockchain
from database import auto_sync_new_signups
auto_sync_new_signups(db, user_manager)

# Returns: Number of users synced
```

**Response Example:**
```
✓ User 'john_doe' added to database (ID: 7)
✓ Wallet created for tourist: 'john_doe' (ID: 7)
```

---

### 2. Get Leaderboard (for display)

```python
# Get top 10
leaderboard_json = api.get_leaderboard(limit=10)
```

**JSON Response:**
```json
{
  "success": true,
  "timestamp": 1234567890,
  "total_users": 50,
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 12,
      "username": "eco_champion",
      "user_type": "tourist",
      "gp_balance": 450.0,
      "reward_points": 25.0,
      "tasks_completed": 15
    }
  ]
}
```

---

### 3. Get All Available Tasks

```python
tasks_json = api.get_all_tasks()
```

**JSON Response:**
```json
{
  "success": true,
  "data": {
    "total_tasks": 12,
    "tasks": [
      {
        "task_id": "abc123xyz",
        "name": "Recycle Paper",
        "description": "Recycle at least 5kg of paper",
        "reward_points": 50,
        "category": "recycling",
        "difficulty": "easy",
        "completion_count": 23
      }
    ]
  }
}
```

---

### 4. User Completes a Task

```python
result_json = api.complete_task(
    user_id=12,
    task_id="abc123xyz",
    evidence="Recycled 10kg at local center"
)
```

**JSON Response:**
```json
{
  "success": true,
  "message": "Task completed successfully",
  "data": {
    "completion_id": "comp789",
    "task": {...},
    "status": "verified",
    "reward_amount": 75.0,
    "base_reward": 50,
    "multiplier": 1.5,
    "pending_mining": true
  }
}
```

---

### 5. Mine Block (Process Pending Rewards)

```python
mine_json = api.mine_block(miner_user_id=1)
```

**When to mine:**
- After tasks are completed
- Periodically (every 5-10 minutes)
- When user requests GP withdrawal

**JSON Response:**
```json
{
  "success": true,
  "message": "Block #5 mined successfully",
  "data": {
    "block": {...},
    "transactions_mined": 7,
    "miner_reward": 10
  }
}
```

---

### 6. Get User Statistics

```python
stats_json = api.get_user_stats(user_id=12)
```

**JSON Response:**
```json
{
  "success": true,
  "user": {
    "user_id": 12,
    "username": "eco_user",
    "user_type": "tourist"
  },
  "balances": {
    "gp_balance": 450.0,
    "reward_points": 25.0,
    "gp_multiplier": 1.5
  },
  "statistics": {
    "rank": 1,
    "total_tasks_completed": 15,
    "total_gp_earned": 500.0,
    "total_transactions": 18
  },
  "recent_transactions": [...]
}
```

---

### 7. Convert GP to Reward Points

```python
conversion_json = api.convert_gp_to_rewards(
    user_id=12,
    gp_amount=100  # Convert 100 GP
)
```

**Conversion Rate:** 10 GP = 1 Reward Point

**JSON Response:**
```json
{
  "success": true,
  "message": "GP converted to reward points successfully",
  "data": {
    "gp_converted": 100,
    "reward_points_earned": 10.0,
    "new_reward_points_balance": 35.0,
    "pending_mining": true
  }
}
```

---

### 8. Get Leaderboard by User Type

```python
# Get top tourists
tourist_leaderboard = api.get_leaderboard_by_type("tourist", limit=10)

# Get top regular users
user_leaderboard = api.get_leaderboard_by_type("user", limit=10)

# Get top businesses
business_leaderboard = api.get_leaderboard_by_type("business", limit=10)
```

---

### 9. Get System Stats (for admin dashboard)

```python
stats_json = api.get_system_stats()
```

**JSON Response:**
```json
{
  "success": true,
  "data": {
    "blockchain": {
      "chain_length": 45,
      "pending_transactions": 3,
      "is_valid": true
    },
    "users": {
      "total_users": 156,
      "by_type": {
        "tourists": 45,
        "users": 89,
        "businesses": 22
      }
    },
    "economy": {
      "total_gp_in_circulation": 12500.0,
      "total_reward_points": 450.0
    }
  }
}
```

---

### 10. Get User Transaction History

```python
history_json = api.get_transaction_history(user_id=12)
```

**JSON Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 12,
    "username": "eco_user",
    "transaction_count": 18,
    "transactions": [
      {
        "from": "SYSTEM",
        "to": "user_address",
        "amount": 75.0,
        "type": "task_reward",
        "task_name": "Recycle Paper",
        "block_index": 5
      }
    ]
  }
}
```

---

## 🎨 Frontend Display Tips

### User Dashboard Widget
```javascript
// Fetch user stats
const stats = JSON.parse(api.get_user_stats(userId));

// Display:
<div class="user-stats">
  <div class="gp-balance">{stats.balances.gp_balance} GP</div>
  <div class="rank">Rank #{stats.statistics.rank}</div>
  <div class="multiplier">{stats.balances.gp_multiplier}x multiplier</div>
  <div class="reward-points">{stats.balances.reward_points} RP</div>
</div>
```

### Leaderboard Table
```javascript
const leaderboard = JSON.parse(api.get_leaderboard(10));

leaderboard.leaderboard.forEach(user => {
  // Display rank, username, GP balance, tasks completed
});
```

### Task List
```javascript
const tasks = JSON.parse(api.get_all_tasks());

tasks.data.tasks.forEach(task => {
  // Show task name, description, reward (with user's multiplier)
  const userMultiplier = getUserMultiplier(); // 1.0, 1.5, or 0.8
  const actualReward = task.reward_points * userMultiplier;
});
```

---

## 🔄 Typical Workflow

```
1. User signs up
   → db.add_user()
   → auto_sync_new_signups()

2. User views tasks
   → api.get_all_tasks()

3. User completes task
   → api.complete_task()

4. System mines block (periodic or manual)
   → api.mine_block()

5. User checks balance
   → api.get_user_stats()

6. User views leaderboard
   → api.get_leaderboard()

7. User converts GP to rewards
   → api.convert_gp_to_rewards()
   → api.mine_block()

8. User redeems rewards (in your app)
   → api.get_reward_balance()
```

---

## ⚡ Quick Testing

```python
# Run the complete demo
python3 demo_centralized.py

# This will show you:
# - 6 users created
# - Tasks completed
# - Blocks mined
# - Leaderboard
# - GP conversions
# - All in JSON format!
```

---

## 🔧 Admin Quick Actions

```python
from admin import AdminSystem

admin = AdminSystem(blockchain, user_manager, task_manager, db)

# Grant bonus GP to user
admin.grant_bonus_gp(user_id=12, amount=100, reason="Contest winner")

# Create special task
admin.create_task(
    name="Special Event",
    description="Participate in cleanup event",
    reward_points=200,
    category="community"
)

# Get dashboard stats
dashboard = admin.get_admin_dashboard()

# Save backup
admin.save_system_backup("backup.json")
```

---

## 📊 User Type Multipliers

```python
# In your frontend, calculate preview rewards:

task_reward = 100  # Base reward

if user_type == "tourist":
    actual_reward = task_reward * 1.5  # 150 GP
elif user_type == "user":
    actual_reward = task_reward * 1.0  # 100 GP
elif user_type == "business":
    actual_reward = task_reward * 0.8  # 80 GP
```

---

## 🎯 Error Handling

All API methods return consistent format:

**Success:**
```json
{
  "success": true,
  "message": "...",
  "data": {...}
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error description",
  "code": 404
}
```

**In your code:**
```python
result = json.loads(api.complete_task(user_id, task_id))

if result["success"]:
    # Show success message
    reward = result["data"]["reward_amount"]
else:
    # Show error
    error_msg = result["error"]
```

---

## 🚀 Production Checklist

- [ ] Change database path from demo to production
- [ ] Add authentication to API endpoints
- [ ] Set up periodic mining (cron job or scheduler)
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Set up logging
- [ ] Enable HTTPS
- [ ] Add admin access control
- [ ] Implement backup strategy
- [ ] Set up monitoring

---

## 💡 Pro Tips

1. **Auto-mine periodically**: Set up a cron job to mine every 5 minutes
2. **Cache leaderboard**: Leaderboard is cached for 5 minutes automatically
3. **Batch operations**: Complete multiple tasks before mining
4. **User types matter**: Show multiplier on task cards
5. **Reward points**: Remind users conversion rate (10:1)

---

## 📞 Need Help?

- Run demo: `python3 demo_centralized.py`
- Check README: `README_CENTRALIZED.md`
- View all API methods: `api.py`
- Admin functions: `admin.py`
- Database sync: `database.py`

---

**All endpoints return JSON - perfect for any frontend framework! 🎉**
