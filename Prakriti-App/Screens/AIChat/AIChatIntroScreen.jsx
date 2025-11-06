
import React, { useState } from "react";
import { View, Text, StyleSheet, TextInput, Pressable } from "react-native";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

const AIChatIntroScreen = ({ navigation }) => {
    const [text, setText] = useState("");

    const startChat = () => {
        if (!text.trim()) return;
        navigation.navigate("AIChatThread", { initialMessage: text });
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Prakriti AI Copilot</Text>
            <Text style={styles.subtitle}>
                Ask anything about waste sorting, refill stations, composting, or eco travel tips 🌿
            </Text>

            <View style={styles.inputRow}>
                <TextInput
                    placeholder="Ask here..."
                    placeholderTextColor="#6D7B72"
                    style={styles.input}
                    value={text}
                    onChangeText={setText}
                />
                <Pressable style={styles.sendBtn} onPress={startChat}>
                    <MaterialCommunityIcons name="send" size={20} color="#FFF" />
                </Pressable>
            </View>
        </View>
    );
};

export default AIChatIntroScreen;

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: "center", padding: 24, backgroundColor: "#F7F9F8" },
    title: { fontSize: 24, fontWeight: "800", color: "#2F5C39", marginBottom: 8 },
    subtitle: { fontSize: 14, color: "#4E5C53", marginBottom: 40 },
    inputRow: { flexDirection: "row", backgroundColor: "#FFFFFF", borderRadius: 14, elevation: 2 },
    input: { flex: 1, paddingHorizontal: 12, paddingVertical: 12, fontSize: 15, color: "#1E2A23" },
    sendBtn: { backgroundColor: "#2F5C39", paddingHorizontal: 16, justifyContent: "center", borderRadius: 14 },
});
