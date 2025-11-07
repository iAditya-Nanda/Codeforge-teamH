# 🚀 Frontend Integration - Start Here!

**Hey Frontend Team!** This guide will get you connected to the blockchain in **5 minutes**. No blockchain knowledge needed!

---

## 🎯 TL;DR - What You Need to Know

1. **Start the server:** `python3 server.py`
2. **Make HTTP requests:** Just like any REST API
3. **Get JSON responses:** Display the data
4. **That's it!** The blockchain handles everything else

---

## ⚡ 5-Minute Setup

### Step 1: Start the API Server (30 seconds)

```bash
cd /home/kenx1kaneki/Desktop/greenpoints-local
python3 server.py
```

**You'll see:**
```
🚀 Starting Green Points Blockchain API Server...
📍 Server running at: http://localhost:5000
```

✅ **Server is ready!**

### Step 2: Test It Works (30 seconds)

Open a new terminal and run:

```bash
curl http://localhost:5000/health
```

**You should see:**
```json
{
  "status": "healthy",
  "service": "Green Points Blockchain API",
  "version": "1.0.0"
}
```

✅ **API is working!**

### Step 3: Your First Request (1 minute)

Register a test user:

```bash
curl -X POST http://localhost:5000/api/sync-user \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"+1234567890"}'
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": 1,
    "wallet_address": "ee817b9d5b0172453620",
    "balance": 0
  }
}
```

✅ **User created with blockchain wallet!**

---

## 📱 Frontend Integration (React Native)

### Create API Service File

```javascript
// services/greenPointsAPI.js

const API_URL = 'http://your-server-ip:5000/api';

export const GreenPointsAPI = {
  
  // ========== USER FUNCTIONS ==========
  
  async getBalance(userId) {
    const response = await fetch(`${API_URL}/balance/${userId}`);
    return await response.json();
  },
  
  async getProfile(userId) {
    const response = await fetch(`${API_URL}/profile/${userId}`);
    return await response.json();
  },
  
  // ========== TASK FUNCTIONS ==========
  
  async submitWasteDisposal(userId, evidence, imageUri, wasteType) {
    const response = await fetch(`${API_URL}/submit-waste`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        evidence: evidence,
        image_path: imageUri,
        waste_type: wasteType  // 'recyclable', 'organic', 'general'
      })
    });
    return await response.json();
  },
  
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
  
  async getSubmissions(userId, status = null) {
    let url = `${API_URL}/submissions/${userId}`;
    if (status) url += `?status=${status}`;
    const response = await fetch(url);
    return await response.json();
  },
  
  // ========== QR FUNCTIONS ==========
  
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
  
  // ========== LEADERBOARD ==========
  
  async getLeaderboard(limit = 10) {
    const response = await fetch(`${API_URL}/leaderboard?limit=${limit}`);
    return await response.json();
  },
  
  async getTransactions(userId, limit = 50) {
    const response = await fetch(`${API_URL}/transactions/${userId}?limit=${limit}`);
    return await response.json();
  }
};
```

---

## 📱 Screen Examples

### 1. Profile Screen

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, ActivityIndicator } from 'react-native';
import { GreenPointsAPI } from './services/greenPointsAPI';

function ProfileScreen({ userId }) {
  const [balance, setBalance] = useState(0);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadBalance();
  }, []);
  
  async function loadBalance() {
    setLoading(true);
    const result = await GreenPointsAPI.getBalance(userId);
    
    if (result.success) {
      setBalance(result.data.balance);
    }
    setLoading(false);
  }
  
  if (loading) {
    return <ActivityIndicator />;
  }
  
  return (
    <View>
      <Text style={{ fontSize: 48, color: '#4CAF50' }}>
        {balance} GP
      </Text>
      <Text>Your Green Points Balance</Text>
    </View>
  );
}
```

---

### 2. Waste Disposal Screen

```javascript
import React, { useState } from 'react';
import { View, Button, Image, Alert } from 'react-native';
import { launchCamera } from 'react-native-image-picker';
import { GreenPointsAPI } from './services/greenPointsAPI';

