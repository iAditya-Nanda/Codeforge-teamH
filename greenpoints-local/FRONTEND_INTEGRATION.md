# 🌱 Green Points Blockchain - Frontend Integration Guide

## Overview

A **centralized blockchain system** for rewarding eco-friendly actions with Green Points (GP). This system is designed for **frontend integration** with a mobile/web app, featuring:

- **2 User Roles**: Users (earn GP) and Businesses (issue QR rewards)
- **SQL Database Integration**: All users synced from your signup system
- **JSON API Responses**: Every operation returns JSON for easy frontend integration
- **Task System**: Waste disposal & litter reporting with verification
- **QR Code System**: Businesses generate codes, users scan to earn instant GP
- **Leaderboard**: Real-time GP rankings

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   Frontend App  │  (React/React Native/Vue/etc)
└────────┬────────┘
         │ HTTP/REST API
         ▼
┌─────────────────┐
│   JSON API      │  (api.py - All responses in JSON)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐  ┌───────────┐
│  SQL   │  │Blockchain │
│Database│  │  Ledger   │
└────────┘  └───────────┘
```

---

## 👥 User Roles

### 1. **USER** Role
- Regular app users
- Can earn GP by:
  - Disposing waste properly (with photo verification)
  - Reporting littered spots (with location)
  - Scanning QR codes at eco-businesses
- Can view leaderboard and transaction history
- **Cannot** generate QR codes

### 2. **BUSINESS** Role  
- Eco-registered businesses/cafes/shops
- Can generate QR codes for customer rewards
- Track QR code usage and GP distributed
- **Cannot** earn GP from tasks

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,              -- Either email
    phone TEXT UNIQUE,              -- or phone required
    role TEXT CHECK(role IN ('user', 'business')),
    wallet_address TEXT UNIQUE,     -- Blockchain wallet
    created_at REAL,
    is_active INTEGER DEFAULT 1
);
```

**Integration**: When a user signs up on your app, call `api.register_user()` to sync to blockchain.

### Pending Verifications Table
```sql
CREATE TABLE pending_verifications (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    task_type TEXT,                 -- 'waste_disposal' or 'litter_report'
    evidence TEXT,                   -- User description
    image_path TEXT,                 -- Path to uploaded photo
    location TEXT,                   -- Location description
    latitude REAL,                   -- GPS coordinates
    longitude REAL,
    submitted_at REAL,
    status TEXT CHECK(status IN ('pending', 'approved', 'rejected')),
    reward_amount REAL,
    transaction_id TEXT              -- Set when approved
);
```

### QR Codes Table
```sql
CREATE TABLE qr_codes (
    id INTEGER PRIMARY KEY,
    qr_code TEXT UNIQUE,            -- e.g., "GP-0001-A1B2C3D4E5F6"
    business_id INTEGER,
    business_name TEXT,
    reward_amount REAL,
    service_description TEXT,
    created_at REAL,
    expires_at REAL,                -- NULL = never expires
    is_used INTEGER DEFAULT 0,
    used_by INTEGER,                -- User ID who scanned
    used_at REAL
);
```

---

## 🔌 API Endpoints (JSON Responses)

### User Management

#### Register User
```python
response = api.register_user(
    name="John Doe",
    email="john@example.com",
    phone="+1234567890"
)
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": 1,
    "wallet_address": "abc123...",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "balance": 0
  }
}
```

#### Login
```python
response = api.login(email="john@example.com")
# OR
response = api.login(phone="+1234567890")
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "wallet_address": "abc123...",
    "balance": 125.5,
    "created_at": 1234567890.0
  }
}
```

### Task Operations

#### Get Available Tasks
```python
response = api.get_available_tasks()
```

