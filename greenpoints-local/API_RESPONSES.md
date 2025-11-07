# 📋 API Response Examples

Complete reference of all API endpoint responses for frontend integration.

---

## 👤 User Endpoints

### POST /api/sync-user
**Register new user and create blockchain wallet**

**Request:**
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "+1234567890"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1234567890",
    "wallet_address": "ee817b9d5b0172453620",
    "role": "user",
    "balance": 0
  }
}
```

**Response (Error - Email exists):**
```json
{
  "success": false,
  "message": "Email already registered",
  "data": null
}
```

---

### POST /api/login
**Login user by email or phone**

**Request:**
```json
{
  "email": "alice@example.com"
}
```
OR
```json
{
  "phone": "+1234567890"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user_id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1234567890",
    "wallet_address": "ee817b9d5b0172453620",
    "balance": 150.0,
    "role": "user"
  }
}
```

**Response (Error - Not found):**
```json
{
  "success": false,
  "message": "User not found",
  "data": null
}
```

---

### GET /api/profile/{user_id}
**Get user profile with current balance**

**Response:**
```json
{
  "success": true,
  "message": "Profile retrieved",
  "data": {
    "user_id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1234567890",
    "wallet_address": "ee817b9d5b0172453620",
    "role": "user",
    "balance": 150.0,
    "created_at": 1699876543.12,
    "is_active": true
  }
}
```

---

### GET /api/balance/{user_id}
**Get user's current GP balance**

**Response:**
```json
{
  "success": true,
  "message": "Balance retrieved",
  "data": {
    "user_id": 1,
    "name": "Alice Johnson",
    "balance": 150.0,
    "currency": "GP"
  }
}
```

---

## 📋 Task Endpoints

### GET /api/tasks
**Get list of available tasks**

**Response:**
```json
{
  "success": true,
  "message": "Available tasks retrieved",
  "data": {
    "tasks": [
      {
        "task_id": "waste_disposal",
        "name": "Waste Disposal",
        "description": "Dispose waste in proper bins",
        "reward": 20.0,
        "currency": "GP",
        "verification_required": true,
        "requirements": ["Photo proof", "Waste type selection"]
      },
      {
        "task_id": "litter_report",
        "name": "Report Littered Spot",
        "description": "Report and document littered areas",
        "base_reward": 30.0,
        "max_reward": 45.0,
        "currency": "GP",
        "verification_required": true,
        "requirements": ["Photo proof", "GPS location", "Severity level"]
      }
    ]
  }
}
```

---

### POST /api/submit-waste
**Submit waste disposal for verification**

**Request:**
```json
{
  "user_id": 1,
  "evidence": "Disposed plastic bottle in recycling bin",
  "image_path": "/uploads/waste_001.jpg",
  "waste_type": "recyclable"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Waste disposal submitted for verification",
  "data": {
    "verification_id": 1,
    "expected_reward": 20.0,
    "status": "pending",
    "estimated_verification_time": "24 hours"
  }
}
```

**Response (Error - User not found):**
```json
{
  "success": false,
  "message": "User not found",
  "data": null
}
```

---

### POST /api/submit-litter
**Submit litter report for verification**

**Request:**
```json
{
  "user_id": 1,
  "evidence": "Large pile of trash at Central Park",
  "image_path": "/uploads/litter_001.jpg",
  "location": "Central Park, North Section",
  "latitude": 40.785091,
  "longitude": -73.968285,
  "severity": "high"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Litter report submitted for verification",
  "data": {
    "verification_id": 2,
    "expected_reward": 45.0,
    "status": "pending",
    "severity": "high",
    "location": "Central Park, North Section",
    "estimated_verification_time": "24 hours"
  }
}
```

---

### GET /api/submissions/{user_id}?status=pending
**Get user's task submissions**

**Query Parameters:**
- `status` (optional): `pending`, `approved`, `rejected`

**Response:**
```json
{
  "success": true,
  "message": "Submissions retrieved",
  "data": {
    "user_id": 1,
    "user_name": "Alice Johnson",
    "total_count": 3,
    "submissions": [
      {
        "verification_id": 1,
        "task_type": "waste_disposal",
        "evidence": "Disposed plastic bottle in recycling bin",
        "image_path": "/uploads/waste_001.jpg",
        "expected_reward": 20.0,
        "status": "pending",
        "submitted_at": 1699876543.12,
        "verified_at": null,
        "verified_by": null
      },
      {
        "verification_id": 2,
        "task_type": "litter_report",
        "evidence": "Large pile of trash at Central Park",
        "image_path": "/uploads/litter_001.jpg",
        "location": "Central Park, North Section",
        "latitude": 40.785091,
        "longitude": -73.968285,
        "severity": "high",
        "expected_reward": 45.0,
        "status": "approved",
        "submitted_at": 1699876123.45,
        "verified_at": 1699890234.56,
        "verified_by": "Admin"
      }
    ]
  }
}
```

---

## 📱 QR Code Endpoints

### POST /api/qr/generate
**Business generates QR code for customer reward**

**Request:**
```json
{
  "business_id": 2,
  "reward_amount": 15,
  "service_description": "Coffee purchase - Large Latte",
  "expires_in_hours": 24
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "QR code generated",
  "data": {
    "qr_code": "GP-0001-A1B2C3D4E5F6",
    "business_name": "Green Cafe",
    "reward_amount": 15,
    "service_description": "Coffee purchase - Large Latte",
    "created_at": 1699876543.12,
    "expires_at": 1699962943.12,
    "status": "active"
  }
}
```

**Response (Error - Not a business):**
```json
{
  "success": false,
  "message": "Only businesses can generate QR codes",
  "data": null
}
```

---

### POST /api/qr/scan
**User scans QR code to receive reward**

**Request:**
```json
{
  "user_id": 1,
  "qr_code": "GP-0001-A1B2C3D4E5F6"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "QR code scanned successfully",
  "data": {
    "qr_code": "GP-0001-A1B2C3D4E5F6",
    "business_name": "Green Cafe",
    "amount": 15,
    "service_description": "Coffee purchase - Large Latte",
    "transaction_id": "a5fd0571e34002c2",
    "new_balance": 165.0,
    "block_mined": true,
    "transaction_confirmed": true
  }
}
```

**Response (Error - Already used):**
```json
{
  "success": false,
  "message": "QR code has already been used",
  "data": null
}
```

**Response (Error - Expired):**
```json
{
  "success": false,
  "message": "QR code has expired",
  "data": null
}
```

**Response (Error - Invalid):**
```json
{
  "success": false,
  "message": "Invalid QR code",
  "data": null
}
```

---

### GET /api/qr/info/{qr_code}
**Get information about a QR code**

**Response (Active QR):**
```json
{
  "success": true,
  "message": "QR code information",
  "data": {
    "qr_code": "GP-0001-A1B2C3D4E5F6",
    "business_name": "Green Cafe",
    "reward_amount": 15,
    "service_description": "Coffee purchase - Large Latte",
    "status": "active",
    "created_at": 1699876543.12,
    "expires_at": 1699962943.12,
    "is_expired": false
  }
}
```

**Response (Used QR):**
```json
{
  "success": true,
  "message": "QR code information",
  "data": {
    "qr_code": "GP-0001-A1B2C3D4E5F6",
    "business_name": "Green Cafe",
    "reward_amount": 15,
    "status": "used",
    "redeemed_by": "Alice Johnson",
    "redeemed_at": 1699890234.56
  }
}
```

---

## 🎯 Admin Endpoints

### GET /api/admin/verifications
**Get all pending task verifications (admin only)**

**Response:**
```json
{
  "success": true,
  "message": "Pending verifications retrieved",
  "data": {
    "total_count": 2,
    "verifications": [
      {
        "id": 1,
        "user_id": 1,
        "user_name": "Alice Johnson",
        "user_email": "alice@example.com",
        "user_phone": "+1234567890",
        "task_type": "waste_disposal",
        "evidence": "Disposed plastic bottle in recycling bin",
        "image_path": "/uploads/waste_001.jpg",
        "reward_amount": 20.0,
        "status": "pending",
        "submitted_at": 1699876543.12,
        "metadata": {
          "waste_type": "recyclable"
        }
      },
      {
        "id": 3,
        "user_id": 5,
        "user_name": "Bob Smith",
        "user_email": "bob@example.com",
        "task_type": "litter_report",
        "evidence": "Trash near beach",
        "image_path": "/uploads/litter_005.jpg",
        "location": "Sunset Beach",
        "latitude": 33.743844,
        "longitude": -118.395248,
        "severity": "medium",
        "reward_amount": 35.0,
        "status": "pending",
        "submitted_at": 1699880123.45
      }
    ]
  }
}
```

---

### POST /api/admin/approve/{verification_id}
**Approve verification and reward user**

**Request:**
```json
{
  "admin_name": "AdminJohn"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Verification approved",
  "data": {
    "verification_id": 1,
    "user_id": 1,
    "user_name": "Alice Johnson",
    "reward_amount": 20.0,
    "transaction_id": "a5fd0571e34002c2",
    "verified_by": "AdminJohn",
    "verified_at": 1699890234.56,
    "user_rewarded": true,
    "block_mined": true,
    "reward_confirmed": true,
    "new_balance": 170.0
  }
}
```

**Response (Error - Already verified):**
```json
{
  "success": false,
  "message": "Verification already processed",
  "data": null
}
```

---

### POST /api/admin/reject/{verification_id}
**Reject verification**

**Request:**
```json
{
  "reason": "Evidence photo is not clear enough",
  "admin_name": "AdminJohn"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Verification rejected",
  "data": {
    "verification_id": 1,
    "user_name": "Alice Johnson",
    "reason": "Evidence photo is not clear enough",
    "rejected_by": "AdminJohn",
    "rejected_at": 1699890234.56
  }
}
```

---

## 🏆 Leaderboard & Stats

### GET /api/leaderboard?limit=10
**Get top GP holders**

**Query Parameters:**
- `limit` (optional, default: 10): Number of top users

**Response:**
```json
{
  "success": true,
  "message": "Leaderboard retrieved",
  "data": {
    "leaderboard": [
      {
        "rank": 1,
        "user_id": 3,
        "name": "Carol Earth",
        "total_gp": 250.0,
        "completed_tasks": 8
      },
      {
        "rank": 2,
        "user_id": 1,
        "name": "Alice Johnson",
        "total_gp": 170.0,
        "completed_tasks": 5
      },
      {
        "rank": 3,
        "user_id": 5,
        "name": "Bob Smith",
        "total_gp": 120.0,
        "completed_tasks": 4
      }
    ],
    "total_users": 15,
    "last_updated": 1699890234.56
  }
}
```

---

### GET /api/transactions/{user_id}?limit=50
**Get user's transaction history**

**Query Parameters:**
- `limit` (optional, default: 50): Number of recent transactions

**Response:**
```json
{
  "success": true,
  "message": "Transaction history retrieved",
  "data": {
    "user_id": 1,
    "user_name": "Alice Johnson",
    "total_transactions": 7,
    "total_earned": 170.0,
    "transactions": [
      {
        "transaction_id": "a5fd0571e34002c2",
        "type": "waste_disposal",
        "amount": 20.0,
        "description": "Waste disposal reward",
        "timestamp": 1699890234.56,
        "status": "confirmed",
        "block_hash": "00254eb5fe7581ba..."
      },
      {
        "transaction_id": "b7c3d891f23456ab",
        "type": "litter_report",
        "amount": 45.0,
        "description": "Litter report reward - high severity",
        "timestamp": 1699885678.90,
        "status": "confirmed",
        "block_hash": "002b610c384221d7..."
      },
      {
        "transaction_id": "c9e4f012a34567bc",
        "type": "qr_scan",
        "amount": 15.0,
        "description": "QR reward from Green Cafe",
        "from_business": "Green Cafe",
        "timestamp": 1699880123.45,
        "status": "confirmed",
        "block_hash": "0015782a593412ef..."
      }
    ]
  }
}
```

---

### GET /api/stats
**Get overall system statistics**

**Response:**
```json
{
  "success": true,
  "message": "System statistics",
  "data": {
    "total_users": 150,
    "active_users": 142,
    "total_businesses": 8,
    "total_gp_in_circulation": 45600.0,
    "total_transactions": 1234,
    "total_blocks_mined": 89,
    "pending_verifications": 5,
    "approved_verifications": 567,
    "rejected_verifications": 12,
    "total_qr_codes_generated": 234,
    "total_qr_codes_redeemed": 198,
    "blockchain_health": "healthy",
    "last_block_time": 1699890234.56,
    "avg_block_mining_time": 1.2
  }
}
```

---

## 🔧 Utility Endpoints

### GET /health
**Health check**

**Response:**
```json
{
  "status": "healthy",
  "service": "Green Points Blockchain API",
  "version": "1.0.0"
}
```

---

### GET /
**API documentation**

**Response:**
```json
{
  "service": "Green Points Blockchain API",
  "version": "1.0.0",
  "endpoints": {
    "users": {
      "POST /api/sync-user": "Register new user",
      "POST /api/login": "Login user",
      "GET /api/profile/<user_id>": "Get user profile",
      "GET /api/balance/<user_id>": "Get user balance"
    },
    "tasks": { "..." },
    "qr_codes": { "..." },
    "admin": { "..." },
    "utilities": { "..." }
  },
  "documentation": "See INTEGRATION_GUIDE.md for complete documentation"
}
```

---

### POST /api/mine
**Manually trigger mining of pending transactions**

**Request:**
```json
{
  "miner": "SYSTEM"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Block mined successfully",
  "data": {
    "block_hash": "00254eb5fe7581ba8a627977b43a25542ef438ae1e2ff606d8dabdc792d2f090",
    "block_index": 3,
    "transactions_included": 5,
    "mining_time": 1.234,
    "difficulty": 2,
    "miner": "SYSTEM",
    "timestamp": 1699890234.56
  }
}
```

**Response (No pending transactions):**
```json
{
  "success": false,
  "message": "No pending transactions to mine",
  "data": null
}
```

---

## 📤 Image Upload

### POST /api/upload-image
**Upload task evidence image**

**Request (multipart/form-data):**
```
Content-Type: multipart/form-data
file: <binary image data>
```

**Response (Success):**
```json
{
  "success": true,
  "path": "/uploads/e4f2a1b3-c5d6-47e8-91f2-3a4b5c6d7e8f.jpg",
  "filename": "e4f2a1b3-c5d6-47e8-91f2-3a4b5c6d7e8f.jpg"
}
```

**Response (Error - No file):**
```json
{
  "success": false,
  "error": "No file provided"
}
```

---

## 📝 Common Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Endpoint not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## ✅ Response Format Standard

All API responses follow this structure:

```json
{
  "success": true,           // boolean: true or false
  "message": "...",           // string: human-readable message
  "data": { ... } or null     // object or null: actual data
}
```

**Success Response:**
- `success`: `true`
- `message`: Descriptive success message
- `data`: Object containing the response data

**Error Response:**
- `success`: `false`
- `message`: Error description
- `data`: `null`

---

## 🎯 Frontend Integration Tips

1. **Always check `success` field first**
   ```javascript
   if (response.success) {
     // Use response.data
   } else {
     // Show response.message as error
   }
   ```

2. **Handle loading states**
   ```javascript
   setLoading(true);
   const response = await api.getBalance(userId);
   setLoading(false);
   ```

3. **Cache leaderboard data**
   ```javascript
   // Leaderboard doesn't change often, cache for 5 minutes
   const CACHE_TIME = 5 * 60 * 1000;
   ```

4. **Show pending submissions**
   ```javascript
   // Refresh submissions list after task submission
   await api.submitWaste(...);
   await loadSubmissions('pending');
   ```

5. **Real-time balance updates**
   ```javascript
   // After QR scan or approval, refresh balance
   const result = await api.scanQR(...);
   if (result.success) {
     setBalance(result.data.new_balance);
   }
   ```

---

Need help integrating any specific endpoint? Check the INTEGRATION_GUIDE.md! 🚀
