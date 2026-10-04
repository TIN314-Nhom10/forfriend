"""
Script sinh toàn bộ hình ảnh minh họa chất lượng cao cho Báo Cáo Dự Án ForFriend.
- Logo ForFriend sử dụng biểu tượng Green Owl chính thức của Home Page (KHÔNG dùng avatar chibi).
- Toàn bộ giao diện người dùng (Home Page / Feed, Register, Create Quest, Virtual Room, Profile & Chat) 
  được trình bày hoàn toàn bằng TIẾNG ANH (English) theo yêu cầu.
- Render bằng Chrome Headless ở độ phân giải Retina cao (1.5x / 2.0x scale).
"""

import os
import subprocess
from PIL import Image

ASSETS_DIR = os.path.abspath("report_assets")
AVATARS_DIR = os.path.abspath(r"frontend/forfriend/assets/avatars")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(ASSETS_DIR, exist_ok=True)

def render_html_to_png(html_content, output_png_path, width=1366, height=768, scale=1.5):
    temp_html = os.path.join(ASSETS_DIR, "temp_render.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--force-device-scale-factor={scale}",
        f"--window-size={width},{height}",
        f"--screenshot={output_png_path}",
        temp_html
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Rendered: {output_png_path} ({os.path.getsize(output_png_path)} bytes)")

OWL_SVG_LARGE = """
<svg width="68" height="68" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 5C12.82 5 7 10.82 7 18C7 26.5 12.5 33 20 35C27.5 33 33 26.5 33 18C33 10.82 27.18 5 20 5Z" fill="#101d24" stroke="#2ceaa3" stroke-width="2.6"/>
    <path d="M9 10.5C11 7.5 14 6 17 6" stroke="#2ceaa3" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M31 10.5C29 7.5 26 6 23 6" stroke="#2ceaa3" stroke-width="2.6" stroke-linecap="round"/>
    <circle cx="15" cy="18" r="4.8" stroke="#2ceaa3" stroke-width="2.2" fill="#0b1319"/>
    <circle cx="15" cy="18" r="2.2" fill="#2ceaa3"/>
    <circle cx="25" cy="18" r="4.8" stroke="#2ceaa3" stroke-width="2.2" fill="#0b1319"/>
    <circle cx="25" cy="18" r="2.2" fill="#2ceaa3"/>
    <path d="M18.2 21.5L20 24.5L21.8 21.5" stroke="#2ceaa3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M15.5 28.5C17.5 30.2 22.5 30.2 24.5 28.5" stroke="#2ceaa3" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

OWL_SVG_HEADER = """
<svg width="34" height="34" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 6C13.3726 6 8 11.3726 8 18C8 26 13 32 20 34C27 32 32 26 32 18C32 11.3726 26.6274 6 20 6Z" fill="#13222a" stroke="#2ceaa3" stroke-width="2.5"/>
    <path d="M10 11C11.5 8 14.5 6.5 17 6.5" stroke="#2ceaa3" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M30 11C28.5 8 25.5 6.5 23 6.5" stroke="#2ceaa3" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="15.5" cy="18" r="4.5" stroke="#2ceaa3" stroke-width="2" fill="#0b1319"/>
    <circle cx="15.5" cy="18" r="2" fill="#2ceaa3"/>
    <circle cx="24.5" cy="18" r="4.5" stroke="#2ceaa3" stroke-width="2" fill="#0b1319"/>
    <circle cx="24.5" cy="18" r="2" fill="#2ceaa3"/>
    <path d="M18.5 21L20 24L21.5 21" stroke="#2ceaa3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M16 28C18 29.5 22 29.5 24 28" stroke="#2ceaa3" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""

COMMON_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=Press+Start+2P&display=swap');

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    background-color: #0b1319;
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
}}

.pixel-font {{
    font-family: 'Press Start 2P', monospace;
}}

.outfit {{
    font-family: 'Outfit', sans-serif;
}}

.glass-card {{
    background: #13222a;
    border: 1px solid rgba(44, 234, 163, 0.16);
    border-radius: 14px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}}

.neon-mint {{
    color: #2ceaa3;
}}

.neon-cyan {{
    color: #00d2ff;
}}

.neon-pink {{
    color: #f43f5e;
}}

.neon-gold {{
    color: #fbbf24;
}}

.btn-primary {{
    background: #2ceaa3;
    color: #0b1319;
    font-weight: 700;
    padding: 9px 18px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-size: 13px;
    box-shadow: 0 2px 12px rgba(44, 234, 163, 0.35);
    display: inline-flex;
    align-items: center;
    gap: 8px;
}}

.btn-secondary {{
    background: rgba(255, 255, 255, 0.05);
    color: #ffffff;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    cursor: pointer;
    font-size: 13px;
}}

.badge {{
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    display: inline-block;
}}

.badge-mint {{
    background: rgba(44, 234, 163, 0.15);
    color: #2ceaa3;
    border: 1px solid rgba(44, 234, 163, 0.3);
}}

.badge-cyan {{
    background: rgba(0, 210, 255, 0.15);
    color: #00d2ff;
    border: 1px solid rgba(0, 210, 255, 0.3);
}}

.badge-gold {{
    background: rgba(251, 191, 36, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(251, 191, 36, 0.3);
}}

.badge-pink {{
    background: rgba(244, 63, 94, 0.15);
    color: #f43f5e;
    border: 1px solid rgba(244, 63, 94, 0.3);
}}
"""

def generate_logo():
    """Tạo logo chính thức với Green Owl Icon từ Home Page, loại bỏ avatar chibi."""
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: radial-gradient(circle at center, #132734 0%, #0b1319 75%);
    padding: 20px;
}}
.logo-container {{
    display: flex;
    align-items: center;
    gap: 28px;
    padding: 28px 48px;
    background: rgba(19, 34, 42, 0.92);
    border: 2px solid rgba(44, 234, 163, 0.35);
    border-radius: 24px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.65), 0 0 35px rgba(44, 234, 163, 0.25);
}}
.owl-box {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 90px;
    height: 90px;
    background: #0e1a22;
    border: 2px solid #2ceaa3;
    border-radius: 20px;
    box-shadow: 0 0 25px rgba(44, 234, 163, 0.45);
}}
.title-box {{
    display: flex;
    flex-direction: column;
}}
.brand-name {{
    font-family: 'Outfit', sans-serif;
    font-size: 52px;
    font-weight: 900;
    letter-spacing: 0.5px;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 6px;
    line-height: 1;
    margin-bottom: 8px;
}}
.tagline {{
    font-family: 'Outfit', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #2ceaa3;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 4px;
}}
.sub-tagline {{
    font-size: 13px;
    color: #8fa0ad;
    font-weight: 500;
}}
</style>
</head>
<body>
<div class="logo-container">
    <div class="owl-box">
        {OWL_SVG_LARGE}
    </div>
    <div class="title-box">
        <div class="brand-name">ForFriend</div>
        <div class="tagline">STUDENT STUDY BUDDY & VIRTUAL ROOM PLATFORM</div>
        <div class="sub-tagline">Peer-to-peer campus networking & integrated video study rooms for students</div>
    </div>
</div>
</body>
</html>"""
    out_path = os.path.join(ASSETS_DIR, "forfriend_logo.png")
    render_html_to_png(html, out_path, width=980, height=250, scale=2.0)

def generate_screen_02_feed():
    """Tái tạo chính xác 100% màn hình Home Page / Feed từ ảnh thực tế của web app với ngôn ngữ Tiếng Anh."""
    av1 = os.path.join(AVATARS_DIR, "avatar-01.png").replace("\\", "/")
    av2 = os.path.join(AVATARS_DIR, "avatar-02.png").replace("\\", "/")
    av3 = os.path.join(AVATARS_DIR, "avatar-03.png").replace("\\", "/")
    av4 = os.path.join(AVATARS_DIR, "avatar-04.png").replace("\\", "/")

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    background: #070d12;
    display: flex;
    height: 100vh;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

/* Sidebar Trái */
.sidebar {{
    width: 220px;
    background: #0b1319;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    flex-direction: column;
    padding: 16px 14px;
}}
.sidebar-logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 16px;
}}
.sidebar-logo h1 {{
    font-family: 'Outfit', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
}}
.nav-list {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}
.nav-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #8fa0ad;
    text-decoration: none;
    cursor: pointer;
}}
.nav-item.active {{
    background: rgba(44, 234, 163, 0.12);
    color: #2ceaa3;
    border: 1px solid rgba(44, 234, 163, 0.25);
}}
.nav-item:hover {{
    color: #ffffff;
}}
.bottom-user-card {{
    margin-top: auto;
    background: #101d24;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 12px;
}}
.user-row {{
    display: flex;
    align-items: center;
    gap: 10px;
}}
.user-avatar-wrap {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 2px solid #2ceaa3;
    overflow: hidden;
    background: #0b1319;
}}
.user-avatar-wrap img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}
.btn-logout {{
    width: 100%;
    background: rgba(244, 63, 94, 0.1);
    border: 1px solid rgba(244, 63, 94, 0.3);
    color: #f43f5e;
    font-size: 11px;
    font-weight: 700;
    padding: 6px;
    border-radius: 6px;
    cursor: pointer;
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}}

