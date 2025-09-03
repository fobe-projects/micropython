# Import required libraries
from micropython import const
from machine import Pin, ADC
import time

# Hardware Pin Assignments

# Power Management
OLED_EN = const(12)  # Power for peripherals, controlled by GPIO1
PERI_EN = const(1)  # Detects if VBUS (5V

# Sense Pins
VBAT_SENSE = const(10)
LED = const(11)

# SPI
SPI_MOSI = const(41)
SPI_MISO = const(39)
SPI_CLK = const(40)

# I2C
I2C_SDA = const(14)
I2C_SCL = const(13)

# Helper functions

# LED & Ambient Light Sensor control
def led_set(state):
    """Set the state of the BLUE LED on IO11"""
    l = Pin(LED, Pin.OUT)
    l.value(state)


def led_blink():
    """Toggle the BLUE LED on IO11"""
    l = Pin(LED, Pin.OUT)
    l.value(not l.value())


def set_peri_power(state):
    """Enable or Disable power to the peripherals"""
    Pin(PERI_EN, Pin.OUT).value(state)

def set_oled_power(state):
    """Enable or Disable power to the OLED display"""
    Pin(OLED_EN, Pin.OUT).value(not state)


def get_battery_voltage():
    """
    Returns the current battery voltage. If no battery is connected, returns 4.2V which is the charge voltage
    This is an approximation only, but useful to detect if the charge state of the battery is getting low.
    """
    adc = ADC(Pin(VBAT_SENSE))  # Assign the ADC pin to read
    adc.atten(ADC.ATTN_11DB)  # Set attenuation to 11dB for full range (0-3.3V)
    # Use read_uv() to get ADC reading as this will use the on-chip calibration data
    measuredvbat = adc.read_uv() / 1000000  # Read micovolts and convert to volts
    measuredvbat *= 1.72  # Multiply by ratio of battery voltage to ADC pin voltage
    return round(measuredvbat, 2)