import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    TextInput,
    FlatList,
    Image,
    Pressable,
    KeyboardAvoidingView,
    Platform,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";

const AIChatThreadScreen = ({ route, navigation }) => {
    const insets = useSafeAreaInsets();
    const { initialMessage } = route.params;

    const [messages, setMessages] = useState([
        { id: "bot-hello", sender: "bot", text: "Hi! I’m Prakriti AI 🌿 Ask me anything." },
        { id: "user-first", sender: "user", text: initialMessage },
    ]);

    const [input, setInput] = useState("");

    const sendMessage = () => {
        if (!input.trim()) return;
        setMessages((prev) => [...prev, { id: Date.now().toString(), sender: "user", text: input }]);
        setInput("");

        setTimeout(() => {
            setMessages((prev) => [
                ...prev,
                {
                    id: (Date.now() + 1).toString(),
                    sender: "bot",
                    text: "I’ll help with that 🌱\nTell me where you are or show me the item.",
                },
            ]);
        }, 600);
    };

    const sendImage = async () => {
        let result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
        });
        if (!result.canceled && result.assets?.[0]?.uri) {
            setMessages((prev) => [
                ...prev,
                { id: Date.now().toString(), sender: "user", image: result.assets[0].uri },
            ]);
        }
    };

    const renderItem = ({ item }) => (
        <View style={[styles.msgBubble, item.sender === "user" ? styles.right : styles.left]}>
            {item.text && (
                <Text style={[styles.msgText, item.sender === "user" && { color: "#FFF" }]}>
                    {item.text}
                </Text>
            )}
            {item.image && <Image source={{ uri: item.image }} style={styles.msgImage} />}
        </View>
    );

    return (
        <SafeAreaView style={styles.safe}>
            {/* Top App Bar */}
            <View style={[styles.header, { paddingTop: insets.top + 4 }]}>
                <Pressable onPress={() => navigation.goBack()}>
                    <MaterialCommunityIcons name="chevron-left" size={26} color="#2F5C39" />
                </Pressable>
                <Text style={styles.headerTitle}>Prakriti AI Copilot</Text>
                <View style={{ width: 26 }} /> {/* For symmetry */}
            </View>

            <KeyboardAvoidingView
                style={{ flex: 1 }}
                behavior={Platform.OS === "ios" ? "padding" : null}
                keyboardVerticalOffset={Platform.OS === "ios" ? 80 : 0}
            >
                {/* Chat messages */}
                <FlatList
                    data={messages}
                    keyExtractor={(i) => i.id}
                    renderItem={renderItem}
                    contentContainerStyle={{ padding: 14, paddingBottom: 90 }}
                />

                {/* Input Bar */}
                <View style={[styles.inputRow, { paddingBottom: insets.bottom || 12 }]}>
                    <Pressable onPress={sendImage} style={styles.attachBtn}>
                        <MaterialCommunityIcons name="image-multiple" size={22} color="#2F5C39" />
                    </Pressable>

                    <TextInput
                        placeholder="Type a message..."
                        placeholderTextColor="#6D7B72"
                        style={styles.input}
                        value={input}
                        onChangeText={setInput}
                    />

                    <Pressable onPress={sendMessage} style={styles.sendBtn}>
                        <MaterialCommunityIcons name="send" size={20} color="#FFF" />
                    </Pressable>
                </View>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );
};

export default AIChatThreadScreen;

const styles = StyleSheet.create({
    safe: { flex: 1, backgroundColor: "#F7F9F8" },

    header: {
        flexDirection: "row",
        alignItems: "center",
        paddingHorizontal: 14,
        paddingBottom: 10,
        backgroundColor: "#F7F9F8",
        borderBottomWidth: 1,
        borderBottomColor: "#E0E6E2",
    },
    headerTitle: { flex: 1, textAlign: "center", fontSize: 17, fontWeight: "800", color: "#2F5C39" },

    msgBubble: {
        padding: 12,
        borderRadius: 14,
        marginBottom: 10,
        maxWidth: "75%",
    },
    left: { backgroundColor: "#EAF3ED", alignSelf: "flex-start" },
    right: { backgroundColor: "#2F5C39", alignSelf: "flex-end" },
    msgText: { fontSize: 14, color: "#1F2A23" },
    msgImage: { width: 170, height: 170, borderRadius: 12, marginTop: 6 },

    inputRow: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "#FFFFFF",
        paddingHorizontal: 12,
        borderTopWidth: 1,
        borderTopColor: "#E0E6E2",
    },
    attachBtn: { paddingRight: 6 },
    input: { flex: 1, paddingHorizontal: 10, paddingVertical: 10, fontSize: 15, color: "#1E2A23" },
    sendBtn: { backgroundColor: "#2F5C39", padding: 12, borderRadius: 14 },
});