**Response:**
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "task_type": "waste_disposal",
        "name": "Proper Waste Disposal",
        "description": "Dispose waste in the correct bin",
        "base_reward": 20.0,
        "requires_verification": true
      },
      {
        "task_type": "litter_report",
        "name": "Report Littered Spot",
        "description": "Report a littered location",
        "base_reward": 30.0,
        "requires_verification": true
      }
    ]
  }
}
```

#### Submit Waste Disposal
```python
response = api.submit_waste_disposal(
    user_id=1,
    evidence="Disposed plastic bottles in recycling bin",
    image_path="/uploads/user1_waste_001.jpg",
    waste_type="recyclable"  # recyclable, organic, or general
)
```

**Response:**
```json
{
  "success": true,
  "message": "Waste disposal submitted for verification",
  "data": {
    "verification_id": 123,
    "expected_reward": 20.0,
    "status": "pending",
    "estimated_verification_time": "24 hours"
  }
}
```

#### Submit Litter Report
```python
response = api.submit_litter_report(
    user_id=1,
    evidence="Large pile of trash near park entrance",
    image_path="/uploads/user1_litter_001.jpg",
    location="Central Park, Main Gate",
    latitude=40.785091,
    longitude=-73.968285,
    severity="high"  # low, medium, or high
)
```

**Response:**
```json
{
  "success": true,
  "message": "Litter report submitted for verification",
  "data": {
    "verification_id": 124,
    "expected_reward": 45.0,
    "severity": "high",
    "status": "pending"
  }
}
```

**Rewards by Severity:**
- Low: 30 GP
- Medium: 36 GP
- High: 45 GP

### QR Code Operations

#### Generate QR Code (Business Only)
```python
response = api.generate_qr_code(
    business_id=5,
    reward_amount=25.0,
    service_description="Coffee purchase",
    expires_in_hours=24  # Optional, None = never expires
)
```

**Response:**
```json
{
  "success": true,
  "message": "QR code created successfully",
  "data": {
    "qr_code": "GP-0005-A1B2C3D4E5F6",
    "reward_amount": 25.0,
    "service_description": "Coffee purchase",
    "expires_in_hours": 24
  }
}
```

#### Scan QR Code (User Only)
```python
response = api.scan_qr_code(
    qr_code="GP-0005-A1B2C3D4E5F6",
    user_id=1
)
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Earned 25.0 GP from Green Cafe!",
  "data": {
    "transaction_id": "abc123",
    "amount": 25.0,
    "business_name": "Green Cafe",
    "service": "Coffee purchase",
    "timestamp": 1234567890.0
  }
}
```

**Response (Already Used):**
```json
{
  "success": false,
  "message": "QR code already used on 2025-11-07 10:30",
  "data": null
}
```

### Blockchain Operations

#### Get Balance
```python
response = api.get_balance(user_id=1)
```

**Response:**
```json
{
  "success": true,
  "message": "Balance retrieved",
  "data": {
    "user_id": 1,
    "name": "John Doe",
    "balance": 125.5,
    "currency": "GP"
  }
}
```

#### Get Transaction History
```python
response = api.get_transaction_history(user_id=1, limit=50)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "from": "SYSTEM",
        "to": "abc123...",
        "amount": 20.0,
        "type": "task_reward",
        "task_name": "Waste Disposal",
        "timestamp": 1234567890.0,
        "block_index": 5
      }
    ],
    "total_count": 15
  }
}
```

#### Get Leaderboard
```python
response = api.get_leaderboard(limit=10)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "leaderboard": [
      {
        "rank": 1,
        "user_id": 3,
        "name": "Alice Green",
        "total_gp": 450.5,
        "tasks_completed": 12
      },
      {
        "rank": 2,
        "user_id": 7,
        "name": "Bob Eco",
        "total_gp": 380.0,
        "tasks_completed": 10
      }
    ],
    "total_count": 2,
    "last_updated": 1234567890.0
  }
}
```

### Admin Operations

#### Get Pending Verifications
```python
response = api.get_pending_verifications()
```

**Response:**
```json
{
  "success": true,
  "data": {
    "verifications": [
      {
        "id": 123,
        "user_id": 1,
        "user_name": "John Doe",
        "user_email": "john@example.com",
        "task_type": "waste_disposal",
        "evidence": "Disposed plastic in recycling",
        "image_path": "/uploads/user1_waste_001.jpg",
        "submitted_at": 1234567890.0,
        "reward_amount": 20.0,
        "status": "pending"
      }
    ],
    "total_count": 5
  }
}
```

#### Approve Verification
```python
response = api.approve_verification(
    verification_id=123,
    admin_name="Admin System"
)
```

**Response:**
```json
{
  "success": true,
  "message": "Verification approved",
  "data": {
    "verification_id": 123,
    "user_name": "John Doe",
    "reward_amount": 20.0,
    "transaction_id": "tx_abc123"
  }
}
```

#### Reject Verification
```python
response = api.reject_verification(
    verification_id=124,
    reason="Photo is unclear, bin label not visible",
    admin_name="Admin System"
)
```

---

## 🔄 Complete User Flow

### 1. User Signup on Frontend
```
Frontend → SQL Database → API.register_user() → Blockchain Wallet Created
```

### 2. User Disposes Waste
```
1. User opens camera in app
2. Takes photo of waste + bin
3. Submits via API.submit_waste_disposal()
4. Verification record created (status: pending)
5. Admin reviews and approves
6. Transaction added to blockchain
7. System mines block
8. User receives GP
```

### 3. User Visits Eco-Business
```
1. User makes purchase at Green Cafe
2. Business generates QR code
3. User scans QR with app
4. API.scan_qr_code() validates and creates transaction
5. System mines block
6. User receives GP instantly
```

### 4. User Checks Leaderboard
```
Frontend → API.get_leaderboard() → JSON response → Display rankings
```

---

## 🚀 Quick Start

### 1. Run the Demo
```bash
python3 demo_frontend.py
```

This creates:
- 3 users
- 2 businesses
- Sample task submissions
- QR code generation and scanning
- Complete blockchain with JSON outputs

### 2. Check Database
```bash
sqlite3 greenpoints_demo.db
.tables
SELECT * FROM users;
SELECT * FROM qr_codes;
SELECT * FROM pending_verifications;
```

### 3. Test API Calls
```python
from blockchain import Blockchain
from database import Database
from api import GreenPointsAPI

