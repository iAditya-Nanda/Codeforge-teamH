
import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    Pressable,
    FlatList,
    ScrollView,
} from "react-native";
import MapView, { Marker } from "react-native-maps";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import Ionicons from "@expo/vector-icons/Ionicons";

const refillStations = [
    {
        id: "1",
        name: "Eco Refill Tap - Mall Road",
        distance: "350m",
        status: "Available",
        coords: { latitude: 32.2438, longitude: 77.1905 },
    },
    {
        id: "2",
        name: "Forest Trails Refill Hut",
        distance: "780m",
        status: "Low Pressure",
        coords: { latitude: 32.2445, longitude: 77.1885 },
    },
    {
        id: "3",
        name: "Himalayan Café - Free Water Refill",
        distance: "1.4 km",
        status: "Available",
        coords: { latitude: 32.2431, longitude: 77.1925 },
    },
];

const statusColor = {
    Available: "#2F5C39",
    "Low Pressure": "#CFAA62",
};

const RefillStationsScreen = ({ navigation }) => {
    const insets = useSafeAreaInsets();
    const [mode, setMode] = useState("map"); // map | list

    return (
        <SafeAreaView style={[styles.safe, { paddingBottom: insets.bottom || 16 }]}>
            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => navigation.goBack()}>
                    <MaterialCommunityIcons name="close" size={26} color="#2F5C39" />
                </Pressable>

                <Text style={styles.title}>Refill Water Stations</Text>
                <View style={{ width: 26 }} /> {/* Symmetry */}
            </View>

            <Text style={styles.subtitle}>Reduce plastic. Carry & refill your bottle 🌿</Text>

            {/* Toggle */}
            <View style={styles.toggleRow}>
                <Pressable
                    onPress={() => setMode("map")}
                    style={[styles.toggleBtn, mode === "map" && styles.toggleActive]}
                >
                    <Ionicons name="map-outline" size={18} color={mode === "map" ? "#FFF" : "#2F5C39"} />
                    <Text style={[styles.toggleText, mode === "map" && styles.toggleTextActive]}>
                        Map View
                    </Text>
                </Pressable>

                <Pressable
                    onPress={() => setMode("list")}
                    style={[styles.toggleBtn, mode === "list" && styles.toggleActive]}
                >
                    <Ionicons name="list-outline" size={18} color={mode === "list" ? "#FFF" : "#2F5C39"} />
                    <Text style={[styles.toggleText, mode === "list" && styles.toggleTextActive]}>
                        List View
                    </Text>
                </Pressable>
            </View>

            {/* MAP VIEW */}
            {mode === "map" && (
                <MapView
                    style={styles.map}
                    initialRegion={{
                        latitude: refillStations[0].coords.latitude,
                        longitude: refillStations[0].coords.longitude,
                        latitudeDelta: 0.01,
                        longitudeDelta: 0.01,
                    }}
                >
                    {refillStations.map((s) => (
                        <Marker key={s.id} coordinate={s.coords}>
                            <MaterialCommunityIcons name="water" size={36} color="#2F5C39" />
                        </Marker>
                    ))}
                </MapView>
            )}

            {/* LIST VIEW */}
            {mode === "list" && (
                <FlatList
                    data={refillStations}
                    keyExtractor={(i) => i.id}
                    contentContainerStyle={{ padding: 20 }}
                    renderItem={({ item }) => (
                        <View style={styles.card}>
                            <View style={styles.cardHeader}>
                                <Text style={styles.cardName}>{item.name}</Text>
                                <Text style={styles.cardDistance}>{item.distance}</Text>
                            </View>

                            <View style={[styles.statusTag, { borderColor: statusColor[item.status] }]}>
                                <Text style={[styles.statusText, { color: statusColor[item.status] }]}>
                                    {item.status}
                                </Text>
                            </View>
                        </View>
                    )}
                />
            )}
        </SafeAreaView>
    );
};

export default RefillStationsScreen;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8" },

    header: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        paddingHorizontal: 18,
        marginTop: 8,
    },
    title: { fontSize: 18, fontWeight: "800", color: "#2F5C39" },
    subtitle: { textAlign: "center", marginTop: 4, fontSize: 13, color: "#647367" },

    toggleRow: {
        flexDirection: "row",
        backgroundColor: "#E4EFE7",
        borderRadius: 12,
        marginHorizontal: 20,
        marginTop: 14,
    },
    toggleBtn: {
        flex: 1,
        paddingVertical: 8,
        flexDirection: "row",
        justifyContent: "center",
        alignItems: "center",
        gap: 6,
    },
    toggleActive: { backgroundColor: "#2F5C39", borderRadius: 12 },
    toggleText: { color: "#2F5C39", fontWeight: "700" },
    toggleTextActive: { color: "#FFF" },

    map: { flex: 1, marginTop: 12 },

    card: {
        backgroundColor: "#FFFFFF",
        padding: 14,
        borderRadius: 14,
        marginBottom: 14,
        elevation: 3,
    },
    cardHeader: { flexDirection: "row", justifyContent: "space-between" },
    cardName: { fontSize: 15, color: "#203B2A", fontWeight: "700" },
    cardDistance: { fontSize: 13, color: "#55675F" },

    statusTag: {
        marginTop: 10,
        alignSelf: "flex-start",
        paddingVertical: 4,
        paddingHorizontal: 10,
        borderWidth: 1.4,
        borderRadius: 10,
    },
    statusText: { fontWeight: "700", fontSize: 12 },
});
