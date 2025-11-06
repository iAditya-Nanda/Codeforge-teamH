import React from "react";
import {
    View,
    Text,
    StyleSheet,
    Pressable,
    Image,
    ScrollView
} from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

const ProfileScreen = ({ navigation }) => {
    const insets = useSafeAreaInsets();

    const handleLogout = () => {
        navigation.reset({
            index: 0,
            routes: [{ name: "Login" }],
        });
    };

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 6 }]}>
            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => navigation.goBack()}>
                    <MaterialCommunityIcons name="chevron-left" size={28} color="#2F5C39" />
                </Pressable>
                <Text style={styles.headerTitle}>Profile</Text>
                <View style={{ width: 28 }} />
            </View>

            <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 90 }}>

                {/* Profile Identity Card */}
                <View style={styles.profileCard}>
                    <Image
                        source={{ uri: "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y" }}
                        style={styles.avatar}
                    />
                    <Text style={styles.name}>Guest User</Text>
                    <Text style={styles.email}>demo@prakriti.app</Text>

                    <View style={styles.impactRow}>
                        <View style={styles.impactItem}>
                            <Text style={styles.impactValue}>120</Text>
                            <Text style={styles.impactLabel}>Green Points</Text>
                        </View>
                        <View style={styles.impactItem}>
                            <Text style={styles.impactValue}>6</Text>
                            <Text style={styles.impactLabel}>Actions Logged</Text>
                        </View>
                    </View>
                </View>

                {/* Action List */}
                <View style={styles.actionList}>
                    <ProfileRow
                        icon="pencil-outline"
                        label="Edit Profile"
                        onPress={() => {}}
                    />
                    <ProfileRow
                        icon="sparkles-outline"
                        label="Redeem Green Points"
                        onPress={() => navigation.navigate("RedeemPoints")}
                    />
                    <ProfileRow
                        icon="time-outline"
                        label="Activity History"
                        onPress={() => navigation.navigate("History")}
                    />
                    <ProfileRow
                        icon="information-outline"
                        label="About Prakriti"
                        onPress={() => {}}
                    />
                </View>
            </ScrollView>

            {/* Logout */}
            <Pressable style={styles.logoutBtn} onPress={handleLogout}>
                <Text style={styles.logoutText}>Logout</Text>
            </Pressable>
        </SafeAreaView>
    );
};

const ProfileRow = ({ icon, label, onPress }) => (
    <Pressable onPress={onPress} style={({ pressed }) => [styles.row, pressed && { opacity: 0.93 }]}>
        <Ionicons name={icon} size={22} color="#2F5C39" />
        <Text style={styles.rowLabel}>{label}</Text>
        <MaterialCommunityIcons name="chevron-right" size={22} color="#647367" />
    </Pressable>
);

export default ProfileScreen;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8" },

    header: {
        flexDirection: "row",
        alignItems: "center",
        paddingHorizontal: 18,
        paddingBottom: 10,
    },
    headerTitle: {
        flex: 1,
        textAlign: "center",
        fontSize: 18,
        fontWeight: "800",
        color: "#2F5C39",
    },

    profileCard: {
        alignItems: "center",
        backgroundColor: "#FFFFFF",
        margin: 18,
        paddingVertical: 26,
        borderRadius: 18,
        elevation: 2,
    },
    avatar: { width: 90, height: 90, borderRadius: 45, marginBottom: 12 },
    name: { fontSize: 20, fontWeight: "800", color: "#2F5C39" },
    email: { fontSize: 13, color: "#647367", marginTop: 4 },

    impactRow: {
        flexDirection: "row",
        marginTop: 20,
        justifyContent: "center",
        gap: 40,
    },
    impactItem: { alignItems: "center" },
    impactValue: { fontSize: 18, fontWeight: "800", color: "#2F5C39" },
    impactLabel: { fontSize: 12, color: "#647367", marginTop: 2 },

    actionList: {
        backgroundColor: "#FFFFFF",
        marginHorizontal: 18,
        borderRadius: 16,
        paddingVertical: 6,
        elevation: 2,
    },
    row: {
        flexDirection: "row",
        alignItems: "center",
        paddingVertical: 14,
        paddingHorizontal: 16,
    },
    rowLabel: { flex: 1, fontSize: 15, fontWeight: "600", color: "#213B27", marginLeft: 12 },

    logoutBtn: {
        position: "absolute",
        bottom: 20,
        alignSelf: "center",
        backgroundColor: "#C84040",
        paddingVertical: 12,
        paddingHorizontal: 34,
        borderRadius: 14,
    },
    logoutText: { color: "#FFF", fontWeight: "700", fontSize: 15 },
});
