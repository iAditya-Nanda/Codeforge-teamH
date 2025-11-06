import React, { useState, useRef } from "react";
import {
    View,
    Text,
    StyleSheet,
    Pressable,
    Image,
    ActivityIndicator,
    Animated,
} from "react-native";
import { CameraView, useCameraPermissions } from "expo-camera";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

const HowToDisposeScreen = ({ navigation }) => {
    const [permission, requestPermission] = useCameraPermissions();
    const cameraRef = useRef(null);

    const [phase, setPhase] = useState("scan"); // scan → result → verify → done
    const [processing, setProcessing] = useState(false);

    const [detected, setDetected] = useState(null);
    const [proofImage, setProofImage] = useState(null);

    const fadeAnim = useRef(new Animated.Value(0)).current;

    if (!permission) return <View style={styles.center}><Text>Loading…</Text></View>;
    if (!permission.granted)
        return (
            <View style={styles.center}>
                <Text style={styles.permissionText}>Camera access needed.</Text>
                <Pressable style={styles.permissionButton} onPress={requestPermission}>
                    <Text style={styles.permissionButtonText}>Allow Camera</Text>
                </Pressable>
            </View>
        );

    const capture = async () => {
        if (!cameraRef.current) return;
        const photo = await cameraRef.current.takePictureAsync({ base64: true });
        return photo.uri;
    };

    const scanTrash = async () => {
        const img = await capture();
        setProcessing(true);

        // 🔮 Mock AI — Replace with real AI later
        setTimeout(() => {
            const mock = {
                label: "Plastic Bottle",
                type: "Plastic Waste",
                confidence: 0.88,
                steps: [
                    "Empty any remaining liquid",
                    "Remove wrapper label if possible",
                    "Crush bottle to reduce space",
                    "Place in **Dry Recyclable / Plastic Bin**",
                ],
                preview: img,
            };
            setDetected(mock);
            setProcessing(false);
            setPhase("result");

            Animated.timing(fadeAnim, { toValue: 1, duration: 350, useNativeDriver: true }).start();
        }, 1400);
    };

    const captureProof = async () => {
        const img = await capture();
        setProofImage(img);
        setPhase("done");
    };

    return (
        <View style={styles.container}>

            {/* PHASE 1 — SCAN */}
            {phase === "scan" && (
                <View style={styles.fullscreen}>
                    <CameraView ref={cameraRef} style={StyleSheet.absoluteFillObject} facing="back" />

                    <Text style={styles.scanHint}>Point at the trash item</Text>

                    <View style={styles.scanCenter}>
                        <View style={styles.scanFrame} />
                    </View>

                    <View style={styles.captureWrapper}>
                        <Pressable style={styles.captureButton} onPress={scanTrash}>
                            <MaterialCommunityIcons name="camera" size={28} color="#FFF" />
                        </Pressable>
                    </View>
                </View>
            )}

            {/* LOADING */}
            {processing && (
                <View style={styles.processing}>
                    <ActivityIndicator size="large" color="#FFF" />
                    <Text style={styles.processingText}>Analyzing…</Text>
                </View>
            )}

            {/* PHASE 2 — RESULT */}
            {phase === "result" && detected && (
                <Animated.View style={[styles.resultPanel, { opacity: fadeAnim }]}>
                    <Image source={{ uri: detected.preview }} style={styles.preview} />

                    <Text style={styles.itemTitle}>{detected.label}</Text>
                    <Text style={styles.itemType}>{detected.type}</Text>

                    <View style={styles.confBar}>
                        <View style={[styles.confFill, { width: `${detected.confidence * 100}%` }]} />
                    </View>
                    <Text style={styles.confText}>
                        Confidence {Math.round(detected.confidence * 100)}%
                    </Text>

                    <Text style={styles.stepsTitle}>How to Dispose</Text>
                    {detected.steps.map((s, i) => (
                        <Text key={i} style={styles.stepLine}>• {s}</Text>
                    ))}

                    <Pressable style={styles.verifyButton} onPress={() => setPhase("verify")}>
                        <Text style={styles.verifyText}>I did it — Verify & Earn Points</Text>
                    </Pressable>
                </Animated.View>
            )}

            {/* PHASE 3 — PROOF CAPTURE */}
            {phase === "verify" && (
                <View style={styles.fullscreen}>
                    <CameraView ref={cameraRef} style={StyleSheet.absoluteFillObject} />
                    <Text style={styles.verifyHint}>Capture proof of correct disposal</Text>

                    <View style={styles.captureWrapper}>
                        <Pressable style={styles.captureButton} onPress={captureProof}>
                            <MaterialCommunityIcons name="check" size={28} color="#FFF" />
                        </Pressable>
                    </View>
                </View>
            )}

            {/* PHASE 4 — DONE */}
            {phase === "done" && (
                <View style={styles.doneCard}>
                    <Text style={styles.doneTitle}>✅ Verified!</Text>
                    <Text style={styles.donePoints}>+8 Green Points</Text>
                    <Image source={{ uri: proofImage }} style={styles.proofImg} />

                    <Pressable style={styles.backBtn} onPress={() => navigation.goBack()}>
                        <Text style={styles.backBtnText}>Return to Home</Text>
                    </Pressable>
                </View>
            )}
        </View>
    );
};

