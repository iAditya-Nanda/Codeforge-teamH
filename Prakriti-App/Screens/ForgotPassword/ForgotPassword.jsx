import React, { useState } from "react";
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    StyleSheet,
    SafeAreaView
} from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

const ForgotPassword = ({ navigation, route }) => {
    // If came from Login, default role is preserved
    const initialRole = route?.params?.role || "user";
    const [role, setRole] = useState(initialRole);
    const [emailOrPhone, setEmailOrPhone] = useState("");

    const handleReset = () => {
        console.log("Password Reset Request:", { role, emailOrPhone });

        // TODO:
        // API POST → `/auth/reset-password` with { role, identifier: emailOrPhone }
        // Show success toast

        navigation.navigate("Login");
    };

    return (
        <SafeAreaView style={styles.container}>

            {/* Back Button */}
            <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
                <Ionicons name="chevron-back" size={26} color="#2F5C39" />
            </TouchableOpacity>

            {/* Header */}
            <View style={styles.headerSection}>
                <Text style={styles.title}>Reset Password</Text>
                <Text style={styles.subtitle}>
                    Enter your email or phone to receive reset instructions.
                </Text>
            </View>

            {/* Role Selector */}
            <View style={styles.roleSelector}>
                <TouchableOpacity
                    style={[styles.roleOption, role === "user" && styles.roleActive]}
                    onPress={() => setRole("user")}
                >
                    <Text style={[styles.roleText, role === "user" && styles.roleTextActive]}>
                        Tourist / User
                    </Text>
                </TouchableOpacity>

                <TouchableOpacity
                    style={[styles.roleOption, role === "business" && styles.roleActive]}
                    onPress={() => setRole("business")}
                >
                    <Text style={[styles.roleText, role === "business" && styles.roleTextActive]}>
                        Business
                    </Text>
                </TouchableOpacity>

                <TouchableOpacity
                    style={[styles.roleOption, role === "verifier" && styles.roleActive]}
                    onPress={() => setRole("verifier")}
                >
                    <Text style={[styles.roleText, role === "verifier" && styles.roleTextActive]}>
                        Verifier
                    </Text>
                </TouchableOpacity>
            </View>

            {/* Input */}
            <TextInput
                style={styles.input}
                placeholder="Email or Mobile Number"
                placeholderTextColor="#8A8A8A"
                value={emailOrPhone}
                onChangeText={setEmailOrPhone}
            />

            {/* Submit */}
            <TouchableOpacity style={styles.resetButton} onPress={handleReset}>
                <Text style={styles.resetText}>Send Reset Link</Text>
            </TouchableOpacity>
        </SafeAreaView>
    );
};

export default ForgotPassword;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#F7F9F8",
        paddingHorizontal: 24,
        paddingTop: 16,
    },
    backBtn: {
        width: 40,
        height: 40,
        justifyContent: "center",
        alignItems: "center",
    },
    headerSection: {
        marginTop: 12,
        marginBottom: 28,
    },
    title: {
        fontSize: 28,
        fontWeight: "800",
        color: "#2F5C39",
    },
    subtitle: {
        fontSize: 14,
        color: "#5F705F",
        marginTop: 6,
        lineHeight: 18,
    },
    roleSelector: {
        flexDirection: "row",
        backgroundColor: "#E7EFEA",
        borderRadius: 12,
        marginBottom: 26,
        padding: 4,
    },
    roleOption: {
        flex: 1,
        paddingVertical: 10,
        borderRadius: 10,
        alignItems: "center",
    },
    roleActive: { backgroundColor: "#2F5C39" },
    roleText: { fontSize: 13, fontWeight: "600", color: "#2F5C39" },
    roleTextActive: { color: "#FFFFFF" },
    input: {
        height: 52,
        backgroundColor: "#FFFFFF",
        borderRadius: 12,
        paddingHorizontal: 16,
        fontSize: 15,
        marginBottom: 20,
        borderWidth: 1,
        borderColor: "#DADADA",
    },
    resetButton: {
        height: 52,
        backgroundColor: "#2F5C39",
        borderRadius: 12,
        alignItems: "center",
        justifyContent: "center",
        marginTop: 6,
    },
    resetText: {
        color: "#FFFFFF",
        fontSize: 16,
        fontWeight: "600",
    },
});