/* Main Content Area */
.main-wrapper {{
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}}

/* Top Search Bar Header */
.top-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 28px;
    background: #0b1319;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}}
.search-input-box {{
    display: flex;
    align-items: center;
    gap: 10px;
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 8px 18px;
    width: 440px;
}}
.search-input-box input {{
    background: transparent;
    border: none;
    color: #fff;
    font-size: 13px;
    width: 100%;
    outline: none;
}}
.top-right-user {{
    display: flex;
    align-items: center;
    gap: 16px;
}}
.bell-btn {{
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 7px 10px;
    color: #fbbf24;
    cursor: pointer;
}}
.user-pill {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 4px 12px 4px 6px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
}}
.user-pill img {{
    width: 26px;
    height: 26px;
    border-radius: 50%;
    border: 1px solid #2ceaa3;
}}

/* Layout Body (Feed Grid + Right Column) */
.page-body {{
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 22px;
    padding: 22px 28px;
}}

/* Filter Bar */
.filter-container {{
    background: #101d24;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}}
.filters-row {{
    display: flex;
    align-items: center;
    gap: 12px;
}}
.filter-dropdown {{
    display: flex;
    flex-direction: column;
    gap: 3px;
}}
.filter-label {{
    font-size: 10px;
    color: #8fa0ad;
    text-transform: uppercase;
    font-weight: 700;
}}
.filter-select {{
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 5px 10px;
    color: #fff;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
}}
.pill-active {{
    background: #2ceaa3;
    color: #0b1319;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 12px;
    border: none;
    cursor: pointer;
}}

/* Quest Cards 2-Col Grid */
.quest-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}}
.quest-item-card {{
    background: #13222a;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 220px;
}}
.q-badge-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}}
.q-category {{
    color: #2ceaa3;
    font-size: 11px;
    font-weight: 700;
}}
.q-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
}}
.q-author-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}}
.q-author-avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 1px solid rgba(44, 234, 163, 0.4);
}}
.q-author-name {{
    font-size: 13px;
    font-weight: 700;
}}
.q-author-uni {{
    font-size: 11px;
    color: #8fa0ad;
}}
.q-snippet {{
    font-size: 12px;
    color: #cbd5e1;
    line-height: 1.4;
    margin-bottom: 12px;
}}
.q-tags {{
    display: flex;
    gap: 6px;
    margin-bottom: 14px;
}}
.q-tag {{
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #8fa0ad;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 4px;
}}
.q-actions {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 12px;
}}
.btn-view {{
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #fff;
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
}}
.btn-join {{
    background: #2ceaa3;
    border: none;
    color: #0b1319;
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
}}
.btn-del {{
    background: rgba(244, 63, 94, 0.15);
    border: 1px solid rgba(244, 63, 94, 0.3);
    color: #f43f5e;
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
}}

