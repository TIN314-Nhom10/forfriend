"""
Script sinh file slide thuyết trình PowerPoint (.pptx) hoàn chỉnh cho ForFriend.
Tuân thủ 100% khung sườn yêu cầu của Giảng viên ThS. Trần Công Minh:
1. Why this? Solve which problem? (Bối cảnh thực tế & Bài toán cần giải quyết)
2. Kỹ thuật đã áp dụng (Pure Python Stack, Zero External Dependency, Reflex, FastAPI, In-Memory Hub, LiveKit WebRTC)
3. Các tính năng đã xây dựng (6 modules cốt lõi từ Quest Feed đến Phòng học ảo)
4. Kịch bản Demo trực quan (5-step end-to-end user journey walkthrough)
Phong cách thiết kế: Neo-Cyber Student / Dark Space Retro (16:9 Widescreen, Obsidian #0B1319, Mint #2CEAA3, Cyan #00D2FF).
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PPTX = os.path.abspath("ForFriend_Presentation.pptx")
ASSETS_DIR = os.path.abspath("report_assets")

# Bảng màu chuẩn Neo-Cyber Student
C_BG_DARK = RGBColor(0x07, 0x0D, 0x12)       # Obsidian Base
C_CARD_BG = RGBColor(0x10, 0x1D, 0x24)       # Card Slate Navy
C_CARD_ALT = RGBColor(0x13, 0x22, 0x2A)      # Card Elevation
C_MINT = RGBColor(0x2C, 0xEA, 0xA3)          # Neon Mint Primary
C_CYAN = RGBColor(0x00, 0xD2, 0xFF)          # Cyan Glow Secondary
C_GOLD = RGBColor(0xFB, 0xBF, 0x24)          # Star Gold Accent
C_PINK = RGBColor(0xF4, 0x3F, 0x5E)          # Cyber Berry Pink
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)         # Pure White
C_MUTED = RGBColor(0x8F, 0xA0, 0xAD)         # Slate Gray Text
C_BORDER = RGBColor(0x1B, 0x38, 0x3E)        # Mint/Teal Subtle Border

def set_slide_background(slide, color=C_BG_DARK):
    """Đặt màu nền đồng nhất cho slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, section_tag, title_text, subtitle_text=None):
    """Tạo Header chuẩn cho các slide nội dung."""
    # Tag nhỏ phía trên
    tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = section_tag.upper()
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_MINT
    p_tag.font.name = "Segoe UI"

    # Tiêu đề slide
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.6))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE
    p_title.font.name = "Segoe UI"

    if subtitle_text:
        p_sub = tf_title.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = C_MUTED
        p_sub.font.name = "Segoe UI"

