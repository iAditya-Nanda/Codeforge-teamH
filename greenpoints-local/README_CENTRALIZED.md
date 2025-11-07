# 🌱 Green Points Blockchain - Centralized System

## Complete Guide for Frontend Integration

A **centralized blockchain** system for rewarding environmental actions with **Green Points (GP)**. Designed specifically for integration with web/mobile frontends, featuring JSON APIs, SQL database sync, and 3 user types.

---

## 🎯 System Overview

### Core Features
- **✅ Centralized Control** - Admin-managed blockchain for your application
- **✅ 3 User Types** - Tourist (1.5x GP), User (1.0x GP), Business (0.8x GP)
- **✅ SQL Database Integration** - Auto-sync from your user database
- **✅ JSON API** - All endpoints return JSON for frontend
- **✅ GP → Reward Points** - Users can convert GP to redeemable rewards
- **✅ Leaderboard System** - Real-time rankings by GP balance
- **✅ Admin Dashboard** - Complete system management

---

## 📊 User Types & Multipliers

| User Type | GP Multiplier | Purpose |
|-----------|--------------|---------|
| **Tourist** | 1.5x | Encourages visitors to participate in green activities |
| **User** | 1.0x | Regular local users |
| **Business** | 0.8x | Businesses earn less GP (they benefit from customer traffic) |

**Example**: A task worth 100 GP gives:
- Tourist: 150 GP
- User: 100 GP
- Business: 80 GP

---

## 🔌 Quick Start for Frontend Integration

### 1. Initialize the System

```python
from blockchain import Blockchain
from wallet_centralized import UserManager
from tasks import TaskManager
from api import BlockchainAPI
from database import DatabaseSync

# Initialize components
blockchain = Blockchain(difficulty=2)
user_manager = UserManager()
task_manager = TaskManager()

# Connect to your database
db = DatabaseSync("your_database.db")
db.connect()
db.create_tables()

# Initialize API
api = BlockchainAPI(blockchain, user_manager, task_manager)
```

### 2. Sync Users from Your Database

```python
# When user signs up in your app
user_id = db.add_user(
    username="john_doe",
    user_type="user",  # or "tourist" or "business"
    email="john@example.com",
    phone="+1234567890"
)

# Sync to blockchain
from database import auto_sync_new_signups
auto_sync_new_signups(db, user_manager)
```

### 3. Use JSON API Endpoints

```python
# Get all users (returns JSON)
users_json = api.get_all_users()

# Get leaderboard (returns JSON)
leaderboard_json = api.get_leaderboard(limit=10)

# Complete a task (returns JSON)
result_json = api.complete_task(user_id=1, task_id="task123", evidence="photo.jpg")

# Convert GP to rewards (returns JSON)
conversion_json = api.convert_gp_to_rewards(user_id=1, gp_amount=100)
```

---

## 📡 JSON API Endpoints

### User Management

#### GET /api/users
Get all users with GP balances
```python
api.get_all_users()
```
**Response:**
```json
{
  "success": true,
  "total_users": 6,
  "users": [...]
}
```

#### GET /api/users/{user_id}
Get specific user details
```python
api.get_user(user_id=1)
```

#### GET /api/users/{user_id}/stats
Get detailed user statistics
```python
api.get_user_stats(user_id=1)
```
**Response includes:**
- GP balance
- Reward points
- Rank
- Tasks completed
- Recent transactions

#### GET /api/users/type/{user_type}
Get users by type (tourist, user, business)
```python
api.get_users_by_type("tourist")
```

---

### Task Management

#### GET /api/tasks
Get all available tasks
```python
api.get_all_tasks()
```
**Response:**
```json
{
  "success": true,
  "data": {
    "total_tasks": 12,
    "tasks": [
      {
        "task_id": "abc123",
        "name": "Recycle Paper",
        "reward_points": 50,
        "category": "recycling",
        "difficulty": "easy"
      }
    ]
  }
}
```

#### POST /api/tasks/complete
User completes a task
```python
api.complete_task(user_id=1, task_id="abc123", evidence="Recycled 10kg")
```
**Response:**
```json
{
  "success": true,
  "data": {
    "reward_amount": 75.0,
    "base_reward": 50,
    "multiplier": 1.5,
    "pending_mining": true
  }
}
```

---

### Blockchain Operations

#### POST /api/blockchain/mine
Mine pending transactions
```python
api.mine_block(miner_user_id=1)
```

#### GET /api/blockchain/state
Get current blockchain state
```python
api.get_blockchain_state()
```

#### GET /api/users/{user_id}/transactions
Get user's transaction history
```python
api.get_transaction_history(user_id=1)
```

