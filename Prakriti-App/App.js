import "react-native-gesture-handler"; // must be first import
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { View, TouchableOpacity, Text, StyleSheet } from "react-native";
import { GestureHandlerRootView } from "react-native-gesture-handler";

import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

// Screens
import SplashScreen from "./Screens/Splash/SplashScreen";

import Login from "./Screens/Login/Login";
import Signup from "./Screens/SignUp/SignUp";

import HomeScreen from "./Screens/HomeScreen/HomeScreen";
import HistoryScreen from "./Screens/History/HistoryScreen";
import ExplorerScreen from "./Screens/Explorer/ExplorerScreen";
import ScanScreen from "./Screens/ScanScreen/ScanScreen";
import HowToDisposeScreen from "./Screens/HowToDispose/HowToDispose";
import RefillStationsScreen from "./Screens/RefillStations/RefillStationsScreen";
import CompostPointsScreen from "./Screens/CompostPoints/CompostPointsScreen";
import ReportLitterScreen from "./Screens/ReportLitter/ReportLitterScreen";
import AIChatIntroScreen from "./Screens/AIChat/AIChatIntroScreen";
import AIChatThreadScreen from "./Screens/AIChat/AIChatThreadScreen";
import RedeemPointsScreen from "./Screens/Redeem/RedeemPointsScreen";
import ProfileScreen from "./Screens/Profile/ProfileScreen";
import BusinessDashboard from "./Screens/Business/BusinessDashboard";
import VerifierDashboard from "./Screens/Verifier/VerifierDashboard";
import BusinessApplyStamp from "./Screens/Business/BusinessApplyStamp";
import BusinessInsights from "./Screens/Business/BusinessInsights";
import BusinessQR from "./Screens/Business/BusinessQR";
import VerifierQueueScreen from "./Screens/Verifier/VerifierQueueScreen";
import VerifierBusinessRequests from "./Screens/Verifier/VerifierBusinessRequests";
import VerifierReports from "./Screens/Verifier/VerifierReports";
import ForgotPassword from "./Screens/ForgotPassword/ForgotPassword";
import VerifierDetailScreen from "./Screens/Verifier/VerifierDetailScreen";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const ScanButton = ({ onPress }) => (
    <TouchableOpacity style={styles.scanButtonWrapper} onPress={onPress}>
        <View style={styles.scanButtonInner}>
            <MaterialCommunityIcons name="qrcode-scan" size={30} color="#FFFFFF" />
        </View>
    </TouchableOpacity>
);

function MainTabs() {
    return (
        <Tab.Navigator
            screenOptions={{
                headerShown: false,
                tabBarShowLabel: true,
                tabBarActiveTintColor: "#2F5C39",
                tabBarInactiveTintColor: "#8A8A8A",
                tabBarStyle: {
                    height: 70,
                    backgroundColor: "#FFFFFF",
                    borderTopWidth: 1,
                    borderTopColor: "#E0E0E0",
                    paddingBottom: 8,
                },
            }}
        >
            <Tab.Screen
                name="HomeScreen"
                component={HomeScreen}
                options={{
                    tabBarLabel: "Home",
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="home-outline" size={26} color={color} />
                    ),
                }}
            />

            <Tab.Screen
                name="Scan"
                component={ScanScreen}
                options={{
                    tabBarLabel: "",
                    tabBarIcon: () => null,
                    tabBarButton: (props) => <ScanButton {...props} />,
                }}
            />

            <Tab.Screen
                name="History"
                component={HistoryScreen}
                options={{
                    tabBarLabel: "History",
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="time-outline" size={26} color={color} />
                    ),
                }}
            />

            <Tab.Screen
                name="Explorer"
                component={ExplorerScreen}
                options={{
                    tabBarLabel: "Explore",
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="map-outline" size={26} color={color} />
                    ),
                }}
            />
        </Tab.Navigator>
    );
}

export default function App() {
    return (
        <GestureHandlerRootView style={{ flex: 1 }}>
            <NavigationContainer>
                <Stack.Navigator screenOptions={{ headerShown: false }}>
                    <Stack.Screen name="Splash" component={SplashScreen} />

                    <Stack.Screen name="Login" component={Login} />
                    <Stack.Screen name="Signup" component={Signup} />
                    <Stack.Screen name="Home" component={MainTabs} />
                    <Stack.Screen name="ForgotPassword" component={ForgotPassword} options={{ headerShown: false }} />

                    <Stack.Screen name="HowToDispose" component={HowToDisposeScreen} />
                    <Stack.Screen
                        name="RefillStations"
                        component={RefillStationsScreen}
                        options={{ presentation: "modal", headerShown: false }}
                    />
                    <Stack.Screen
                        name="CompostPoints"
                        component={CompostPointsScreen}
                        options={{ presentation: "modal", headerShown: false }}
                    />
                    <Stack.Screen name="ReportLitter" component={ReportLitterScreen} options={{ headerShown: false }} />
                    <Stack.Screen name="AIChatIntro" component={AIChatIntroScreen} options={{ headerShown: false }} />
                    <Stack.Screen name="AIChatThread" component={AIChatThreadScreen} options={{ headerShown: false }} />
                    <Stack.Screen
                        name="RedeemPoints"
                        component={RedeemPointsScreen}
                        options={{ presentation: "modal", headerShown: false }}
                    />
                    <Stack.Screen name="Profile" component={ProfileScreen} options={{ headerShown: false }} />
                    <Stack.Screen name="BusinessDashboard" component={BusinessDashboard} options={{ headerShown: false }} />
                    <Stack.Screen name="BusinessApplyStamp" component={BusinessApplyStamp} options={{ headerShown: false }} />
                    <Stack.Screen name="BusinessInsights" component={BusinessInsights} options={{ headerShown: false }} />
                    <Stack.Screen name="BusinessQR" component={BusinessQR} options={{ headerShown: false }} />

                    <Stack.Screen name="VerifierDashboard" component={VerifierDashboard} options={{ headerShown: false }} />
                    <Stack.Screen name="VerifierDetail" component={VerifierDetailScreen} options={{ headerShown: false }} />
                    <Stack.Screen name="VerifierQueue" component={VerifierQueueScreen} options={{ headerShown: false }} />
                    <Stack.Screen name="VerifierBusinessRequests" component={VerifierBusinessRequests} options={{ headerShown: false }} />
                    <Stack.Screen name="VerifierReports" component={VerifierReports} options={{ headerShown: false }} />
                </Stack.Navigator>
            </NavigationContainer>
        </GestureHandlerRootView>
    );
}

const styles = StyleSheet.create({
    scanButtonWrapper: {
        position: "absolute",
        alignSelf: "center",
        bottom: 18,
    },
    scanButtonInner: {
        width: 72,
        height: 72,
        borderRadius: 40,
        backgroundColor: "#2F5C39",
        justifyContent: "center",
        alignItems: "center",
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.25,
        shadowRadius: 6,
        elevation: 9,
    },
});
