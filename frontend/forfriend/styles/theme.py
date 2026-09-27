"""Design tokens và Theme cấu hình phong cách Neo-Cyber Student (Discord Nitro + Raycast Gaming Hub)."""

# Bảng màu Neo-Cyber Student (Obsidian Canvas + Electric Mint & Cyan Glow)
COLORS = {
    "bg_dark": "#0b1319",                        # Deep Sleek Obsidian Teal Canvas
    "bg_primary": "#0b1319",
    "bg_secondary": "#0e1a22",                   # Dark Slate Navy
    "bg_card": "#13222a",                        # Card Slate Navy
    "bg_card_hover": "#182c36",                  # Card hover state
    "bg_panel": "#101d24",                       # Panel background
    "neon_green": "#2ceaa3",                     # Vibrant Mint Green (Mockup Primary)
    "accent_primary": "#2ceaa3",
    "neon_cyan": "#00d2ff",                      # Cyan Glow (Mockup Secondary)
    "accent_secondary": "#00d2ff",
    "neon_pink": "#f43f5e",                      # Cyber Berry
    "accent_tertiary": "#f43f5e",
    "neon_gold": "#fbbf24",                      # Star Rating Gold
    "accent_gold": "#fbbf24",
    "neon_purple": "#8b5cf6",                    # Electric Violet
    "accent_purple": "#8b5cf6",
    "text_main": "#ffffff",                      # Crisp Pure White
    "text_primary": "#ffffff",
    "text_muted": "#8fa0ad",                     # Slate Muted Text
    "text_secondary": "#8fa0ad",
    "border_color": "rgba(44, 234, 163, 0.15)",  # Subtle mint border
    "border": "rgba(44, 234, 163, 0.15)",
    "border_glow": "rgba(44, 234, 163, 0.35)",
    "danger": "#f43f5e",
    "warning": "#fbbf24",
    "success": "#2ceaa3",
}

# Alias lowercase
colors = COLORS

# Typography
FONTS = {
    "heading": "'Outfit', -apple-system, BlinkMacSystemFont, sans-serif",
    "ui": "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif",
    "body": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    "pixel": "'Press Start 2P', monospace",
}
fonts = FONTS

# Shadows & Modern Glows
RETRO_BORDER = f"1px solid {COLORS['neon_green']}"
RETRO_BOX_SHADOW = f"0 4px 20px rgba(0, 245, 155, 0.25)"
RETRO_BOX_SHADOW_PINK = f"0 4px 20px rgba(244, 63, 94, 0.25)"
RETRO_BOX_SHADOW_CYAN = f"0 4px 20px rgba(0, 210, 255, 0.25)"

game_card_style = {
    "background_color": "#13222a",
    "backdrop_filter": "blur(20px)",
    "-webkit-backdrop-filter": "blur(20px)",
    "border": "1px solid rgba(44, 234, 163, 0.16)",
    "border_radius": "16px",
    "padding": "20px",
    "box_shadow": "0 8px 30px rgba(0, 0, 0, 0.35)",
    "transition": "all 200ms ease",
    "_hover": {
        "border_color": "rgba(44, 234, 163, 0.35)",
        "box_shadow": "0 10px 25px rgba(0, 0, 0, 0.5), 0 0 15px rgba(44, 234, 163, 0.12)",
        "transform": "translateY(-2px)",
    },
}

btn_primary_style = {
    "font_family": FONTS["ui"],
    "font_size": "13px",
    "font_weight": "700",
    "padding": "9px 18px",
    "background": "#2ceaa3",
    "color": "#0b1319",
    "border": "none",
    "border_radius": "8px",
    "cursor": "pointer",
    "letter_spacing": "0.3px",
    "box_shadow": "0 2px 12px rgba(44, 234, 163, 0.35)",
    "transition": "all 150ms ease",
    "_hover": {
        "background": "#24d493",
        "box_shadow": "0 4px 18px rgba(44, 234, 163, 0.5)",
        "transform": "translateY(-1px)",
    },
    "_active": {
        "transform": "translateY(0)",
    },
}

btn_secondary_style = {
    "font_family": FONTS["ui"],
    "font_size": "13px",
    "font_weight": "600",
    "padding": "8px 16px",
    "background_color": "transparent",
    "color": "#ffffff",
    "border": "1px solid rgba(255, 255, 255, 0.15)",
    "border_radius": "8px",
    "cursor": "pointer",
    "letter_spacing": "0.2px",
    "transition": "all 150ms ease",
    "_hover": {
        "background_color": "rgba(255, 255, 255, 0.06)",
        "border_color": "rgba(44, 234, 163, 0.4)",
        "color": "#2ceaa3",
    },
    "_active": {
        "transform": "translateY(0)",
    },
}

btn_pink_style = {
    "font_family": FONTS["ui"],
    "font_size": "13px",
    "font_weight": "700",
    "padding": "10px 20px",
    "background": "linear-gradient(135deg, #f43f5e 0%, #e11d48 100%)",
    "color": "#ffffff",
    "border": "none",
    "border_radius": "10px",
    "cursor": "pointer",
    "letter_spacing": "0.3px",
    "box_shadow": "0 4px 18px rgba(244, 63, 94, 0.35)",
    "transition": "all 200ms ease",
    "_hover": {
        "transform": "translateY(-2px)",
        "box_shadow": "0 6px 24px rgba(244, 63, 94, 0.5)",
        "filter": "brightness(1.08)",
    },
    "_active": {
        "transform": "translateY(0)",
    },
}

# Input style: KHÔNG dùng outer vertical padding làm ép bẹp chữ, dùng height="44px"
game_input_style = {
    "background_color": "rgba(11, 15, 25, 0.85)",
    "border": "1px solid rgba(255, 255, 255, 0.12)",
    "color": COLORS["text_main"],
    "font_family": FONTS["ui"],
    "font_size": "14px",
    "border_radius": "10px",
    "height": "44px",
    "width": "100%",
    "transition": "all 200ms ease",
    "_focus_within": {
        "border_color": COLORS["neon_green"],
        "box_shadow": "0 0 0 3px rgba(0, 245, 155, 0.2)",
    },
}

GLOBAL_STYLES = {
    "::selection": {
        "background_color": COLORS["neon_green"],
        "color": "#04120a",
    },
    "body": {
        "background_color": COLORS["bg_dark"],
        "color": COLORS["text_main"],
        "font_family": FONTS["ui"],
        "margin": "0",
        "padding": "0",
    },
}