/* Right Column Widgets */
.right-col {{
    display: flex;
    flex-direction: column;
    gap: 18px;
}}
.hero-status-widget {{
    background: #101d24;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}}
.hero-avatar-big {{
    width: 82px;
    height: 82px;
    border-radius: 50%;
    border: 3px solid #2ceaa3;
    box-shadow: 0 0 20px rgba(44, 234, 163, 0.35);
    margin: 0 auto 12px auto;
    display: block;
}}
.hero-welcome {{
    font-family: 'Outfit', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: #fff;
    margin-bottom: 2px;
}}
.hero-sub {{
    font-size: 12px;
    color: #2ceaa3;
    font-weight: 700;
    margin-bottom: 12px;
}}
.exp-bar {{
    background: #0e1a22;
    border-radius: 10px;
    height: 6px;
    overflow: hidden;
    margin-bottom: 12px;
}}
.exp-fill {{
    background: #2ceaa3;
    height: 100%;
    width: 72%;
}}
.hero-bio {{
    font-size: 11px;
    color: #8fa0ad;
    line-height: 1.4;
}}
.widget-panel {{
    background: #101d24;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
}}
.widget-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 12px;
}}
.contact-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
}}
</style>
</head>
<body>
    <!-- Cột Trái Sidebar -->
    <div class="sidebar">
        <div class="sidebar-logo">
            {OWL_SVG_HEADER}
            <h1>ForFriend</h1>
        </div>
        <div class="nav-list">
            <div class="nav-item">🏠 Dashboard</div>
            <div class="nav-item active">🔍 Discover Partners</div>
            <div class="nav-item">👥 Study Groups</div>
            <div class="nav-item">💬 Messages</div>
            <div class="nav-item">👤 Profile</div>
            <div class="nav-item">⚙️ Settings</div>
        </div>
        <div class="bottom-user-card">
            <div class="user-row">
                <div class="user-avatar-wrap">
                    <img src="file:///{av1}" />
                </div>
                <div>
                    <div style="font-size: 12px; font-weight: 700;">Nguyễn Văn A</div>
                    <div style="font-size: 10px; color: #2ceaa3;">🟢 ONLINE</div>
                </div>
            </div>
            <button class="btn-logout">🚪 Logout</button>
        </div>
    </div>

    <!-- Khung Nội Dung Chính -->
    <div class="main-wrapper">
        <!-- Top Header -->
        <div class="top-header">
            <div class="search-input-box">
                <span style="color: #8fa0ad;">🔍</span>
                <input placeholder="Search for partners, subjects, or quests..." />
            </div>
            <div class="top-right-user">
                <div class="bell-btn">🔔</div>
                <div class="user-pill">
                    <img src="file:///{av1}" />
                    <span>Nguyễn Văn A ▾</span>
                </div>
            </div>
        </div>

        <!-- Body: Filters + Feed + Right Column -->
        <div class="page-body">
            <div>
                <!-- Filter Bar -->
                <div class="filter-container">
                    <div class="filters-row">
                        <div class="filter-dropdown">
                            <span class="filter-label">Subject</span>
                            <div class="filter-select">All Subjects ▾</div>
                        </div>
                        <div class="filter-dropdown">
                            <span class="filter-label">Level</span>
                            <div class="filter-select">All Levels ▾</div>
                        </div>
                        <div class="filter-dropdown">
                            <span class="filter-label">Time Zone</span>
                            <div class="filter-select">All ▾</div>
                        </div>
                        <div class="filter-dropdown">
                            <span class="filter-label">Availability</span>
                            <div class="filter-select">▾</div>
                        </div>
                        <div class="filter-dropdown">
                            <span class="filter-label">Schedule</span>
                            <button class="pill-active">Weekly</button>
                        </div>
                    </div>
                    <button class="btn-primary" style="font-size: 12px; padding: 7px 14px;">+ Post Quest</button>
                </div>

                <!-- Quest Cards Grid -->
                <div class="quest-grid">
                    <!-- Card 1 -->
                    <div class="quest-item-card">
                        <div>
                            <div class="q-badge-row">
                                <span class="q-category">Study Quest</span>
                                <span style="color: #8fa0ad; cursor: pointer;">•••</span>
                            </div>
                            <div class="q-title">test</div>
                            <div class="q-author-row">
                                <img class="q-author-avatar" src="file:///{av1}" />
                                <div>
                                    <div class="q-author-name">Nguyễn Văn A</div>
                                    <div class="q-author-uni">Uni: Đại học Ngoại Thương Hà Nội <span style="color: #fbbf24; font-weight:700;">4.9★</span></div>
                                </div>
                            </div>
                            <div class="q-snippet">test cái</div>
                            <div class="q-tags">
                                <span class="q-tag">python</span>
                                <span class="q-tag">math</span>
                                <span class="q-tag">ai</span>
                            </div>
                        </div>
                        <div class="q-actions">
                            <button class="btn-view">View Details</button>
                            <button class="btn-del">🗑 Delete</button>
                        </div>
                    </div>

                    <!-- Card 2 -->
                    <div class="quest-item-card">
                        <div>
                            <div class="q-badge-row">
                                <span class="q-category">Study Quest</span>
                                <span style="color: #8fa0ad; cursor: pointer;">•••</span>
                            </div>
                            <div class="q-title">History Essay</div>
                            <div class="q-author-row">
                                <img class="q-author-avatar" src="file:///{av2}" />
                                <div>
                                    <div class="q-author-name">Anya L.</div>
                                    <div class="q-author-uni">Uni: Writing <span style="color: #fbbf24; font-weight:700;">5★</span></div>
                                </div>
                            </div>
                            <div class="q-snippet">History essay and descriptions to students' problemic history, mister combination.</div>
                            <div class="q-tags">
                                <span class="q-tag">History</span>
                                <span class="q-tag">Research</span>
                                <span class="q-tag">Daytime</span>
                            </div>
                        </div>
                        <div class="q-actions">
                            <button class="btn-view">View Details</button>
                            <button class="btn-join">Request Join</button>
                        </div>
                    </div>

                    <!-- Card 3 -->
                    <div class="quest-item-card">
                        <div>
                            <div class="q-badge-row">
                                <span class="q-category">Study Quest</span>
                                <span style="color: #8fa0ad; cursor: pointer;">•••</span>
                            </div>
                            <div class="q-title">Python Project: AI Chatbot</div>
                            <div class="q-author-row">
                                <img class="q-author-avatar" src="file:///{av3}" />
                                <div>
                                    <div class="q-author-name">Liam M.</div>
                                    <div class="q-author-uni">Uni: Gaming headphones <span style="color: #fbbf24; font-weight:700;">5★</span></div>
                                </div>
                            </div>
                            <div class="q-snippet">Python project of - AI Chatbot in Python for a term project, know basic API integration.</div>
                            <div class="q-tags">
                                <span class="q-tag">Python</span>
                                <span class="q-tag">AI</span>
                                <span class="q-tag">FastAPI</span>
                            </div>
                        </div>
                        <div class="q-actions">
                            <button class="btn-view">View Details</button>
                            <button class="btn-join">Request Join</button>
                        </div>
                    </div>

                    <!-- Card 4 -->
                    <div class="quest-item-card">
                        <div>
                            <div class="q-badge-row">
                                <span class="q-category">Study Quest</span>
                                <span style="color: #8fa0ad; cursor: pointer;">•••</span>
                            </div>
                            <div class="q-title">Math Prep: Calculus II</div>
                            <div class="q-author-row">
                                <img class="q-author-avatar" src="file:///{av4}" />
                                <div>
                                    <div class="q-author-name">Chloe T.</div>
                                    <div class="q-author-uni">Uni: Reading <span style="color: #fbbf24; font-weight:700;">4.9★</span></div>
                                </div>
                            </div>
                            <div class="q-snippet">Reading study partners to find reviewer channels for math and midterm calculus test.</div>
                            <div class="q-tags">
                                <span class="q-tag">Math</span>
                                <span class="q-tag">Calculus</span>
                                <span class="q-tag">Offline</span>
                            </div>
                        </div>
                        <div class="q-actions">
                            <button class="btn-view">View Details</button>
                            <button class="btn-join">Request Join</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Cột Phải Widgets -->
            <div class="right-col">
                <div class="hero-status-widget">
                    <img class="hero-avatar-big" src="file:///{av1}" />
                    <div class="hero-welcome">Welcome, Nguyễn Văn A</div>
                    <div class="hero-sub">Level 14 Study Hero</div>
                    <div class="exp-bar">
                        <div class="exp-fill"></div>
                    </div>
                    <div class="hero-bio">
                        Bio, cute chibi cat, gaming headset, and master unique study partners.
                    </div>
                </div>

                <div class="widget-panel">
                    <div class="widget-head">
                        <span>Active Quests</span>
                        <span style="color: #2ceaa3; font-size: 11px; cursor: pointer;">View all</span>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <img src="file:///{av3}" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #2ceaa3;" />
                            <div>
                                <div style="font-size: 12px; font-weight: 700;">Liam M.</div>
                                <div style="font-size: 10px; color: #2ceaa3;">Math Prep: Calculus II</div>
                            </div>
                        </div>
                        <span style="color: #8fa0ad;">›</span>
                    </div>
                </div>

                <div class="widget-panel">
                    <div class="widget-head">
                        <span>Recent Contacts</span>
                    </div>
                    <div class="contact-item">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <img src="file:///{av3}" style="width: 28px; height: 28px; border-radius: 50%;" />
                            <div>
                                <div style="font-size: 12px; font-weight: 700;">Liam M.</div>
                                <div style="font-size: 10px; color: #8fa0ad;">Gaming Hub</div>
                            </div>
                        </div>
                        <span class="badge badge-mint" style="font-size: 9px;">Online</span>
                    </div>
                    <div class="contact-item">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <img src="file:///{av4}" style="width: 28px; height: 28px; border-radius: 50%;" />
                            <div>
                                <div style="font-size: 12px; font-weight: 700;">Chloe T.</div>
                                <div style="font-size: 10px; color: #8fa0ad;">Reading</div>
                            </div>
                        </div>
                        <span class="badge badge-cyan" style="font-size: 9px;">Active</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    out_path = os.path.join(ASSETS_DIR, "screen_02_quest_feed.png")
    render_html_to_png(html, out_path, width=1366, height=768, scale=1.5)

