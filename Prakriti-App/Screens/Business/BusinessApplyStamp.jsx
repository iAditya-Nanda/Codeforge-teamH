import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    Pressable,
    TextInput,
    Image,
    ScrollView,
} from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import * as ImagePicker from "expo-image-picker";
import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

const BusinessApplyStamp = ({ navigation }) => {
    const insets = useSafeAreaInsets();

    const [photos, setPhotos] = useState([]);
    const [description, setDescription] = useState("");
    const [checklist, setChecklist] = useState({
        refill: false,
        wasteSegregation: false,
        localProducts: false,
        noSingleUse: false,
    });

    const toggleCheck = (key) =>
        setChecklist((prev) => ({ ...prev, [key]: !prev[key] }));

    const pickImage = async () => {
        let result = await ImagePicker.launchImageLibraryAsync({
            allowsMultipleSelection: true,
            quality: 0.8,
        });

        if (!result.canceled) {
            const selected = result.assets || [result];
            setPhotos((prev) => [...prev, ...selected.map((x) => x.uri)]);
        }
    };

    const handleSubmit = () => {
        // TODO: API POST request
        navigation.navigate("BusinessDashboard");
    };

    return (
        <SafeAreaView style={[styles.safe, { paddingTop: insets.top + 6 }]}>
            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => navigation.goBack()}>
                    <MaterialCommunityIcons name="chevron-left" size={28} color="#2F5C39" />
                </Pressable>
                <Text style={styles.headerTitle}>Green Stamp Application</Text>
                <View style={{ width: 28 }} />
            </View>

            <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 90 }}>

                {/* AI Smart Helper */}
                <View style={styles.aiCard}>
                    <MaterialCommunityIcons name="robot-happy-outline" size={22} color="#2F5C39" />
                    <Text style={styles.aiTitle}>Prakriti AI Audit Helper</Text>
                    <Text style={styles.aiSubtitle}>
                        Describe how your café/shop follows sustainable practices.
                        AI will pre-evaluate before final verification.
                    </Text>

                    <TextInput
                        style={styles.aiInput}
                        placeholder="e.g., We offer water refills, avoid plastic, compost organic waste..."
                        placeholderTextColor="#6E7C71"
                        multiline
                        value={description}
                        onChangeText={setDescription}
                    />
                </View>

                {/* Checklist */}
                <Text style={styles.sectionTitle}>Sustainability Practices</Text>
                {[
                    { key: "refill", label: "Provides Water Refill" },
                    { key: "wasteSegregation", label: "Segregates Waste Properly" },
                    { key: "localProducts", label: "Promotes Local & Organic Products" },
                    { key: "noSingleUse", label: "Avoids Single-Use Plastics" },
                ].map((item) => (
                    <Pressable key={item.key} style={styles.checkRow} onPress={() => toggleCheck(item.key)}>
                        <MaterialCommunityIcons
                            name={checklist[item.key] ? "checkbox-marked" : "checkbox-blank-outline"}
                            size={22}
                            color="#2F5C39"
                        />
                        <Text style={styles.checkLabel}>{item.label}</Text>
                    </Pressable>
                ))}

                {/* Photo Upload */}
                <Text style={styles.sectionTitle}>Upload Proof Photos</Text>
                <Pressable onPress={pickImage} style={styles.uploadBtn}>
                    <Ionicons name="image-outline" size={20} color="#2F5C39" />
                    <Text style={styles.uploadText}>Upload Images</Text>
                </Pressable>

                <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: 14 }}>
                    {photos.map((uri, index) => (
                        <Image key={index} source={{ uri }} style={styles.preview} />
                    ))}
                </ScrollView>

                {/* Submit */}
                <Pressable style={styles.submitBtn} onPress={handleSubmit}>
                    <Text style={styles.submitText}>Submit for Verification</Text>
                </Pressable>

            </ScrollView>
        </SafeAreaView>
    );
};

export default BusinessApplyStamp;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8", paddingHorizontal: 20 },

    header: { flexDirection: "row", alignItems: "center", marginBottom: 16 },
    headerTitle: { flex: 1, textAlign: "center", fontSize: 18, fontWeight: "800", color: "#2F5C39" },

    aiCard: {
        backgroundColor: "#FFFFFF",
        padding: 14,
        borderRadius: 16,
        elevation: 2,
        marginBottom: 20,
    },
    aiTitle: { fontSize: 15, fontWeight: "800", color: "#2F5C39", marginTop: 6 },
    aiSubtitle: { color: "#63746B", fontSize: 13, marginTop: 4, lineHeight: 18 },
    aiInput: {
        marginTop: 10,
        backgroundColor: "#F1F5F3",
        borderRadius: 12,
        padding: 12,
        minHeight: 90,
        fontSize: 14,
        color: "#213B27",
    },

    sectionTitle: { fontSize: 15, fontWeight: "800", color: "#213B27", marginBottom: 8, marginTop: 18 },

    checkRow: { flexDirection: "row", alignItems: "center", paddingVertical: 8 },
    checkLabel: { marginLeft: 10, fontSize: 14, color: "#2F5C39", fontWeight: "600" },

    uploadBtn: {
        backgroundColor: "#EAF3ED",
        borderRadius: 12,
        paddingVertical: 10,
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "row",
        gap: 8,
    },
    uploadText: { color: "#2F5C39", fontWeight: "700" },

    preview: {
        width: 90,
        height: 90,
        borderRadius: 12,
        marginRight: 12,
    },

    submitBtn: {
        backgroundColor: "#2F5C39",
        paddingVertical: 14,
        borderRadius: 14,
        alignItems: "center",
        marginTop: 26,
        marginBottom: 30,
    },
    submitText: { color: "#FFFFFF", fontSize: 15, fontWeight: "700" },
});
