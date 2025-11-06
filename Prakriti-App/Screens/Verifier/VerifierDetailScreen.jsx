import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    Pressable,
    Image,
    Animated,
} from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

const VerifierDetailScreen = ({ route, navigation }) => {
    const insets = useSafeAreaInsets();
    const { item } = route.params; // { type, title, timestamp, image, location }
    const [mode, setMode] = useState("tap"); // tap | swipe | confirm
    const [translateX] = useState(new Animated.Value(0));

    const handleApprove = () => {
        console.log("APPROVED:", item);
        navigation.goBack();
    };

    const handleReject = () => {
        console.log("REJECTED:", item);
        navigation.goBack();
    };

    // Swipe mode behavior
    const startSwipe = (direction) => {
        Animated.timing(translateX, {
            toValue: direction === "right" ? 300 : -300,
            duration: 200,
            useNativeDriver: true,
        }).start(() => {
            direction === "right" ? handleApprove() : handleReject();
        });
    };

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 6 }]}>
            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => navigation.goBack()}>
                    <Ionicons name="chevron-back" size={26} color="#2F5C39" />
                </Pressable>
                <Text style={styles.headerTitle}>Review Submission</Text>
                <View style={{ width: 26 }} />
            </View>

            {/* Mode Selector */}
            <View style={styles.modeRow}>
                {[
                    { key: "tap", label: "Tap Mode" },
                    { key: "swipe", label: "Swipe Mode" },
                    { key: "confirm", label: "Confirm Mode" },
                ].map((m) => (
                    <Pressable
                        key={m.key}
                        onPress={() => setMode(m.key)}
                        style={[styles.modeBtn, mode === m.key && styles.modeActive]}
                    >
                        <Text style={[styles.modeText, mode === m.key && styles.modeTextActive]}>
                            {m.label}
                        </Text>
                    </Pressable>
                ))}
            </View>

            {/* Card Content */}
            <Animated.View style={[styles.card, mode === "swipe" && { transform: [{ translateX }] }]}>
                {item.image && <Image source={{ uri: item.image }} style={styles.image} />}

                <Text style={styles.title}>{item.title}</Text>
                <Text style={styles.location}>{item.location}</Text>
                <Text style={styles.info}>Submitted: {item.timestamp}</Text>
            </Animated.View>

            {/* Mode: TAP Mode (Fast) */}
            {mode === "tap" && (
                <View style={styles.buttonRow}>
                    <Pressable onPress={handleReject} style={[styles.actionBtn, styles.reject]}>
                        <MaterialCommunityIcons name="close" size={20} color="#FFF" />
                        <Text style={styles.btnText}>Reject</Text>
                    </Pressable>

                    <Pressable onPress={handleApprove} style={[styles.actionBtn, styles.approve]}>
                        <MaterialCommunityIcons name="check" size={20} color="#FFF" />
                        <Text style={styles.btnText}>Approve</Text>
                    </Pressable>
                </View>
            )}

            {/* Mode: SWIPE Mode */}
            {mode === "swipe" && (
                <View style={styles.swipeHint}>
                    <Text style={styles.hintText}>Swipe Right to Approve — Swipe Left to Reject</Text>
                </View>
            )}

            {/* Mode: CONFIRMATION Mode */}
            {mode === "confirm" && (
                <View style={styles.confirmContainer}>
                    <Pressable onPress={handleApprove} style={[styles.confirmBtn, styles.approve]}>
                        <Text style={styles.btnText}>Approve (Confirm)</Text>
                    </Pressable>

                    <Pressable onPress={handleReject} style={[styles.confirmBtn, styles.reject]}>
                        <Text style={styles.btnText}>Reject (Confirm)</Text>
                    </Pressable>
                </View>
            )}
        </SafeAreaView>
    );
};

export default VerifierDetailScreen;

// ------------------------ Styles ------------------------

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8", paddingHorizontal: 20 },

    header: {
        height: 52,
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
    },
    headerTitle: { fontSize: 18, fontWeight: "800", color: "#2F5C39" },

    modeRow: {
        flexDirection: "row",
        backgroundColor: "#E4EEE7",
        borderRadius: 12,
        padding: 4,
        marginTop: 16,
    },
    modeBtn: {
        flex: 1,
        paddingVertical: 8,
        borderRadius: 10,
        alignItems: "center",
    },
    modeActive: { backgroundColor: "#2F5C39" },
    modeText: { color: "#2F5C39", fontSize: 12, fontWeight: "600" },
    modeTextActive: { color: "#FFFFFF" },

    card: {
        backgroundColor: "#FFFFFF",
        borderRadius: 16,
        marginTop: 20,
        padding: 16,
        elevation: 3,
        alignItems: "center",
    },
    image: { width: "100%", height: 180, borderRadius: 12, marginBottom: 14 },
    title: { fontSize: 17, fontWeight: "700", color: "#23412A" },
    location: { fontSize: 13, color: "#6A7A6F", marginTop: 2 },
    info: { fontSize: 12, color: "#88968C", marginTop: 8 },

    buttonRow: { flexDirection: "row", justifyContent: "space-between", marginTop: 30 },
    actionBtn: {
        flex: 1,
        paddingVertical: 14,
        borderRadius: 12,
        flexDirection: "row",
        justifyContent: "center",
        gap: 8,
    },
    approve: { backgroundColor: "#2F5C39", marginLeft: 6 },
    reject: { backgroundColor: "#B34040", marginRight: 6 },
    btnText: { color: "#FFF", fontWeight: "700", fontSize: 14 },

    swipeHint: { alignItems: "center", marginTop: 20 },
    hintText: { color: "#6D7D72", fontSize: 12 },

    confirmContainer: { marginTop: 30, gap: 12 },
    confirmBtn: { borderRadius: 12, paddingVertical: 14, alignItems: "center" },
});
