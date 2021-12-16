# Code written by Prof. John Gallaugher, modified by Noe Ruiz for Adafruit Industries. Modified by Shawn Esterman for personal use.
# Adafruit Circuit Playground Express Bluefruit
# Sourced from: https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Circuit_Playground_Bluefruit_Pumpkin/code.py

import time
import board
import digitalio
import neopixel
import random
from math import fabs

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket


# Setup Neopixels
SETTINGS_INT_NEOPIXELS = 10
SETTINGS_FLOAT_BRIGHTNESS = 1.0
pixels = neopixel.NeoPixel(board.NEOPIXEL, SETTINGS_INT_NEOPIXELS, brightness=SETTINGS_FLOAT_BRIGHTNESS, auto_write=True)


# Define simple colors
COLOR_MAROON = (82, 26, 19)
COLOR_RED = (255, 0, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_YELLOW = (255, 230, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_INDIGO = (75, 0, 130)
COLOR_PURPLE = (100, 0, 255)
COLOR_VIOLET = (238, 130, 238)
COLOR_GOLD = (255, 215, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (187, 187, 187)
COLOR_PAIRS = [
    (COLOR_RED, COLOR_GREEN),
    (COLOR_WHITE, COLOR_GOLD),
    (COLOR_WHITE, COLOR_BLACK),
    (COLOR_WHITE, COLOR_BLUE),
    (COLOR_WHITE, COLOR_RED),
    (COLOR_WHITE, COLOR_GREEN),
    (COLOR_GOLD, COLOR_BLACK)
]

def get_random_color_pair():
    index = random.randint(0, (len(COLOR_PAIRS)-1))
    return COLOR_PAIRS[index]

# Define some color lists
# https://personal.sron.nl/~pault/data/colourschemes.pdf
COLOR_LIST_BRIGHT = [(68, 119, 170), (102, 204, 238), (34, 136, 51), (204, 187, 68), (238, 102, 119), (170, 51, 119), COLOR_GREY]
COLOR_LIST_VIBRANT = [(0, 119, 187), (51, 187, 238), (0, 153, 136), (238, 119, 51), (204, 51, 17), (238, 51, 119), COLOR_GREY]
COLOR_LIST_MUTED = [(51, 34, 136), (136, 204, 238), (68, 170, 153), (17, 119, 51), (153, 153, 51), (221, 204, 119), (221, 204, 119), (136, 34, 85), (170, 68, 153)]
COLOR_LIST_LIGHT = [(119, 170, 221), (153, 221, 255), (68, 187, 153), (187, 204, 51), (187, 204, 51), (238, 221, 136), (238, 136, 102), (255, 170, 187), (221, 221, 221)]
COLOR_LIST_SUNSET = [(54, 75, 154), (74, 123, 183), (110, 166, 205), (152, 202, 225), (194, 228, 239), (234, 236, 204), (254, 218, 139), (253, 179, 102), (246, 126, 75), (221, 61, 45), (165, 0, 38)]
COLOR_LIST_BLUERED = [(33, 102, 172), (67, 147, 195), (146, 197, 222), (209, 229, 240), (247, 247, 247), (253, 219, 199), (244, 165, 130), (214, 96, 77), (178, 24, 43)]
COLOR_LIST_PURPLEGREEN = [(178, 24, 43), (178, 24, 43), (194, 165, 207), (231, 212, 232), (231, 212, 232), (217, 240, 211), (172, 211, 158), (90, 174, 97), (27, 120, 55)]
COLOR_LIST_RAINBOW = [(136, 46, 114), (25, 101, 176), (123, 175, 222), (78, 178, 101), (202, 224, 171), (247, 240, 86), (244, 167, 54), (232, 96, 28), (220, 5, 12), (114, 25, 14)]
COLOR_LISTS = [COLOR_LIST_BRIGHT, COLOR_LIST_VIBRANT, COLOR_LIST_MUTED, COLOR_LIST_LIGHT, COLOR_LIST_SUNSET, COLOR_LIST_BLUERED, COLOR_LIST_PURPLEGREEN, COLOR_LIST_RAINBOW]

def get_random_color_list():
    index = random.randint(0, (len(COLOR_LISTS)-1))
    return COLOR_LISTS[index]


# Define animation functions
def neopixel_reset():
    pixels.fill(COLOR_BLACK)  # reset background to black
    pixels.brightness = SETTINGS_FLOAT_BRIGHTNESS  # reset brightness


def neopixel_color_chase(primary, secondary=COLOR_BLACK, length=1, delay_seconds=0.1, total_seconds=60, exit_on_connect=False):
    pixels.fill(secondary)  # set background to Secondary color
    loops = int(total_seconds/delay_seconds)  # Calculate how many loops to do

    for i in range(loops):
        index_neopixel = i % SETTINGS_INT_NEOPIXELS
        illuminate = []
        for j in range(index_neopixel, index_neopixel+length):
            index = j % SETTINGS_INT_NEOPIXELS
            illuminate.append(index)

        for k in range(SETTINGS_INT_NEOPIXELS):
            if k in illuminate:
                pixels[k] = primary
            else:
                pixels[k] = secondary

        if exit_on_connect:
            if ble.connected:
                neopixel_reset()
                break

        time.sleep(delay_seconds)
        
    neopixel_reset()
    

def neopixel_color_swap(primary, secondary=COLOR_BLACK, delay_seconds=0.1, total_seconds=60, exit_on_connect=False):
    pixels.fill(secondary)  # set background to Secondary color
    loops = int(total_seconds/delay_seconds)  # Calculate how many loops to do
    
    for i in range(loops):
        if i % 5:
            # Swap every 5 iterations
            primary, secondary = secondary, primary
        
            for i in range(SETTINGS_INT_NEOPIXELS):
                if (i % 2) == 0:
                    pixels[i] = primary
                else:
                    pixels[i] = secondary

        
        if exit_on_connect:
            if ble.connected:
                neopixel_reset()
                break
                
        time.sleep(delay_seconds)
        
    neopixel_reset()

    
def neopixel_color_pulse(primary = COLOR_WHITE, pulses=5, delay_seconds=0.05, total_seconds=60, exit_on_connect=False):
    pixels.fill(primary)
    loops = int(total_seconds/delay_seconds)  # Calculate how many loops to do about 60 seconds
    
    minimum_brightness = 0.2
    peakpoint = int(loops / pulses)
    modifier = (1-minimum_brightness)/peakpoint
    
    for i in range(loops):
        # Wave algorithm to peak every 
        pixels.brightness = modifier*fabs(((i+peakpoint) % (2*peakpoint)) - peakpoint) + minimum_brightness
        
        if exit_on_connect:
            if ble.connected:
                neopixel_reset()
                break

        time.sleep(delay_seconds)

    neopixel_reset() 
    
    
def neopixel_colorlist_randomizer(color_list=COLOR_LIST_RAINBOW, delay_seconds=0.25, total_seconds=60, pulses=0, exit_on_connect=False):
    pixels.fill(COLOR_BLACK)
    loops = int(total_seconds/delay_seconds)  # Calculate how many loops to do about 60 seconds
    
    if pulses > 0:
        minimum_brightness = 0.2
        peakpoint = int(loops / pulses)
        modifier = (1-minimum_brightness)/peakpoint
    
    color_list_count = len(color_list)

    # Set inital colors
    for i in range(SETTINGS_INT_NEOPIXELS):
        index_color = i % color_list_count
        pixels[i] = color_list[index_color]

    # Swap colors every iteration
    for i in range(loops):
        if pulses > 0:
            # Wave algorithm to peak every 
            pixels.brightness = modifier*fabs(((i+peakpoint) % (2*peakpoint)) - peakpoint) + minimum_brightness
        
        for j in range(SETTINGS_INT_NEOPIXELS):
            k = random.randint(0,SETTINGS_INT_NEOPIXELS-1)
            if j != k:
                pixels[j], pixels[k] = pixels[k], pixels[j]
        
        if exit_on_connect:
            if ble.connected:
                neopixel_reset()
                break

        time.sleep(delay_seconds)
        
    neopixel_reset()


def neopixel_colorlist_chase(color_list=COLOR_LIST_RAINBOW, delay_seconds=0.1, total_seconds=60, pulses=0, exit_on_connect=False):
    pixels.fill(COLOR_BLACK)  # Clear out the pixels
    loops = int(total_seconds/delay_seconds)  # Calculate how many loops to do about 60 seconds
    
    if pulses > 0:
        minimum_brightness = 0.2
        peakpoint = int(loops / pulses)
        modifier = (1-minimum_brightness)/peakpoint
    
    color_list_count = len(color_list)
    
    for i in range(loops):
        if pulses > 0:
            # Wave algorithm to peak every 
            pixels.brightness = modifier*fabs(((i+peakpoint) % (2*peakpoint)) - peakpoint) + minimum_brightness
        
        for j in range(SETTINGS_INT_NEOPIXELS):
            index_pixel = (i + j) % SETTINGS_INT_NEOPIXELS
            index_color = j % color_list_count
            pixels[index_pixel] = color_list[index_color]

        if exit_on_connect:
            if ble.connected:
                break

        time.sleep(delay_seconds)
        
    neopixel_reset()


# Display Quick Startup
neopixel_reset()
neopixel_color_swap(COLOR_BLACK, COLOR_WHITE, delay_seconds=0.1, total_seconds=2)


# Setup bluetooth
ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)


# Main loop
while True:
    # set CPXb up so that it can be discovered by the app
    ble.start_advertising(advertisement)
    while not ble.connected:
        
        animation = random.randint(0, 4)
        if animation == 0:
            primary, secondary = get_random_color_pair()
            length = random.randint(4,8)
            delay_seconds = float(random.randint(1,4) / 10)
            neopixel_color_chase(primary=primary, secondary=secondary, length=length, delay_seconds=delay_seconds, total_seconds=20)
        elif animation == 1:
            primary, secondary = get_random_color_pair()
            delay_seconds = float(random.randint(3,10) / 10)
            neopixel_color_swap(primary=primary, secondary=secondary, delay_seconds=delay_seconds, total_seconds=20)
        elif animation == 2:
            primary, secondary = get_random_color_pair()
            pulses = random.randint(4,8)
            neopixel_color_pulse(primary=primary, pulses=pulses, delay_seconds=0.1, total_seconds=20)
        elif animation == 3:
            color_list = get_random_color_list()
            delay_seconds = float(random.randint(3,10) / 10)
            pulses = random.randint(4,8)
            neopixel_colorlist_randomizer(color_list=color_list, delay_seconds=delay_seconds, pulses=pulses, total_seconds=20)
        elif animation == 4:
            color_list = get_random_color_list()
            delay_seconds = float(random.randint(1,4) / 10)
            pulses = random.randint(4,8)
            neopixel_colorlist_chase(color_list=color_list, delay_seconds=delay_seconds, pulses=pulses, total_seconds=20)

        time.sleep(0.5)

    # Now we're connected

    while ble.connected:

        if uart_service.in_waiting:
            try:
                packet = Packet.from_stream(uart_service)
            except ValueError:
                continue # or pass.

            if isinstance(packet, ColorPacket): # check if a color was sent from color picker
                pixels.fill(packet.color)
            if isinstance(packet, ButtonPacket): # check if a button was pressed from control pad
                if packet.pressed:
                    if packet.button == ButtonPacket.BUTTON_1: # if button #1
                        # pixels.fill(BLUE)
                        
                        time.sleep(3)
                        # pixels.fill(BLACK)
                    if packet.button == ButtonPacket.BUTTON_2: # if button #2
                        # pixels.fill(ORANGE)
                        
                        time.sleep(3)
                        # pixels.fill(BLACK)
                    if packet.button == ButtonPacket.BUTTON_3: # if button #3
                        # pixels.fill(PURPLE)
                        
                        time.sleep(2)
                        # pixels.fill(BLACK)
                    if packet.button == ButtonPacket.BUTTON_4: # if button #4
                        # pixels.fill(GREEN)
                        
                        time.sleep(3)
                        # pixels.fill(BLACK)
                    if packet.button == ButtonPacket.UP: # if button UP
                        # pixels.fill(YELLOW)
                        
                        time.sleep(2.6)
                        # pixels.fill(BLACK)
                    if packet.button == ButtonPacket.DOWN: # if button DOWN
                        # pixels.fill(PURPLE)
                        
                        time.sleep(2)
                        # pixels.fill(BLACK)
                    if packet.button == ButtonPacket.LEFT: # if button LEFT
                        # pixels.fill(GREEN)
                        
                        time.sleep(2.5)
                        # pixels.fill(BLACK)
                    if packet.button == ButtonPacket.RIGHT: # if button RIGHT
                        # pixels.fill(ORANGE)
                        
                        time.sleep(2)
                        # pixels.fill(BLACK)
