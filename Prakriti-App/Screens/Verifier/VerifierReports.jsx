import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

const VerifierReports = ({ navigation }) => {
    const insets = useSafeAreaInsets();

    // Temporary values (replace with API later)
    const stats = {
        verifiedActions: 148,
        certifiedBusinesses: 9,
        plasticDivertedKg: 42.7,
    };

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 6 }]}>

            {/* Header */}
            <View style={styles.header}>
                <Ionicons name="chevron-back" size={26} color="#2F5C39" onPress={() => navigation.goBack()} />
                <Text style={styles.headerTitle}>Verified Impact</Text>
                <View style={{ width: 26 }} />
            </View>

            <View style={styles.card}>
                <MaterialCommunityIcons name="recycle" size={38} color="#2F5C39" />
                <Text style={styles.big}>{stats.verifiedActions}</Text>
                <Text style={styles.label}>Eco Actions Verified</Text>
            </View>

            <View style={styles.row}>
                <SmallStat value={stats.certifiedBusinesses} label="Businesses Certified" icon="store-check" />
                <SmallStat value={stats.plasticDivertedKg + " kg"} label="Plastic Diverted" icon="bottle-tonic-outline" />
            </View>

            <Text style={styles.note}>
                These numbers reflect the positive environmental impact validated through your work.
            </Text>

        </SafeAreaView>
    );
};

const SmallStat = ({ value, label, icon }) => (
    <View style={styles.smallCard}>
        <MaterialCommunityIcons name={icon} size={28} color="#2F5C39" />
        <Text style={styles.smallValue}>{value}</Text>
        <Text style={styles.smallLabel}>{label}</Text>
    </View>
);

export default VerifierReports;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8", paddingHorizontal: 20 },

    header: { flexDirection: "row", alignItems: "center", marginBottom: 18 },
    headerTitle: { flex: 1, textAlign: "center", fontSize: 18, fontWeight: "800", color: "#2F5C39" },

    card: {
        backgroundColor: "#FFFFFF",
        borderRadius: 18,
        alignItems: "center",
        paddingVertical: 28,
        elevation: 3,
    },
    big: { fontSize: 40, fontWeight: "900", color: "#2F5C39", marginTop: 10 },
    label: { fontSize: 14, color: "#607066", marginTop: 4 },

    row: { flexDirection: "row", gap: 12, marginTop: 20 },
    smallCard: {
        flex: 1,
        backgroundColor: "#FFFFFF",
        borderRadius: 14,
        paddingVertical: 20,
        alignItems: "center",
        elevation: 2,
    },
    smallValue: { fontSize: 20, fontWeight: "800", color: "#2F5C39", marginTop: 6 },
    smallLabel: { fontSize: 12, color: "#607066", marginTop: 2 },

    note: { marginTop: 24, fontSize: 13, color: "#4F5C52", textAlign: "center" },
});
