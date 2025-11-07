# 🔗 Frontend Integration Guide

## Complete Guide to Connect Your Existing App to Green Points Blockchain

---

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Database Synchronization](#database-synchronization)
3. [REST API Setup](#rest-api-setup)
4. [Frontend Integration Examples](#frontend-integration-examples)
5. [Deployment Guide](#deployment-guide)

---

## 🏗️ System Overview

### Current Architecture

```
┌──────────────────────────────────────────────────┐
│         YOUR EXISTING FRONTEND APP                │
│    (React Native / React / Flutter)              │
│                                                   │
│    - User signup ✓ (already working)            │
│    - User login ✓ (already working)             │
│    - Your existing database ✓                   │
└────────────────┬─────────────────────────────────┘
                 │
                 │ Need to add: HTTP API calls
                 ▼
┌──────────────────────────────────────────────────┐
│         NEW: GREEN POINTS API SERVER              │
│         (Python Flask/FastAPI)                    │
│                                                   │
│    ┌─────────────────────────────────┐          │
│    │  Your Existing User Database    │          │
│    │  (MySQL/PostgreSQL/etc.)        │          │
│    └──────────────┬──────────────────┘          │
│                   │                               │
│    ┌──────────────▼──────────────────┐          │
│    │  Blockchain System (SQLite)     │          │
│    │  - GP balances                  │          │
│    │  - Transactions                 │          │
│    │  - Verifications                │          │
│    │  - QR codes                     │          │
│    └─────────────────────────────────┘          │
└──────────────────────────────────────────────────┘
```

---

## 🔄 Database Synchronization Strategy

### Option 1: ⭐ **Recommended - Webhook on Signup**

When user signs up in your existing app, send their data to blockchain:

```javascript
// In your existing signup function
async function signupUser(name, email, phone) {
  // 1. Save to YOUR database (existing code)
  const user = await yourDatabase.createUser(name, email, phone);
  
  // 2. NEW: Send to blockchain system
  try {
    const response = await fetch('http://your-server:5000/api/sync-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: user.id,  // Your database user ID
        name: name,
        email: email,
        phone: phone
      })
    });
    
    const data = await response.json();
    // data.wallet_address - save this in your database
    await yourDatabase.updateUser(user.id, {
      wallet_address: data.wallet_address
    });
    
  } catch (error) {
    console.error('Blockchain sync failed:', error);
    // Handle error - maybe retry later
  }
  
  return user;
}
```

### Option 2: **Batch Sync Existing Users**

Sync all existing users at once:

```python
# Run this once to sync existing users from your database
import mysql.connector  # or your database driver
from api import GreenPointsAPI
from blockchain import Blockchain
from database import Database

# Connect to YOUR existing database
your_db = mysql.connector.connect(
    host="your-host",
    user="your-user",
    password="your-password",
    database="your-database"
)

# Connect to blockchain
blockchain = Blockchain()
gp_db = Database()
api = GreenPointsAPI(blockchain, gp_db)

# Fetch all users from YOUR database
cursor = your_db.cursor(dictionary=True)
cursor.execute("SELECT id, name, email, phone FROM users")

# Sync each user to blockchain
for user in cursor.fetchall():
    response = api.register_user(
        name=user['name'],
        email=user['email'],
        phone=user['phone']
    )
    
    if response['success']:
        wallet_address = response['data']['wallet_address']
        
        # Update YOUR database with wallet address
        update_cursor = your_db.cursor()
        update_cursor.execute(
            "UPDATE users SET wallet_address = %s WHERE id = %s",
            (wallet_address, user['id'])
        )
        your_db.commit()
        print(f"✓ Synced user: {user['name']}")

print("Sync completed!")
```

---

## 🚀 REST API Setup

### Step 1: Create Flask API Server

Create `server.py`:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from blockchain import Blockchain
from database import Database
from api import GreenPointsAPI

app = Flask(__name__)
CORS(app)  # Allow requests from your frontend

# Initialize blockchain system
blockchain = Blockchain(difficulty=2)
db = Database("greenpoints.db")
api = GreenPointsAPI(blockchain, db)

# ==================== USER ENDPOINTS ====================

@app.route('/api/sync-user', methods=['POST'])
def sync_user():
    """Called when user signs up in your app"""
    data = request.json
    response = api.register_user(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone')
    )
    return jsonify(response)

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    response = api.login(
        email=data.get('email'),
        phone=data.get('phone')
    )
    return jsonify(response)

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile with GP balance"""
    response = api.get_user_profile(user_id)
    return jsonify(response)

@app.route('/api/balance/<int:user_id>', methods=['GET'])
def get_balance(user_id):
    """Get user's GP balance"""
    response = api.get_balance(user_id)
    return jsonify(response)

# ==================== TASK ENDPOINTS ====================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get available tasks"""
    response = api.get_available_tasks()
    return jsonify(response)

@app.route('/api/submit-waste', methods=['POST'])
def submit_waste():
    """Submit waste disposal task"""
    data = request.json
    response = api.submit_waste_disposal(
        user_id=data['user_id'],
        evidence=data['evidence'],
        image_path=data.get('image_path'),
        waste_type=data.get('waste_type', 'general')
    )
    return jsonify(response)

@app.route('/api/submit-litter', methods=['POST'])
def submit_litter():
    """Submit litter report"""
    data = request.json
    response = api.submit_litter_report(
        user_id=data['user_id'],
        evidence=data['evidence'],
        image_path=data.get('image_path'),
        location=data.get('location'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        severity=data.get('severity', 'medium')
    )
    return jsonify(response)

@app.route('/api/submissions/<int:user_id>', methods=['GET'])
def get_submissions(user_id):
    """Get user's task submissions"""
    status = request.args.get('status')  # pending, approved, rejected
    response = api.get_user_submissions(user_id, status)
    return jsonify(response)

# ==================== QR CODE ENDPOINTS ====================

@app.route('/api/qr/generate', methods=['POST'])
def generate_qr():
    """Business generates QR code"""
    data = request.json
    response = api.generate_qr_code(
        business_id=data['business_id'],
        reward_amount=data['reward_amount'],
        service_description=data.get('service_description', ''),
        expires_in_hours=data.get('expires_in_hours')
    )
    return jsonify(response)

@app.route('/api/qr/scan', methods=['POST'])
def scan_qr():
    """User scans QR code"""
    data = request.json
    response = api.scan_qr_code(
        qr_code=data['qr_code'],
        user_id=data['user_id']
    )
    
    # After successful scan, mine the block to process reward
    if response['success']:
        api.mine_block("SYSTEM")
    
    return jsonify(response)

@app.route('/api/qr/info/<qr_code>', methods=['GET'])
def get_qr_info(qr_code):
    """Get QR code information"""
    response = api.get_qr_code_info(qr_code)
    return jsonify(response)

# ==================== LEADERBOARD ====================

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top GP holders"""
    limit = request.args.get('limit', 10, type=int)
    response = api.get_leaderboard(limit)
    return jsonify(response)

# ==================== ADMIN ENDPOINTS ====================

@app.route('/api/admin/verifications', methods=['GET'])
def get_pending_verifications():
    """Get pending verifications (admin only)"""
    # TODO: Add admin authentication
    response = api.get_pending_verifications()
    return jsonify(response)

@app.route('/api/admin/approve/<int:verification_id>', methods=['POST'])
def approve_verification(verification_id):
    """Approve verification (admin only)"""
    # TODO: Add admin authentication
    data = request.json
    response = api.approve_verification(
        verification_id=verification_id,
        admin_name=data.get('admin_name', 'SYSTEM')
    )
    
    # Mine block to process reward
    if response['success']:
        api.mine_block("SYSTEM")
    
    return jsonify(response)

@app.route('/api/admin/reject/<int:verification_id>', methods=['POST'])
def reject_verification(verification_id):
    """Reject verification (admin only)"""
    # TODO: Add admin authentication
    data = request.json
    response = api.reject_verification(
        verification_id=verification_id,
        reason=data['reason'],
        admin_name=data.get('admin_name', 'SYSTEM')
    )
    return jsonify(response)

# ==================== UTILITIES ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    response = api.get_system_stats()
    return jsonify(response)

@app.route('/api/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    """Get user's transaction history"""
    limit = request.args.get('limit', 50, type=int)
    response = api.get_transaction_history(user_id, limit)
    return jsonify(response)

# Auto-mine blocks periodically (optional)
@app.route('/api/mine', methods=['POST'])
def mine_block():
    """Mine pending transactions"""
    response = api.mine_block("SYSTEM")
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Step 2: Install Dependencies

```bash
pip install flask flask-cors
```

### Step 3: Run the Server

```bash
python server.py
```

Server will run on `http://localhost:5000`

---

## 📱 Frontend Integration Examples

### React Native Example

```javascript
// services/greenPointsAPI.js

const API_URL = 'http://your-server-ip:5000/api';

export const GreenPointsAPI = {
  
  // Get user balance
  async getBalance(userId) {
    const response = await fetch(`${API_URL}/balance/${userId}`);
    return await response.json();
  },
  
  // Submit waste disposal
  async submitWasteDisposal(userId, evidence, imageUri, wasteType) {
    const response = await fetch(`${API_URL}/submit-waste`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        evidence: evidence,
        image_path: imageUri,  // Upload image first, get path
        waste_type: wasteType  // 'recyclable', 'organic', 'general'
      })
    });
    return await response.json();
  },
  
  // Submit litter report
  async submitLitterReport(userId, evidence, imageUri, location, coords, severity) {
    const response = await fetch(`${API_URL}/submit-litter`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        evidence: evidence,
        image_path: imageUri,
        location: location,
        latitude: coords.latitude,
        longitude: coords.longitude,
        severity: severity  // 'low', 'medium', 'high'
      })
    });
    return await response.json();
  },
  
  // Scan QR code
  async scanQRCode(userId, qrCode) {
    const response = await fetch(`${API_URL}/qr/scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        qr_code: qrCode
      })
    });
    return await response.json();
  },
  
  // Get leaderboard
  async getLeaderboard(limit = 10) {
    const response = await fetch(`${API_URL}/leaderboard?limit=${limit}`);
    return await response.json();
  },
  
  // Get user submissions
  async getSubmissions(userId, status = null) {
    let url = `${API_URL}/submissions/${userId}`;
    if (status) url += `?status=${status}`;
    const response = await fetch(url);
    return await response.json();
  },
  
  // Get transaction history
  async getTransactions(userId, limit = 50) {
    const response = await fetch(`${API_URL}/transactions/${userId}?limit=${limit}`);
    return await response.json();
  }
};
```

### Usage in React Native Component

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, Button, Image } from 'react-native';
import { GreenPointsAPI } from './services/greenPointsAPI';

function WasteDisposalScreen({ userId }) {
  const [balance, setBalance] = useState(0);
  const [image, setImage] = useState(null);
  
  // Load balance on mount
  useEffect(() => {
    loadBalance();
  }, []);
  
  async function loadBalance() {
    const result = await GreenPointsAPI.getBalance(userId);
    if (result.success) {
      setBalance(result.data.balance);
    }
  }
  
  async function submitWaste() {
    // 1. Take photo (use react-native-image-picker)
    const photo = await takePhoto();
    
    // 2. Upload image to your server (get path)
    const imagePath = await uploadImage(photo.uri);
    
    // 3. Submit to blockchain
    const result = await GreenPointsAPI.submitWasteDisposal(
      userId,
      "Disposed plastic in recycling bin",
      imagePath,
      "recyclable"
    );
    
    if (result.success) {
      alert(`Submitted! Expected reward: ${result.data.expected_reward} GP`);
      // Reload balance after verification
    } else {
      alert(`Error: ${result.message}`);
    }
  }
  
  return (
    <View>
      <Text>Your GP Balance: {balance}</Text>
      <Button title="Submit Waste Disposal" onPress={submitWaste} />
    </View>
  );
}

function QRScannerScreen({ userId }) {
  async function handleQRScan(qrCode) {
    const result = await GreenPointsAPI.scanQRCode(userId, qrCode);
    
    if (result.success) {
      alert(`You earned ${result.data.amount} GP from ${result.data.business_name}!`);
      // Update balance
    } else {
      alert(`Error: ${result.message}`);
    }
  }
  
  return (
    <QRCodeScanner
      onRead={(e) => handleQRScan(e.data)}
    />
  );
}

function LeaderboardScreen() {
  const [leaderboard, setLeaderboard] = useState([]);
  
  useEffect(() => {
    loadLeaderboard();
  }, []);
  
  async function loadLeaderboard() {
    const result = await GreenPointsAPI.getLeaderboard(10);
    if (result.success) {
      setLeaderboard(result.data.leaderboard);
    }
  }
  
  return (
    <View>
      {leaderboard.map((user, index) => (
        <View key={user.user_id}>
          <Text>#{user.rank} - {user.name}: {user.total_gp} GP</Text>
        </View>
      ))}
    </View>
  );
}
```

