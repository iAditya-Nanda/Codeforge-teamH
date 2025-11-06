import React, { useState, useRef } from "react";
import {
    View,
    Text,
    StyleSheet,
    Pressable,
    Animated,
    TouchableOpacity,
} from "react-native";
import { CameraView, useCameraPermissions } from "expo-camera";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

const ScanScreen = ({ navigation }) => {
    const [permission, requestPermission] = useCameraPermissions();
    const [isScanned, setIsScanned] = useState(false);
    const fadeAnim = useRef(new Animated.Value(0)).current;

    if (!permission) {
        return <View style={styles.center}><Text>Loading...</Text></View>;
    }
    if (!permission.granted) {
        return (
            <View style={styles.center}>
                <Text style={styles.permissionText}>Camera access needed to scan QR codes.</Text>
                <Pressable style={styles.permissionButton} onPress={requestPermission}>
                    <Text style={styles.permissionButtonText}>Grant Permission</Text>
                </Pressable>
            </View>
        );
    }

    const handleScan = ({ data }) => {
        if (isScanned) return;
        setIsScanned(true);

        // animate success card
        Animated.timing(fadeAnim, {
            toValue: 1,
            duration: 350,
            useNativeDriver: true,
        }).start();

        // TODO: Send to backend + update points
        console.log("Scanned Data:", data);
    };

    return (
        <View style={styles.container}>
            <CameraView
                style={StyleSheet.absoluteFillObject}
                onBarcodeScanned={isScanned ? undefined : handleScan}
            />

            {/* Overlay UI */}
            <View style={styles.overlay}>

                <Text style={styles.instructionText}>
                    Scan at a Green Action Point
                </Text>

                {/* Scan Focus Box */}
                <View style={styles.scanFrame} />

                {/* Close Button */}
                <TouchableOpacity onPress={() => navigation.goBack()} style={styles.closeButton}>
                    <MaterialCommunityIcons name="close" size={26} color="#FFFFFF" />
                </TouchableOpacity>
            </View>

            {/* Confirmation UI */}
            {isScanned && (
                <Animated.View style={[styles.confirmationCard, { opacity: fadeAnim }]}>
                    <Text style={styles.confirmTitle}>Action Recorded ✅</Text>

                    <Text style={styles.confirmDesc}>
                        Plastic sorted correctly at WasteHub Station – Sector 5
                    </Text>

                    <View style={styles.pointsBox}>
                        <Text style={styles.pointsValue}>+12</Text>
                        <Text style={styles.pointsLabel}>Green Points Earned</Text>
                    </View>

                    <Text style={styles.reinforceText}>
                        You’re helping keep the environment clean — keep going!
                    </Text>

                    <Pressable
                        style={styles.doneButton}
                        onPress={() => {
                            fadeAnim.setValue(0);
                            setIsScanned(false);
                            navigation.goBack();
                        }}
                    >
                        <Text style={styles.doneButtonText}>Done</Text>
                    </Pressable>
                </Animated.View>
            )}
        </View>
    );
};

export default ScanScreen;

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: "#000" },
    center: { flex: 1, justifyContent: "center", alignItems: "center" },

    permissionText: { fontSize: 15, color: "#333", marginBottom: 16, textAlign: "center" },
    permissionButton: { backgroundColor: "#2F5C39", paddingVertical: 12, paddingHorizontal: 30, borderRadius: 10 },
    permissionButtonText: { color: "#FFF", fontWeight: "600" },

    overlay: {
        position: "absolute",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
        height: "100%",
    },

    instructionText: {
        position: "absolute",
        top: 70,
        fontSize: 16,
        fontWeight: "600",
        color: "#FFFFFF",
    },

    scanFrame: {
        width: 230,
        height: 230,
        borderRadius: 14,
        borderWidth: 3,
        borderColor: "#FFFFFFD9",
    },

    closeButton: {
        position: "absolute",
        top: 50,
        right: 28,
    },

    confirmationCard: {
        position: "absolute",
        bottom: 60,
        left: 24,
        right: 24,
        backgroundColor: "#FFFFFF",
        borderRadius: 16,
        padding: 20,
        alignItems: "center",
        elevation: 7,
    },

    confirmTitle: { fontSize: 20, fontWeight: "800", color: "#2F5C39" },
    confirmDesc: { marginTop: 6, textAlign: "center", fontSize: 14, color: "#4B4B4B" },

    pointsBox: { marginTop: 12, alignItems: "center" },
    pointsValue: { fontSize: 38, fontWeight: "800", color: "#2F5C39" },
    pointsLabel: { fontSize: 13, color: "#666" },

    reinforceText: {
        marginTop: 10,
        textAlign: "center",
        fontSize: 13,
        color: "#2F5C39",
        fontWeight: "600",
    },

    doneButton: {
        marginTop: 16,
        backgroundColor: "#2F5C39",
        paddingVertical: 12,
        paddingHorizontal: 40,
        borderRadius: 12,
    },
    doneButtonText: { color: "#FFFFFF", fontWeight: "600", fontSize: 15 },
});
