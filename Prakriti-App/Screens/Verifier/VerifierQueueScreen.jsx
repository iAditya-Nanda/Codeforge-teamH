import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    FlatList,
    Pressable,
} from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import Ionicons from "@expo/vector-icons/Ionicons";

const VerifierQueueScreen = ({ navigation }) => {
    const insets = useSafeAreaInsets();
    const [filter, setFilter] = useState("all");

    // Temporary Demo Data (Replace with DB later)
    const items = [
        {
            id: "a1",
            type: "tourist",
            title: "Plastic Bottle Sorted",
            location: "Cafe Mountain Root",
            timestamp: "2 min ago",
            image: "https://images.unsplash.com/photo-1581578017423-cf2f22004ce5"
        },
        {
            id: "b2",
            type: "business",
            title: "Blue Leaf Eco Café Applied for Stamp",
            location: "Old Manali, HP",
            timestamp: "1 hour ago",
            image: null
        },
        {
            id: "a3",
            type: "tourist",
            title: "Refill Bottle Action",
            location: "Sunrise Homestay",
            timestamp: "Today",
            image: null
        },
    ];

    const filtered = filter === "all" ? items : items.filter(i => i.type === filter);

    const renderItem = ({ item }) => (
        <Pressable
            onPress={() => navigation.navigate("VerifierDetail", { item })}
            style={({ pressed }) => [styles.card, pressed && { opacity: 0.95 }]}
        >
            <View style={styles.row}>
                <MaterialCommunityIcons
                    name={item.type === "tourist" ? "account-check-outline" : "storefront-outline"}
                    size={26}
                    color={item.type === "tourist" ? "#2F5C39" : "#B8860B"}
                />

                <View style={{ flex: 1 }}>
                    <Text style={styles.title}>{item.title}</Text>
                    <Text style={styles.subtitle}>{item.location}</Text>
                    <Text style={styles.time}>{item.timestamp}</Text>
                </View>

                <MaterialCommunityIcons name="chevron-right" size={22} color="#6A7D71" />
            </View>

            <Text style={[styles.tag, item.type === "tourist" ? styles.tagTourist : styles.tagBusiness]}>
                {item.type === "tourist" ? "Tourist Action" : "Business Request"}
            </Text>
        </Pressable>
    );

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 6 }]}>

            {/* Header */}
            <View style={styles.topBar}>
                <View style={{ flexDirection: "row", alignItems: "center", gap: 6 }}>
                    <MaterialCommunityIcons name="shield-account" size={20} color="#2F5C39" />
                    <Text style={styles.brand}>Prakriti Verifier</Text>
                </View>

                <Pressable onPress={() => navigation.navigate("VerifierProfile")}>
                    <Ionicons name="person-circle-outline" size={32} color="#2F5C39" />
                </Pressable>
            </View>

            {/* Filter Tabs */}
            <View style={styles.filterRow}>
                {[
                    { key: "all", label: "All" },
                    { key: "tourist", label: "Tourist Actions" },
                    { key: "business", label: "Business Requests" },
                ].map((tab) => (
                    <Pressable
                        key={tab.key}
                        onPress={() => setFilter(tab.key)}
                        style={[styles.filterBtn, filter === tab.key && styles.filterActive]}
                    >
                        <Text style={[styles.filterText, filter === tab.key && styles.filterTextActive]}>
                            {tab.label}
                        </Text>
                    </Pressable>
                ))}
            </View>

            {/* Pending List */}
            <FlatList
                data={filtered}
                keyExtractor={(i) => i.id}
                renderItem={renderItem}
                contentContainerStyle={{ paddingBottom: 40 }}
                showsVerticalScrollIndicator={false}
                style={{ marginTop: 10 }}
            />
        </SafeAreaView>
    );
};

export default VerifierQueueScreen;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8", paddingHorizontal: 20 },

    topBar: {
        height: 52,
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    brand: { fontSize: 18, fontWeight: "800", color: "#2F5C39" },

    filterRow: {
        flexDirection: "row",
        backgroundColor: "#E4EEE7",
        borderRadius: 12,
        padding: 4,
        marginTop: 14,
    },
    filterBtn: {
        flex: 1,
        paddingVertical: 8,
        borderRadius: 10,
        alignItems: "center",
    },
    filterActive: { backgroundColor: "#2F5C39" },
    filterText: { color: "#2F5C39", fontWeight: "600", fontSize: 12 },
    filterTextActive: { color: "#FFFFFF" },

    card: {
        backgroundColor: "#FFFFFF",
        borderRadius: 14,
        padding: 14,
        marginVertical: 6,
        elevation: 2,
    },
    row: { flexDirection: "row", alignItems: "center", gap: 10 },
    title: { fontWeight: "700", fontSize: 15, color: "#1E2D23" },
    subtitle: { fontSize: 12, color: "#6A7D71", marginTop: 2 },
    time: { fontSize: 11, color: "#9AA79F", marginTop: 4 },

    tag: {
        alignSelf: "flex-start",
        paddingHorizontal: 8,
        paddingVertical: 3,
        borderRadius: 8,
        fontSize: 11,
        fontWeight: "600",
        marginTop: 8,
    },
    tagTourist: { backgroundColor: "#E4F4E8", color: "#2F5C39" },
    tagBusiness: { backgroundColor: "#FFF4D6", color: "#B58B00" },
});