---

## 🔐 Important Security Considerations

### 1. Add Authentication

```python
from functools import wraps
import jwt

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "No token provided"}), 401
        
        try:
            # Verify JWT token
            data = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            request.user_id = data['user_id']
        except:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# Use it:
@app.route('/api/submit-waste', methods=['POST'])
@require_auth
def submit_waste():
    # request.user_id is now available
    pass
```

### 2. Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/submit-waste', methods=['POST'])
@limiter.limit("5 per hour")  # Max 5 submissions per hour
def submit_waste():
    pass
```

---

## 📤 Image Upload Handling

```python
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    return jsonify({
        "success": True,
        "path": filepath
    })
```

Frontend usage:
```javascript
async function uploadImage(imageUri) {
  const formData = new FormData();
  formData.append('file', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'photo.jpg'
  });
  
  const response = await fetch(`${API_URL}/upload-image`, {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  return result.path;
}
```

---

## 🚀 Deployment Guide

### Option 1: Deploy on Your Existing Server

```bash
# 1. Copy blockchain files to your server
scp -r greenPoints-local-Blockchain/ user@your-server:/opt/greenpoints/

# 2. Install dependencies
ssh user@your-server
cd /opt/greenpoints
pip install flask flask-cors

# 3. Run with gunicorn (production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install flask flask-cors gunicorn

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
```

Run:
```bash
docker build -t greenpoints-api .
docker run -p 5000:5000 greenpoints-api
```

---

## ✅ Quick Start Checklist

- [ ] 1. Run `python server.py` to start API
- [ ] 2. Test API: `curl http://localhost:5000/api/stats`
- [ ] 3. Sync existing users (run batch sync script)
- [ ] 4. Update frontend signup to call `/api/sync-user`
- [ ] 5. Add balance display in user profile
- [ ] 6. Integrate waste disposal submission
- [ ] 7. Integrate litter reporting
- [ ] 8. Add QR code scanner
- [ ] 9. Add leaderboard screen
- [ ] 10. Deploy to production server

---

## 🎯 Summary

**What You Need to Do:**

1. **Run the API server** (`server.py`)
2. **Sync existing users** (one-time batch script)
3. **Update your frontend** to call these endpoints:
   - On signup: `POST /api/sync-user`
   - Display balance: `GET /api/balance/:id`
   - Submit tasks: `POST /api/submit-waste`, `POST /api/submit-litter`
   - Scan QR: `POST /api/qr/scan`
   - Show leaderboard: `GET /api/leaderboard`

**That's it!** Your blockchain is ready to use. 🚀

---

Need help with any specific part? Let me know!
