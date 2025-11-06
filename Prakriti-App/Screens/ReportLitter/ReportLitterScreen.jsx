import React, { useRef, useState, useEffect } from "react";
import {
    View,
    Text,
    StyleSheet,
    Pressable,
    ActivityIndicator,
    Image,
} from "react-native";
import { CameraView, useCameraPermissions } from "expo-camera";
import * as Location from "expo-location";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import MapView, { Marker } from "react-native-maps";

const ReportLitterScreen = ({ navigation }) => {
    const [permission, requestPermission] = useCameraPermissions();
    const cameraRef = useRef(null);

    const [phase, setPhase] = useState("camera"); // camera → analyzing → location → done
    const [image, setImage] = useState(null);
    const [isLitter, setIsLitter] = useState(null);

    const [coords, setCoords] = useState(null);

    const takePhoto = async () => {
        const photo = await cameraRef.current.takePictureAsync({ base64: true });
        setImage(photo.uri);
        setPhase("analyzing");

        // 🔮 Mock AI - Replace with real later
        setTimeout(() => {
            setIsLitter(true);
            setPhase("location");
        }, 1400);
    };

    const fetchLocation = async () => {
        let { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== "granted") return;
        const loc = await Location.getCurrentPositionAsync({});
        setCoords({ latitude: loc.coords.latitude, longitude: loc.coords.longitude });
    };

    useEffect(() => {
        if (phase === "location") fetchLocation();
    }, [phase]);

    const submitReport = () => {
        setPhase("done");

        // TODO: send image + coords to backend
    };

    if (!permission) return <View style={styles.center}><Text>Loading...</Text></View>;
    if (!permission.granted)
        return (
            <View style={styles.center}>
                <Text style={styles.permissionText}>Camera required to report litter.</Text>
                <Pressable style={styles.permissionBtn} onPress={requestPermission}>
                    <Text style={styles.permissionBtnText}>Allow Camera</Text>
                </Pressable>
            </View>
        );

    return (
        <View style={styles.container}>

            {/* STEP 1 — CAPTURE LITTER PHOTO */}
            {phase === "camera" && (
                <>
                    <CameraView ref={cameraRef} style={StyleSheet.absoluteFillObject} facing="back" />

                    <Text style={styles.scanHint}>Capture photo of the litter</Text>

                    <View style={styles.bottomCenter}>
                        <Pressable style={styles.captureBtn} onPress={takePhoto}>
                            <MaterialCommunityIcons name="camera" size={28} color="#FFF" />
                        </Pressable>
                    </View>
                </>
            )}

            {/* STEP 2 — AI ANALYZING */}
            {phase === "analyzing" && (
                <View style={styles.center}>
                    <ActivityIndicator size="large" color="#FFFFFF" />
                    <Text style={styles.analyzingText}>AI analyzing litter…</Text>
                </View>
            )}

            {/* STEP 3 — CONFIRM LOCATION */}
            {phase === "location" && (
                <View style={styles.locationScreen}>
                    <Image source={{ uri: image }} style={styles.preview} />

                    <Text style={styles.title}>Litter Detected ✅</Text>
                    <Text style={styles.subtitle}>Pin the location or use GPS</Text>

                    <View style={styles.mapWrap}>
                        <MapView
                            style={styles.map}
                            initialRegion={{
                                latitude: coords?.latitude || 28.61,
                                longitude: coords?.longitude || 77.23,
                                latitudeDelta: 0.02,
                                longitudeDelta: 0.02,
                            }}
                            onPress={(e) => setCoords(e.nativeEvent.coordinate)}
                        >
                            {coords && <Marker coordinate={coords} />}
                        </MapView>
                    </View>

                    <Pressable style={styles.submitBtn} onPress={submitReport}>
                        <Text style={styles.submitText}>Submit Report & Earn Points</Text>
                    </Pressable>
                </View>
            )}

            {/* STEP 4 — DONE */}
            {phase === "done" && (
                <View style={styles.doneScreen}>
                    <Text style={styles.doneTitle}>Thank you 🌿</Text>
                    <Text style={styles.doneMsg}>Your report helps keep Himachal clean.</Text>
                    <Text style={styles.points}>+10 Green Points</Text>

                    <Pressable style={styles.backBtn} onPress={() => navigation.goBack()}>
                        <Text style={styles.backBtnText}>Return to Home</Text>
                    </Pressable>
                </View>
            )}
        </View>
    );
};

export default ReportLitterScreen;

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: "#000" },
    center: { flex: 1, justifyContent: "center", alignItems: "center" },
    permissionText: { color: "#FFF", marginBottom: 12 },
    permissionBtn: { backgroundColor: "#2F5C39", padding: 12, borderRadius: 8 },
    permissionBtnText: { color: "#FFF", fontWeight: "700" },

    scanHint: { position: "absolute", top: 80, alignSelf: "center", color: "#FFF", fontSize: 16, fontWeight: "600" },

    bottomCenter: { position: "absolute", bottom: 70, width: "100%", alignItems: "center" },
    captureBtn: { backgroundColor: "#2F5C39", padding: 22, borderRadius: 50 },

    analyzingText: { marginTop: 12, color: "#FFF", fontWeight: "600" },

    locationScreen: { flex: 1, backgroundColor: "#F7F9F8" },
    preview: { alignSelf: "center", width: 110, height: 110, borderRadius: 14, marginTop: 20 },
    title: { fontSize: 20, textAlign: "center", fontWeight: "800", marginTop: 8, color: "#2F5C39" },
    subtitle: { textAlign: "center", color: "#5E6D64", marginBottom: 10 },

    mapWrap: { flex: 1, margin: 16, borderRadius: 14, overflow: "hidden" },
    map: { flex: 1 },

    submitBtn: { margin: 16, padding: 14, borderRadius: 12, backgroundColor: "#2F5C39", alignItems: "center" },
    submitText: { color: "#FFF", fontWeight: "700" },

    doneScreen: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#F6FFF2" },
    doneTitle: { fontSize: 26, fontWeight: "800", color: "#2F5C39" },
    doneMsg: { marginTop: 6, fontSize: 14, color: "#425348" },
    points: { marginTop: 14, fontSize: 20, fontWeight: "800", color: "#2F5C39" },
    backBtn: { marginTop: 26, backgroundColor: "#2F5C39", paddingVertical: 12, paddingHorizontal: 36, borderRadius: 14 },
    backBtnText: { color: "#FFF", fontWeight: "700" },
});