def generate_screen_01_register():
    """Màn hình Đăng ký / Hero Creation bằng Tiếng Anh."""
    avatar_items = ""
    for i in range(1, 16):
        num_str = f"{i:02d}"
        path = os.path.join(AVATARS_DIR, f"avatar-{num_str}.png").replace("\\", "/")
        is_selected = (i == 1)
        sel_class = "selected-avatar" if is_selected else ""
        badge = '<div class="sel-badge">SELECTED</div>' if is_selected else ""
        avatar_items += f"""
        <div class="avatar-item {sel_class}">
            <img src="file:///{path}" />
            <div class="avatar-num">Hero #{i}</div>
            {badge}
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    background: #0b1319;
    padding: 24px;
}}
.top-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #101d24;
    border: 1px solid rgba(44, 234, 163, 0.2);
    border-radius: 12px;
    padding: 12px 24px;
    margin-bottom: 24px;
}}
.logo-area {{
    display: flex;
    align-items: center;
    gap: 10px;
}}
.logo-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
}}
.page-title {{
    text-align: center;
    margin-bottom: 24px;
}}
.page-title h1 {{
    font-family: 'Outfit', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
}}
.page-title p {{
    color: #8fa0ad;
    font-size: 14px;
    margin-top: 4px;
}}
.register-layout {{
    display: grid;
    grid-template-columns: 1fr 1.35fr;
    gap: 24px;
    max-width: 1240px;
    margin: 0 auto;
}}
.form-card {{
    padding: 24px;
}}
.form-group {{
    margin-bottom: 14px;
}}
.form-group label {{
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: #cbd5e1;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.form-input {{
    width: 100%;
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    padding: 10px 14px;
    color: #ffffff;
    font-size: 13px;
}}
.grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}}
.avatar-section {{
    padding: 24px;
}}
.avatar-section-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}}
.avatar-section-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: #2ceaa3;
}}
.avatars-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
}}
.avatar-item {{
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 8px 6px;
    text-align: center;
    position: relative;
    cursor: pointer;
    transition: all 0.2s;
}}
.avatar-item img {{
    width: 58px;
    height: 58px;
    object-fit: contain;
}}
.avatar-num {{
    font-size: 10px;
    font-weight: 700;
    color: #8fa0ad;
    margin-top: 4px;
}}
.selected-avatar {{
    border: 2px solid #2ceaa3;
    background: rgba(44, 234, 163, 0.1);
    box-shadow: 0 0 16px rgba(44, 234, 163, 0.4);
}}
.selected-avatar .avatar-num {{
    color: #2ceaa3;
}}
.sel-badge {{
    position: absolute;
    top: -6px;
    right: -6px;
    background: #2ceaa3;
    color: #0b1319;
    font-size: 9px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 4px;
}}
.upload-box {{
    border: 1px dashed rgba(44, 234, 163, 0.4);
    border-radius: 8px;
    padding: 10px;
    text-align: center;
    background: rgba(44, 234, 163, 0.03);
    font-size: 12px;
    color: #2ceaa3;
    cursor: pointer;
}}
</style>
</head>
<body>
    <div class="top-nav">
        <div class="logo-area">
            {OWL_SVG_HEADER}
            <span class="logo-title">ForFriend</span>
            <span class="badge badge-mint">CAMPUS RPG</span>
        </div>
        <div>
            <span style="font-size: 13px; color: #8fa0ad; margin-right: 12px;">Already have an account?</span>
            <button class="btn-secondary">Sign In</button>
        </div>
    </div>

    <div class="page-title">
        <h1>CREATE HERO ACCOUNT (STUDENT REGISTRATION)</h1>
        <p>Join the #1 peer-to-peer study network at Foreign Trade University & Partner Universities</p>
    </div>

    <div class="register-layout">
        <!-- Form Left -->
        <div class="glass-card form-card">
            <div class="form-group">
                <label>Full Student Name</label>
                <input class="form-input" value="Nguyễn Văn A" />
            </div>
            <div class="grid-2">
                <div class="form-group">
                    <label>University Email (.edu.vn)</label>
                    <input class="form-input" value="nguyen.va@ftu.edu.vn" />
                </div>
                <div class="form-group">
                    <label>Student ID (MSSV)</label>
                    <input class="form-input" value="2311110245" />
                </div>
            </div>
            <div class="grid-2">
                <div class="form-group">
                    <label>University</label>
                    <input class="form-input" value="Foreign Trade University (FTU)" />
                </div>
                <div class="form-group">
                    <label>Major / Department</label>
                    <input class="form-input" value="Data Science in Economics" />
                </div>
            </div>
            <div class="grid-2">
                <div class="form-group">
                    <label>District / Area</label>
                    <input class="form-input" value="Dong Da - Chua Lang, Hanoi" />
                </div>
                <div class="form-group">
                    <label>Birth Year</label>
                    <input class="form-input" value="2005 (Cohort 62)" />
                </div>
            </div>
            <div class="grid-2" style="margin-top: 6px;">
                <div class="form-group">
                    <label>Student ID Card Verification</label>
                    <div class="upload-box">📷 student_card_ftu.jpg (Uploaded)</div>
                </div>
                <div class="form-group">
                    <label>Academic CV / Portfolio</label>
                    <div class="upload-box">📄 CV_NguyenVanA.pdf</div>
                </div>
            </div>
            <button class="btn-primary" style="width: 100%; justify-content: center; margin-top: 14px; padding: 12px;">
                🚀 COMPLETE REGISTRATION & ENTER LOBBY
            </button>
        </div>

        <!-- 15 Avatars Right -->
        <div class="glass-card avatar-section">
            <div class="avatar-section-header">
                <div class="avatar-section-title">CHOOSE 1 OF 15 CHIBI AVATARS</div>
                <span class="badge badge-cyan">PIXEL CHIBI COLLECTION</span>
            </div>
            <p style="font-size: 13px; color: #8fa0ad; margin-bottom: 16px;">
                Your representative chibi hero will be displayed on Quest Feed, Virtual Study Rooms, and Star Ratings.
            </p>
            <div class="avatars-grid">
                {avatar_items}
            </div>
            <div style="margin-top: 18px; padding: 12px; background: rgba(0, 210, 255, 0.05); border: 1px solid rgba(0, 210, 255, 0.2); border-radius: 8px; font-size: 12px; color: #00d2ff; display: flex; align-items: center; gap: 8px;">
                <span>✨</span>
                <span><strong>Hero #1 (Cyber Scholar)</strong> is selected. You can switch avatars anytime in Hero Profile!</span>
            </div>
        </div>
    </div>
</body>
</html>"""
    out_path = os.path.join(ASSETS_DIR, "screen_01_register_avatars.png")
    render_html_to_png(html, out_path, width=1300, height=840, scale=1.5)

def generate_screen_03_create_quest():
    """Modal Tạo Quest mới bằng Tiếng Anh."""
    av1 = os.path.join(AVATARS_DIR, "avatar-01.png").replace("\\", "/")
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    background: #0b1319;
    padding: 24px;
}}
.modal-overlay {{
    max-width: 920px;
    margin: 0 auto;
    background: #13222a;
    border: 2px solid #2ceaa3;
    border-radius: 18px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.7), 0 0 30px rgba(44, 234, 163, 0.25);
    overflow: hidden;
}}
.modal-header {{
    background: #0e1a22;
    padding: 16px 24px;
    border-bottom: 1px solid rgba(44, 234, 163, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.modal-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: #2ceaa3;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.modal-body {{
    padding: 28px;
    display: grid;
    grid-template-columns: 1.25fr 0.85fr;
    gap: 24px;
}}
.form-group {{
    margin-bottom: 16px;
}}
.form-group label {{
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: #cbd5e1;
    margin-bottom: 6px;
    text-transform: uppercase;
}}
.form-input {{
    width: 100%;
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    padding: 10px 14px;
    color: #ffffff;
    font-size: 13px;
}}
.mode-selector {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}}
.mode-card {{
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    cursor: pointer;
}}
.mode-card.selected {{
    border: 2px solid #2ceaa3;
    background: rgba(44, 234, 163, 0.08);
}}
.preview-card {{
    background: #0e1a22;
    border: 1px dashed rgba(44, 234, 163, 0.3);
    border-radius: 12px;
    padding: 20px;
}}
</style>
</head>
<body>
    <div class="modal-overlay">
        <div class="modal-header">
            <div class="modal-title">
                <span>⚔️</span>
                <span>CREATE NEW STUDY QUEST</span>
            </div>
            <span class="badge badge-mint">AUTO-MATCHING ENABLED</span>
        </div>

        <div class="modal-body">
            <!-- Form Left -->
            <div>
                <label style="display:block; font-size:11px; font-weight:700; color:#cbd5e1; margin-bottom:8px; text-transform:uppercase;">
                    Study Mode
                </label>
                <div class="mode-selector">
                    <div class="mode-card selected">
                        <div style="font-size: 18px; margin-bottom: 4px;">☕ 📚</div>
                        <div style="font-weight: 700; color: #2ceaa3; font-size: 13px;">Offline (In-Person)</div>
                        <div style="font-size: 11px; color: #8fa0ad;">Library, Cafe, Campus</div>
                    </div>
                    <div class="mode-card">
                        <div style="font-size: 18px; margin-bottom: 4px;">💻 🌐</div>
                        <div style="font-weight: 700; color: #00d2ff; font-size: 13px;">Online (Virtual Room)</div>
                        <div style="font-size: 11px; color: #8fa0ad;">LiveKit WebRTC Video Call</div>
                    </div>
                </div>

                <div class="form-group">
                    <label>Quest Title</label>
                    <input class="form-input" value="Python Project: AI Chatbot & Web Application" />
                </div>

                <div class="form-group">
                    <label>Subject & Tags (Used by Matching Algorithm)</label>
                    <input class="form-input" value="Web Programming, Python, FastAPI, Reflex, SQLite" />
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div class="form-group">
                        <label>Preferred Location</label>
                        <input class="form-input" value="FTU Building A Library / Chua Lang Cafe" />
                    </div>
                    <div class="form-group">
                        <label>Max Partners Needed</label>
                        <input class="form-input" value="3 students (Team of 4)" />
                    </div>
                </div>

                <div class="form-group">
                    <label>Description & Partner Expectations</label>
                    <textarea class="form-input" style="height: 90px; resize: none;">Hi everyone! Looking for passionate teammates to build our final Web Development project. We plan to meet twice a week offline at the library to code, review progress, and test features.</textarea>
                </div>

                <div style="display: flex; gap: 12px; margin-top: 18px;">
                    <button class="btn-secondary" style="flex: 1;">Cancel</button>
                    <button class="btn-primary" style="flex: 2; justify-content: center;">🚀 POST QUEST & ACTIVATE MATCHING</button>
                </div>
            </div>

            <!-- Preview Right -->
            <div>
                <div style="font-size: 11px; font-weight: 700; color: #8fa0ad; margin-bottom: 8px; text-transform: uppercase;">
                    Feed Display Live Preview
                </div>
                <div class="preview-card">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                        <img src="file:///{av1}" style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid #2ceaa3;" />
                        <div>
                            <div style="font-weight: 700; font-size: 14px;">Nguyễn Văn A</div>
                            <div style="font-size: 11px; color: #8fa0ad;">FTU • K62 Data Science • Just now</div>
                        </div>
                    </div>
                    <div style="font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 6px;">
                        Python Project: AI Chatbot & Web Application
                    </div>
                    <p style="font-size: 12px; color: #cbd5e1; line-height: 1.4; margin-bottom: 12px;">
                        Hi everyone! Looking for passionate teammates to build our final Web Development project...
                    </p>
                    <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px;">
                        <span class="badge badge-mint">Python/FastAPI</span>
                        <span class="badge badge-cyan">FTU Library</span>
                        <span class="badge badge-pink">Needs 3</span>
                    </div>
                    <div style="padding: 10px; background: rgba(44,234,163,0.08); border-radius: 8px; font-size: 11px; color: #2ceaa3;">
                        💡 <strong>Auto-Matching:</strong> This quest will be prioritized on feeds of students with matching subjects and university.
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    out_path = os.path.join(ASSETS_DIR, "screen_03_create_quest_modal.png")
    render_html_to_png(html, out_path, width=1100, height=750, scale=1.5)

