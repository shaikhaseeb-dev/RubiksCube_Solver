import pygame

# --- UI & 3D Settings ---
WINDOW_SIZE = (1280, 800)

# --- REFINED BLACK & WHITE THEME ---
C_BG = (10, 10, 10)              # Pure Black Background
C_PANEL = (28, 28, 28)           # Dark Gray Panel
C_BORDER = (60, 60, 60)          # Lighter Gray Border
C_TEXT = (235, 235, 235)         # Bright White Text
C_TEXT_DARK = (160, 160, 160)    # Dimmer Text for inactive elements
C_BTN = (44, 44, 44)             # Button Base
C_BTN_HOVER = (70, 70, 70)       # Button Hover
C_ACCENT = (255, 255, 255)       # White Accent for active/highlighted items
C_ACCENT_TEXT = (0, 0, 0)        # Black text for accented buttons

# --- Cube Face Colors ---
COLORS = {
    0: (255, 255, 255),  # U: White
    1: (255, 213, 0),    # D: Yellow
    2: (0, 70, 173),     # L: Blue
    3: (0, 155, 72),     # R: Green
    4: (183, 18, 52),    # F: Red
    5: (255, 88, 0)      # B: Orange
}

# --- Cube Face Indices ---
U, D, L, R, F, B = 0, 1, 2, 3, 4, 5
