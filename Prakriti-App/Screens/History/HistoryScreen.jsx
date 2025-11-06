import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    Pressable,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import Ionicons from "@expo/vector-icons/Ionicons";

const ACTION_TYPES = [
    { label: "Waste Disposal", key: "waste", icon: "delete-sweep-outline" },
    { label: "Refill", key: "refill", icon: "water-outline" },
    { label: "Compost", key: "compost", icon: "leaf-circle-outline" },
    { label: "Reuse / Eco Shopping", key: "shopping", icon: "recycle" },
];

const HistoryScreen = () => {
    const [filter, setFilter] = useState("all");

    const history = [
        {
            type: "waste",
            title: "Plastic sorted correctly",
            location: "WasteHub Station – Sector 5",
            points: 12,
            time: "Today • 2:45 PM",
        },
        {
            type: "refill",
            title: "Bottle Refilled",
            location: "Blue Leaf Eco Café",
            points: 5,
            time: "Today • 12:18 PM",
        },
        {
            type: "compost",
            title: "Organic Waste Composted",
            location: "Green Compost Bin – Riverwalk",
            points: 8,
            time: "Yesterday • 5:52 PM",
        },
        {
            type: "shopping",
            title: "Purchased reusable travel cup",
            location: "Eco Market Corner",
            points: 10,
            time: "2 days ago • 3:15 PM",
        },
    ];

    const filteredHistory = filter === "all"
        ? history
        : history.filter(item => item.type === filter);

    // monthly progression mock
    const monthlyActions = history.length;
    const plasticSaved = 3.4; // placeholder — tie to backend later

    return (
        <SafeAreaView style={styles.safe}>
            <ScrollView
                contentContainerStyle={{ padding: 20, paddingBottom: 120 }}
                showsVerticalScrollIndicator={false}
            >
                {/* HEADER */}
                <Text style={styles.title}>Your Eco Journey</Text>
                <Text style={styles.subtitle}>Recognize your positive impact 🌱</Text>

                {/* PROGRESS SUMMARY */}
                <View style={styles.summaryCard}>
                    <View>
                        <Text style={styles.summaryValue}>{monthlyActions}</Text>
                        <Text style={styles.summaryLabel}>Actions This Month</Text>
                    </View>
                    <View>
                        <Text style={styles.summaryValue}>{plasticSaved}kg</Text>
                        <Text style={styles.summaryLabel}>Plastic Avoided</Text>
                    </View>
                </View>

                {/* FILTERS */}
                <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: 16 }}>
                    <Pressable
                        onPress={() => setFilter("all")}
                        style={[styles.filterChip, filter === "all" && styles.filterChipActive]}
                    >
                        <Text style={[styles.filterText, filter === "all" && styles.filterTextActive]}>All</Text>
                    </Pressable>

                    {ACTION_TYPES.map(({ key, label }) => (
                        <Pressable
                            key={key}
                            onPress={() => setFilter(key)}
                            style={[styles.filterChip, filter === key && styles.filterChipActive]}
                        >
                            <Text style={[styles.filterText, filter === key && styles.filterTextActive]}>
                                {label}
                            </Text>
                        </Pressable>
                    ))}
                </ScrollView>

                {/* HISTORY LIST */}
                <View style={{ marginTop: 22 }}>
                    {filteredHistory.map((item, index) => {
                        const icon = ACTION_TYPES.find(a => a.key === item.type)?.icon || "leaf-outline";
                        return (
                            <View key={index} style={styles.historyItem}>
                                <View style={styles.iconWrap}>
                                    <MaterialCommunityIcons name={icon} size={22} color="#2F5C39" />
                                </View>

                                <View style={{ flex: 1 }}>
                                    <Text style={styles.itemTitle}>{item.title}</Text>
                                    <Text style={styles.itemLocation}>{item.location}</Text>
                                    <Text style={styles.itemTime}>{item.time}</Text>
                                </View>

                                <View style={styles.pointsBadge}>
                                    <Text style={styles.pointsText}>+{item.points}</Text>
                                </View>
                            </View>
                        );
                    })}
                </View>
            </ScrollView>
        </SafeAreaView>
    );
};

export default HistoryScreen;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F8F8F8" },

    title: { fontSize: 22, fontWeight: "800", color: "#2F5C39" },
    subtitle: { fontSize: 14, color: "#55675A", marginTop: 4 },

    summaryCard: {
        marginTop: 18,
        backgroundColor: "#FFFFFF",
        borderRadius: 14,
        padding: 18,
        flexDirection: "row",
        justifyContent: "space-between",
        elevation: 3,
    },
    summaryValue: { fontSize: 22, fontWeight: "800", color: "#2F5C39" },
    summaryLabel: { fontSize: 12, color: "#5D6A61", marginTop: 2 },

    filterChip: {
        paddingHorizontal: 14,
        paddingVertical: 8,
        borderRadius: 20,
        backgroundColor: "#E7EFEA",
        marginRight: 8,
    },
    filterChipActive: { backgroundColor: "#2F5C39" },
    filterText: { color: "#2F5C39", fontWeight: "600", fontSize: 13 },
    filterTextActive: { color: "#FFFFFF" },

    historyItem: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "#FFFFFF",
        padding: 14,
        borderRadius: 12,
        marginBottom: 12,
        elevation: 2,
    },
    iconWrap: {
        width: 40, height: 40,
        borderRadius: 8,
        backgroundColor: "#EAF3ED",
        alignItems: "center",
        justifyContent: "center",
        marginRight: 14,
    },
    itemTitle: { fontSize: 15, fontWeight: "700", color: "#1F2F25" },
    itemLocation: { fontSize: 13, color: "#6C7D73" },
    itemTime: { fontSize: 12, color: "#88988F", marginTop: 4 },

    pointsBadge: {
        backgroundColor: "#2F5C39",
        borderRadius: 8,
        paddingVertical: 4,
        paddingHorizontal: 10,
    },
    pointsText: { color: "#FFFFFF", fontSize: 13, fontWeight: "700" },
});
