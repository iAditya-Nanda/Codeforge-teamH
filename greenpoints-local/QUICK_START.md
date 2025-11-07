# ⚡ Quick Start Guide - Frontend Integration

## 🎯 What You Need to Do (Simple Summary)

Your existing frontend app already has user signup/login working with your database. Now you just need to:

1. **Start the API server** (one command)
2. **Call the API from your frontend** (simple HTTP requests)
3. **Display the JSON data** (you already know how to do this)

That's it! No blockchain knowledge needed on the frontend side.

---

## 📋 Step-by-Step Integration

### Step 1: Start the Blockchain API Server

```bash
cd /home/kenx1kaneki/Desktop/greenpoints-local
python3 server.py
```

**Output:**
```
🚀 Starting Green Points Blockchain API Server...
📍 Server running at: http://localhost:5000
```

Server is now ready to receive requests from your frontend!

---

### Step 2: Connect Your Existing Signup

When a user signs up in your app, send their info to the blockchain:

**Your Frontend Code (React Native example):**

```javascript
// In your existing signup function
async function signupUser(name, email, phone, password) {
  
  // 1. YOUR EXISTING CODE - Create user in your database
  const user = await yourAPI.createUser({ name, email, phone, password });
  
  // 2. NEW: Also create blockchain wallet
  try {
    const response = await fetch('http://your-server:5000/api/sync-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone })
    });
    
    const result = await response.json();
    
    if (result.success) {
      // Save the wallet address in YOUR database
      await yourAPI.updateUser(user.id, {
        blockchain_user_id: result.data.user_id,
        wallet_address: result.data.wallet_address
      });
    }
  } catch (error) {
    console.log('Blockchain sync failed, will retry later');
  }
  
  return user;
}
```

**That's it for signup!** Users now have blockchain wallets automatically.

---

### Step 3: Show GP Balance in Profile

**Your Frontend Code:**

```javascript
// In user profile screen
async function loadUserProfile(userId) {
  const response = await fetch(`http://your-server:5000/api/balance/${userId}`);
  const result = await response.json();
  
  if (result.success) {
    setGPBalance(result.data.balance);  // Show: "100 GP"
  }
}
```

**Display in UI:**
```javascript
<View>
  <Text>Your Green Points: {gpBalance} GP</Text>
</View>
```

---

### Step 4: Waste Disposal Submission

**Your Frontend Code:**

```javascript
async function submitWasteDisposal(userId, imageUri, wasteType) {
  
  // 1. Upload image first (to your server)
  const imagePath = await uploadImage(imageUri);
  
  // 2. Submit to blockchain
  const response = await fetch('http://your-server:5000/api/submit-waste', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      evidence: "Disposed waste in proper bin",
      image_path: imagePath,
      waste_type: wasteType  // 'recyclable', 'organic', 'general'
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    Alert.alert(
      'Success!',
      `Submitted for verification. You'll get ${result.data.expected_reward} GP after approval.`
    );
  }
}
```

---

### Step 5: Litter Reporting

**Your Frontend Code:**

```javascript
async function submitLitterReport(userId, imageUri, location, coords, severity) {
  
  const imagePath = await uploadImage(imageUri);
  
  const response = await fetch('http://your-server:5000/api/submit-litter', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      evidence: "Reported littered area",
      image_path: imagePath,
      location: location,
      latitude: coords.latitude,
      longitude: coords.longitude,
      severity: severity  // 'low', 'medium', 'high'
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    Alert.alert('Success!', `Expected reward: ${result.data.expected_reward} GP`);
  }
}
```

---

### Step 6: QR Code Scanning

**Your Frontend Code:**

```javascript
import { RNCamera } from 'react-native-camera';

function QRScannerScreen({ userId }) {
  
  async function handleQRCodeScanned(qrCode) {
    const response = await fetch('http://your-server:5000/api/qr/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        qr_code: qrCode
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      Alert.alert(
        '🎉 Reward Earned!',
        `You earned ${result.data.amount} GP from ${result.data.business_name}!`
      );
      // Refresh balance
      loadUserProfile(userId);
    } else {
      Alert.alert('Error', result.message);
    }
  }
  
  return (
    <RNCamera
      onBarCodeRead={(e) => handleQRCodeScanned(e.data)}
    />
  );
}
```

---

### Step 7: Show Leaderboard

**Your Frontend Code:**

```javascript
async function loadLeaderboard() {
  const response = await fetch('http://your-server:5000/api/leaderboard?limit=10');
  const result = await response.json();
  
  if (result.success) {
    setLeaderboard(result.data.leaderboard);
  }
}

