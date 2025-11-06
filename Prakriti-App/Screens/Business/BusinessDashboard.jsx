import React from "react";
import { View, Text, StyleSheet, Pressable, Image } from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import Ionicons from "@expo/vector-icons/Ionicons";

const BusinessDashboard = ({ navigation }) => {
    const insets = useSafeAreaInsets();

    const businessName = "Blue Leaf Eco Café";
    const location = "Old Manali, Himachal Pradesh";
    const stampStatus = "pending"; // or "approved"

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 8 }]}>

            {/* Header */}
            <View style={styles.topBar}>
                <View style={styles.brandRow}>
                    <MaterialCommunityIcons name="leaf" size={22} color="#2F5C39" />
                    <Text style={styles.brand}>Prakriti Business</Text>
                </View>

                <Pressable onPress={() => navigation.navigate("Profile")}>
                    <Ionicons name="person-circle-outline" size={34} color="#2F5C39" />
                </Pressable>
            </View>

            {/* Hero Card */}
            <View style={styles.heroCard}>
                <Image
                    source={{ uri: "https://cdn-icons-png.flaticon.com/512/1046/1046857.png" }}
                    style={styles.avatar}
                />

                <View style={{ alignItems: "center" }}>
                    <Text style={styles.title}>{businessName}</Text>
                    <Text style={styles.subtitle}>{location}</Text>
                </View>

                <View style={[
                    styles.stampBadge,
                    stampStatus === "approved" ? styles.stampApproved : styles.stampPending
                ]}>
                    <MaterialCommunityIcons
                        name="check-decagram"
                        size={18}
                        color={stampStatus === "approved" ? "#FFFFFF" : "#B58B00"}
                    />
                    <Text style={[
                        styles.stampText,
                        stampStatus === "approved" ? { color: "#FFFFFF" } : { color: "#B58B00" }
                    ]}>
                        {stampStatus === "approved" ? "Green Stamp Certified" : "Awaiting Certification"}
                    </Text>
                </View>
            </View>

            {/* Metrics */}
            <View style={styles.metricsContainer}>
                <Metric label="Visitors" value="42" icon="account-group" />
                <Metric label="Points Issued" value="320" icon="ticket-percent" />
                <Metric label="Refills Given" value="58" icon="water" />
            </View>

            {/* Action Section */}
            <Text style={styles.sectionTitle}>Manage</Text>

            <View style={styles.actionGrid}>
                <ActionCard
                    label="Apply Certification"
                    icon="certificate-outline"
                    onPress={() => navigation.navigate("BusinessApplyStamp")}
                />
                <ActionCard
                    label="View Insights"
                    icon="chart-line"
                    onPress={() => navigation.navigate("BusinessInsights")}
                />
                <ActionCard
                    label="Generate QR"
                    icon="qrcode-scan"
                    onPress={() => navigation.navigate("BusinessQR")}
                />
            </View>

        </SafeAreaView>
    );
};

const Metric = ({ label, value, icon }) => (
    <View style={styles.metricCard}>
        <MaterialCommunityIcons name={icon} size={22} color="#23452F" />
        <Text style={styles.metricValue}>{value}</Text>
        <Text style={styles.metricLabel}>{label}</Text>
    </View>
);

const ActionCard = ({ label, icon, onPress }) => (
    <Pressable onPress={onPress} style={({ pressed }) => [styles.actionCard, pressed && { opacity: 0.9 }]}>
        <MaterialCommunityIcons name={icon} size={24} color="#2F5C39" />
        <Text style={styles.actionText}>{label}</Text>
    </Pressable>
);

export default BusinessDashboard;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F6F8F5", paddingHorizontal: 22 },

    topBar: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
    brandRow: { flexDirection: "row", alignItems: "center", gap: 6 },
    brand: { fontSize: 18, fontWeight: "800", color: "#2F5C39" },

    heroCard: {
        backgroundColor: "#FFFFFF",
        paddingVertical: 28,
        borderRadius: 20,
        marginTop: 26,
        alignItems: "center",
        shadowColor: "#000",
        shadowOpacity: 0.07,
        shadowRadius: 12,
        elevation: 3,
    },
    avatar: { width: 72, height: 72, borderRadius: 16, marginBottom: 12 },
    title: { fontSize: 19, fontWeight: "800", color: "#2F5C39" },
    subtitle: { fontSize: 13, color: "#5F6E64", marginTop: 2 },

    stampBadge: { flexDirection: "row", alignItems: "center", gap: 6, paddingHorizontal: 14, paddingVertical: 6, borderRadius: 12, marginTop: 16 },
    stampApproved: { backgroundColor: "#2F5C39" },
    stampPending: { backgroundColor: "#FFF2CC" },
    stampText: { fontSize: 13, fontWeight: "600" },

    metricsContainer: { flexDirection: "row", justifyContent: "space-between", marginTop: 30 },
    metricCard: { flex: 1, alignItems: "center", backgroundColor: "#FFFFFF", paddingVertical: 18, borderRadius: 16, marginHorizontal: 4, elevation: 2 },
    metricValue: { fontSize: 18, fontWeight: "800", color: "#2F5C39", marginTop: 4 },
    metricLabel: { fontSize: 12, color: "#63746B", marginTop: 2 },

    sectionTitle: { marginTop: 34, marginBottom: 12, fontSize: 15, fontWeight: "800", color: "#2F5C39" },

    actionGrid: { flexDirection: "row", justifyContent: "space-between" },
    actionCard: { flex: 1, backgroundColor: "#FFFFFF", borderRadius: 16, paddingVertical: 20, alignItems: "center", marginHorizontal: 4, elevation: 2 },
    actionText: { marginTop: 8, fontSize: 13, fontWeight: "700", color: "#2F5C39" },
});
