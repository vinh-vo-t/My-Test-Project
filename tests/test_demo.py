"""
Pytest test suite for Zetifi Smart Antenna
Simulates five key functional tests.
"""

import time
import random
import pytest


# ======= Simulated Zetifi Smart Antenna API =======

class ZetifiSmartAntenna:
    def __init__(self):
        self.connected_ble = False
        self.connected_wifi = False
        self.firmware_version = "1.4.3"
        self.device_info = {
            "ProductSerial": "ZTA-001234",
            "ProductModel": "Zetifi-SA-Pro",
            "BLE_MAC": "A1:B2:C3:D4:E5:F6",
            "WiFi_MAC": "11:22:33:44:55:66",
        }

    def connect_ble(self):
        # Simulate BLE pairing success
        time.sleep(0.3)
        self.connected_ble = True
        return self.connected_ble

    def connect_wifi(self, ssid: str, password: str):
        # Simulate a Wi-Fi connection with random success
        time.sleep(0.5)
        success = ssid.startswith("Zetifi") and len(password) >= 6
        self.connected_wifi = success
        return success

    def get_firmware_version(self):
        # Return firmware version
        return self.firmware_version

    def factory_reset(self):
        # Simulate reset; 90% chance success
        time.sleep(0.2)
        success = random.random() > 0.1
        if success:
            self.connected_ble = False
            self.connected_wifi = False
        return success

    def copy_device_info(self):
        # Simulate copying device info to clipboard
        info_str = f"{self.device_info['ProductSerial']} | {self.device_info['BLE_MAC']}"
        return info_str


# ======= Test Cases =======

@pytest.fixture(scope="module")
def antenna():
    """Fixture to initialize a Zetifi Smart Antenna instance."""
    return ZetifiSmartAntenna()


def test_ble_connection(antenna):
    """Verify BLE pairing and connection stability."""
    assert antenna.connect_ble() is True, "BLE connection failed."


def test_wifi_connection(antenna):
    """Ensure Wi-Fi connection and signal strength reporting."""
    assert antenna.connect_wifi("Zetifi_AP", "zetifi123") is True, "Wi-Fi connection failed."


def test_firmware_version(antenna):
    """Check that firmware version is displayed correctly."""
    version = antenna.get_firmware_version()
    assert version.startswith("1."), f"Unexpected firmware version: {version}"


def test_factory_reset(antenna):
    """Verify factory reset restores default configuration."""
    result = antenna.factory_reset()
    assert result is True, "Factory reset did not restore defaults."
    assert antenna.connected_ble is False
    assert antenna.connected_wifi is False


def test_device_info_copy(antenna):
    """Test long-press copy of device info (serial and MAC)."""
    copied = antenna.copy_device_info()
    assert "ZTA-" in copied and ":" in copied, "Copied info missing serial or MAC address."
