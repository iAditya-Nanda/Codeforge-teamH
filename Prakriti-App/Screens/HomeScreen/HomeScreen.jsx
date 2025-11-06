import React, { useMemo } from "react";
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    Pressable,
    TextInput,
    useWindowDimensions,
    Platform,
} from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

const G = { xs: 6, sm: 10, md: 12, lg: 16, xl: 20 };

const HomeScreen = ({ navigation }) => {
    const insets = useSafeAreaInsets();
    const { width } = useWindowDimensions();

    const cardGap = 12;
    const hPad = G.xl;
    const cardWidth = useMemo(() => Math.min(width - hPad * 2, 520), [width]);

    const prompts = [
        "Blue Leaf Eco Café nearby—refill to avoid 1–2 bottles.",
        "Walk short hops today—cut CO₂ and breathe easier.",
        "Green Market Corner: refills + low-waste gifts.",
    ];

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top || G.lg }]}>
            {/* TOP BAR: Brand + Points micro-badge */}
            <View style={[styles.topBar, { paddingHorizontal: G.xl }]}>
                <View style={styles.brandRow}>
                    <MaterialCommunityIcons name="leaf" size={20} color="#2F5C39" />
                    <Text style={styles.brand}>Prakriti</Text>
                </View>

                <View style={{ flexDirection: "row", alignItems: "center", gap: 10 }}>
                    <Pressable
                        onPress={() => navigation.navigate("RedeemPoints")}
                        style={styles.pointsPill}
                    >
                        <Ionicons name="sparkles-outline" size={14} color="#2F5C39" />
                        <Text style={styles.pointsText}>120</Text>
                    </Pressable>

                    <Pressable onPress={() => navigation.navigate("Profile")}>
                        <Ionicons name="person-circle-outline" size={30} color="#2F5C39" />
                    </Pressable>
                </View>
            </View>

            <ScrollView
                showsVerticalScrollIndicator={false}
                contentContainerStyle={{
                    paddingHorizontal: G.xl,
                    paddingBottom: (insets.bottom || 12) + 88,
                }}
            >
                {/* PRIMARY ACTIONS: QR + Scan Trash AI */}
                <View style={styles.primaryRow}>
                    <Pressable
                        onPress={() => navigation.navigate("Scan")}
                        style={({ pressed }) => [
                            styles.primaryCard,
                            pressed && styles.pressed,
                        ]}
                    >
                        <View style={styles.primaryIconBadge}>
                            <MaterialCommunityIcons name="qrcode-scan" size={22} color="#fff" />
                        </View>
                        <Text style={styles.primaryTitle}>Scan QR</Text>
                        <Text style={styles.primarySub}>Record eco action fast</Text>
                    </Pressable>

                    <Pressable
                        onPress={() => navigation.navigate("HowToDispose")}
                        style={({ pressed }) => [
                            styles.primaryCard,
                            pressed && styles.pressed,
                        ]}
                    >
                        <View style={[styles.primaryIconBadge, { backgroundColor: "#23412A" }]}>
                            <MaterialCommunityIcons name="delete-sweep-outline" size={22} color="#fff" />
                        </View>
                        <Text style={styles.primaryTitle}>Scan Trash (AI)</Text>
                        <Text style={styles.primarySub}>Identify & sort correctly</Text>
                    </Pressable>
                </View>

                {/* AI COPILOT: compact prompt + chips */}
                <View style={styles.aiBlock}>
                    <View style={styles.aiHeader}>
                        <MaterialCommunityIcons name="robot-happy-outline" size={18} color="#2F5C39" />
                        <Text style={styles.aiTitle}>Prakriti AI Copilot</Text>
                    </View>

                    <View style={styles.aiRow}>
                        <Pressable
                            style={styles.aiFakeInput}
                            onPress={() => navigation.navigate("AIChatIntro")}
                        >
                            <Text style={styles.aiFakeInputText}>Ask how to dispose… e.g., coffee cup lid</Text>
                        </Pressable>

                        <Pressable
                            onPress={() => navigation.navigate("AIChatIntro")}
                            style={styles.aiSend}
                        >
                            <Ionicons name="chatbubble-ellipses-outline" size={16} color="#FFF" />
                        </Pressable>
                    </View>

                    <View style={styles.chipsRow}>
                        {["Plastic bottle", "Food box", "Coffee lid", "Wet waste"].map((query) => (
                            <Pressable
                                key={query}
                                onPress={() =>
                                    navigation.navigate("AIChatThread", { initialMessage: query })
                                }
                                style={styles.chip}
                            >
                                <Text style={styles.chipText}>{query}</Text>
                            </Pressable>
                        ))}
                    </View>
                </View>

                {/* MICRO PROMPTS CAROUSEL (tight) */}
                <Text style={styles.sectionTitle}>Suggestions</Text>
                <ScrollView
                    horizontal
                    showsHorizontalScrollIndicator={false}
                    snapToAlignment="center"
                    decelerationRate={Platform.OS === "ios" ? "fast" : 0.98}
                    snapToInterval={cardWidth + cardGap}
                    contentContainerStyle={{ paddingRight: G.xl - cardGap }}
                    style={{ marginBottom: G.lg }}
                >
                    {prompts.map((msg, i) => (
                        <View
                            key={`p-${i}`}
                            style={[styles.promptCard, { width: cardWidth, marginRight: i === prompts.length - 1 ? 0 : cardGap }]}
                        >
                            <Text style={styles.promptText}>{msg}</Text>
                        </View>
                    ))}
                </ScrollView>

                {/* WASTE ACTION CENTER: crisp 2-col with most-used */}
                <Text style={styles.sectionTitle}>Waste Action Center</Text>
                <View style={styles.grid}>
                    <GridItem
                        icon="recycle"
                        label="How to Dispose?"
                        onPress={() => navigation.navigate("HowToDispose")}
                    />
                    <GridItem
                        icon="water-outline"
                        label="Refill Stations"
                        onPress={() => navigation.navigate("RefillStations")}
                    />
                    <GridItem
                        icon="leaf-circle-outline"
                        label="Compost Points"
                        onPress={() => navigation.navigate("CompostPoints")}
                    />
                    <GridItem
                        icon="alert-octagon-outline"
                        label="Report Litter"
                        onPress={() => navigation.navigate("ReportLitter")}
                        accent
                    />
                </View>
                {/* FULL-WIDTH DISPOSAL CTA */}
                <Pressable
                    onPress={() => navigation.navigate("HowToDispose")}
                    style={({ pressed }) => [
                        styles.disposalCTA,
                        pressed && { opacity: 0.9, transform: [{ scale: 0.995 }] },
                    ]}
                >
                    <MaterialCommunityIcons name="trash-can-outline" size={20} color="#FFFFFF" />
                    <Text style={styles.disposalCTAText}>Have trash? Dispose properly</Text>
                </Pressable>


                {/* MAP CTA */}
                <Pressable
                    onPress={() => navigation.navigate("Explorer")}
                    style={({ pressed }) => [styles.mapCTA, pressed && styles.mapPressed]}
                >
                    <Ionicons name="map-outline" size={18} color="#2F5C39" />
                    <Text style={styles.mapText}>View Green Places Map</Text>
                </Pressable>
            </ScrollView>
        </SafeAreaView>
    );
};

