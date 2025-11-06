import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    Pressable,
    FlatList,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import MapView, { Marker } from "react-native-maps";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import Ionicons from "@expo/vector-icons/Ionicons";

const places = [
    {
        id: "1",
        name: "Himalayan Roots Café",
        distance: "600m",
        type: "Café",
        level: "Gold",
        tags: ["Refill Available", "Local Produce"],
        coords: { latitude: 32.2433, longitude: 77.1890 },
    },
    {
        id: "2",
        name: "Eco Refill Water Station - Mall Road",
        distance: "350m",
        type: "Refill Station",
        level: "Certified",
        tags: ["Free Refill", "Reduce Plastic"],
        coords: { latitude: 32.2438, longitude: 77.1905 },
    },
    {
        id: "3",
        name: "Pahadi Compost Hub",
        distance: "1.1 km",
        type: "Compost Point",
        level: "Silver",
        tags: ["Organic Waste Drop", "Community Run"],
        coords: { latitude: 32.2440, longitude: 77.1870 },
    },
];

const levelColor = {
    Gold: "#CFAA62",
    Silver: "#A4A9B6",
    Certified: "#2E5D3F",
};

const ExplorerScreen = () => {
    const [viewMode, setViewMode] = useState("map");

    return (
        <SafeAreaView style={styles.safe}>
            <View style={styles.header}>
                <Text style={styles.title}>Explore Green Places</Text>
                <Text style={styles.subtitle}>Himachal • Sustainable & Local</Text>
            </View>

            {/* Toggle */}
            <View style={styles.toggleRow}>
                <Pressable
                    onPress={() => setViewMode("map")}
                    style={[styles.toggleBtn, viewMode === "map" && styles.toggleActive]}
                >
                    <MaterialCommunityIcons
                        name="map"
                        size={18}
                        color={viewMode === "map" ? "#FFF" : "#2E5D3F"}
                    />
                    <Text style={[styles.toggleText, viewMode === "map" && styles.toggleTextActive]}>
                        Map
                    </Text>
                </Pressable>

                <Pressable
                    onPress={() => setViewMode("list")}
                    style={[styles.toggleBtn, viewMode === "list" && styles.toggleActive]}
                >
                    <MaterialCommunityIcons
                        name="view-list"
                        size={18}
                        color={viewMode === "list" ? "#FFF" : "#2E5D3F"}
                    />
                    <Text style={[styles.toggleText, viewMode === "list" && styles.toggleTextActive]}>
                        List
                    </Text>
                </Pressable>
            </View>

            {/* MAP VIEW */}
            {viewMode === "map" && (
                <MapView
                    style={styles.map}
                    initialRegion={{
                        latitude: places[0].coords.latitude,
                        longitude: places[0].coords.longitude,
                        latitudeDelta: 0.01,
                        longitudeDelta: 0.01,
                    }}
                >
                    {places.map((p) => (
                        <Marker key={p.id} coordinate={p.coords}>
                            <MaterialCommunityIcons name="map-marker" size={38} color="#2E5D3F" />
                        </Marker>
                    ))}
                </MapView>
            )}

            {/* LIST VIEW */}
            {viewMode === "list" && (
                <FlatList
                    data={places}
                    keyExtractor={(item) => item.id}
                    contentContainerStyle={{ padding: 20 }}
                    renderItem={({ item }) => (
                        <View style={styles.card}>
                            <View style={styles.cardHeaderRow}>
                                <Text style={styles.cardName}>{item.name}</Text>
                                <Text style={styles.cardDistance}>{item.distance}</Text>
                            </View>

                            <View style={[styles.levelTag, { borderColor: levelColor[item.level] }]}>
                                <Text style={[styles.levelText, { color: levelColor[item.level] }]}>
                                    {item.level} Stamp
                                </Text>
                            </View>

                            <View style={styles.tagRow}>
                                {item.tags.map((t, i) => (
                                    <View key={i} style={styles.tagChip}>
                                        <Text style={styles.tagText}>{t}</Text>
                                    </View>
                                ))}
                            </View>
                        </View>
                    )}
                />
            )}
        </SafeAreaView>
    );
};

export default ExplorerScreen;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F5F8F6" },

    header: { padding: 20 },
    title: { fontSize: 20, fontWeight: "800", color: "#2E5D3F" },
    subtitle: { fontSize: 13, color: "#6F7D75", marginTop: 4 },

    toggleRow: { flexDirection: "row", backgroundColor: "#E3ECE6", borderRadius: 10, marginHorizontal: 20 },
    toggleBtn: { flex: 1, alignItems: "center", flexDirection: "row", justifyContent: "center", paddingVertical: 8, gap: 6 },
    toggleActive: { backgroundColor: "#2E5D3F", borderRadius: 10 },
    toggleText: { color: "#2E5D3F", fontWeight: "700" },
    toggleTextActive: { color: "#FFF" },

    map: { flex: 1, marginTop: 12 },

    card: { backgroundColor: "#FFF", borderRadius: 12, padding: 16, marginBottom: 14, elevation: 3 },
    cardHeaderRow: { flexDirection: "row", justifyContent: "space-between" },
    cardName: { fontSize: 16, fontWeight: "700", color: "#1F2F25" },
    cardDistance: { fontSize: 13, color: "#55675F" },

    levelTag: { marginTop: 8, borderWidth: 1.3, alignSelf: "flex-start", borderRadius: 8, paddingHorizontal: 8, paddingVertical: 3 },
    levelText: { fontSize: 12, fontWeight: "700" },

    tagRow: { flexDirection: "row", flexWrap: "wrap", marginTop: 10 },
    tagChip: { backgroundColor: "#E7EFEA", paddingVertical: 4, paddingHorizontal: 10, borderRadius: 8, marginRight: 6, marginBottom: 6 },
    tagText: { fontSize: 12, fontWeight: "600", color: "#2E5D3F" },
});
