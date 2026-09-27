"""Script sinh 15 Avatar Chibi phong cách Retro Pixel Art chuẩn định dạng SVG và PNG thuần Python (Zero external dependencies)."""
import os
import struct
import zlib

AVATAR_DEFS = [
    {
        "id": 1,
        "name": "Warrior",
        "title": "Chiến binh Tri thức",
        "bg_color": "#1a0b12",
        "primary_color": "#ff3366",
        "secondary_color": "#ffd700",
        "skin_color": "#ffd1b3",
        "hair_color": "#4a0e17",
        "acc_symbol": "⚔",
        "helmet": "HORNS",
    },
    {
        "id": 2,
        "name": "Mage",
        "title": "Pháp sư Code",
        "bg_color": "#0d0b24",
        "primary_color": "#7928ca",
        "secondary_color": "#00dfd8",
        "skin_color": "#ffe0bd",
        "hair_color": "#1f104f",
        "acc_symbol": "✦",
        "helmet": "WIZARD_HAT",
    },
    {
        "id": 3,
        "name": "Scholar",
        "title": "Học giả Sách",
        "bg_color": "#081a14",
        "primary_color": "#00ff88",
        "secondary_color": "#ffd700",
        "skin_color": "#ffd1b3",
        "hair_color": "#1b3a2b",
        "acc_symbol": "📖",
        "helmet": "GRAD_CAP",
    },
    {
        "id": 4,
        "name": "Engineer",
        "title": "Kỹ sư Robot",
        "bg_color": "#1c1408",
        "primary_color": "#ff8800",
        "secondary_color": "#00e5ff",
        "skin_color": "#fcd0a1",
        "hair_color": "#332211",
        "acc_symbol": "⚙",
        "helmet": "CYBORG_VISOR",
    },
    {
        "id": 5,
        "name": "Artist",
        "title": "Họa sĩ Pixel",
        "bg_color": "#1f0d1a",
        "primary_color": "#ff007f",
        "secondary_color": "#ffeb3b",
        "skin_color": "#ffe0bd",
        "hair_color": "#e91e63",
        "acc_symbol": "🎨",
        "helmet": "BERET",
    },
    {
        "id": 6,
        "name": "Healer",
        "title": "Bác sĩ Tương lai",
        "bg_color": "#0a1f1c",
        "primary_color": "#00e5ff",
        "secondary_color": "#ffffff",
        "skin_color": "#fde2cf",
        "hair_color": "#164e63",
        "acc_symbol": "✚",
        "helmet": "HEADBAND",
    },
    {
        "id": 7,
        "name": "Alchemist",
        "title": "Nhà Hóa học",
        "bg_color": "#141c08",
        "primary_color": "#a3e635",
        "secondary_color": "#d946ef",
        "skin_color": "#ffd1b3",
        "hair_color": "#365314",
        "acc_symbol": "🧪",
        "helmet": "GOGGLES",
    },
    {
        "id": 8,
        "name": "Strategist",
        "title": "Chiến lược gia Kinh tế",
        "bg_color": "#141126",
        "primary_color": "#fbbf24",
        "secondary_color": "#818cf8",
        "skin_color": "#ffe0bd",
        "hair_color": "#312e81",
        "acc_symbol": "♚",
        "helmet": "CROWN",
    },
    {
        "id": 9,
        "name": "Explorer",
        "title": "Nhà Thám hiểm Ngoại ngữ",
        "bg_color": "#1c180e",
        "primary_color": "#f59e0b",
        "secondary_color": "#10b981",
        "skin_color": "#fcd0a1",
        "hair_color": "#78350f",
        "acc_symbol": "🧭",
        "helmet": "FEDORA",
    },
    {
        "id": 10,
        "name": "Judge",
        "title": "Thẩm phán Luật",
        "bg_color": "#111827",
        "primary_color": "#9ca3af",
        "secondary_color": "#fbbf24",
        "skin_color": "#fde2cf",
        "hair_color": "#374151",
        "acc_symbol": "⚖",
        "helmet": "JUDGE_WIG",
    },
    {
        "id": 11,
        "name": "Architect",
        "title": "Kiến trúc sư",
        "bg_color": "#0c1d2e",
        "primary_color": "#38bdf8",
        "secondary_color": "#facc15",
        "skin_color": "#ffd1b3",
        "hair_color": "#0369a1",
        "acc_symbol": "📐",
        "helmet": "HARDHAT",
    },
    {
        "id": 12,
        "name": "Musician",
        "title": "Nhạc sĩ Giai điệu",
        "bg_color": "#210926",
        "primary_color": "#ec4899",
        "secondary_color": "#06b6d4",
        "skin_color": "#ffe0bd",
        "hair_color": "#831843",
        "acc_symbol": "♫",
        "helmet": "HEADPHONES",
    },
    {
        "id": 13,
        "name": "Astronomer",
        "title": "Nhà Thiên văn",
        "bg_color": "#0a0a23",
        "primary_color": "#818cf8",
        "secondary_color": "#f43f5e",
        "skin_color": "#fde2cf",
        "hair_color": "#1e1b4b",
        "acc_symbol": "★",
        "helmet": "HOOD",
    },
    {
        "id": 14,
        "name": "Ranger",
        "title": "Hướng đạo sinh",
        "bg_color": "#0f2010",
        "primary_color": "#22c55e",
        "secondary_color": "#eab308",
        "skin_color": "#fcd0a1",
        "hair_color": "#14532d",
        "acc_symbol": "🏹",
        "helmet": "ARCHER_CAP",
    },
    {
        "id": 15,
        "name": "Cyber Ninja",
        "title": "Hiệp sĩ ATTT",
        "bg_color": "#18090f",
        "primary_color": "#ff0055",
        "secondary_color": "#00ffcc",
        "skin_color": "#fde2cf",
        "hair_color": "#000000",
        "acc_symbol": "⚡",
        "helmet": "NINJA_MASK",
    },
]