/** ——— Small, focused grid item ——— */
const GridItem = ({ icon, label, onPress, accent }) => (
    <Pressable onPress={onPress} style={({ pressed }) => [styles.gridItem, pressed && styles.pressed, accent && styles.gridAccent]}>
        <MaterialCommunityIcons name={icon} size={22} color={accent ? "#C63F3F" : "#2F5C39"} />
        <Text style={[styles.gridText, accent && { color: "#C63F3F" }]}>{label}</Text>
    </Pressable>
);

export default HomeScreen;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8" },

    // Top bar
    topBar: { height: 48, alignItems: "center", flexDirection: "row", justifyContent: "space-between" },
    brandRow: { flexDirection: "row", alignItems: "center", gap: 6 },
    brand: { fontSize: 18, fontWeight: "800", color: "#2F5C39", letterSpacing: 0.2 },
    pointsPill: {
        flexDirection: "row", alignItems: "center", gap: 6,
        backgroundColor: "#EAF3ED", paddingHorizontal: 10, height: 30, borderRadius: 16,
    },
    pointsText: { color: "#2F5C39", fontWeight: "800", fontSize: 13 },

    // Primary pair
    primaryRow: { flexDirection: "row", gap: 12, marginTop: 10, marginBottom: 14 },
    primaryCard: {
        flex: 1,
        backgroundColor: "#FFFFFF",
        borderRadius: 14,
        paddingVertical: 14,
        paddingHorizontal: 12,
        elevation: 3,
    },
    pressed: { opacity: 0.92, transform: [{ scale: 0.997 }] },
    primaryIconBadge: {
        width: 36, height: 36, borderRadius: 10, backgroundColor: "#2F5C39",
        alignItems: "center", justifyContent: "center",
    },
    primaryTitle: { marginTop: 10, fontSize: 16, fontWeight: "800", color: "#213B27" },
    primarySub: { marginTop: 2, fontSize: 12, color: "#5C6B61" },

    // AI block
    aiBlock: { backgroundColor: "#FFFFFF", borderRadius: 14, padding: 12, elevation: 3, marginBottom: 14 },
    aiHeader: { flexDirection: "row", alignItems: "center", gap: 8, marginBottom: 8 },
    aiTitle: { fontSize: 14, fontWeight: "800", color: "#2F5C39" },
    aiRow: { flexDirection: "row", alignItems: "center", gap: 8 },
    aiInput: {
        flex: 1, height: 42, borderRadius: 10, paddingHorizontal: 12, fontSize: 14,
        backgroundColor: "#F1F5F3", color: "#1F2A22",
    },
    chipsRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 10 },
    chip: { paddingHorizontal: 10, height: 30, borderRadius: 16, backgroundColor: "#EAF3ED", justifyContent: "center" },
    chipText: { color: "#2F5C39", fontWeight: "700", fontSize: 12 },

    // Suggestions
    sectionTitle: { fontSize: 14, fontWeight: "800", color: "#1E3324", marginBottom: 8, marginTop: 2 },
    promptCard: { backgroundColor: "#FFFFFF", borderRadius: 12, padding: 12, elevation: 2 },
    promptText: { fontSize: 13, lineHeight: 18, color: "#34443A" },

    // Grid
    grid: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginBottom: 10, marginTop: 2 },
    gridItem: {
        width: "48%",
        backgroundColor: "#FFFFFF",
        borderRadius: 12,
        paddingVertical: 14,
        alignItems: "center",
        elevation: 2,
    },
    gridAccent: { borderWidth: 1.2, borderColor: "#C63F3F22", backgroundColor: "#FFF8F8" },
    gridText: { marginTop: 6, fontSize: 13, fontWeight: "700", color: "#2F5C39", textAlign: "center" },

    // Map CTA
    mapCTA: {
        alignSelf: "center",
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
        backgroundColor: "#EAF3ED",
        paddingVertical: 10,
        paddingHorizontal: 14,
        borderRadius: 12,
    },
    mapPressed: { opacity: 0.9, transform: [{ scale: 0.997 }] },
    mapText: { color: "#2F5C39", fontWeight: "800", fontSize: 14 },
    disposalCTA: {
        marginTop: 14,
        marginBottom: 20,
        borderRadius: 14,
        backgroundColor: "#2F5C39",
        paddingVertical: 14,
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        gap: 10,
        elevation: 3,
    },
    disposalCTAText: {
        color: "#FFFFFF",
        fontSize: 15,
        fontWeight: "700",
    },
    aiFakeInput: {
        flex: 1,
        height: 42,
        borderRadius: 10,
        paddingHorizontal: 12,
        justifyContent: "center",
        backgroundColor: "#F1F5F3",
    },
    aiFakeInputText: {
        color: "#6E7C71",
        fontSize: 14,
    },

    aiSend: {
        width: 42,
        height: 42,
        borderRadius: 10,
        backgroundColor: "#2F5C39",
        alignItems: "center",
        justifyContent: "center",
    },

});