def generate_screen_04_virtual_rooms():
    """Phòng học ảo LiveKit WebRTC bằng Tiếng Anh."""
    av1 = os.path.join(AVATARS_DIR, "avatar-01.png").replace("\\", "/")
    av2 = os.path.join(AVATARS_DIR, "avatar-02.png").replace("\\", "/")
    av3 = os.path.join(AVATARS_DIR, "avatar-03.png").replace("\\", "/")
    av4 = os.path.join(AVATARS_DIR, "avatar-04.png").replace("\\", "/")

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    background: #0b1319;
    padding: 20px;
}}
.lobby-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #101d24;
    border: 1px solid rgba(0, 210, 255, 0.3);
    border-radius: 12px;
    padding: 14px 24px;
    margin-bottom: 20px;
}}
.room-grid {{
    display: grid;
    grid-template-columns: 2.2fr 1fr;
    gap: 20px;
}}
.video-stage {{
    background: #0e1a22;
    border: 1px solid rgba(44, 234, 163, 0.25);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}
.video-tiles {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    height: 440px;
    margin-bottom: 16px;
}}
.video-tile {{
    background: #13222a;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}
.video-tile.active-speaker {{
    border: 2px solid #2ceaa3;
    box-shadow: 0 0 15px rgba(44, 234, 163, 0.4);
}}
.cam-feed {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    background: #182c36;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.tile-avatar {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: #0e1a22;
    border: 2px solid rgba(44, 234, 163, 0.4);
}}
.participant-tag {{
    position: absolute;
    bottom: 10px;
    left: 10px;
    background: rgba(11, 19, 25, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}}
.video-controls {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #13222a;
    border-radius: 12px;
    padding: 10px 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}
.control-buttons {{
    display: flex;
    gap: 12px;
}}
.control-btn {{
    width: 42px;
    height: 42px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    background: #0e1a22;
    color: #fff;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}}
.control-btn.active {{
    background: #2ceaa3;
    color: #0b1319;
    border-color: #2ceaa3;
}}
.control-btn.danger {{
    width: auto;
    min-width: 125px;
    padding: 0 16px;
    gap: 6px;
    font-size: 13px;
    font-weight: 700;
    white-space: nowrap;
    background: #f43f5e;
    color: #fff;
    border-color: #f43f5e;
    box-shadow: 0 2px 10px rgba(244, 63, 94, 0.35);
}}
.pomodoro-box {{
    background: rgba(251, 191, 36, 0.1);
    border: 1px solid rgba(251, 191, 36, 0.3);
    padding: 6px 14px;
    border-radius: 8px;
    font-family: 'Press Start 2P', monospace;
    font-size: 12px;
    color: #fbbf24;
}}
.chat-panel {{
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    height: 540px;
}}
.chat-messages {{
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 12px;
}}
.msg-bubble {{
    background: #13222a;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 12px;
}}
.msg-bubble.mine {{
    background: rgba(44, 234, 163, 0.12);
    border: 1px solid rgba(44, 234, 163, 0.25);
    align-self: flex-end;
}}
</style>
</head>
<body>
    <div class="lobby-header">
        <div style="display: flex; align-items: center; gap: 14px;">
            <span class="outfit" style="font-size: 18px; font-weight: 800; color: #00d2ff;">🏛️ ADVENTURE ZONE: FTU ECONOMETRICS STUDY ROOM</span>
            <span class="badge badge-mint">🔴 LIVEKIT SFU WEBRTC</span>
            <span class="badge badge-cyan">ROOM ID: #FTU-ECO-882</span>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="pomodoro-box">⏱️ POMODORO: 21:45</div>
            <button class="btn-secondary" style="padding: 6px 14px; font-size: 12px;">+ Invite Peer</button>
        </div>
    </div>

    <div class="room-grid">
        <!-- Video Stage -->
        <div class="video-stage">
            <div class="video-tiles">
                <!-- Tile 1 -->
                <div class="video-tile active-speaker">
                    <div class="cam-feed">
                        <img class="tile-avatar" src="file:///{av1}" />
                    </div>
                    <div class="participant-tag">
                        <span>🎙️</span>
                        <span>Nguyễn Văn A (Host - You)</span>
                        <span class="badge badge-mint" style="font-size: 9px;">TALKING</span>
                    </div>
                </div>

                <!-- Tile 2 -->
                <div class="video-tile">
                    <div class="cam-feed">
                        <img class="tile-avatar" src="file:///{av2}" />
                    </div>
                    <div class="participant-tag">
                        <span>🎙️</span>
                        <span>Anya L. (Writing)</span>
                    </div>
                </div>

                <!-- Tile 3 -->
                <div class="video-tile">
                    <div class="cam-feed">
                        <img class="tile-avatar" src="file:///{av3}" />
                    </div>
                    <div class="participant-tag">
                        <span style="color: #f43f5e;">🔇</span>
                        <span>Liam M. (Gaming Hub)</span>
                    </div>
                </div>

                <!-- Tile 4 -->
                <div class="video-tile">
                    <div class="cam-feed">
                        <img class="tile-avatar" src="file:///{av4}" />
                    </div>
                    <div class="participant-tag">
                        <span>🎙️</span>
                        <span>Chloe T. (Reading)</span>
                    </div>
                </div>
            </div>

            <!-- Controls Bar -->
            <div class="video-controls">
                <div style="font-size: 12px; color: #8fa0ad;">
                    ⚡ <strong>LiveKit Cloud:</strong> RTT 18ms • Packet Loss 0.0% • 720p HD
                </div>
                <div class="control-buttons">
                    <button class="control-btn active" title="Mic On">🎤</button>
                    <button class="control-btn active" title="Camera On">📹</button>
                    <button class="control-btn" title="Share Screen">🖥️</button>
                    <button class="control-btn" title="Raise Hand">✋</button>
                    <button class="control-btn danger" title="Leave Room">📞 Leave Room</button>
                </div>
                <div>
                    <span class="badge badge-gold">⭐ POST-STUDY RATING ACTIVE</span>
                </div>
            </div>
        </div>

        <!-- Chat Panel -->
        <div class="chat-panel">
            <div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 14px; color: #2ceaa3; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                💬 IN-ROOM CHAT & STUDY NOTES
            </div>
            <div class="chat-messages">
                <div class="msg-bubble">
                    <div style="font-weight: 700; color: #00d2ff; font-size: 11px; margin-bottom: 2px;">Anya L.</div>
                    <div>Everyone open chapter 3 exercises on page 45, let's start with the White test!</div>
                </div>
                <div class="msg-bubble mine">
                    <div style="font-weight: 700; color: #2ceaa3; font-size: 11px; margin-bottom: 2px;">Nguyễn Văn A (You)</div>
                    <div>Sure! I am sharing my screen with the Stata regression script.</div>
                </div>
                <div class="msg-bubble">
                    <div style="font-weight: 700; color: #fbbf24; font-size: 11px; margin-bottom: 2px;">Chloe T.</div>
                    <div>After this 25m Pomodoro interval, let's take a 5-minute break!</div>
                </div>
            </div>
            <div style="display: flex; gap: 8px;">
                <input class="form-input" style="flex: 1;" placeholder="Type message..." value="Sounds great, let's do it!" />
                <button class="btn-primary" style="padding: 8px 14px;">Send</button>
            </div>
        </div>
    </div>
</body>
</html>"""
    out_path = os.path.join(ASSETS_DIR, "screen_04_virtual_rooms_lobby.png")
    render_html_to_png(html, out_path, width=1350, height=750, scale=1.5)

def generate_screen_05_profile_chat():
    """Hồ sơ cá nhân & Chat 1-1 bằng Tiếng Anh."""
    av1 = os.path.join(AVATARS_DIR, "avatar-01.png").replace("\\", "/")
    av2 = os.path.join(AVATARS_DIR, "avatar-02.png").replace("\\", "/")

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    background: #0b1319;
    padding: 20px;
}}
.profile-grid {{
    display: grid;
    grid-template-columns: 1.25fr 1fr;
    gap: 24px;
    max-width: 1250px;
    margin: 0 auto;
}}
.hero-card {{
    padding: 24px;
}}
.hero-header {{
    display: flex;
    gap: 20px;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 20px;
    margin-bottom: 20px;
}}
.hero-avatar-large {{
    width: 96px;
    height: 96px;
    border-radius: 50%;
    background: #0e1a22;
    border: 3px solid #2ceaa3;
    box-shadow: 0 0 25px rgba(44, 234, 163, 0.4);
}}
.exp-bar-container {{
    background: #0e1a22;
    border-radius: 10px;
    height: 14px;
    width: 100%;
    overflow: hidden;
    margin: 8px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}
.exp-bar-fill {{
    background: linear-gradient(90deg, #2ceaa3, #00d2ff);
    height: 100%;
    width: 78%;
}}
.badge-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 14px;
}}
.badge-item {{
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 10px 8px;
    text-align: center;
    font-size: 11px;
}}
.chat-window {{
    background: #13222a;
    border: 1px solid rgba(44, 234, 163, 0.2);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    height: 600px;
    overflow: hidden;
}}
.chat-header {{
    background: #0e1a22;
    padding: 14px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    gap: 12px;
}}
.chat-body {{
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 14px;
}}
.chat-bubble {{
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 13px;
    line-height: 1.5;
}}
.chat-bubble.them {{
    background: #0e1a22;
    border: 1px solid rgba(255, 255, 255, 0.1);
    align-self: flex-start;
}}
.chat-bubble.me {{
    background: rgba(44, 234, 163, 0.15);
    border: 1px solid rgba(44, 234, 163, 0.35);
    color: #ffffff;
    align-self: flex-end;
}}
</style>
</head>
<body>
    <div class="profile-grid">
        <!-- Hero Profile Left -->
        <div class="glass-card hero-card">
            <div class="hero-header">
                <img class="hero-avatar-large" src="file:///{av1}" />
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <h2 class="outfit" style="font-size: 22px; font-weight: 800;">Nguyễn Văn A</h2>
                        <span class="badge badge-mint">VERIFIED FTU</span>
                    </div>
                    <div style="font-size: 13px; color: #8fa0ad; margin: 4px 0;">
                        K62 Data Science • Foreign Trade University
                    </div>
                    <div style="display: flex; gap: 10px; margin-top: 8px;">
                        <span class="badge badge-gold">⭐ 4.95 / 5.0 (38 Reviews)</span>
                        <span class="badge badge-cyan">LV.14 STUDY HERO</span>
                    </div>
                </div>
            </div>

            <!-- EXP Progress -->
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700;">
                    <span style="color: #2ceaa3;">CURRENT LEVEL EXP</span>
                    <span style="color: #00d2ff;">2,450 / 3,000 EXP (Level 15 Soon)</span>
                </div>
                <div class="exp-bar-container">
                    <div class="exp-bar-fill"></div>
                </div>
            </div>

            <!-- Academic Info -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 20px;">
                <div style="background: #0e1a22; padding: 12px; border-radius: 10px;">
                    <div style="font-size: 11px; color: #8fa0ad; text-transform: uppercase;">Enrolled Subjects</div>
                    <div style="font-size: 13px; font-weight: 700; color: #fff; margin-top: 4px;">Econometrics, Python, Calculus II</div>
                </div>
                <div style="background: #0e1a22; padding: 12px; border-radius: 10px;">
                    <div style="font-size: 11px; color: #8fa0ad; text-transform: uppercase;">Credentials Verification</div>
                    <div style="font-size: 13px; font-weight: 700; color: #2ceaa3; margin-top: 4px;">Student ID & CV Approved</div>
                </div>
            </div>

            <!-- Badges -->
            <div>
                <div class="outfit" style="font-size: 14px; font-weight: 800; color: #00d2ff; margin-bottom: 10px;">
                    🎖️ GAMIFIED ACADEMIC BADGES
                </div>
                <div class="badge-grid">
                    <div class="badge-item">
                        <div style="font-size: 20px;">🔥</div>
                        <div style="font-weight: 700; color: #2ceaa3;">Top Scholar</div>
                        <div style="color: #8fa0ad; font-size: 10px;">Top 5% Rating</div>
                    </div>
                    <div class="badge-item">
                        <div style="font-size: 20px;">⏰</div>
                        <div style="font-weight: 700; color: #fbbf24;">Punctual Master</div>
                        <div style="color: #8fa0ad; font-size: 10px;">100% on time</div>
                    </div>
                    <div class="badge-item">
                        <div style="font-size: 20px;">💡</div>
                        <div style="font-weight: 700; color: #00d2ff;">Peer Mentor</div>
                        <div style="color: #8fa0ad; font-size: 10px;">25+ Thank-yous</div>
                    </div>
                    <div class="badge-item">
                        <div style="font-size: 20px;">🦉</div>
                        <div style="font-weight: 700; color: #f43f5e;">Night Owl</div>
                        <div style="color: #8fa0ad; font-size: 10px;">50h in Rooms</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 1-1 Chat Right -->
        <div class="chat-window">
            <div class="chat-header">
                <img src="file:///{av2}" style="width: 42px; height: 42px; border-radius: 50%; border: 1px solid #2ceaa3;" />
                <div style="flex: 1;">
                    <div style="font-weight: 700; font-size: 14px;">Anya L.</div>
                    <div style="font-size: 11px; color: #2ceaa3;">🟢 Online • FTU K62 International Economics</div>
                </div>
                <button class="btn-secondary" style="padding: 6px 12px; font-size: 11px;">Call Video 📞</button>
            </div>

            <div class="chat-body">
                <div class="chat-bubble them">
                    Hi Nam! I saw your study quest for Econometrics on the feed. Are you free to meet tomorrow at 2 PM at FTU Library Building A?
                </div>
                <div class="chat-bubble me">
                    Hi Anya! Yes, 2 PM works great for me. I have prepared the slides for multiple regression and the Stata lab exercises!
                </div>
                <div class="chat-bubble them">
                    Awesome! I will bring my laptop with Stata 17 installed. See you at the 2nd-floor round table!
                </div>
                <div class="chat-bubble me">
                    Deal! I've accepted your study buddy invitation on ForFriend as well.
                </div>
            </div>

            <div style="padding: 14px 20px; background: #0e1a22; border-top: 1px solid rgba(255,255,255,0.1); display: flex; gap: 10px;">
                <input class="form-input" style="flex: 1;" placeholder="Type your message..." value="See you tomorrow afternoon! 👋" />
                <button class="btn-primary" style="padding: 8px 18px;">Send</button>
            </div>
        </div>
    </div>
</body>
</html>"""
    out_path = os.path.join(ASSETS_DIR, "screen_05_hero_profile_chat.png")
    render_html_to_png(html, out_path, width=1300, height=720, scale=1.5)

def generate_technical_diagrams():
    """Tạo sơ đồ kiến trúc, ERD và Matching Engine bằng Tiếng Anh chuẩn."""
    # 1. Architecture Diagram
    html_arch = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    background: #0b1319;
    padding: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.arch-card {{
    background: #0e1a22;
    border: 2px solid rgba(44, 234, 163, 0.35);
    border-radius: 20px;
    padding: 30px;
    width: 1080px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
}}
.arch-title {{
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 20px;
    color: #2ceaa3;
    text-align: center;
    margin-bottom: 24px;
}}
.tiers {{
    display: flex;
    flex-direction: column;
    gap: 18px;
}}
.tier-box {{
    background: #13222a;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;
    padding: 16px 20px;
}}
.tier-label {{
    font-family: 'Outfit', sans-serif;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.components-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}}
.comp-item {{
    background: #0e1a22;
    border: 1px solid rgba(44, 234, 163, 0.2);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}}
.comp-name {{
    font-weight: 700;
    font-size: 13px;
    color: #fff;
    margin-bottom: 4px;
}}
.comp-desc {{
    font-size: 11px;
    color: #8fa0ad;
}}
.flow-arrow {{
    text-align: center;
    color: #2ceaa3;
    font-size: 16px;
    font-weight: 700;
    margin: -6px 0;
}}
</style>
</head>
<body>
    <div class="arch-card">
        <div class="arch-title">FORFRIEND SYSTEM ARCHITECTURE (PURE PYTHON FULLSTACK ARCHITECTURE)</div>
        <div class="tiers">
            <!-- Tier 1: Frontend -->
            <div class="tier-box" style="border-left: 4px solid #00d2ff;">
                <div class="tier-label" style="color: #00d2ff;">
                    <span>🖥️ PRESENTATION LAYER (REFLEX PYTHON-TO-REACT SPA)</span>
                    <span class="badge badge-cyan">100% PYTHON UI</span>
                </div>
                <div class="components-row">
                    <div class="comp-item">
                        <div class="comp-name">Reflex Pages & State</div>
                        <div class="comp-desc">Feed, Rooms, Friends, Profile</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">Neo-Cyber Tokens</div>
                        <div class="comp-desc">Obsidian & Neon Mint Vanilla CSS</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">LiveKit WebRTC Component</div>
                        <div class="comp-desc">Custom Component Video Call</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">Async HTTP / WS Client</div>
                        <div class="comp-desc">Httpx & Native Reflex WS Engine</div>
                    </div>
                </div>
            </div>

            <div class="flow-arrow">⬇ REST API JSON (/api/v1/) & NATIVE WEBSOCKET CHANNELS ⬆</div>

            <!-- Tier 2: Backend -->
            <div class="tier-box" style="border-left: 4px solid #2ceaa3;">
                <div class="tier-label" style="color: #2ceaa3;">
                    <span>⚙️ BUSINESS & SERVICE LAYER (FASTAPI ASYNCHRONOUS ENGINE)</span>
                    <span class="badge badge-mint">PYTHON 3.11+</span>
                </div>
                <div class="components-row">
                    <div class="comp-item">
                        <div class="comp-name">FastAPI Core & Routers</div>
                        <div class="comp-desc">Auth, Posts, Rooms, Chat, Rating</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">Matching Engine</div>
                        <div class="comp-desc">Multi-Factor Relevance Scoring</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">In-Memory ConnectionManager</div>
                        <div class="comp-desc">Real-time Hub & In-Memory Cache TTL</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">Security & Token Manager</div>
                        <div class="comp-desc">JWT Bearer & Bcrypt Passlib</div>
                    </div>
                </div>
            </div>

            <div class="flow-arrow">⬇ SQLALCHEMY 2.0 ASYNC SESSIONS & IN-MEMORY DATA PIPELINES ⬇</div>

            <!-- Tier 3: Storage -->
            <div class="tier-box" style="border-left: 4px solid #fbbf24;">
                <div class="tier-label" style="color: #fbbf24;">
                    <span>💾 DATA & MEDIA STORAGE LAYER (ZERO DOCKER / EMBEDDED LAYER)</span>
                    <span class="badge badge-gold">SQLITE & LIVEKIT SFU</span>
                </div>
                <div class="components-row">
                    <div class="comp-item">
                        <div class="comp-name">SQLite 3 (aiosqlite)</div>
                        <div class="comp-desc">File forfriend.db (10 relations)</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">In-Memory RAM Cache</div>
                        <div class="comp-desc">Python Dict + TTL (Redis alternative)</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">Local File Storage</div>
                        <div class="comp-desc">Student IDs, CVs & 15 Chibi Avatars</div>
                    </div>
                    <div class="comp-item">
                        <div class="comp-name">LiveKit Cloud SFU</div>
                        <div class="comp-desc">WebRTC Video/Audio Streaming</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    out_arch = os.path.join(ASSETS_DIR, "architecture_diagram.png")
    render_html_to_png(html_arch, out_arch, width=1150, height=650, scale=1.5)

    # 2. Database ERD
    html_erd = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    background: #0b1319;
    padding: 24px;
}}
.erd-container {{
    max-width: 1200px;
    margin: 0 auto;
    background: #0e1a22;
    border: 2px solid rgba(0, 210, 255, 0.35);
    border-radius: 18px;
    padding: 24px;
}}
.erd-title {{
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 18px;
    color: #00d2ff;
    text-align: center;
    margin-bottom: 20px;
}}
.tables-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
}}
.db-table {{
    background: #13222a;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    overflow: hidden;
}}
.table-header {{
    background: #182c36;
    padding: 8px 12px;
    font-weight: 700;
    font-size: 12px;
    color: #2ceaa3;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
}}
.fields-list {{
    padding: 8px 12px;
    font-size: 11px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}}