def create_svg_avatar(char: dict) -> str:
    """Tạo file SVG pixel art retro chibi đẹp mắt."""
    name = char["name"]
    title = char["title"]
    bg = char["bg_color"]
    prim = char["primary_color"]
    sec = char["secondary_color"]
    skin = char["skin_color"]
    hair = char["hair_color"]
    symbol = char["acc_symbol"]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <filter id="glow-{char['id']}" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="1.5" flood-color="{prim}" flood-opacity="0.8"/>
    </filter>
  </defs>

  <!-- Background Shield -->
  <rect x="0" y="0" width="64" height="64" rx="8" fill="{bg}"/>
  <rect x="2" y="2" width="60" height="60" rx="6" fill="none" stroke="{prim}" stroke-width="2" opacity="0.6"/>

  <!-- Body / Cloak -->
  <rect x="18" y="44" width="28" height="16" fill="{prim}" rx="2"/>
  <rect x="24" y="46" width="16" height="14" fill="{sec}" opacity="0.3"/>

  <!-- Head Base -->
  <rect x="16" y="18" width="32" height="26" fill="{skin}" rx="4"/>

  <!-- Hair / Helmet Base -->
  <rect x="14" y="12" width="36" height="12" fill="{hair}" rx="2"/>
  <rect x="12" y="16" width="6" height="16" fill="{hair}"/>
  <rect x="46" y="16" width="6" height="16" fill="{hair}"/>

  <!-- Distinct Class Hat / Helmet Accent -->
  <rect x="22" y="6" width="20" height="8" fill="{prim}" filter="url(#glow-{char['id']})"/>
  <rect x="26" y="4" width="12" height="4" fill="{sec}"/>

  <!-- Big Chibi Eyes -->
  <!-- Left Eye -->
  <rect x="20" y="26" width="7" height="9" fill="#000000" rx="1"/>
  <rect x="21" y="27" width="3" height="3" fill="#ffffff"/>
  <rect x="23" y="31" width="2" height="2" fill="{sec}"/>

  <!-- Right Eye -->
  <rect x="37" y="26" width="7" height="9" fill="#000000" rx="1"/>
  <rect x="38" y="27" width="3" height="3" fill="#ffffff"/>
  <rect x="40" y="31" width="2" height="2" fill="{sec}"/>

  <!-- Cheeks Blush -->
  <rect x="17" y="34" width="5" height="2" fill="#ff77aa" opacity="0.6"/>
  <rect x="42" y="34" width="5" height="2" fill="#ff77aa" opacity="0.6"/>

  <!-- Mouth -->
  <rect x="30" y="36" width="4" height="2" fill="#aa4444"/>

  <!-- Class Crest Badge -->
  <circle cx="32" cy="52" r="6" fill="#0a0a1a" stroke="{sec}" stroke-width="1.5"/>
  <text x="32" y="55" font-family="'Press Start 2P', monospace, sans-serif" font-size="7" fill="{sec}" text-anchor="middle" font-weight="bold">{symbol}</text>

  <!-- Level / Hero ID badge -->
  <rect x="44" y="4" width="16" height="10" fill="#0a0a1a" rx="2" stroke="{prim}" stroke-width="1"/>
  <text x="52" y="11" font-family="'Press Start 2P', monospace, sans-serif" font-size="5" fill="{prim}" text-anchor="middle">#{char['id']}</text>