export default HowToDisposeScreen;

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: "#000" },

    fullscreen: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
    },

    scanHint: {
        position: "absolute",
        top: 80,
        alignSelf: "center",
        color: "#FFFFFF",
        fontSize: 16,
        fontWeight: "600",
    },

    scanCenter: { flex: 1, justifyContent: "center", alignItems: "center" },
    scanFrame: {
        width: 260,
        height: 260,
        borderWidth: 3,
        borderColor: "#FFFFFF",
        borderRadius: 18,
    },

    captureWrapper: { position: "absolute", bottom: 70, width: "100%", alignItems: "center" },
    captureButton: {
        backgroundColor: "#2F5C39",
        padding: 22,
        borderRadius: 50,
    },

    processing: { position: "absolute", top: "45%", width: "100%", alignItems: "center" },
    processingText: { color: "#FFF", marginTop: 10, fontWeight: "600" },

    resultPanel: {
        position: "absolute",
        bottom: 0, left: 0, right: 0,
        backgroundColor: "#FFFFFF",
        borderTopLeftRadius: 22,
        borderTopRightRadius: 22,
        padding: 22,
        alignItems: "center",
    },

    preview: { width: 90, height: 90, borderRadius: 12, marginBottom: 12 },
    itemTitle: { fontSize: 20, fontWeight: "800", color: "#2F5C39" },
    itemType: { fontSize: 14, color: "#6C7D73", marginBottom: 14 },

    confBar: { height: 6, width: "100%", backgroundColor: "#E5ECE8", borderRadius: 4 },
    confFill: { height: "100%", backgroundColor: "#2F5C39", borderRadius: 4 },
    confText: { fontSize: 12, color: "#455147", marginTop: 6 },

    stepsTitle: { fontSize: 16, fontWeight: "700", marginTop: 12, marginBottom: 6 },
    stepLine: { fontSize: 14, color: "#334238", marginTop: 3, textAlign: "center" },

    verifyButton: {
        marginTop: 18,
        backgroundColor: "#2F5C39",
        paddingVertical: 14,
        paddingHorizontal: 22,
        borderRadius: 14,
    },
    verifyText: { color: "#FFF", fontWeight: "700", fontSize: 14 },

    verifyHint: {
        position: "absolute",
        top: 80,
        color: "#FFFFFF",
        fontSize: 16,
        fontWeight: "700",
    },

    doneCard: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#F8FFF6" },
    doneTitle: { fontSize: 26, fontWeight: "800", color: "#2F5C39" },
    donePoints: { fontSize: 18, marginTop: 4, fontWeight: "600", color: "#415D49" },
    proofImg: { width: 140, height: 140, borderRadius: 18, marginTop: 18 },
    backBtn: { marginTop: 30, backgroundColor: "#2F5C39", paddingVertical: 12, paddingHorizontal: 30, borderRadius: 12 },
    backBtnText: { color: "#FFF", fontWeight: "700" },
});