function WasteDisposalScreen({ userId }) {
  const [imageUri, setImageUri] = useState(null);
  const [wasteType, setWasteType] = useState('recyclable');
  
  async function takePhoto() {
    const result = await launchCamera({
      mediaType: 'photo',
      quality: 0.8
    });
    
    if (result.assets && result.assets[0]) {
      setImageUri(result.assets[0].uri);
    }
  }
  
  async function submitWaste() {
    if (!imageUri) {
      Alert.alert('Error', 'Please take a photo first');
      return;
    }
    
    // 1. Upload image (implement your upload function)
    const imagePath = await uploadImage(imageUri);
    
    // 2. Submit to blockchain
    const result = await GreenPointsAPI.submitWasteDisposal(
      userId,
      'Disposed waste properly',
      imagePath,
      wasteType
    );
    
    if (result.success) {
      Alert.alert(
        'Success!',
        `Submitted for verification.\nExpected reward: ${result.data.expected_reward} GP`,
        [{ text: 'OK', onPress: () => navigation.goBack() }]
      );
    } else {
      Alert.alert('Error', result.message);
    }
  }
  
  return (
    <View>
      {imageUri && <Image source={{ uri: imageUri }} style={{ width: 300, height: 300 }} />}
      
      <Button title="Take Photo" onPress={takePhoto} />
      
      {/* Waste type picker */}
      <Picker
        selectedValue={wasteType}
        onValueChange={setWasteType}
      >
        <Picker.Item label="Recyclable" value="recyclable" />
        <Picker.Item label="Organic" value="organic" />
        <Picker.Item label="General" value="general" />
      </Picker>
      
      <Button 
        title="Submit for 20 GP" 
        onPress={submitWaste}
        disabled={!imageUri}
      />
    </View>
  );
}
```

---

### 3. QR Scanner Screen

```javascript
import React from 'react';
import { View, Text, Alert } from 'react-native';
import { RNCamera } from 'react-native-camera';
import { GreenPointsAPI } from './services/greenPointsAPI';

function QRScannerScreen({ userId, navigation }) {
  const [scanning, setScanning] = useState(true);
  
  async function handleQRScan(qrCode) {
    if (!scanning) return;
    
    setScanning(false);  // Prevent multiple scans
    
    const result = await GreenPointsAPI.scanQRCode(userId, qrCode);
    
    if (result.success) {
      Alert.alert(
        '🎉 Reward Earned!',
        `You earned ${result.data.amount} GP from ${result.data.business_name}!`,
        [{ 
          text: 'Awesome!', 
          onPress: () => navigation.navigate('Profile')  // Go back to see new balance
        }]
      );
    } else {
      Alert.alert('Error', result.message);
      setScanning(true);  // Allow retry
    }
  }
  
  return (
    <View style={{ flex: 1 }}>
      <RNCamera
        style={{ flex: 1 }}
        onBarCodeRead={(e) => handleQRScan(e.data)}
      >
        <View style={{ flex: 1, backgroundColor: 'transparent', justifyContent: 'center', alignItems: 'center' }}>
          <Text style={{ color: 'white', fontSize: 18 }}>
            Scan QR Code to Earn GP
          </Text>
        </View>
      </RNCamera>
    </View>
  );
}
```

---

### 4. Leaderboard Screen

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { GreenPointsAPI } from './services/greenPointsAPI';

function LeaderboardScreen() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadLeaderboard();
  }, []);
  
  async function loadLeaderboard() {
    setLoading(true);
    const result = await GreenPointsAPI.getLeaderboard(10);
    
    if (result.success) {
      setLeaderboard(result.data.leaderboard);
    }
    setLoading(false);
  }
  
  function renderUser({ item }) {
    return (
      <View style={styles.userRow}>
        <Text style={styles.rank}>#{item.rank}</Text>
        <Text style={styles.name}>{item.name}</Text>
        <Text style={styles.gp}>{item.total_gp} GP</Text>
      </View>
    );
  }
  
  if (loading) {
    return <ActivityIndicator />;
  }
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>🏆 Top Green Heroes</Text>
      
      <FlatList
        data={leaderboard}
        renderItem={renderUser}
        keyExtractor={(item) => item.user_id.toString()}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  userRow: { flexDirection: 'row', padding: 15, borderBottomWidth: 1, borderBottomColor: '#eee' },
  rank: { fontSize: 18, fontWeight: 'bold', width: 50 },
  name: { flex: 1, fontSize: 16 },
  gp: { fontSize: 16, color: '#4CAF50', fontWeight: 'bold' }
});
```