---

### Leaderboard

#### GET /api/leaderboard?limit=10
Get top GP holders (all types)
```python
api.get_leaderboard(limit=10)
```
**Response:**
```json
{
  "success": true,
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 4,
      "username": "alice",
      "user_type": "tourist",
      "gp_balance": 250.0,
      "tasks_completed": 5
    }
  ]
}
```

#### GET /api/leaderboard/{user_type}?limit=10
Get leaderboard by user type
```python
api.get_leaderboard_by_type("tourist", limit=10)
```

---

### Reward Points System

#### POST /api/rewards/convert
Convert GP to reward points
```python
api.convert_gp_to_rewards(user_id=1, gp_amount=100)
```
**Conversion Rate:** 10 GP = 1 Reward Point

**Response:**
```json
{
  "success": true,
  "data": {
    "gp_converted": 100,
    "reward_points_earned": 10.0,
    "new_reward_points_balance": 10.0
  }
}
```

#### GET /api/rewards/{user_id}
Get user's reward points balance
```python
api.get_reward_balance(user_id=1)
```

---

### System Statistics

#### GET /api/stats
Get complete system statistics
```python
api.get_system_stats()
```
**Response includes:**
- Blockchain stats
- User counts by type
- Total GP in circulation
- Total reward points
- Task completion stats

---

## 🔧 Admin Functions

```python
from admin import AdminSystem

admin = AdminSystem(blockchain, user_manager, task_manager, db)

# Grant bonus GP
admin.grant_bonus_gp(user_id=1, amount=100, reason="Contest winner")

# Create custom task
admin.create_task(
    name="Beach Cleanup",
    description="Participate in beach cleanup event",
    reward_points=150,
    category="community",
    difficulty="medium"
)

# Get admin dashboard
dashboard_json = admin.get_admin_dashboard()

# Force mine block
admin.force_mine_block()

# Save system backup
admin.save_system_backup("backup.json")
```

---

## 💾 Database Integration

### Your SQL Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    phone TEXT,
    user_type TEXT CHECK(user_type IN ('tourist', 'user', 'business')),
    blockchain_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sync Users to Blockchain

```python
from database import DatabaseSync, auto_sync_new_signups

db = DatabaseSync("your_db.db")
db.connect()

# Automatic sync on signup
def handle_user_signup(username, user_type, email, phone):
    # Add to your database
    user_id = db.add_user(username, user_type, email, phone)
    
    # Auto-sync to blockchain
    auto_sync_new_signups(db, user_manager)
    
    return user_id
```

---

## 🎮 Frontend Integration Examples

### React/Vue/Angular Example

```javascript
// Fetch leaderboard
async function getLeaderboard() {
    const response = await fetch('/api/leaderboard?limit=10');
    const data = await response.json();
    
    if (data.success) {
        displayLeaderboard(data.leaderboard);
    }
}

// Complete a task
async function completeTask(userId, taskId, evidence) {
    const response = await fetch('/api/tasks/complete', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            user_id: userId,
            task_id: taskId,
            evidence: evidence
        })
    });
    
    const data = await response.json();
    
    if (data.success) {
        alert(`Earned ${data.data.reward_amount} GP!`);
    }
}

// Get user stats
async function getUserStats(userId) {
    const response = await fetch(`/api/users/${userId}/stats`);
    const data = await response.json();
    
    if (data.success) {
        updateUserDashboard(data);
    }
}
```

---

## 🏆 Leaderboard Display

### Sample Leaderboard Data Structure

```json
{
  "leaderboard": [
    {
      "rank": 1,
      "username": "eco_warrior",
      "user_type": "tourist",
      "gp_balance": 450.0,
      "reward_points": 25.0,
      "tasks_completed": 12
    },
    {
      "rank": 2,
      "username": "green_user",
      "user_type": "user",
      "gp_balance": 380.0,
      "reward_points": 15.0,
      "tasks_completed": 10
    }
  ]
}
```

### Display Tips
- Show user rank badge (🥇 🥈 🥉)
- Highlight current user
- Filter by user type
- Show GP balance prominently
- Display tasks completed count

---

## 📱 Mobile App Integration

### REST API Wrapper

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    return api.get_all_users()

@app.route('/api/tasks/complete', methods=['POST'])
def complete_task():
    data = request.json
    return api.complete_task(
        user_id=data['user_id'],
        task_id=data['task_id'],
        evidence=data.get('evidence')
    )

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    limit = request.args.get('limit', 10, type=int)
    return api.get_leaderboard(limit=limit)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 🔄 Workflow Example

