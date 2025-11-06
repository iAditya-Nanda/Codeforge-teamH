import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    Pressable,
    ScrollView,
    Dimensions,
} from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import Ionicons from "@expo/vector-icons/Ionicons";
import Svg, { Circle, Path } from "react-native-svg";

// Demo Data (replace with API later)
const visitsData = [2, 5, 8, 12, 10, 15, 18, 20];
const refills = 58;
const pointsIssued = 320;
const visitors = 42;

// Small sparkline generator (no external chart lib)
const generatePath = (data, w, h) => {
    const max = Math.max(...data);
    const step = w / (data.length - 1);
    return data
        .map((val, i) => {
            const x = i * step;
            const y = h - (val / max) * h;
            return `${i === 0 ? "M" : "L"} ${x} ${y}`;
        })
        .join(" ");
};

const BusinessInsights = ({ navigation }) => {
    const insets = useSafeAreaInsets();
    const size = 130;
    const stroke = 10;
    const radius = (size - stroke) / 2;
    const circumference = 2 * Math.PI * radius;
    const progress = 0.65; // 65% progress toward certification goal

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 6 }]}>

            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => navigation.goBack()}>
                    <Ionicons name="chevron-back" size={26} color="#2F5C39" />
                </Pressable>
                <Text style={styles.headerTitle}>Business Insights</Text>
                <View style={{ width: 26 }} />
            </View>

            <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 120 }}>

                {/* Metric Tiles */}
                <View style={styles.tilesRow}>
                    <Tile label="Visitors" value={visitors} />
                    <Tile label="Points Issued" value={pointsIssued} />
                    <Tile label="Refills" value={refills} />
                </View>

                {/* Sparkline Trend */}
                <Text style={styles.sectionTitle}>Visitor Growth (Last 7 Days)</Text>
                <View style={styles.chartBox}>
                    <Svg width="100%" height="80">
                        <Path
                            d={generatePath(visitsData, Dimensions.get("window").width - 60, 70)}
                            stroke="#2F5C39"
                            strokeWidth="3"
                            fill="none"
                        />
                    </Svg>
                </View>

                {/* Certification Progress Ring */}
                <Text style={styles.sectionTitle}>Progress Toward Green Stamp</Text>
                <View style={styles.progressContainer}>
                    <Svg width={size} height={size}>
                        <Circle
                            cx={size / 2}
                            cy={size / 2}
                            r={radius}
                            stroke="#DDE7E1"
                            strokeWidth={stroke}
                            fill="none"
                        />
                        <Circle
                            cx={size / 2}
                            cy={size / 2}
                            r={radius}
                            stroke="#2F5C39"
                            strokeWidth={stroke}
                            strokeDasharray={circumference}
                            strokeDashoffset={circumference - progress * circumference}
                            strokeLinecap="round"
                            fill="none"
                            rotation="-90"
                            origin={`${size / 2}, ${size / 2}`}
                        />
                    </Svg>
                    <Text style={styles.progressText}>{Math.round(progress * 100)}%</Text>
                </View>

                <Text style={styles.progressCaption}>
                    You're close to earning your **Green Stamp**. Keep improving your refill and waste practices!
                </Text>

            </ScrollView>
        </SafeAreaView>
    );
};

const Tile = ({ value, label }) => (
    <View style={styles.tile}>
        <Text style={styles.tileValue}>{value}</Text>
        <Text style={styles.tileLabel}>{label}</Text>
    </View>
);

export default BusinessInsights;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8", paddingHorizontal: 20 },

    header: { flexDirection: "row", alignItems: "center", marginBottom: 10 },
    headerTitle: { flex: 1, textAlign: "center", fontSize: 18, fontWeight: "800", color: "#2F5C39" },

    tilesRow: { flexDirection: "row", justifyContent: "space-between", marginTop: 20 },
    tile: {
        flex: 1,
        backgroundColor: "#FFFFFF",
        paddingVertical: 14,
        borderRadius: 14,
        alignItems: "center",
        marginHorizontal: 4,
        elevation: 2,
    },
    tileValue: { fontSize: 18, fontWeight: "800", color: "#2F5C39" },
    tileLabel: { fontSize: 12, color: "#647367", marginTop: 4 },

    sectionTitle: {
        marginTop: 30,
        marginBottom: 8,
        fontWeight: "800",
        fontSize: 15,
        color: "#213B27",
    },

    chartBox: {
        backgroundColor: "#FFFFFF",
        borderRadius: 16,
        padding: 10,
        elevation: 2,
    },

    progressContainer: {
        alignSelf: "center",
        marginTop: 20,
        marginBottom: 8,
    },
    progressText: {
        position: "absolute",
        top: "40%",
        alignSelf: "center",
        fontSize: 20,
        fontWeight: "800",
        color: "#2F5C39",
    },
    progressCaption: {
        textAlign: "center",
        fontSize: 13,
        color: "#546257",
        lineHeight: 20,
        paddingHorizontal: 20,
        marginBottom: 30,
    },
});