</svg>"""


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def write_png_file(filepath: str, width: int, height: int, pixels: list[tuple[int, int, int, int]]):
    """Ghi file PNG thuần Python sử dụng zlib và struct."""
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # Filter type None
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            raw_data.extend([r, g, b, a])

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(raw_data, 9))
    iend = chunk(b"IEND", b"")

    with open(filepath, "wb") as f:
        f.write(header + ihdr + idat + iend)


def create_png_avatar(char: dict, filepath: str):
    """Sinh file PNG 64x64 pixel art tương ứng với char."""
    width, height = 64, 64
    bg_r, bg_g, bg_b = hex_to_rgb(char["bg_color"])
    p_r, p_g, p_b = hex_to_rgb(char["primary_color"])
    s_r, s_g, s_b = hex_to_rgb(char["secondary_color"])
    sk_r, sk_g, sk_b = hex_to_rgb(char["skin_color"])
    h_r, h_g, h_b = hex_to_rgb(char["hair_color"])

    pixels = [(bg_r, bg_g, bg_b, 255)] * (width * height)

    def set_pixel(x, y, r, g, b, a=255):
        if 0 <= x < width and 0 <= y < height:
            pixels[y * width + x] = (r, g, b, a)

    def fill_rect(x1, y1, w, h, r, g, b, a=255):
        for y in range(y1, y1 + h):
            for x in range(x1, x1 + w):
                set_pixel(x, y, r, g, b, a)

    # Outer border
    for x in range(2, 62):
        set_pixel(x, 2, p_r, p_g, p_b)
        set_pixel(x, 61, p_r, p_g, p_b)
    for y in range(2, 62):
        set_pixel(2, y, p_r, p_g, p_b)
        set_pixel(61, y, p_r, p_g, p_b)

    # Body
    fill_rect(18, 44, 28, 16, p_r, p_g, p_b)
    fill_rect(24, 46, 16, 12, s_r, s_g, s_b)

    # Head
    fill_rect(16, 18, 32, 26, sk_r, sk_g, sk_b)

    # Hair / Helmet
    fill_rect(14, 12, 36, 10, h_r, h_g, h_b)
    fill_rect(12, 16, 6, 16, h_r, h_g, h_b)
    fill_rect(46, 16, 6, 16, h_r, h_g, h_b)

    # Hat Crown Accent
    fill_rect(22, 6, 20, 8, p_r, p_g, p_b)
    fill_rect(26, 4, 12, 4, s_r, s_g, s_b)

    # Eyes
    fill_rect(20, 26, 7, 9, 0, 0, 0)
    fill_rect(21, 27, 3, 3, 255, 255, 255)
    fill_rect(23, 31, 2, 2, s_r, s_g, s_b)

    fill_rect(37, 26, 7, 9, 0, 0, 0)
    fill_rect(38, 27, 3, 3, 255, 255, 255)
    fill_rect(40, 31, 2, 2, s_r, s_g, s_b)

    # Blush
    fill_rect(17, 34, 5, 2, 255, 120, 170)
    fill_rect(42, 34, 5, 2, 255, 120, 170)

    # Mouth
    fill_rect(30, 36, 4, 2, 180, 60, 60)

    write_png_file(filepath, width, height, pixels)


def main():
    target_dirs = [
        os.path.abspath("c:/Users/duybu/ruybk/code/forfriend/frontend/forfriend/assets/avatars"),
        os.path.abspath("c:/Users/duybu/ruybk/code/forfriend/frontend/assets/avatars"),
    ]

    for d in target_dirs:
        os.makedirs(d, exist_ok=True)
        for char in AVATAR_DEFS:
            cid = char["id"]
            # 1. Write SVG
            svg_content = create_svg_avatar(char)
            svg_path = os.path.join(d, f"avatar_{cid}.svg")
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)

            # 2. Write PNG with multiple name variants
            png_path1 = os.path.join(d, f"avatar_{cid}.png")
            png_path2 = os.path.join(d, f"avatar-{cid:02d}.png")
            create_png_avatar(char, png_path1)
            create_png_avatar(char, png_path2)

        print(f"Generated 15 avatars in {d}")


if __name__ == "__main__":
    main()