### Complete User Journey

```
1. User signs up in app
   ↓
2. User record created in SQL database
   ↓
3. Auto-sync creates blockchain wallet
   ↓
4. User sees available tasks in app
   ↓
5. User completes task (uploads evidence)
   ↓
6. API creates transaction with multiplier
   ↓
7. Transaction added to pending pool
   ↓
8. Block mined (automatically or manually)
   ↓
9. User receives GP (adjusted by multiplier)
   ↓
10. User appears on leaderboard
    ↓
11. User converts GP to reward points
    ↓
12. User redeems rewards in app
```

---

## 📊 Data Flow

```
Frontend (React/Vue/Angular)
         ↓
    REST API Layer
         ↓
   BlockchainAPI Class
         ↓
   ┌──────┴──────┐
   ↓             ↓
Blockchain   UserManager
   ↓             ↓
Database ←→ SQL Sync
```

---

## 🎨 UI Components Suggestions

### 1. User Dashboard
- GP Balance (large number)
- Reward Points Balance
- Current Rank (#1, #24, etc.)
- GP Multiplier Badge
- Recent Transactions (last 5)

### 2. Leaderboard Page
- Top 10 users
- Filter by user type
- "My Rank" highlight
- Progress bars
- Avatar/username display

### 3. Tasks Page
- Available tasks grid/list
- Task difficulty badges
- GP reward (with multiplier preview)
- Task categories
- Completion button

### 4. Rewards Shop
- Display reward points balance
- Conversion calculator
- Available rewards
- Redemption history

---

## 🚀 Running the System

### Demo (See Everything)
```bash
python3 demo_centralized.py
```

### Production Use
```python
# In your main application
from blockchain import Blockchain
from wallet_centralized import UserManager
from tasks import TaskManager
from api import BlockchainAPI
from database import DatabaseSync

# Initialize once at startup
blockchain = Blockchain(difficulty=2)
user_manager = UserManager()
task_manager = TaskManager()
api = BlockchainAPI(blockchain, user_manager, task_manager)

# Use api.* methods in your routes
```

---

## 📝 Files Overview

### Core System
- `blockchain.py` - Blockchain core
- `wallet_centralized.py` - User management with 3 types
- `tasks.py` - Task definitions
- `transaction.py` - Transaction handling

### API & Integration
- `api.py` - **JSON API endpoints** (use this!)
- `database.py` - **SQL database sync**
- `admin.py` - **Admin controls**

### Demos & Testing
- `demo_centralized.py` - Complete demo
- `cli.py` - Interactive testing

---

## 🔐 Security Notes

### For Production
1. Add authentication to API endpoints
2. Validate user permissions
3. Rate limit API calls
4. Sanitize task evidence uploads
5. Use environment variables for config
6. Enable HTTPS for API
7. Implement admin access control

### Example Auth Wrapper
```python
def require_auth(func):
    def wrapper(*args, **kwargs):
        # Verify user token/session
        if not is_authenticated():
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper
```

---

## 📈 Scaling Considerations

### Current Setup (Local/Small Scale)
- SQLite database
- In-memory blockchain
- Single server

### For Larger Scale
- Switch to PostgreSQL/MySQL
- Implement blockchain persistence
- Add caching (Redis)
- Load balancer for API
- Background workers for mining
- Websockets for real-time leaderboard

---

## 🎯 Key Benefits for Your App

✅ **Gamification** - Users compete for GP  
✅ **Engagement** - Leaderboard drives participation  
✅ **Rewards** - GP converts to real rewards  
✅ **Transparency** - Blockchain shows all transactions  
✅ **Fair** - Multipliers balance different user types  
✅ **Scalable** - JSON API ready for any frontend  
✅ **Admin Control** - Full system management  

---

## 📞 Integration Support

All API methods return consistent JSON:
```json
{
  "success": true/false,
  "message": "Human readable message",
  "data": {...},
  "timestamp": 1234567890.123
}
```

**Error format:**
```json
{
  "success": false,
  "error": "Error description",
  "code": 404,
  "timestamp": 1234567890.123
}
```

---

## 🌟 Next Steps

1. **Run the demo**: `python3 demo_centralized.py`
2. **Review JSON outputs**: Check console for API responses
3. **Test with your database**: Modify `database.py` connection
4. **Integrate API**: Use `api.py` methods in your backend
5. **Build frontend**: Consume JSON endpoints
6. **Deploy**: Add authentication and go live!

---

**Made with 💚 for a greener planet**

**Questions?** All endpoints are documented in `api.py`  
**Examples?** Run `demo_centralized.py` to see everything in action
