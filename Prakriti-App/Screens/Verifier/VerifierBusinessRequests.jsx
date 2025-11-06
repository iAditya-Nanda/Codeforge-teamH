import React, { useState } from "react";
import { View, Text, StyleSheet, FlatList, Pressable } from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import Ionicons from "@expo/vector-icons/Ionicons";

const VerifierBusinessRequests = ({ navigation }) => {
    const insets = useSafeAreaInsets();

    const [requests, setRequests] = useState([
        {
            id: "1",
            name: "Blue Leaf Eco Café",
            location: "Old Manali",
            type: "Café",
        },
        {
            id: "2",
            name: "Eco Trek Supplies Store",
            location: "Kasol",
            type: "Retail Shop",
        },
    ]);

    const handleDecision = (id, approved) => {
        setRequests((prev) => prev.filter((r) => r.id !== id));
        // TODO: push update to server
    };

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 6 }]}>
            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => navigation.goBack()}>
                    <Ionicons name="chevron-back" size={26} color="#2F5C39" />
                </Pressable>
                <Text style={styles.headerTitle}>Business Stamp Requests</Text>
                <View style={{ width: 26 }} />
            </View>

            <FlatList
                data={requests}
                keyExtractor={(item) => item.id}
                contentContainerStyle={{ paddingVertical: 12 }}
                renderItem={({ item }) => (
                    <View style={styles.card}>
                        <MaterialCommunityIcons name="storefront-outline" size={28} color="#2F5C39" />
                        <View style={{ flex: 1 }}>
                            <Text style={styles.name}>{item.name}</Text>
                            <Text style={styles.sub}>{item.location} • {item.type}</Text>
                        </View>

                        <View style={styles.actionButtons}>
                            <Pressable
                                onPress={() => handleDecision(item.id, true)}
                                style={[styles.btn, styles.approve]}
                            >
                                <Text style={styles.btnTextApprove}>Approve</Text>
                            </Pressable>

                            <Pressable
                                onPress={() => handleDecision(item.id, false)}
                                style={[styles.btn, styles.reject]}
                            >
                                <Text style={styles.btnTextReject}>Reject</Text>
                            </Pressable>
                        </View>
                    </View>
                )}
                ListEmptyComponent={
                    <View style={styles.emptyBox}>
                        <MaterialCommunityIcons name="check" size={28} color="#2F5C39" />
                        <Text style={styles.emptyText}>No pending requests right now.</Text>
                    </View>
                }
            />
        </SafeAreaView>
    );
};

export default VerifierBusinessRequests;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8", paddingHorizontal: 20 },

    header: { flexDirection: "row", alignItems: "center", marginBottom: 8 },
    headerTitle: { flex: 1, textAlign: "center", fontSize: 18, fontWeight: "800", color: "#2F5C39" },

    card: {
        backgroundColor: "#FFFFFF",
        borderRadius: 14,
        padding: 14,
        marginBottom: 12,
        flexDirection: "row",
        alignItems: "center",
        gap: 12,
        elevation: 2,
    },
    name: { fontSize: 15, fontWeight: "700", color: "#1F3326" },
    sub: { fontSize: 13, color: "#667569" },

    actionButtons: { flexDirection: "row", gap: 6 },
    btn: { borderRadius: 10, paddingVertical: 6, paddingHorizontal: 12 },

    approve: { backgroundColor: "#2F5C39" },
    reject: { backgroundColor: "#FFF0F0", borderWidth: 1, borderColor: "#C63F3F66" },

    btnTextApprove: { color: "#FFFFFF", fontWeight: "700", fontSize: 13 },
    btnTextReject: { color: "#C63F3F", fontWeight: "700", fontSize: 13 },

    emptyBox: { marginTop: 60, alignItems: "center" },
    emptyText: { marginTop: 8, color: "#55645D", fontSize: 14 },
});
