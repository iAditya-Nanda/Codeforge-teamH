import React, { useState } from "react";
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    StyleSheet,
    SafeAreaView,
    Image,
} from "react-native";

const Login = ({ navigation }) => {
    const [role, setRole] = useState("user");
    const [emailOrPhone, setEmailOrPhone] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = () => {
        console.log("Login Attempt:", { emailOrPhone, password, role });

        if (role === "user") {
            navigation.navigate("Home");
        } else if (role === "business") {
            navigation.navigate("BusinessDashboard");
        } else if (role === "verifier") {
            navigation.navigate("VerifierDashboard");
        }
    };

    const handleGoogleLogin = () => {
        console.log("Google OAuth start for:", role);
    };

    return (
        <SafeAreaView style={styles.container}>
            {/* Hero Graphic */}
            <Image
                source={{
                    uri: "https://cdn-icons-png.flaticon.com/512/4208/4208394.png",
                }}
                style={styles.heroImage}
            />

            <View style={styles.headerSection}>
                <Text style={styles.appTitle}>Prakriti</Text>
                <Text style={styles.subtitle}>
                    Travel Responsibly. Earn Green Points.
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

            <View style={styles.formSection}>
                <TextInput
                    style={styles.input}
                    placeholder="Email or Mobile Number"
                    placeholderTextColor="#8A8A8A"
                    value={emailOrPhone}
                    onChangeText={setEmailOrPhone}
                />

                <TextInput
                    style={styles.input}
                    placeholder="Password"
                    placeholderTextColor="#8A8A8A"
                    secureTextEntry
                    value={password}
                    onChangeText={setPassword}
                />

                <TouchableOpacity onPress={() => navigation.navigate("ForgotPassword")}>
                    <Text style={styles.forgotPassword}>Forgot Password?</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
                    <Text style={styles.loginButtonText}>Login</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.googleButton} onPress={handleGoogleLogin}>
                    <Text style={styles.googleButtonText}>Continue with Google</Text>
                </TouchableOpacity>

                <View style={styles.signupLinkWrapper}>
                    <Text style={styles.signupText}>New here? </Text>
                    <TouchableOpacity onPress={() => navigation.navigate("Signup", { role })}>
                        <Text style={styles.signupAction}>Create an Account</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </SafeAreaView>
    );
};

export default Login;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#F8F8F8",
        paddingHorizontal: 24,
        justifyContent: "center",
    },
    heroImage: {
        width: 120,
        height: 120,
        alignSelf: "center",
        marginBottom: 20,
        opacity: 0.95,
    },
    headerSection: {
        marginBottom: 26,
        alignItems: "center",
    },
    appTitle: {
        fontSize: 32,
        fontWeight: "700",
        color: "#2F5C39",
    },
    subtitle: {
        fontSize: 14,
        color: "#5F705F",
        marginTop: 4,
        textAlign: "center",
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
    roleActive: {
        backgroundColor: "#2F5C39",
    },
    roleText: {
        fontSize: 13,
        fontWeight: "600",
        color: "#2F5C39",
    },
    roleTextActive: {
        color: "#FFFFFF",
    },

    formSection: {
        width: "100%",
    },
    input: {
        height: 52,
        backgroundColor: "#FFFFFF",
        borderRadius: 12,
        paddingHorizontal: 16,
        fontSize: 15,
        marginBottom: 14,
        borderWidth: 1,
        borderColor: "#E3E3E3",
    },
    forgotPassword: {
        alignSelf: "flex-end",
        fontSize: 13,
        color: "#2F5C39",
        marginBottom: 20,
    },
    loginButton: {
        height: 52,
        backgroundColor: "#2F5C39",
        borderRadius: 12,
        alignItems: "center",
        justifyContent: "center",
        marginBottom: 16,
    },
    loginButtonText: {
        color: "#FFFFFF",
        fontSize: 16,
        fontWeight: "600",
    },
    googleButton: {
        height: 52,
        backgroundColor: "#FFFFFF",
        borderRadius: 12,
        justifyContent: "center",
        alignItems: "center",
        borderWidth: 1.2,
        borderColor: "#D3D3D3",
    },
    googleButtonText: {
        fontSize: 15,
        color: "#333333",
    },
    signupLinkWrapper: {
        flexDirection: "row",
        justifyContent: "center",
        marginTop: 26,
    },
    signupText: {
        color: "#5B5B5B",
        fontSize: 14,
    },
    signupAction: {
        color: "#2F5C39",
        fontSize: 14,
        fontWeight: "600",
    },
});