.field-row {{
    display: flex;
    justify-content: space-between;
    color: #cbd5e1;
}}
.pk {{
    color: #fbbf24;
    font-weight: 700;
}}
.fk {{
    color: #00d2ff;
}}
</style>
</head>
<body>
    <div class="erd-container">
        <div class="erd-title">SQLITE DATABASE SCHEMA (10 RELATIONAL ENTITIES)</div>
        <div class="tables-grid">
            <!-- Table 1: USER -->
            <div class="db-table" style="grid-column: span 2;">
                <div class="table-header">
                    <span>TABLE: user</span>
                    <span style="color: #fbbf24;">CORE HERO ENTITY</span>
                </div>
                <div class="fields-list" style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px 16px;">
                    <div class="field-row"><span class="pk">🔑 id (UUID)</span><span>PK</span></div>
                    <div class="field-row"><span>email</span><span>VARCHAR(255)</span></div>
                    <div class="field-row"><span>password_hash</span><span>VARCHAR(255)</span></div>
                    <div class="field-row"><span>name</span><span>VARCHAR(100)</span></div>
                    <div class="field-row"><span>school</span><span>VARCHAR(200)</span></div>
                    <div class="field-row"><span>major</span><span>VARCHAR(100)</span></div>
                    <div class="field-row"><span>city / district</span><span>VARCHAR(100)</span></div>
                    <div class="field-row"><span>avatar_id</span><span>INTEGER (1-15)</span></div>
                    <div class="field-row"><span>avg_rating</span><span>FLOAT (0.0-5.0)</span></div>
                    <div class="field-row"><span>total_ratings</span><span>INTEGER</span></div>
                </div>
            </div>

            <!-- Table 2: POST -->
            <div class="db-table" style="grid-column: span 2;">
                <div class="table-header">
                    <span>TABLE: post (Quest)</span>
                    <span style="color: #2ceaa3;">STUDY QUESTS</span>
                </div>
                <div class="fields-list" style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px 16px;">
                    <div class="field-row"><span class="pk">🔑 id (UUID)</span><span>PK</span></div>
                    <div class="field-row"><span class="fk">🔗 author_id</span><span>FK → user.id</span></div>
                    <div class="field-row"><span>content</span><span>TEXT</span></div>
                    <div class="field-row"><span>study_type</span><span>online / offline</span></div>
                    <div class="field-row"><span>location</span><span>VARCHAR(200)</span></div>
                    <div class="field-row"><span>preferred_school</span><span>VARCHAR(200)</span></div>
                    <div class="field-row"><span>study_date</span><span>TIMESTAMP</span></div>
                    <div class="field-row"><span>max_people</span><span>INTEGER</span></div>
                </div>
            </div>

            <!-- Table 3: ROOM -->
            <div class="db-table">
                <div class="table-header"><span>room</span><span>VIRTUAL</span></div>
                <div class="fields-list">
                    <div class="field-row"><span class="pk">🔑 id</span><span>PK</span></div>
                    <div class="field-row"><span class="fk">🔗 host_id</span><span>FK</span></div>
                    <div class="field-row"><span>name</span><span>VARCHAR</span></div>
                    <div class="field-row"><span>topic</span><span>VARCHAR</span></div>
                    <div class="field-row"><span>status</span><span>active</span></div>
                    <div class="field-row"><span>room_code</span><span>UNIQUE</span></div>
                </div>
            </div>

            <!-- Table 4: ROOM_PARTICIPANT -->
            <div class="db-table">
                <div class="table-header"><span>room_participant</span><span>JOIN</span></div>
                <div class="fields-list">
                    <div class="field-row"><span class="pk">🔑 id</span><span>PK</span></div>
                    <div class="field-row"><span class="fk">🔗 room_id</span><span>FK</span></div>
                    <div class="field-row"><span class="fk">🔗 user_id</span><span>FK</span></div>
                    <div class="field-row"><span>status</span><span>accepted</span></div>
                    <div class="field-row"><span>joined_at</span><span>TIME</span></div>
                </div>
            </div>

            <!-- Table 5: RATING -->
            <div class="db-table">
                <div class="table-header"><span>rating</span><span>FEEDBACK</span></div>
                <div class="fields-list">
                    <div class="field-row"><span class="pk">🔑 id</span><span>PK</span></div>
                    <div class="field-row"><span class="fk">🔗 rater_id</span><span>FK</span></div>
                    <div class="field-row"><span class="fk">🔗 ratee_id</span><span>FK</span></div>
                    <div class="field-row"><span class="fk">🔗 room_id</span><span>FK</span></div>
                    <div class="field-row"><span style="color:#fbbf24;">stars</span><span>1-5 ★</span></div>
                    <div class="field-row"><span>comment</span><span>TEXT</span></div>
                </div>
            </div>

            <!-- Table 6: FRIENDSHIP -->
            <div class="db-table">
                <div class="table-header"><span>friendship</span><span>SOCIAL</span></div>
                <div class="fields-list">
                    <div class="field-row"><span class="pk">🔑 id</span><span>PK</span></div>
                    <div class="field-row"><span class="fk">🔗 requester</span><span>FK</span></div>
                    <div class="field-row"><span class="fk">🔗 addressee</span><span>FK</span></div>
                    <div class="field-row"><span>status</span><span>accepted</span></div>
                </div>
            </div>

            <!-- Table 7: MESSAGE -->
            <div class="db-table">
                <div class="table-header"><span>message</span><span>1-1 CHAT</span></div>
                <div class="fields-list">
                    <div class="field-row"><span class="pk">🔑 id</span><span>PK</span></div>
                    <div class="field-row"><span class="fk">🔗 sender_id</span><span>FK</span></div>
                    <div class="field-row"><span class="fk">🔗 receiver_id</span><span>FK</span></div>
                    <div class="field-row"><span>content</span><span>TEXT</span></div>
                    <div class="field-row"><span>is_read</span><span>BOOLEAN</span></div>
                </div>
            </div>

            <!-- Table 8: USER_SUBJECT -->
            <div class="db-table">
                <div class="table-header"><span>user_subject</span><span>SUBJECTS</span></div>
                <div class="fields-list">
                    <div class="field-row"><span class="pk">🔑 id</span><span>PK</span></div>
                    <div class="field-row"><span class="fk">🔗 user_id</span><span>FK</span></div>
                    <div class="field-row"><span>subject_name</span><span>VARCHAR</span></div>
                </div>
            </div>

            <!-- Table 9: POST_TAG -->
            <div class="db-table">
                <div class="table-header"><span>post_tag</span><span>TAGS</span></div>
                <div class="fields-list">
                    <div class="field-row"><span class="pk">🔑 id</span><span>PK</span></div>
                    <div class="field-row"><span class="fk">🔗 post_id</span><span>FK</span></div>
                    <div class="field-row"><span>tag_name</span><span>VARCHAR</span></div>
                </div>
            </div>

            <!-- Table 10: ROOM_CATEGORY -->
            <div class="db-table">
                <div class="table-header"><span>room_category</span><span>ZONES</span></div>
                <div class="fields-list">
                    <div class="field-row"><span class="pk">🔑 id</span><span>PK</span></div>
                    <div class="field-row"><span>name</span><span>UNIQUE</span></div>
                    <div class="field-row"><span>icon / color</span><span>VARCHAR</span></div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    out_erd = os.path.join(ASSETS_DIR, "database_erd.png")
    render_html_to_png(html_erd, out_erd, width=1250, height=620, scale=1.5)

    # 3. Matching Diagram
    html_match = f"""<!DOCTYPE html>
<html>
<head>
<style>
{COMMON_CSS}
body {{
    background: #0b1319;
    padding: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.match-card {{
    background: #0e1a22;
    border: 2px solid rgba(44, 234, 163, 0.4);
    border-radius: 18px;
    padding: 26px 36px;
    width: 1050px;
}}
.formula-box {{
    background: #13222a;
    border: 1px solid #2ceaa3;
    border-radius: 10px;
    padding: 14px 20px;
    text-align: center;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 15px;
    color: #2ceaa3;
    margin: 16px 0 24px 0;
    box-shadow: 0 0 20px rgba(44, 234, 163, 0.2);
}}
.factors-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
}}
.factor-card {{
    background: #13222a;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 14px 10px;
    text-align: center;
}}
.factor-weight {{
    font-family: 'Press Start 2P', monospace;
    font-size: 14px;
    color: #00d2ff;
    margin-bottom: 6px;
}}
.factor-name {{
    font-weight: 700;
    font-size: 13px;
    color: #fff;
    margin-bottom: 4px;
}}
.factor-desc {{
    font-size: 10px;
    color: #8fa0ad;
    line-height: 1.3;
}}
</style>
</head>
<body>
    <div class="match-card">
        <div style="text-align: center;">
            <div class="outfit" style="font-size: 18px; font-weight: 800; color: #2ceaa3; margin-bottom: 4px;">MULTI-FACTOR STUDY BUDDY MATCHING ENGINE</div>
            <div style="font-size: 13px; color: #8fa0ad;">Optimizing peer-to-peer student connections across 5 weighted dimensions</div>
        </div>

        <div class="formula-box">
            Relevance_Score = W1·Same_School + W2·Same_Area + W3·Jaccard(Subjects) + W4·e^(-λ·Δt) + W5·Rating_Norm
        </div>

        <div class="factors-grid">
            <div class="factor-card" style="border-top: 3px solid #2ceaa3;">
                <div class="factor-weight">W1 = 3.0</div>
                <div class="factor-name">Same University</div>
                <div class="factor-desc">Highest weight factor. Binary match based on enrolled school (e.g. FTU = FTU).</div>
            </div>

            <div class="factor-card" style="border-top: 3px solid #00d2ff;">
                <div class="factor-weight">W2 = 2.0</div>
                <div class="factor-name">Geographic Area</div>
                <div class="factor-desc">70% weight for same City + 30% for same District (Chua Lang, Dong Da, Cau Giay).</div>
            </div>

            <div class="factor-card" style="border-top: 3px solid #fbbf24;">
                <div class="factor-weight">W3 = 2.5</div>
                <div class="factor-name">Subject Overlap</div>
                <div class="factor-desc">Jaccard Similarity index between student subjects and quest tags.</div>
            </div>

            <div class="factor-card" style="border-top: 3px solid #f43f5e;">
                <div class="factor-weight">W4 = 1.0</div>
                <div class="factor-name">Recency Decay</div>
                <div class="factor-desc">Exponential decay exp(-0.029*Δt) with 24-hour half-life for fresh quests.</div>
            </div>

            <div class="factor-card" style="border-top: 3px solid #8b5cf6;">
                <div class="factor-weight">W5 = 1.5</div>
                <div class="factor-name">Author Rating</div>
                <div class="factor-desc">Normalized peer review score (Rating / 5.0) prioritizing reliable partners.</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    out_match = os.path.join(ASSETS_DIR, "matching_algorithm_diagram.png")
    render_html_to_png(html_match, out_match, width=1150, height=480, scale=1.5)

if __name__ == "__main__":
    print("Regenerating ForFriend Report Assets with Official Owl Logo & English UI...")
    generate_logo()
    generate_screen_01_register()
    generate_screen_02_feed()
    generate_screen_03_create_quest()
    generate_screen_04_virtual_rooms()
    generate_screen_05_profile_chat()
    generate_technical_diagrams()
    print("All English UI & Owl Logo assets generated successfully!")
