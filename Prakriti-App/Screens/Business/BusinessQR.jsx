import React, { useState } from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import QRCode from "react-native-qrcode-svg";

const BusinessQR = ({ navigation }) => {
    const insets = useSafeAreaInsets();
    const [mode, setMode] = useState("refill");

    const qrPayload = JSON.stringify({
        businessId: "DEMO-BUSINESS-123",
        action: mode,
        timestamp: Date.now(),
    });

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 6 }]}>

            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => navigation.goBack()}>
                    <Ionicons name="chevron-back" size={26} color="#2F5C39" />
                </Pressable>
                <Text style={styles.headerTitle}>Reward QR Code</Text>
                <Pressable onPress={() => navigation.navigate("Profile")}>
                    <Ionicons name="person-circle-outline" size={26} color="#2F5C39" />
                </Pressable>
            </View>

            <Text style={styles.caption}>
                Tourists scan this to earn <Text style={{ fontWeight: "700" }}>Green Points</Text> at your venue.
            </Text>

            {/* QR Container */}
            <View style={styles.qrCard}>
                <QRCode value={qrPayload} size={200} color="#23452F" backgroundColor="#FFFFFF" />
                <Text style={styles.qrFooter}>
                    Mode: <Text style={{ fontWeight: "800" }}>{mode}</Text>
                </Text>
            </View>

            <Text style={styles.modeTitle}>Select Reward Type</Text>

            <View style={styles.modeRow}>
                {[
                    { key: "refill", label: "Water Refill", icon: "water-outline" },
                    { key: "purchase", label: "Purchase", icon: "shopping-outline" },
                    { key: "eco-action", label: "Eco Action", icon: "leaf-circle-outline" },
                ].map((item) => (
                    <Pressable
                        key={item.key}
                        onPress={() => setMode(item.key)}
                        style={[styles.modeBtn, mode === item.key && styles.modeActive]}
                    >
                        <MaterialCommunityIcons
                            name={item.icon}
                            size={20}
                            color={mode === item.key ? "#FFFFFF" : "#2F5C39"}
                        />
                        <Text style={[styles.modeText, mode === item.key && styles.modeTextActive]}>
                            {item.label}
                        </Text>
                    </Pressable>
                ))}
            </View>

            <Text style={styles.note}>QR updates instantly when you change the type.</Text>

        </SafeAreaView>
    );
};

export default BusinessQR;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8", paddingHorizontal: 20 },

    header: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", marginBottom: 16 },
    headerTitle: { fontSize: 18, fontWeight: "800", color: "#2F5C39" },

    caption: { textAlign: "center", fontSize: 14, color: "#55655A", marginBottom: 16 },

    qrCard: {
        alignSelf: "center",
        backgroundColor: "#FFFFFF",
        padding: 24,
        borderRadius: 18,
        elevation: 5,
        shadowColor: "#000",
        shadowOpacity: 0.08,
        shadowRadius: 12,
        alignItems: "center",
        marginBottom: 20,
    },
    qrFooter: { marginTop: 10, fontSize: 13, color: "#4E5D52" },

    modeTitle: { fontSize: 15, fontWeight: "800", color: "#2F5C39", textAlign: "center", marginBottom: 12 },

    modeRow: { flexDirection: "row", justifyContent: "space-between" },

    modeBtn: {
        flex: 1,
        flexDirection: "row",
        gap: 6,
        alignItems: "center",
        justifyContent: "center",
        paddingVertical: 12,
        marginHorizontal: 4,
        borderRadius: 12,
        backgroundColor: "#E9F1EC",
    },
    modeActive: { backgroundColor: "#2F5C39" },

    modeText: { fontSize: 14, fontWeight: "600", color: "#2F5C39" },
    modeTextActive: { color: "#FFFFFF" },

    note: { textAlign: "center", marginTop: 14, fontSize: 12, color: "#77857B" },
});