---

## 🔗 Connect Your Existing Signup

When a user signs up in your app, also create their blockchain wallet:

```javascript
// In your existing signup function
async function signupUser(name, email, phone, password) {
  
  // 1. YOUR EXISTING CODE - Create user in your database
  const user = await yourAPI.createUser({ name, email, phone, password });
  
  // 2. NEW - Create blockchain wallet
  try {
    const response = await fetch('http://your-server:5000/api/sync-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone })
    });
    
    const result = await response.json();
    
    if (result.success) {
      // Save wallet info in YOUR database
      await yourAPI.updateUser(user.id, {
        blockchain_user_id: result.data.user_id,
        wallet_address: result.data.wallet_address
      });
    }
  } catch (error) {
    console.log('Blockchain sync failed, will retry later');
    // Don't fail signup if blockchain sync fails
  }
  
  return user;
}
```

---

## 📋 All API Endpoints (Cheat Sheet)

```javascript
// USER
GET  /api/balance/:userId           → Get GP balance
GET  /api/profile/:userId           → Get user profile
POST /api/sync-user                 → Register new user

// TASKS
POST /api/submit-waste              → Submit waste disposal (20 GP)
POST /api/submit-litter             → Report littered spot (30-45 GP)
GET  /api/submissions/:userId       → Get user's submissions

// QR CODES
POST /api/qr/scan                   → Scan QR code for reward

// LEADERBOARD
GET  /api/leaderboard?limit=10      → Get top GP holders
GET  /api/transactions/:userId      → Get transaction history

// STATS
GET  /api/stats                     → System statistics
```

**For detailed API docs with example responses, see:** [API_RESPONSES.md](API_RESPONSES.md)

---

## ✅ Integration Checklist

- [ ] Server is running (`python3 server.py`)
- [ ] Health check works (`curl http://localhost:5000/health`)
- [ ] Created `services/greenPointsAPI.js` file
- [ ] Profile screen shows GP balance
- [ ] Waste disposal submission works
- [ ] Litter report submission works
- [ ] QR scanner works
- [ ] Leaderboard displays
- [ ] Signup creates blockchain wallet
- [ ] Tested on real device (not just emulator)

---

## 🐛 Common Issues

### "Network request failed"
- ✅ Make sure server is running
- ✅ Use your computer's IP address, not `localhost` (for real devices)
- ✅ Check firewall allows port 5000

### "User not found" after signup
- ✅ Make sure you're calling `/api/sync-user` on signup
- ✅ Save the returned `user_id` in your database

### QR scanner not working
- ✅ Request camera permissions
- ✅ Test with a generated QR code first (use admin to generate)

### Balance not updating
- ✅ Reload balance after QR scan
- ✅ Check if task was approved by admin
- ✅ Pending tasks don't increase balance until approved

---

## 📖 More Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick integration guide
- **[API_RESPONSES.md](API_RESPONSES.md)** - Complete API reference with examples
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Detailed integration guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture diagrams

---

## 🎯 What You DON'T Need to Worry About

❌ **Blockchain details** - The API handles everything  
❌ **Mining blocks** - Happens automatically  
❌ **Transaction validation** - System does it  
❌ **Wallet management** - Created automatically  
❌ **GP calculations** - Pre-defined rewards  
❌ **Security** - Blockchain ensures integrity  

You just make HTTP requests and display JSON! 🚀

---

## 🎉 You're Ready!

1. Start server: `python3 server.py`
2. Import the API service
3. Make requests
4. Display data
5. Done! 🎊

**Questions?** Check the detailed docs above or test with curl commands first.

Happy coding! 💚🌍