// Display
function LeaderboardScreen() {
  return (
    <FlatList
      data={leaderboard}
      renderItem={({ item }) => (
        <View>
          <Text>#{item.rank} - {item.name}</Text>
          <Text>{item.total_gp} GP</Text>
        </View>
      )}
    />
  );
}
```

---

## 🔧 Admin Verification (Web Dashboard)

Create a simple admin page to approve/reject submissions:

```javascript
// Admin panel - Get pending verifications
async function loadPendingVerifications() {
  const response = await fetch('http://your-server:5000/api/admin/verifications');
  const result = await response.json();
  
  if (result.success) {
    setPendingVerifications(result.data.verifications);
  }
}

// Approve a submission
async function approveVerification(verificationId) {
  const response = await fetch(`http://your-server:5000/api/admin/approve/${verificationId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ admin_name: 'Admin' })
  });
  
  const result = await response.json();
  
  if (result.success) {
    alert(`Approved! User ${result.data.user_name} received ${result.data.reward_amount} GP`);
    loadPendingVerifications();  // Refresh list
  }
}

// Reject a submission
async function rejectVerification(verificationId, reason) {
  const response = await fetch(`http://your-server:5000/api/admin/reject/${verificationId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      reason: reason,
      admin_name: 'Admin'
    })
  });
  
  if (response.json().success) {
    alert('Verification rejected');
    loadPendingVerifications();
  }
}
```

---

## 📊 Complete API Endpoints Reference

### User Endpoints
- `POST /api/sync-user` - Register new user
- `POST /api/login` - Login user
- `GET /api/profile/:userId` - Get user profile
- `GET /api/balance/:userId` - Get GP balance

### Task Endpoints
- `GET /api/tasks` - Get available tasks
- `POST /api/submit-waste` - Submit waste disposal
- `POST /api/submit-litter` - Submit litter report
- `GET /api/submissions/:userId?status=pending` - Get user submissions

### QR Code Endpoints
- `POST /api/qr/generate` - Generate QR (business only)
- `POST /api/qr/scan` - Scan QR code
- `GET /api/qr/info/:qrCode` - Get QR info

### Admin Endpoints
- `GET /api/admin/verifications` - Get pending verifications
- `POST /api/admin/approve/:id` - Approve verification
- `POST /api/admin/reject/:id` - Reject verification

### Utility Endpoints
- `GET /api/leaderboard?limit=10` - Get top users
- `GET /api/transactions/:userId?limit=50` - Get transaction history
- `GET /api/stats` - Get system statistics

---

## 🚀 Deployment

### Deploy on Your Server

```bash
# 1. Copy files to server
scp -r greenpoints-local/ user@your-server:/opt/greenpoints/

# 2. SSH to server
ssh user@your-server

# 3. Install dependencies
cd /opt/greenpoints
pip install flask flask-cors gunicorn

# 4. Run with gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 server:app

# 5. Or use systemd for auto-restart
sudo nano /etc/systemd/system/greenpoints.service
```

**systemd service file:**
```ini
[Unit]
Description=Green Points Blockchain API
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/greenpoints
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:5000 server:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable greenpoints
sudo systemctl start greenpoints
```

---

## ✅ Testing Checklist

- [ ] Server starts successfully
- [ ] User registration works
- [ ] Balance shows correctly
- [ ] Waste disposal submission works
- [ ] Admin can approve verifications
- [ ] Balance updates after approval
- [ ] QR code generation works
- [ ] QR code scanning works
- [ ] Leaderboard displays
- [ ] Transaction history shows

---

## 🎉 You're Done!

Your frontend is now connected to the blockchain. Users can:

✅ Earn GP by submitting waste disposal  
✅ Earn GP by reporting littered spots  
✅ Earn GP by scanning QR codes from businesses  
✅ See their balance and rank on leaderboard  
✅ View transaction history  

**No blockchain knowledge required on the frontend side!**

Just make HTTP requests and display the JSON data. 🚀