# Initialize
blockchain = Blockchain()
db = Database("greenpoints.db")
api = GreenPointsAPI(blockchain, db)

# Register a user
response = api.register_user(
    name="Test User",
    email="test@example.com"
)
print(response)

# Submit waste disposal
response = api.submit_waste_disposal(
    user_id=1,
    evidence="Test submission",
    image_path="/uploads/test.jpg"
)
print(response)
```

---

## 📱 Frontend Integration Examples

### React/React Native Example
```javascript
// Register user
const registerUser = async (name, email, phone) => {
  const response = await fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, phone })
  });
  const data = await response.json();
  
  if (data.success) {
    // Save user_id and wallet_address
    localStorage.setItem('user_id', data.data.user_id);
    localStorage.setItem('wallet_address', data.data.wallet_address);
  }
};

// Submit waste disposal
const submitWasteDisposal = async (userId, evidence, imageFile, wasteType) => {
  const formData = new FormData();
  formData.append('user_id', userId);
  formData.append('evidence', evidence);
  formData.append('image', imageFile);
  formData.append('waste_type', wasteType);
  
  const response = await fetch('/api/submit-waste', {
    method: 'POST',
    body: formData
  });
  const data = await response.json();
  
  if (data.success) {
    alert(`Submitted! Expected reward: ${data.data.expected_reward} GP`);
  }
};

// Scan QR code
const scanQRCode = async (qrCode, userId) => {
  const response = await fetch('/api/scan-qr', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ qr_code: qrCode, user_id: userId })
  });
  const data = await response.json();
  
  if (data.success) {
    alert(`${data.message}\n+${data.data.amount} GP`);
  } else {
    alert(`Error: ${data.message}`);
  }
};

// Get leaderboard
const getLeaderboard = async () => {
  const response = await fetch('/api/leaderboard?limit=10');
  const data = await response.json();
  
  if (data.success) {
    return data.data.leaderboard;
  }
};
```

---

## 🔧 System Configuration

### Mining
- **Difficulty**: 2 (adjustable)
- **Mining Reward**: 10 GP per block
- **Auto-mining**: System automatically mines when transactions pending

### Rewards
- **Waste Disposal**: 20 GP
- **Litter Report**: 30-45 GP (based on severity)
- **QR Scan**: Set by business (typically 10-50 GP)

### Verification
- Status: pending → approved/rejected
- Estimated time: 24 hours
- Admin review required for waste disposal and litter reports

---

## 📝 Database Files

- `greenpoints.db` - Main production database
- `greenpoints_demo.db` - Demo/testing database

---

## 🎯 Next Steps for Production

1. **Add REST API Server** (Flask/FastAPI)
2. **Add Authentication** (JWT tokens)
3. **Add Image Upload** (AWS S3/local storage)
4. **Add Push Notifications** (approval/rejection alerts)
5. **Add Reward Redemption** (convert GP to real rewards)
6. **Add Analytics Dashboard** (admin panel)

---

## 📞 Support

All API methods return consistent JSON format:
```json
{
  "success": true/false,
  "message": "Human-readable message",
  "data": { /* actual data or null */ }
}
```

Check `demo_frontend.py` for complete working examples!
