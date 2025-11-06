import React, { useState } from "react";
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    StyleSheet,
    SafeAreaView,
    ScrollView,
    Image,
} from "react-native";

const Signup = ({ navigation, route }) => {
    const initialRole = route?.params?.role || "user";
    const [role, setRole] = useState(initialRole);

    const [fullName, setFullName] = useState("");
    const [emailOrPhone, setEmailOrPhone] = useState("");
    const [password, setPassword] = useState("");

    const handleSignup = () => {
        console.log("Signup Request:", { fullName, emailOrPhone, password, role });

        // Navigate based on selected role
        if (role === "user") {
            navigation.navigate("Home");
        } else if (role === "business") {
            navigation.navigate("BusinessDashboard");
        } else if (role === "verifier") {
            navigation.navigate("VerifierDashboard");
        }
    };

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 40 }}>

                {/* Hero Image */}
                <Image
                    source={{ uri: "https://cdn-icons-png.flaticon.com/512/4208/4208394.png" }}
                    style={styles.heroImage}
                />

                <View style={styles.headerSection}>
                    <Text style={styles.appTitle}>Create Account</Text>
                    <Text style={styles.subtitle}>
                        Join Prakriti and start contributing to responsible and sustainable travel.
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
                        placeholder="Full Name"
                        placeholderTextColor="#8A8A8A"
                        value={fullName}
                        onChangeText={setFullName}
                    />

                    <TextInput
                        style={styles.input}
                        placeholder="Email or Mobile Number"
                        placeholderTextColor="#8A8A8A"
                        value={emailOrPhone}
                        onChangeText={setEmailOrPhone}
                    />

                    <TextInput
                        style={styles.input}
                        placeholder="Create Password"
                        placeholderTextColor="#8A8A8A"
                        secureTextEntry
                        value={password}
                        onChangeText={setPassword}
                    />

                    <TouchableOpacity style={styles.signupButton} onPress={handleSignup}>
                        <Text style={styles.signupButtonText}>Sign Up</Text>
                    </TouchableOpacity>

                    <View style={styles.orDividerWrapper}>
                        <View style={styles.divider} />
                        <Text style={styles.orText}>or</Text>
                        <View style={styles.divider} />
                    </View>

                    <TouchableOpacity style={styles.googleButton}>
                        <Text style={styles.googleButtonText}>Continue with Google</Text>
                    </TouchableOpacity>

                    <View style={styles.loginLinkWrapper}>
                        <Text style={styles.loginText}>Already have an account? </Text>
                        <TouchableOpacity onPress={() => navigation.navigate("Login")}>
                            <Text style={styles.loginAction}>Login</Text>
                        </TouchableOpacity>
                    </View>
                </View>

            </ScrollView>
        </SafeAreaView>
    );
};

export default Signup;

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: "#F8F8F8", paddingHorizontal: 24 },

    heroImage: {
        width: 120,
        height: 120,
        alignSelf: "center",
        marginTop: 30,
        marginBottom: 20,
        opacity: 0.95,
    },

    headerSection: { marginBottom: 28 },
    appTitle: { fontSize: 28, fontWeight: "700", color: "#2F5C39" },
    subtitle: { fontSize: 14, color: "#5F705F", marginTop: 8, lineHeight: 18 },

    roleSelector: {
        flexDirection: "row",
        backgroundColor: "#E7EFEA",
        borderRadius: 12,
        marginBottom: 30,
        padding: 4,
    },
    roleOption: { flex: 1, paddingVertical: 10, borderRadius: 10, alignItems: "center" },
    roleActive: { backgroundColor: "#2F5C39" },
    roleText: { fontSize: 13, fontWeight: "600", color: "#2F5C39" },
    roleTextActive: { color: "#FFFFFF" },

    formSection: { width: "100%" },
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

    signupButton: {
        height: 52,
        backgroundColor: "#2F5C39",
        borderRadius: 12,
        alignItems: "center",
        justifyContent: "center",
        marginTop: 6,
        marginBottom: 18,
    },
    signupButtonText: { color: "#FFFFFF", fontSize: 16, fontWeight: "600" },

    orDividerWrapper: { flexDirection: "row", alignItems: "center", marginBottom: 20 },
    divider: { flex: 1, height: 1, backgroundColor: "#D3D3D3" },
    orText: { marginHorizontal: 8, fontSize: 13, color: "#666666" },

    googleButton: {
        height: 52,
        backgroundColor: "#FFFFFF",
        borderRadius: 12,
        justifyContent: "center",
        alignItems: "center",
        borderWidth: 1.2,
        borderColor: "#D3D3D3",
    },
    googleButtonText: { fontSize: 15, color: "#333333" },

    loginLinkWrapper: {
        flexDirection: "row",
        justifyContent: "center",
        marginTop: 26,
    },
    loginText: { color: "#5B5B5B", fontSize: 14 },
    loginAction: { color: "#2F5C39", fontSize: 14, fontWeight: "600" },
});