def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
    """Tạo khối card bo góc làm nền cho nội dung."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
    else:
        shape.line.fill.background()
    return shape

def create_presentation():
    prs = pptx.Presentation()
    # Chuẩn 16:9 Widescreen (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (BÌA THUYẾT TRÌNH)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Viền trang trí neon mint phía trên
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = C_MINT
    accent_bar.line.fill.background()

    # Logo FTU & Logo ForFriend
    ftu_logo_path = os.path.join(ASSETS_DIR, "ftu_logo.png")
    if os.path.exists(ftu_logo_path):
        slide1.shapes.add_picture(ftu_logo_path, Inches(0.8), Inches(0.7), height=Inches(1.1))

    ff_logo_path = os.path.join(ASSETS_DIR, "forfriend_logo.png")
    if os.path.exists(ff_logo_path):
        slide1.shapes.add_picture(ff_logo_path, Inches(2.2), Inches(0.8), height=Inches(0.9))

    # Thông tin cơ sở đào tạo
    tb_univ = slide1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.7), Inches(0.5))
    p_u = tb_univ.text_frame.paragraphs[0]
    p_u.text = "TRƯỜNG ĐẠI HỌC NGOẠI THƯƠNG • KHOA CÔNG NGHỆ VÀ KHOA HỌC DỮ LIỆU"
    p_u.font.size = Pt(12)
    p_u.font.bold = True
    p_u.font.color.rgb = C_CYAN
    p_u.font.name = "Segoe UI"

    # Tên đề tài chính
    tb_main_title = slide1.shapes.add_textbox(Inches(0.8), Inches(2.7), Inches(11.7), Inches(1.8))
    tf_mt = tb_main_title.text_frame
    tf_mt.word_wrap = True
    p_mt1 = tf_mt.paragraphs[0]
    p_mt1.text = "BÁO CÁO ĐỒ ÁN MÔN HỌC: LẬP TRÌNH ỨNG DỤNG WEB (TIN314)"
    p_mt1.font.size = Pt(15)
    p_mt1.font.bold = True
    p_mt1.font.color.rgb = C_MUTED
    p_mt1.font.name = "Segoe UI"

    p_mt2 = tf_mt.add_paragraph()
    p_mt2.text = "FORFRIEND: STUDENT STUDY BUDDY & VIRTUAL ROOM"
    p_mt2.font.size = Pt(32)
    p_mt2.font.bold = True
    p_mt2.font.color.rgb = C_WHITE
    p_mt2.font.name = "Segoe UI"

    p_mt3 = tf_mt.add_paragraph()
    p_mt3.text = "Nền tảng kết nối tìm bạn học nhóm sinh viên & Phòng học ảo tích hợp Video Call (Pure Python Fullstack)"
    p_mt3.font.size = Pt(14)
    p_mt3.font.color.rgb = C_MINT
    p_mt3.font.name = "Segoe UI"

    # Khung Card thông tin Giảng viên & Nhóm sinh viên
    card_info = add_card(slide1, Inches(0.8), Inches(4.8), Inches(11.733), Inches(1.9), bg_color=C_CARD_BG, border_color=C_BORDER)

    tb_meta = slide1.shapes.add_textbox(Inches(1.2), Inches(5.0), Inches(11.0), Inches(1.5))
    tf_meta = tb_meta.text_frame
    tf_meta.word_wrap = True

    p_gv = tf_meta.paragraphs[0]
    p_gv.text = "Giảng viên hướng dẫn: ThS. Trần Công Minh"
    p_gv.font.size = Pt(13)
    p_gv.font.bold = True
    p_gv.font.color.rgb = C_GOLD
    p_gv.font.name = "Segoe UI"

    p_nhom = tf_meta.add_paragraph()
    p_nhom.text = "Nhóm thực hiện: Nhóm 10 • Lớp tín chỉ: TIN314(2526-2)He.1"
    p_nhom.font.size = Pt(12)
    p_nhom.font.bold = True
    p_nhom.font.color.rgb = C_WHITE
    p_nhom.font.name = "Segoe UI"

    p_mb = tf_meta.add_paragraph()
    p_mb.text = "Thành viên: Nguyễn Hoàng Nam (Lead) • Lê Phương Anh • Trần Quang Minh • Đặng Thùy Linh • Vũ Minh Đức"
    p_mb.font.size = Pt(11)
    p_mb.font.color.rgb = C_MUTED
    p_mb.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 2: AGENDA / FLOW BÁO CÁO (THEO ĐÚNG ĐỊNH HƯỚNG CỦA THẦY MINH)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "PRESENTATION FLOW", "Nội Dung Thuyết Trình Đồ Án", "Cấu trúc 4 phần giải quyết trọn vẹn yêu cầu của giảng viên hướng dẫn")

    agenda_items = [
        ("01", "WHY THIS? SOLVE WHICH PROBLEM?", 
         "Bối cảnh sinh viên học một mình • Nhu cầu tìm bạn học nhóm • Các pain points của Facebook/Zalo • Giá trị cốt lõi của ForFriend.", C_MINT),
        ("02", "KỸ THUẬT & CÔNG NGHỆ ÁP DỤNG", 
         "Kiến trúc Pure Python Stack (Zero Docker/Redis) • Reflex SPA Frontend • FastAPI Async • SQLite 3 • In-Memory Hub • LiveKit WebRTC.", C_CYAN),
        ("03", "CÁC TÍNH NĂNG ĐÃ XÂY DỰNG", 
         "15 Chibi Avatars • Bảng tin Quest & Bộ lọc môn/trường • Thuật toán Matching 5 trọng số • Phòng học ảo LiveKit & Pomodoro • Đánh giá 5★.", C_GOLD),
        ("04", "KỊCH BẢN DEMO THỰC TẾ", 
         "Luồng trải nghiệm 5 bước: Khởi tạo Hero -> Tìm Quest & Match -> Tạo Quest mới -> Họp phòng LiveKit Video Call -> Đánh giá bạn học.", C_PINK),
    ]

    card_w = Inches(5.65)
    card_h = Inches(2.2)
    positions = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.85), Inches(1.8)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.85), Inches(4.3)),
    ]

    for idx, (num, title, desc, accent) in enumerate(agenda_items):
        pos_l, pos_t = positions[idx]
        add_card(slide2, pos_l, pos_t, card_w, card_h, bg_color=C_CARD_BG, border_color=accent)
        
        tb = slide2.shapes.add_textbox(pos_l + Inches(0.3), pos_t + Inches(0.25), card_w - Inches(0.6), card_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_n = tf.paragraphs[0]
        p_n.text = f"PHẦN {num}"
        p_n.font.size = Pt(13)
        p_n.font.bold = True
        p_n.font.color.rgb = accent
        p_n.font.name = "Segoe UI"

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE
        p_t.font.name = "Segoe UI"

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_MUTED
        p_d.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 3: PART 1 — WHY THIS? SOLVE WHICH PROBLEM? (VẤN ĐỀ CỦA SINH VIÊN)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "PART 1: WHY THIS? SOLVE WHICH PROBLEM?", "Thực Trạng Học Tập & Nhu Cầu Cấp Thiết Của Sinh Viên", "Tại sao sinh viên cần một nền tảng chuyên biệt thay vì các công cụ mạng xã hội hiện có?")

    # Cột trái: Thực trạng sinh viên
    add_card(slide3, Inches(0.8), Inches(1.8), Inches(5.65), Inches(5.0), bg_color=C_CARD_BG, border_color=C_PINK)
    tb_l = slide3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.05), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "🚨 THỰC TRẠNG: NỖI ĐAU CỦA SINH VIÊN"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_PINK

    items_l = [
        ("Áp lực môn học nặng", "Các môn Kinh tế lượng, Toán cao cấp, Lập trình ứng dụng, Ôn thi IELTS đòi hỏi thảo luận và giải bài tập theo nhóm."),
        ("Cảm giác cô đơn & Bế tắc", "82% sinh viên khảo sát tại khu vực Đống Đa - Cầu Giấy từng bế tắc khi tự học một mình, dễ bỏ cuộc giữa chừng."),
        ("Học online thiếu kỷ luật", "Học qua Meet/Zoom cá nhân dễ xao nhãng, tắt camera lướt mạng xã hội, thiếu sự giám sát đồng đội tích cực."),
        ("Khó tìm bạn đúng trình độ", "Rất khó tìm được bạn cùng trường, cùng lịch rảnh và có cùng quyết tâm đạt điểm cao (Target A/A+)."),
    ]
    for h, b in items_l:
        p_h = tf_l.add_paragraph()
        p_h.text = f"• {h}: "
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        p_b = tf_l.add_paragraph()
        p_b.text = f"  {b}"
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = C_MUTED

    # Cột phải: Hạn chế của giải pháp hiện tại
    add_card(slide3, Inches(6.85), Inches(1.8), Inches(5.65), Inches(5.0), bg_color=C_CARD_BG, border_color=C_CYAN)
    tb_r = slide3.shapes.add_textbox(Inches(7.15), Inches(2.0), Inches(5.05), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "⚡ HẠN CHẾ CỦA CÁC GIẢI PHÁP HIỆN CÓ"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    items_r = [
        ("Hội nhóm Facebook / Zalo", "Tin đăng tìm bạn trôi sau vài phút; không có bộ lọc môn học; lẫn lộn quảng cáo, cho thuê trọ và spam; nguy cơ lộ thông tin cá nhân."),
        ("Google Meet / Zoom", "Chỉ là công cụ gọi video thuần túy; link phòng rời rạc, hết hạn; không có cộng đồng và không thể ghép nối bạn mới."),
        ("Discord Study Servers", "Quá phức tạp đối với sinh viên không chuyên IT; thiếu tính bản địa hóa theo từng trường đại học Việt Nam (FTU, NEU)."),
        ("Thiếu cơ chế tín nhiệm", "Không có đánh giá sao sau buổi học dẫn đến tình trạng 'bùng kèo' hẹn học nhóm offline/online thường xuyên."),
    ]
    for h, b in items_r:
        p_h = tf_r.add_paragraph()
        p_h.text = f"• {h}: "
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        p_b = tf_r.add_paragraph()
        p_b.text = f"  {b}"
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 4: PART 1 — THE SOLUTION: FORFRIEND PLATFORM
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "PART 1: THE SOLUTION", "Giải Pháp ForFriend: Mô Hình Hybrid All-In-One", "Nền tảng kết nối học tập game hóa kết hợp hoàn hảo giữa Offline và Online")

    # Cột trái: 3 trụ cột giải pháp
    add_card(slide4, Inches(0.8), Inches(1.8), Inches(5.4), Inches(5.0), bg_color=C_CARD_BG, border_color=C_MINT)
    tb_sol = slide4.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(4.8), Inches(4.5))
    tf_s = tb_sol.text_frame
    tf_s.word_wrap = True

    p = tf_s.paragraphs[0]
    p.text = "🎯 3 TRỤ CỘT GIÁ TRỊ VƯỢT TRỘI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_MINT

    sol_items = [
        ("1. Mô hình Hybrid linh hoạt", "Hỗ trợ cả hẹn học Offline (Thư viện Tòa A - FTU, Cà phê Chùa Láng) lẫn Online (Phòng học ảo tích hợp Video Call không cần rời web)."),
        ("2. Thuật toán Matching đa chiều", "Tự động so khớp hồ sơ sinh viên với Quest học tập dựa trên 5 trọng số: Cùng trường (40%), Cùng khu vực (20%), Trùng môn học (25%), Recency & Rating."),
        ("3. Trải nghiệm Gamification Retro", "Biến việc học thành các 'Study Quest' đồng đội; hệ thống 15 Avatar Chibi Pixel bảo vệ danh tính; tích lũy EXP thăng cấp và đánh giá 1-5 sao uy tín."),
    ]
    for h, b in sol_items:
        p_h = tf_s.add_paragraph()
        p_h.text = f"{h}"
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        p_b = tf_s.add_paragraph()
        p_b.text = f"{b}"
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = C_MUTED

    # Cột phải: Hình ảnh màn hình Home Page Feed
    add_card(slide4, Inches(6.5), Inches(1.8), Inches(6.033), Inches(5.0), bg_color=C_CARD_BG, border_color=C_BORDER)
    feed_img_path = os.path.join(ASSETS_DIR, "screen_02_quest_feed.png")
    if os.path.exists(feed_img_path):
        slide4.shapes.add_picture(feed_img_path, Inches(6.6), Inches(1.9), width=Inches(5.833))

    tb_cap = slide4.shapes.add_textbox(Inches(6.6), Inches(6.2), Inches(5.833), Inches(0.4))
    p_c = tb_cap.text_frame.paragraphs[0]
    p_c.text = "Giao diện Discover Partners: Bảng tin Quest Feed, Bộ lọc môn học & Widget Hero"
    p_c.font.size = Pt(10)
    p_c.font.italic = True
    p_c.font.color.rgb = C_MINT
    p_c.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 5: PART 2 — KỸ THUẬT ĐÃ ÁP DỤNG: PURE PYTHON STACK
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "PART 2: TECHNICAL ARCHITECTURE", "Kiến Trúc Hệ Thống: 100% Pure Python Stack", "Zero External Dependencies — Không phụ thuộc Docker, Redis hay cơ sở dữ liệu ngoài")

    # Cột trái: Sơ đồ kiến trúc
    add_card(slide5, Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.0), bg_color=C_CARD_BG, border_color=C_CYAN)
    arch_img_path = os.path.join(ASSETS_DIR, "architecture_diagram.png")
    if os.path.exists(arch_img_path):
        slide5.shapes.add_picture(arch_img_path, Inches(0.95), Inches(1.95), width=Inches(6.5))

    # Cột phải: Điểm sáng kiến trúc
    add_card(slide5, Inches(7.85), Inches(1.8), Inches(4.683), Inches(5.0), bg_color=C_CARD_BG, border_color=C_BORDER)
    tb_arch = slide5.shapes.add_textbox(Inches(8.1), Inches(2.0), Inches(4.2), Inches(4.5))
    tf_a = tb_arch.text_frame
    tf_a.word_wrap = True

    p = tf_a.paragraphs[0]
    p.text = "⚙️ ĐẶC ĐIỂM KIẾN TRÚC NỔI BẬT"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    arch_highlights = [
        ("Zero External Dependencies", "Chạy trực tiếp bằng Python virtualenv (.venv). Giảng viên và hội đồng có thể khởi chạy đồ án ngay mà không cần cài đặt Docker hay Redis."),
        ("Frontend: Reflex (Python-first)", "100% mã UI viết bằng Python, tự động compile sang React SPA. Quản lý trạng thái tập trung qua rx.State và WebSocket sync."),
        ("Backend: FastAPI Async", "Python 3.11+ bất đồng bộ toàn diện, cung cấp RESTful API chuẩn OpenAPI (Swagger UI tại /docs) và native WebSocket."),
        ("In-Memory Real-time Hub", "Quản lý kết nối socket và bộ nhớ đệm (Cache TTL) thuần Python trong RAM, thay thế 100% Redis."),
    ]
    for h, b in arch_highlights:
        p_h = tf_a.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        p_b = tf_a.add_paragraph()
        p_b.text = f"  {b}"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 6: PART 2 — KỸ THUẬT: CƠ SỞ DỮ LIỆU & IN-MEMORY REAL-TIME HUB
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "PART 2: DATA & REAL-TIME ENGINEERING", "Cơ Sở Dữ Liệu SQLite & In-Memory Real-Time Hub", "Mô hình dữ liệu chuẩn hóa 10 bảng và cơ chế điều phối WebSocket độ trễ thấp")

    # Cột trái: Sơ đồ ERD 10 bảng
    add_card(slide6, Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.0), bg_color=C_CARD_BG, border_color=C_GOLD)
    erd_img_path = os.path.join(ASSETS_DIR, "database_erd.png")
    if os.path.exists(erd_img_path):
        slide6.shapes.add_picture(erd_img_path, Inches(0.95), Inches(1.95), width=Inches(6.5))

    # Cột phải: Chi tiết kỹ thuật dữ liệu & real-time
    add_card(slide6, Inches(7.85), Inches(1.8), Inches(4.683), Inches(5.0), bg_color=C_CARD_BG, border_color=C_BORDER)
    tb_db = slide6.shapes.add_textbox(Inches(8.1), Inches(2.0), Inches(4.2), Inches(4.5))
    tf_d = tb_db.text_frame
    tf_d.word_wrap = True

    p = tf_d.paragraphs[0]
    p.text = "💾 DỮ LIỆU & GIAO TIẾP THỜI GIAN THỰC"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GOLD

    db_points = [
        ("SQLite 3 Async (aiosqlite)", "Lưu trữ tập tin forfriend.db nhúng. Kết hợp SQLAlchemy 2.0 Async Session cho hiệu năng đọc/ghi bất đồng bộ cao, không nghẽn luồng."),
        ("10 Quan hệ chuẩn 3NF", "Thiết kế đầy đủ: user, user_subject, post (quest), post_tag, room, room_category, room_participant, rating, friendship, message."),
        ("In-Memory ConnectionManager", "Quản lý kết nối socket dict[str, WebSocket] giúp phát thông báo real-time khi có người xin vào phòng hoặc tin nhắn mới với độ trễ < 30ms."),
        ("LiveKit Cloud SFU WebRTC", "Tích hợp dịch vụ SFU WebRTC phân phối luồng Video/Audio 720p bảo mật qua token động sinh từ backend."),
    ]
    for h, b in db_points:
        p_h = tf_d.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        p_b = tf_d.add_paragraph()
        p_b.text = f"  {b}"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 7: PART 2 — KỸ THUẬT: THUẬT TOÁN GHÉP BẠN (MATCHING ENGINE)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "PART 2: MATCHING ALGORITHM", "Thuật Toán Ghép Bạn Học: Multi-Factor Relevance Scoring", "Tối ưu hóa khả năng gợi ý bạn học phù hợp dựa trên 5 chiều dữ liệu trọng số")

    # Cột trái: Sơ đồ thuật toán
    add_card(slide7, Inches(0.8), Inches(1.8), Inches(7.5), Inches(5.0), bg_color=C_CARD_BG, border_color=C_MINT)
    match_img_path = os.path.join(ASSETS_DIR, "matching_algorithm_diagram.png")
    if os.path.exists(match_img_path):
        slide7.shapes.add_picture(match_img_path, Inches(0.95), Inches(2.2), width=Inches(7.2))

    # Cột phải: Giải thích trọng số W1 - W5
    add_card(slide7, Inches(8.55), Inches(1.8), Inches(3.983), Inches(5.0), bg_color=C_CARD_BG, border_color=C_BORDER)
    tb_m = slide7.shapes.add_textbox(Inches(8.8), Inches(2.0), Inches(3.5), Inches(4.5))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p = tf_m.paragraphs[0]
    p.text = "🎯 Ý NGHĨA 5 TRỌNG SỐ"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_MINT

    weights = [
        ("W1 = 3.0 (Same School)", "Trọng số lớn nhất. So khớp chính xác trường đại học (FTU = FTU) để sinh viên dễ gặp nhau."),
        ("W2 = 2.0 (Same Area)", "70% cùng thành phố + 30% cùng quận/huyện (Đống Đa, Chùa Láng) phục vụ học offline."),
        ("W3 = 2.5 (Subject Overlap)", "Tính chỉ số Jaccard Similarity giữa môn học của user và tags của Quest: |A ∩ B| / |A ∪ B|."),
        ("W4 = 1.0 (Recency Decay)", "Hàm suy giảm số mũ exp(-0.029*t) với chu kỳ bán rã 24h, ưu tiên tin đăng mới."),
        ("W5 = 1.5 (Author Rating)", "Chuẩn hóa sao (Rating/5.0), khuyến khích kết nối với bạn học uy tín, chăm chỉ."),
    ]
    for h, b in weights:
        p_h = tf_m.add_paragraph()
        p_h.text = f"{h}"
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        p_b = tf_m.add_paragraph()
        p_b.text = f"{b}"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 8: PART 3 — CÁC TÍNH NĂNG ĐÃ XÂY DỰNG (MODULE 1 & 2)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "PART 3: FEATURES BUILT (MODULE 1 & 2)", "Tính Năng: Khởi Tạo Hero & Bảng Tin Quest Feed", "Đăng ký an toàn danh tính với 15 Chibi Avatars và Đăng/Lọc nhiệm vụ học tập thông minh")

    # Khối 1: Register & 15 Chibi
    add_card(slide8, Inches(0.8), Inches(1.8), Inches(5.65), Inches(5.0), bg_color=C_CARD_BG, border_color=C_BORDER)
    reg_img_path = os.path.join(ASSETS_DIR, "screen_01_register_avatars.png")
    if os.path.exists(reg_img_path):
        slide8.shapes.add_picture(reg_img_path, Inches(0.95), Inches(1.95), width=Inches(5.35))

    tb_f1 = slide8.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(5.25), Inches(1.3))
    tf_f1 = tb_f1.text_frame
    tf_f1.word_wrap = True
    p1 = tf_f1.paragraphs[0]
    p1.text = "F1: Hero Registration & 15 Chibi Avatars"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = C_MINT
    p2 = tf_f1.add_paragraph()
    p2.text = "Thu thập thông tin học thuật (Email trường .edu.vn, MSSV, Khoa, Ngành) kết hợp chọn 1 trong 15 Avatar Chibi Pixel độc quyền, bảo vệ danh tính sinh viên."
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    # Khối 2: Create Quest & Live Preview
    add_card(slide8, Inches(6.85), Inches(1.8), Inches(5.65), Inches(5.0), bg_color=C_CARD_BG, border_color=C_BORDER)
    quest_img_path = os.path.join(ASSETS_DIR, "screen_03_create_quest_modal.png")
    if os.path.exists(quest_img_path):
        slide8.shapes.add_picture(quest_img_path, Inches(7.0), Inches(1.95), width=Inches(5.35))

    tb_f2 = slide8.shapes.add_textbox(Inches(7.0), Inches(5.4), Inches(5.25), Inches(1.3))
    tf_f2 = tb_f2.text_frame
    tf_f2.word_wrap = True
    p1 = tf_f2.paragraphs[0]
    p1.text = "F2: Create Study Quest Modal & Live Preview"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = C_CYAN
    p2 = tf_f2.add_paragraph()
    p2.text = "Tạo nhiệm vụ học tập Offline (Thư viện/Cà phê) hoặc Online (Phòng ảo). Form thông minh tự động gắn tags môn học và có khung xem trước hiển thị thời gian thực."
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 9: PART 3 — CÁC TÍNH NĂNG ĐÃ XÂY DỰNG (MODULE 3 & 4)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "PART 3: FEATURES BUILT (MODULE 3 & 4)", "Tính Năng: Phòng Học Ảo LiveKit & Đánh Giá Tín Nhiệm", "Hội thảo video HD tích hợp đồng hồ Pomodoro, Chat 1-1 và hệ thống tích lũy EXP")

    # Khối 3: Phòng học ảo LiveKit WebRTC
    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.65), Inches(5.0), bg_color=C_CARD_BG, border_color=C_BORDER)
    room_img_path = os.path.join(ASSETS_DIR, "screen_04_virtual_rooms_lobby.png")
    if os.path.exists(room_img_path):
        slide9.shapes.add_picture(room_img_path, Inches(0.95), Inches(1.95), width=Inches(5.35))

    tb_f3 = slide9.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(5.25), Inches(1.3))
    tf_f3 = tb_f3.text_frame
    tf_f3.word_wrap = True
    p1 = tf_f3.paragraphs[0]
    p1.text = "F3: Adventure Zones & LiveKit WebRTC Call"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = C_GOLD
    p2 = tf_f3.add_paragraph()
    p2.text = "Truyền phát video HD 720p (< 20ms RTT), nhận diện người nói Active Speaker, chia sẻ màn hình, đồng hồ Pomodoro 25 phút đếm ngược và In-Room Chat ghi chú."
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    # Khối 4: Profile, Rating & 1-1 Chat
    add_card(slide9, Inches(6.85), Inches(1.8), Inches(5.65), Inches(5.0), bg_color=C_CARD_BG, border_color=C_BORDER)
    chat_img_path = os.path.join(ASSETS_DIR, "screen_05_hero_profile_chat.png")
    if os.path.exists(chat_img_path):
        slide9.shapes.add_picture(chat_img_path, Inches(7.0), Inches(1.95), width=Inches(5.35))

    tb_f4 = slide9.shapes.add_textbox(Inches(7.0), Inches(5.4), Inches(5.25), Inches(1.3))
    tf_f4 = tb_f4.text_frame
    tf_f4.word_wrap = True
    p1 = tf_f4.paragraphs[0]
    p1.text = "F4: Star Rating, Gamified Badges & 1-1 Chat"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = C_PINK
    p2 = tf_f4.add_paragraph()
    p2.text = "Đánh giá 1-5 sao sau buổi học, tích lũy EXP thăng cấp Hero, mở khóa huy hiệu (Top Scholar, Punctual Master) và nhắn tin riêng 1-1 thời gian thực qua WebSocket."
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 10: PART 4 — KỊCH BẢN DEMO THỰC TẾ (DEMO WALKTHROUGH FLOW)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "PART 4: DEMO WALKTHROUGH", "Kịch Bản Demo Trực Quan (5-Step User Journey)", "Quy trình tuần tự chứng minh tính hoàn thiện và khả năng chạy thực tế của dự án")

    steps = [
        ("BƯỚC 1", "Khởi Tạo Hero", "Đăng ký thông tin học tập, chọn Avatar Chibi #1 'Cyber Scholar', tải thẻ SV xác minh tài khoản.", C_MINT),
        ("BƯỚC 2", "Khám Phá Quest", "Vào bảng tin Discover Partners, chọn lọc môn 'Kinh tế lượng' / 'Python', kiểm tra Match Score 98%.", C_CYAN),
        ("BƯỚC 3", "Đăng Quest Mới", "Mở modal tạo Quest Offline tại Thư viện FTU Tòa A, hệ thống tự động đẩy tin đến bạn học cùng trường.", C_GOLD),
        ("BƯỚC 4", "Phòng Học LiveKit", "Tham gia phòng học ảo Adventure Zone, bật WebRTC call, bật Pomodoro 25 phút tập trung giải bài tập.", C_PINK),
        ("BƯỚC 5", "Đánh Giá & Chat", "Rời phòng, chấm 5★ cho bạn học, thăng cấp Level 14 Study Hero, nhắn tin 1-1 hẹn lịch học tuần sau.", C_MINT),
    ]

    card_step_w = Inches(2.2)
    card_step_h = Inches(4.8)
    for idx, (step_num, step_title, step_desc, accent) in enumerate(steps):
        left_pos = Inches(0.8) + idx * Inches(2.38)
        add_card(slide10, left_pos, Inches(1.8), card_step_w, card_step_h, bg_color=C_CARD_BG, border_color=accent)

        tb = slide10.shapes.add_textbox(left_pos + Inches(0.15), Inches(2.0), card_step_w - Inches(0.3), card_step_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_s = tf.paragraphs[0]
        p_s.text = step_num
        p_s.font.size = Pt(12)
        p_s.font.bold = True
        p_s.font.color.rgb = accent

        p_t = tf.add_paragraph()
        p_t.text = step_title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        p_d = tf.add_paragraph()
        p_d.text = step_desc
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 11: TỔNG KẾT DỰ ÁN & HIỆU QUẢ TRIỂN KHAI
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "PROJECT IMPACT & METRICS", "Tổng Kết Dự Án & Hiệu Quả Triển Khai", "Đánh giá mức độ hoàn thiện, chi phí hạ tầng và giá trị ứng dụng thực tế")

    metrics = [
        ("100% Pure Python", "Fullstack Reflex + FastAPI + SQLite, 0% phụ thuộc Docker / Redis, sẵn sàng triển khai trên mọi môi trường."),
        ("Chi Phí ~0-5$/Tháng", "Tối ưu hóa tối đa chi phí hạ tầng nhờ SQLite nhúng và In-Memory RAM Hub, miễn phí 100% cho sinh viên."),
        ("< 20ms Độ Trễ WebRTC", "Hạ tầng LiveKit Cloud SFU cung cấp trải nghiệm gọi video nhóm mượt mà, ổn định chuẩn 720p HD."),
        ("Bản Quyền Đồ Án Nhóm 10", "Dự án hoàn chỉnh cả về Business Plan, Design System, Báo cáo DOCX 30 trang và mã nguồn chạy thực tế."),
    ]

    card_m_w = Inches(5.65)
    card_m_h = Inches(2.2)
    m_positions = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.85), Inches(1.8)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.85), Inches(4.3)),
    ]

    for idx, (title, desc) in enumerate(metrics):
        pos_l, pos_t = m_positions[idx]
        add_card(slide11, pos_l, pos_t, card_m_w, card_m_h, bg_color=C_CARD_BG, border_color=C_MINT)
        
        tb = slide11.shapes.add_textbox(pos_l + Inches(0.3), pos_t + Inches(0.3), card_m_w - Inches(0.6), card_m_h - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(18)
        p_t.font.bold = True
        p_t.font.color.rgb = C_MINT

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 12: Q&A & THANK YOU (KẾT THÚC & CHUYỂN SANG DEMO)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)

    # Khung trung tâm
    add_card(slide12, Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5), bg_color=C_CARD_BG, border_color=C_MINT)

    tb_end = slide12.shapes.add_textbox(Inches(2.0), Inches(2.0), Inches(9.333), Inches(3.5))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    p1 = tf_end.paragraphs[0]
    p1.text = "CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE!"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf_end.add_paragraph()
    p2.text = "FORFRIEND: STUDENT STUDY BUDDY & VIRTUAL ROOM"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = C_MINT
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_end.add_paragraph()
    p3.text = "\nNhóm 10 — Lớp tín chỉ TIN314(2526-2)He.1"
    p3.font.size = Pt(13)
    p3.font.color.rgb = C_CYAN
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf_end.add_paragraph()
    p4.text = "Giảng viên hướng dẫn: ThS. Trần Công Minh"
    p4.font.size = Pt(12)
    p4.font.color.rgb = C_GOLD
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf_end.add_paragraph()
    p5.text = "🚀 Xin mời Thầy và các bạn cùng theo dõi phần Live Demonstration!"
    p5.font.size = Pt(13)
    p5.font.bold = True
    p5.font.color.rgb = C_PINK
    p5.alignment = PP_ALIGN.CENTER

    prs.save(OUTPUT_PPTX)
    print(f"Presentation saved successfully at: {OUTPUT_PPTX}")
    print(f"File size: {os.path.getsize(OUTPUT_PPTX)} bytes")

if __name__ == "__main__":
    create_presentation()
