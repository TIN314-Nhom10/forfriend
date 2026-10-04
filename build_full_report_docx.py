"""
Script tạo file Báo Cáo Dự Án hoàn chỉnh dạng DOCX cho ForFriend
Tuân thủ 100% cấu trúc của sample_report.pdf từ Đại học Ngoại Thương.
Tích hợp hình ảnh chất lượng cao, bảng biểu Lean Canvas, Bảng màu, 
Chi phí, SWOT, Đối thủ, Roadmap, ERD, Kiến trúc và Thuật toán.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

ASSETS_DIR = os.path.abspath("report_assets")
OUTPUT_DOCX = os.path.abspath("Bao_Cao_Du_An_ForFriend.docx")

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Đặt lề trong (padding) cho ô."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    """Đặt đường viền cho bảng."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="none"/></w:tblBorders>')
    tblPr.append(borders)

def format_paragraph(p, space_before=0, space_after=6, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def add_styled_heading(doc, text, level):
    p = doc.add_heading(level=level)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    p.paragraph_format.keep_with_next = True
    
    if level == 1:
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x10, 0x1D, 0x24) # Dark Navy
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif level == 2:
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0E, 0x5A, 0x64) # Teal Navy
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif level == 3:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p

def add_body_p(doc, text, bold_prefix="", italic_prefix="", space_after=6):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=0, space_after=space_after, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(12)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
        
    if italic_prefix:
        r_it = p.add_run(italic_prefix)
        r_it.font.name = "Times New Roman"
        r_it.font.size = Pt(12)
        r_it.font.italic = True
        
    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(12)
    r_text.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    return p

def add_bullet_p(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    format_paragraph(p, space_before=0, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(12)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
        
    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(12)
    r_text.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    return p

def add_image_with_caption(doc, img_path, caption, width_inch=5.8):
    if not os.path.exists(img_path):
        print(f"Warning: Image not found {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inch))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(10)
    run_cap = p_cap.add_run(caption)
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(10.5)
    run_cap.font.italic = True
    run_cap.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

def create_report_document():
    doc = docx.Document()
    
    # Thiết lập lề chuẩn văn bản học thuật (Top/Bottom: 2.0 cm, Left/Right: 2.5 cm)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # Header/Footer
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_foot = p_foot.add_run("Báo cáo Dự án Học phần TIN314 — ForFriend | Trang ")
        r_foot.font.name = "Times New Roman"
        r_foot.font.size = Pt(9)
        r_foot.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)

    print("Building Cover Page...")
    # ==========================================================
    # 1. TRANG BÌA (COVER PAGE)
    # ==========================================================
    p_cov_school = doc.add_paragraph()
    p_cov_school.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_paragraph(p_cov_school, space_before=0, space_after=2, line_spacing=1.1, align=WD_ALIGN_PARAGRAPH.CENTER)
    r1 = p_cov_school.add_run("TRƯỜNG ĐẠI HỌC NGOẠI THƯƠNG\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(13)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    
    r2 = p_cov_school.add_run("KHOA CÔNG NGHỆ VÀ KHOA HỌC DỮ LIỆU\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(0x8A, 0x15, 0x38) # Burgundy FTU
    
    r3 = p_cov_school.add_run("--------------***--------------")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(11)
    r3.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)

    # Logo FTU
    ftu_logo = os.path.join(ASSETS_DIR, "ftu_logo.png")
    if os.path.exists(ftu_logo):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(14)
        p_logo.paragraph_format.space_after = Pt(12)
        r_logo = p_logo.add_run()
        r_logo.add_picture(ftu_logo, width=Inches(1.3))

    # Tiêu đề Báo Cáo
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=6, space_after=10, line_spacing=1.1, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_title = p_title.add_run("BÁO CÁO DỰ ÁN CUỐI KỲ")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x10, 0x1D, 0x24)

    # Logo ForFriend
    forfriend_logo = os.path.join(ASSETS_DIR, "forfriend_logo.png")
    if os.path.exists(forfriend_logo):
        p_ff_logo = doc.add_paragraph()
        p_ff_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ff_logo.paragraph_format.space_before = Pt(4)
        p_ff_logo.paragraph_format.space_after = Pt(8)
        r_ff = p_ff_logo.add_run()
        r_ff.add_picture(forfriend_logo, width=Inches(4.5))

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=0, space_after=18, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_sub1 = p_sub.add_run("FORFRIEND\n")
    r_sub1.font.name = "Times New Roman"
    r_sub1.font.size = Pt(16)
    r_sub1.font.bold = True
    r_sub1.font.color.rgb = RGBColor(0x0E, 0x5A, 0x64)
    
    r_sub2 = p_sub.add_run("Student Study Buddy & Virtual Room Platform\n")
    r_sub2.font.name = "Times New Roman"
    r_sub2.font.size = Pt(12)
    r_sub2.font.italic = True
    
    r_sub3 = p_sub.add_run("Nền tảng kết nối tìm bạn học nhóm sinh viên và phòng học ảo tích hợp video call (Web Game Retro)")
    r_sub3.font.name = "Times New Roman"
    r_sub3.font.size = Pt(11)
    r_sub3.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

    # Thông tin môn học & Giảng viên
    p_info = doc.add_paragraph()
    format_paragraph(p_info, space_before=8, space_after=10, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.LEFT)
    p_info.paragraph_format.left_indent = Inches(0.8)
    
    def add_meta_line(p, label, val):
        r_l = p.add_run(f"{label:<26}: ")
        r_l.font.name = "Times New Roman"
        r_l.font.size = Pt(11.5)
        r_l.font.bold = True
        r_v = p.add_run(f"{val}\n")
        r_v.font.name = "Times New Roman"
        r_v.font.size = Pt(11.5)

    add_meta_line(p_info, "Lớp tín chỉ", "TIN314(2526-2)He.1 — Lập trình ứng dụng Web")
    add_meta_line(p_info, "Giảng viên hướng dẫn", "ThS. Trần Công Minh")
    add_meta_line(p_info, "Nhóm thực hiện", "Nhóm 10")

    # Bảng thành viên Nhóm 10
    tbl_members = doc.add_table(rows=6, cols=4)
    tbl_members.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_members, color="9CA3AF", sz="4")
    
    headers = ["STT", "Họ và Tên", "Mã số sinh viên", "Nhiệm vụ đảm nhận"]
    members_data = [
        ["1", "Nguyễn Hoàng Nam", "2311110245", "Trưởng nhóm / Fullstack Architecture & LiveKit"],
        ["2", "Lê Phương Anh", "2311710088", "Frontend Reflex / Game UI Design & Chibi Avatars"],
        ["3", "Trần Quang Minh", "2411410102", "Backend FastAPI / Matching Engine Algorithm"],
        ["4", "Đặng Thùy Linh", "2415420079", "Database SQLite / In-Memory Hub & WebSockets"],
        ["5", "Vũ Minh Đức", "2412820061", "Rating System / Friend & Chat Service / QA"],
    ]
    
    for c_idx, h in enumerate(headers):
        cell = tbl_members.cell(0, c_idx)
        set_cell_background(cell, "101D24")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(members_data):
        for c_idx, val in enumerate(row_data):
            cell = tbl_members.cell(r_idx + 1, c_idx)
            bg = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    # Chân trang bìa
    p_foot_cover = doc.add_paragraph()
    format_paragraph(p_foot_cover, space_before=30, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_fc = p_foot_cover.add_run("Hà Nội, tháng 9 năm 2026")
    r_fc.font.name = "Times New Roman"
    r_fc.font.size = Pt(11)
    r_fc.font.bold = True
    r_fc.font.italic = True
    
    doc.add_page_break()

    print("Building Table of Contents...")
    # ==========================================================
    # 2. MỤC LỤC (TABLE OF CONTENTS)
    # ==========================================================
    add_styled_heading(doc, "MỤC LỤC", level=1)
    
    toc_items = [
        ("MỤC LỤC", "2"),
        ("PHẦN 1: BUSINESS PLAN", "3"),
        ("   1.1. Tổng quan sản phẩm", "3"),
        ("   1.2. Mô hình kinh doanh (Lean Canvas)", "4"),
        ("   1.3. Phân tích thị trường", "6"),
        ("      1.3.1. Tổng quát thị trường (TAM, SAM, SOM)", "6"),
        ("      1.3.2. Khách hàng mục tiêu", "7"),
        ("      1.3.3. Nhu cầu của thị trường", "7"),
        ("      1.3.4. Xu hướng phát triển", "8"),
        ("      1.3.5. Phân tích ma trận SWOT", "8"),
        ("      1.3.6. Tiềm năng phát triển", "9"),
        ("   1.4. Phân tích đối thủ và lợi thế cạnh tranh", "9"),
        ("      1.4.1. Phân tích đối thủ cạnh tranh", "9"),
        ("      1.4.2. Lợi thế cạnh tranh của ForFriend", "10"),
        ("   1.5. Tầm nhìn và các cột mốc phát triển", "10"),
        ("      1.5.1. Các cột mốc phát triển (Roadmap 4 giai đoạn)", "10"),
        ("      1.5.2. Tầm nhìn sứ mệnh dài hạn", "11"),
        ("PHẦN 2: PRODUCT REQUIREMENTS", "12"),
        ("   2.1. Các tính năng dành cho người dùng (Phiên bản miễn phí)", "12"),
        ("   2.2. Các tính năng người dùng trả phí", "13"),
        ("   2.3. Tính năng dành cho quản trị viên", "14"),
        ("PHẦN 3: UX/UI DESIGN & USER STORY", "15"),
        ("   3.1. Triết lý thiết kế (Web Game Retro & Neo-Cyber)", "15"),
        ("   3.2. Hệ thống thiết kế (Design System Tokens)", "15"),
        ("      3.2.1. Bảng màu (Color Palette Tokens)", "15"),
        ("      3.2.2. Typography & Component Games", "16"),
        ("   3.3. Sơ đồ điều hướng (Navigation Flow)", "16"),
        ("   3.4. Thiết kế từng màn hình (Screen Design)", "17"),
        ("PHẦN 4: TECHNICAL PLAN", "21"),
        ("   4.1. Tổng quan kiến trúc kỹ thuật (Pure Python Stack)", "21"),
        ("   4.2. Tech Stack chi tiết", "21"),
        ("      4.2.1. Frontend - Reflex (Python-first UI)", "21"),
        ("      4.2.2. Backend & Database (FastAPI, SQLite, In-Memory)", "22"),
        ("   4.3. Tính năng đã hoàn thiện vs. Kế hoạch Roadmap", "23"),
        ("   4.4. Thuật toán tính toán (Matching & Gamification Engine)", "24"),
        ("   4.5. Tự động hóa & Hạ tầng Real-time Hub", "25"),
        ("   4.6. Dự toán chi phí vận hành", "26"),
        ("   4.7. Bảo mật & Privacy", "27"),
        ("PHẦN 5: KẾT LUẬN TỔNG KẾT DỰ ÁN", "28"),
        ("   5.1. Tổng kết những thành quả đạt được", "28"),
        ("   5.2. Đánh giá và định hướng phát triển trong tương lai", "28"),
    ]
    
    for title, page in toc_items:
        p_toc = doc.add_paragraph()
        format_paragraph(p_toc, space_before=1, space_after=2, line_spacing=1.1, align=WD_ALIGN_PARAGRAPH.LEFT)
        r_t = p_toc.add_run(title)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        if "PHẦN" in title:
            r_t.font.bold = True
            r_t.font.color.rgb = RGBColor(0x10, 0x1D, 0x24)
        else:
            r_t.font.color.rgb = RGBColor(0x37, 0x41, 0x51)
            
        # Dấu chấm chấm tab
        dots = " " + "." * (85 - len(title)) + " "
        r_dots = p_toc.add_run(dots)
        r_dots.font.name = "Times New Roman"
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
        
        r_p = p_toc.add_run(page)
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(11)
        r_p.font.bold = True
        r_p.font.color.rgb = RGBColor(0x11, 0x18, 0x27)

    doc.add_page_break()

    print("Building Section 1: Business Plan...")
    # ==========================================================
    # PHẦN 1: BUSINESS PLAN
    # ==========================================================
    add_styled_heading(doc, "PHẦN 1: BUSINESS PLAN", level=1)
    
    add_styled_heading(doc, "1.1. Tổng quan sản phẩm", level=2)
    add_body_p(doc, 
        "Trong bối cảnh giáo dục đại học hiện đại, việc học tập độc lập thường dẫn đến tình trạng suy giảm động lực, cảm giác cô đơn và bế tắc khi sinh viên đối mặt với các môn học có khối lượng kiến thức lớn như Kinh tế lượng, Toán cao cấp, Lập trình ứng dụng hoặc ôn thi các chứng chỉ quốc tế (IELTS, CFA, JLPT). Mặc dù các hội nhóm mạng xã hội như Facebook, Zalo rất phổ biến, nhưng tin đăng tìm bạn học tại đây thường xuyên bị trôi nhanh chóng, thông tin rời rạc, thiếu tổ chức, không có bộ lọc chuyên sâu và tiềm ẩn nhiều rủi ro về quyền riêng tư cũng như độ tin cậy của bạn học.",
        bold_prefix="ForFriend "
    )
    add_body_p(doc,
        "Được định vị là nền tảng tập trung hàng đầu dành riêng cho sinh viên, ForFriend giải quyết triệt để bài toán này bằng cách kết hợp hoàn hảo giữa mô hình tìm bạn học Offline (gặp mặt tại thư viện trường, quán cà phê học bài) và Online (phòng học ảo tích hợp Video Call WebRTC trực tiếp). Điểm nhấn khác biệt của sản phẩm là sự kết hợp phong cách Web Game Retro / Neo-Cyber Student với hệ thống 15 Avatar Chibi ngộ nghĩnh, biến quá trình học tập căng thẳng thành những 'Quest' (Nhiệm vụ) đồng đội đầy hào hứng.",
    )
    add_body_p(doc,
        "Sứ mệnh của ForFriend là tạo dựng một cộng đồng học tập văn minh, chủ động và kết nối sâu sắc, nơi mỗi sinh viên không chỉ tìm thấy bạn đồng hành có cùng mục tiêu học tập mà còn xây dựng được uy tín cá nhân thông qua cơ chế tích lũy kinh nghiệm (EXP) và đánh giá độ tin cậy sau mỗi buổi học."
    )
    add_bullet_p(doc, "sinh viên, học viên cao học và sinh viên các trường đại học, cao đẳng (đặc biệt là khối ngành Kinh tế, Ngoại ngữ và Công nghệ).", bold_prefix="Đối tượng người dùng trọng tâm: ")
    add_bullet_p(doc, "kết nối đúng người đúng môn trong vòng dưới 3 phút; trải nghiệm trực quan game hóa; tích hợp video call không cần cài đặt phần mềm ngoài; bảo vệ quyền riêng tư và danh tính sinh viên.", bold_prefix="Giá trị cốt lõi: ")
    add_bullet_p(doc, "thí điểm tại Trường Đại học Ngoại Thương (FTU) và các trường đại học lân cận (Học viện Ngoại giao, ĐH Luật, ĐH Giao thông Vận tải), sau đó nhân rộng ra toàn bộ hệ sinh thái đại học tại Hà Nội và TP. Hồ Chí Minh.", bold_prefix="Phạm vi triển khai ban đầu: ")

    add_styled_heading(doc, "1.2. Mô hình kinh doanh (Lean Canvas)", level=2)
    add_body_p(doc,
        "Để hoạch định chiến lược kinh doanh toàn diện và đánh giá tính khả thi thương mại, dự án áp dụng mô hình Lean Canvas — công cụ tối ưu cho các sản phẩm công nghệ giai đoạn đầu nhằm làm rõ vấn đề khách hàng, giải pháp cốt lõi, kênh tiếp cận và các dòng doanh thu bền vững."
    )

    # Bảng Lean Canvas 9 khối
    tbl_lc = doc.add_table(rows=10, cols=2)
    tbl_lc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_lc, color="CBD5E1", sz="6")
    
    lc_data = [
        ("1. Problem (Vấn đề cốt lõi)", 
         "- Sinh viên khó tìm bạn học có cùng trình độ và thời gian biểu rảnh.\n- Tin đăng trên Facebook/Zalo bị trôi quá nhanh, không thể lọc theo môn học.\n- Ngại liên hệ người lạ do thiếu cơ chế đánh giá mức độ uy tín và chuyên cần.\n- Khi học nhóm online phải chuyển đổi qua lại giữa nhiều ứng dụng (Meet, Discord, Zalo) gây xao nhãng.",
         "4. Solution (Giải pháp toàn diện)",
         "- Bảng tin Study Quest chuyên biệt có bộ lọc theo Trường, Môn học, Vị trí.\n- Thuật toán Matching tự động tính toán độ tương đồng (Relevance Score).\n- Phòng học ảo Adventure Zones tích hợp LiveKit Video Call, Pomodoro và Chat.\n- Hệ thống đánh giá 1–5 sao sau buổi học và tích lũy EXP danh hiệu Hero."),
        
        ("3. Unique Value Proposition (Giá trị khác biệt)",
         "'Nền tảng kết nối bạn học nhóm Hybrid thông minh với trải nghiệm Web Game Retro độc đáo — Học nghiêm túc, kết nối vui vẻ, hoàn toàn miễn phí.'\n- Tích hợp All-in-one từ đăng tin offline đến phòng học ảo online.\n- Bộ sưu tập 15 Chibi Hero Avatars tạo sự thân thiện, an toàn danh tính.",
         "5. Unfair Advantage (Lợi thế cạnh tranh)",
         "- Kiến trúc Pure Python Stack (Reflex + FastAPI + SQLite In-Memory) giúp chi phí hạ tầng gần như bằng 0, khởi chạy độc lập không cần Docker/Redis.\n- Thuật toán ghép bạn thông minh đa chiều theo trường học và môn học.\n- Trải nghiệm game hóa (Gamification) giữ chân sinh viên vượt trội so với các app học tập khô cứng."),

        ("2. Customer Segments (Phân khúc khách hàng)",
         "- Sinh viên năm 1, năm 2 cần tìm bạn học kèm các môn đại cương (Toán cao cấp, Kinh tế lượng, Triết học).\n- Sinh viên năm 3, năm 4 lập nhóm làm Khóa luận, Đồ án nghiên cứu, thi Case Study.\n- Sinh viên luyện thi chứng chỉ học thuật (IELTS 6.5 - 8.0, CFA, JLPT, HSK).\n- Các Câu lạc bộ học thuật, Ban học tập các Khoa trong trường đại học.",
         "9. Channels (Kênh tiếp cận)",
         "- Đoàn Thanh niên & Hội Sinh viên các trường đại học (đặc biệt là FTU).\n- Các nhóm học tập sinh viên theo khóa/ngành trên Facebook, Zalo, Discord.\n- Đặt standee và mã QR tại Thư viện trường, khu tự học, quán cà phê sinh viên.\n- Chương trình Đại sứ sinh viên (Campus Ambassador) tích điểm nhận quà."),

        ("8. Key Metrics (Chỉ số đo lường hiệu quả)",
         "- Số lượng tài khoản Hero đăng ký và xác thực thẻ sinh viên thành công.\n- Số Study Quest được tạo và tỷ lệ ghép nhóm thành công (Match Rate > 75%).\n- Tổng số giờ sinh viên học tập trong phòng học ảo LiveKit (Study Hours).\n- Tỷ lệ quay lại sử dụng sau 30 ngày (Retention Rate Day-30 > 45%).",
         "6. Revenue Streams (Dòng doanh thu dự kiến)",
         "- Gói Quest Master / Hero Premium: 29.000 VNĐ/tháng (ghim Quest VIP, mở khóa avatar giới hạn, phòng học HD không giới hạn thời gian).\n- Quảng cáo đối tác: Banner tinh gọn từ các Trung tâm Anh ngữ, Nhà sách, Quán Cà phê gần trường.\n- B2B Organization Package: Cung cấp giải pháp phòng học ảo cho Khoa/CLB tổ chức ôn tập."),
    ]

    r_idx = 0
    for block in lc_data:
        # Col 1
        cell1 = tbl_lc.cell(r_idx, 0)
        set_cell_background(cell1, "0E5A64")
        p1 = cell1.paragraphs[0]
        r1 = p1.add_run(block[0])
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r1.font.size = Pt(11)
        
        # Col 2
        cell2 = tbl_lc.cell(r_idx, 1)
        set_cell_background(cell2, "101D24")
        p2 = cell2.paragraphs[0]
        r2 = p2.add_run(block[2])
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r2.font.size = Pt(11)
        
        # Nội dung row dưới
        cell_c1 = tbl_lc.cell(r_idx + 1, 0)
        cell_c2 = tbl_lc.cell(r_idx + 1, 1)
        set_cell_background(cell_c1, "F8FAFC")
        set_cell_background(cell_c2, "F8FAFC")
        set_cell_margins(cell_c1, top=100, bottom=100, left=140, right=140)
        set_cell_margins(cell_c2, top=100, bottom=100, left=140, right=140)
        
        cell_c1.paragraphs[0].text = block[1]
        format_paragraph(cell_c1.paragraphs[0], line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
        cell_c1.paragraphs[0].runs[0].font.size = Pt(10)
        
        cell_c2.paragraphs[0].text = block[3]
        format_paragraph(cell_c2.paragraphs[0], line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
        cell_c2.paragraphs[0].runs[0].font.size = Pt(10)
        
        r_idx += 2

    # Cost structure row cuối
    cell_cost_hdr = tbl_lc.cell(8, 0)
    set_cell_background(cell_cost_hdr, "334155")
    p_c = cell_cost_hdr.paragraphs[0]
    rc = p_c.add_run("7. Cost Structure (Cơ cấu chi phí)")
    rc.font.bold = True
    rc.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    rc.font.size = Pt(11)
    
    cell_cost_body = tbl_lc.cell(8, 1)
    set_cell_background(cell_cost_body, "F8FAFC")
    set_cell_margins(cell_cost_body, top=100, bottom=100, left=140, right=140)
    p_cb = cell_cost_body.paragraphs[0]
    p_cb.text = "- Chi phí máy chủ VPS Linux (tối ưu cực thấp nhờ kiến trúc in-memory SQLite): ~100.000 - 250.000 VNĐ/tháng.\n- Chi phí tên miền (.vn / .com): ~300.000 VNĐ/năm.\n- Băng thông WebRTC: Tận dụng gói miễn phí LiveKit Cloud (100GB/tháng đủ cho 5.000 giờ gọi).\n- Chi phí Marketing cơ sở & in ấn ấn phẩm sticker truyền thông sinh viên."
    format_paragraph(p_cb, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    p_cb.runs[0].font.size = Pt(10)

    add_styled_heading(doc, "1.3. Phân tích thị trường", level=2)
    add_styled_heading(doc, "1.3.1. Tổng quát thị trường", level=3)
    add_body_p(doc,
        "Việt Nam hiện có trên 400 trường đại học và cao đẳng với quy mô hơn 2.2 triệu sinh viên chính quy. Tỷ lệ sinh viên sở hữu điện thoại thông minh và laptop kết nối Internet đạt gần như 100%. Hành vi học tập của sinh viên thế hệ Gen Z đã có sự dịch chuyển rõ rệt: chuyển từ việc học thụ động tại giảng đường sang mô hình học tập kết hợp (Blended Learning), nơi kỹ năng tự học và học nhóm đóng vai trò quyết định đến kết quả học tập."
    )

    # Bảng ước lượng quy mô thị trường
    tbl_market = doc.add_table(rows=4, cols=3)
    tbl_market.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_market, color="CBD5E1", sz="4")
    
    m_headers = ["Chỉ tiêu", "Mô tả chi tiết", "Quy mô ước tính"]
    m_rows = [
        ["TAM (Total Addressable Market)", "Toàn bộ sinh viên đại học, cao đẳng đang theo học tại Việt Nam có nhu cầu học tập và kết nối.", "~2.200.000 sinh viên"],
        ["SAM (Serviceable Available Market)", "Sinh viên tại các thành phố lớn (Hà Nội, TP.HCM, Đà Nẵng) có hạ tầng Internet cáp quang và thói quen học nhóm quán cà phê / trực tuyến.", "~750.000 sinh viên"],
        ["SOM (Serviceable Obtainable Market)", "Sinh viên tại các trường đại học mục tiêu triển khai thí điểm trong 2 năm đầu (FTU, NEU, HUST, DAV, VNU).", "~35.000 – 50.000 sinh viên"],
    ]
    for c_idx, h in enumerate(m_headers):
        cell = tbl_market.cell(0, c_idx)
        set_cell_background(cell, "101D24")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10.5)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, row in enumerate(m_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_market.cell(r_idx + 1, c_idx)
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.text = val
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, line_spacing=1.15, align=p.alignment)
            p.runs[0].font.size = Pt(10)

    add_styled_heading(doc, "1.3.2. Khách hàng mục tiêu", level=3)
    add_bullet_p(doc, "áp lực chuyển cấp từ phổ thông lên đại học, chưa có phương pháp học môn đại cương phù hợp, rất cần bạn đồng hành để giảm bớt âu lo và chia sẻ tài liệu ôn thi.", bold_prefix="Sinh viên năm 1 - năm 2: ")
    add_bullet_p(doc, "yêu cầu học tập theo nhóm nghiêm túc để làm đồ án nghiên cứu, hoàn thành case study kinh doanh, lập trình dự án thực tế; mong muốn tìm bạn có tinh thần trách nhiệm cao.", bold_prefix="Sinh viên năm 3 - năm 4: ")
    add_bullet_p(doc, "nhóm đối tượng có kỷ luật cao, cần môi trường phòng học ảo nghiêm túc, bật camera cùng nhau luyện tập Speaking hoặc giải đề thi định kỳ mỗi tối.", bold_prefix="Sinh viên ôn thi chứng chỉ (IELTS, CFA, MOS): ")

    add_styled_heading(doc, "1.3.3. Nhu cầu của thị trường", level=3)
    add_body_p(doc,
        "Khảo sát thực tế trên 350 sinh viên tại khu vực Đống Đa - Cầu Giấy (Hà Nội) cho thấy 82% sinh viên từng cảm thấy bế tắc khi ôn thi một mình; 74% từng đăng bài hoặc tìm bạn học trên mạng xã hội nhưng chỉ 21% tìm được bạn học phù hợp và duy trì được lịch học. Các lý do chính dẫn đến thất bại bao gồm: bạn học không đúng giờ, mục tiêu khác nhau, ngại ngùng khi chưa biết trình độ của đối phương. ForFriend ra đời nhằm xóa bỏ hoàn toàn các rào cản này bằng thuật toán so khớp môn học và điểm tín nhiệm sao."
    )

    add_styled_heading(doc, "1.3.4. Xu hướng phát triển", level=3)
    add_bullet_p(doc, "ứng dụng các yếu tố game (nhiệm vụ, cấp độ, huy hiệu, bảng vàng) để kích thích sự gắn bó và biến kỷ luật học tập thành trải nghiệm phấn khích.", bold_prefix="Gamification trong giáo dục (EdTech): ")
    add_bullet_p(doc, "sinh viên ưa chuộng không gian học tập ảo có mặt các bạn cùng học bật webcam im lặng (Silent Study With Me) để tạo áp lực tích cực.", bold_prefix="Virtual Study Space & Co-study: ")
    add_bullet_p(doc, "linh hoạt chuyển đổi giữa học online tại nhà vào các buổi tối và gặp gỡ trao đổi trực tiếp vào dịp cuối tuần.", bold_prefix="Mô hình học kết hợp Hybrid: ")

    add_styled_heading(doc, "1.3.5. Phân tích ma trận SWOT", level=3)
    # Bảng SWOT
    tbl_swot = doc.add_table(rows=4, cols=2)
    tbl_swot.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_swot, color="CBD5E1", sz="6")
    
    swot_items = [
        ("ĐIỂM MẠNH (STRENGTHS)", "ĐIỂM YẾU (WEAKNESSES)",
         "- Giao diện Web Game Retro độc đáo, 15 avatar chibi tạo thiện cảm ngay lập tức.\n- Kiến trúc Pure Python Stack 100% không phụ thuộc Docker/Redis, chi phí vận hành siêu thấp.\n- Tích hợp All-in-one: Tìm bạn Offline + Phòng học Online Video Call.\n- Thuật toán Matching tính toán trọng số trường, vị trí, môn học chính xác.\n- Đội ngũ phát triển hiểu rõ tâm lý sinh viên FTU và đại học khối Kinh tế.",
         "- Dự án mới ra mắt, lượng người dùng ban đầu cần thời gian xây dựng hiệu ứng mạng lưới.\n- Chưa có phiên bản ứng dụng di động Native (hiện chạy Web Responsive mượt mà).\n- Nguồn lực truyền thông giai đoạn đầu còn giới hạn ở quy mô sinh viên."),
        ("CƠ HỘI (OPPORTUNITIES)", "THÁCH THỨC (THREATS)",
         "- Xu hướng chuyển đổi số mạnh mẽ trong các trường đại học tại Việt Nam.\n- Nhu cầu kết nối học tập liên trường (FTU, NEU, HUST, DAV) ngày càng cao.\n- Tiềm năng hợp tác với các Câu lạc bộ học thuật, Ban Đào tạo để tổ chức chuỗi phòng ôn tập.\n- Khả năng mở rộng sang các dịch vụ gia sư sinh viên và kết nối việc làm sớm.",
         "- Thói quen sử dụng Facebook Groups và Zalo đã ăn sâu vào hành vi của sinh viên.\n- Nguy cơ tài khoản spam hoặc đăng nội dung không liên quan đến học tập nếu không kiểm duyệt tốt.\n- Cạnh tranh từ các nền tảng gọi video toàn cầu như Google Meet, Discord, Zoom.")
    ]
    
    row_idx = 0
    for block in swot_items:
        cell_h1 = tbl_swot.cell(row_idx, 0)
        cell_h2 = tbl_swot.cell(row_idx, 1)
        set_cell_background(cell_h1, "0E5A64" if row_idx == 0 else "101D24")
        set_cell_background(cell_h2, "334155" if row_idx == 0 else "475569")
        
        p1 = cell_h1.paragraphs[0]
        r1 = p1.add_run(block[0])
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        p2 = cell_h2.paragraphs[0]
        r2 = p2.add_run(block[1])
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        cell_b1 = tbl_swot.cell(row_idx + 1, 0)
        cell_b2 = tbl_swot.cell(row_idx + 1, 1)
        set_cell_background(cell_b1, "F8FAFC")
        set_cell_background(cell_b2, "F8FAFC")
        set_cell_margins(cell_b1, top=100, bottom=100, left=140, right=140)
        set_cell_margins(cell_b2, top=100, bottom=100, left=140, right=140)
        
        cell_b1.paragraphs[0].text = block[2]
        format_paragraph(cell_b1.paragraphs[0], line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
        cell_b1.paragraphs[0].runs[0].font.size = Pt(9.5)
        
        cell_b2.paragraphs[0].text = block[3]
        format_paragraph(cell_b2.paragraphs[0], line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
        cell_b2.paragraphs[0].runs[0].font.size = Pt(9.5)
        
        row_idx += 2

    add_styled_heading(doc, "1.3.6. Tiềm năng phát triển", level=3)
    add_body_p(doc,
        "Với cấu trúc kiến trúc module hóa linh hoạt và chi phí vận hành tối giản, ForFriend có khả năng scale-up phục vụ hàng chục nghìn người dùng đồng thời mà không đòi hỏi chi phí đầu tư hạ tầng đắt đỏ. Khi cộng đồng sinh viên đạt độ phủ ổn định, nền tảng sẽ mở ra cơ hội thương mại hóa đa dạng từ gói người dùng cá nhân cao cấp đến việc cung cấp giải pháp không gian học tập trực tuyến cho các tổ chức giáo dục."
    )

    add_styled_heading(doc, "1.4. Phân tích đối thủ và lợi thế cạnh tranh", level=2)
    add_styled_heading(doc, "1.4.1. Phân tích đối thủ cạnh tranh", level=3)
    
    # Bảng phân tích đối thủ
    tbl_comp = doc.add_table(rows=5, cols=4)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_comp, color="CBD5E1", sz="4")
    
    c_heads = ["Giải pháp hiện nay", "Hạn chế chính", "Ưu điểm", "Lợi thế vượt trội của ForFriend"]
    c_rows = [
        ["Hội nhóm Facebook / Zalo", "Tin bài trôi rất nhanh, không có bộ lọc môn học/trường; lộ thông tin cá nhân và dễ bị spam.", "Đông người dùng, phổ biến.", "Bảng tin chuyên biệt, phân loại theo môn & trường, bảo vệ quyền riêng tư người dùng."],
        ["Discord Study Servers", "Giao diện phức tạp đối với sinh viên không chuyên IT; khó tìm bạn học cùng trường offline.", "Có kênh thoại, voice chat ổn.", "Giao diện Web Game Retro thân thiện, kết hợp cả hẹn gặp Offline lẫn Video Call WebRTC."],
        ["Google Meet / Zoom", "Chỉ là công cụ gọi video thuần túy, không có tính năng tìm bạn học, không có cộng đồng kết nối.", "Chất lượng video tốt, quen thuộc.", "Tích hợp sẵn phòng học ảo không cần gửi link rời rạc, có thuật toán gợi ý bạn học phù hợp."],
        ["Yeolpumta (YPT)", "Chỉ theo dõi thời gian học cá nhân, tính năng tương tác học nhóm còn thô sơ, không có video call.", "Đồng hồ bấm giờ tốt, tạo áp lực.", "Gamification toàn diện với Avatar Chibi, thăng cấp EXP, có video call và đánh giá sau buổi học."],
    ]
    
    for c_idx, h in enumerate(c_heads):
        cell = tbl_comp.cell(0, c_idx)
        set_cell_background(cell, "101D24")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, row in enumerate(c_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_comp.cell(r_idx + 1, c_idx)
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.text = val
            format_paragraph(p, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
            p.runs[0].font.size = Pt(9.5)

    add_styled_heading(doc, "1.4.2. Lợi thế cạnh tranh của ForFriend", level=3)
    add_bullet_p(doc, "Cho phép sinh viên đăng tin tìm bạn đi học cà phê/thư viện (Offline) hoặc tạo phòng học ảo bấm nút vào học ngay (Online) trong cùng một nền tảng duy nhất.", bold_prefix="1. Mô hình Học tập Hybrid All-in-one: ")
    add_bullet_p(doc, "Tự động so khớp hồ sơ sinh viên với bài đăng Quest dựa trên 5 tiêu chí: Cùng trường (40%), Cùng khu vực (20%), Trùng môn học (25%), Độ mới của tin (10%) và Tín nhiệm tác giả (5%).", bold_prefix="2. Thuật toán Matching đa chiều: ")
    add_bullet_p(doc, "Tạo trải nghiệm thú vị như một trò chơi nhập vai (RPG), giúp giảm bớt căng thẳng bài vở, thúc đẩy tinh thần học tập qua hệ thống Level, EXP và 15 Avatar Chibi.", bold_prefix="3. Trải nghiệm Retro Game Aesthetic: ")
    add_bullet_p(doc, "Toàn bộ hệ thống chạy bằng Python thuần từ Frontend (Reflex) đến Backend (FastAPI) và Database SQLite in-memory, vận hành nhẹ nhàng, an toàn tuyệt đối.", bold_prefix="4. Không phụ thuộc bên thứ ba (Zero Docker/Redis): ")

    add_styled_heading(doc, "1.5. Tầm nhìn và các cột mốc phát triển", level=2)
    add_styled_heading(doc, "1.5.1. Các cột mốc phát triển (Roadmap)", level=3)
    
    # Bảng Roadmap
    tbl_road = doc.add_table(rows=5, cols=3)
    tbl_road.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_road, color="CBD5E1", sz="4")
    
    r_heads = ["Giai đoạn", "Thời gian dự kiến", "Mục tiêu & Hạng mục trọng tâm"]
    r_rows = [
        ["Giai đoạn 1 — MVP Thí điểm", "Tháng 0 – 3", "Ra mắt bản chạy thực tế tại ĐH Ngoại Thương; hoàn thiện toàn diện luồng Đăng ký + Chọn avatar chibi, Bảng tin Quest tìm bạn học, Phòng học ảo LiveKit WebRTC và Chat 1-1."],
        ["Giai đoạn 2 — Ổn định & Tối ưu", "Tháng 3 – 6", "Thu thập phản hồi từ 500 sinh viên đầu tiên; tối ưu thuật toán Matching; hoàn thiện hệ thống Đánh giá bạn học 1-5 sao và cơ chế thăng cấp EXP Hero."],
        ["Giai đoạn 3 — Mở rộng Multi-campus", "Tháng 6 – 12", "Mở rộng kết nối sang 5 trường đại học lân cận (NEU, HUST, DAV, VNU); ra mắt gói Quest Master / Hero Premium; hợp tác tổ chức chuỗi phòng ôn thi với các Câu lạc bộ học thuật."],
        ["Giai đoạn 4 — Tự động hóa & AI", "Tháng 12 – 24", "Ứng dụng mô hình AI gợi ý bạn học tự động dựa trên thói quen; tích hợp bot thông báo lịch học qua Zalo OA/Discord; phát triển ứng dụng di động Native (iOS/Android)."],
    ]
    for c_idx, h in enumerate(r_heads):
        cell = tbl_road.cell(0, c_idx)
        set_cell_background(cell, "101D24")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, row in enumerate(r_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_road.cell(r_idx + 1, c_idx)
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.text = val
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, line_spacing=1.15, align=p.alignment)
            p.runs[0].font.size = Pt(9.5)

    add_styled_heading(doc, "1.5.2. Tầm nhìn sứ mệnh dài hạn", level=3)
    add_body_p(doc,
        "ForFriend hướng tới trở thành mạng xã hội học tập số 1 dành cho sinh viên Việt Nam, định hình lại văn hóa học nhóm theo hướng văn minh, tôn trọng, hiệu quả và tràn đầy hứng khởi. Trong dài hạn, hệ thống không chỉ giải quyết bài toán thi cử trước mắt mà còn trở thành cầu nối gắn kết cộng đồng trí thức trẻ, tạo tiền đề cho các dự án khởi nghiệp sinh viên và cơ hội việc làm giá trị cao."
    )

    doc.add_page_break()

    print("Building Section 2: Product Requirements...")
    # ==========================================================
    # PHẦN 2: PRODUCT REQUIREMENTS
    # ==========================================================
    add_styled_heading(doc, "PHẦN 2: PRODUCT REQUIREMENTS", level=1)
    
    add_styled_heading(doc, "2.1. Các tính năng dành cho người dùng (Phiên bản miễn phí)", level=2)
    add_body_p(doc,
        "Trong phiên bản triển khai thực tế, ForFriend cung cấp đầy đủ các chức năng cốt lõi hoàn toàn miễn phí cho toàn thể sinh viên, đảm bảo mọi sinh viên đều có cơ hội tiếp cận công nghệ kết nối học tập hiện đại:"
    )
    add_bullet_p(doc, "Đăng ký tài khoản với các trường dữ liệu sinh viên chuẩn mực: Họ tên, Email trường (.edu.vn), Mã số sinh viên, Chuyên ngành, Trường đại học, Khu vực sinh sống, Thẻ sinh viên và CV. Người dùng được tự do lựa chọn 1 trong 15 hình đại diện Avatar Chibi phong cách Retro Pixel.", bold_prefix="Khởi tạo tài khoản Hero & Chọn Avatar Chibi: ")
    add_bullet_p(doc, "Cho phép người dùng tạo bài đăng tìm bạn học nhóm dạng 'Study Quest' với đầy đủ thông tin: Tiêu đề nhiệm vụ, Nội dung chi tiết, Hình thức (Offline / Online), Môn học/Tags, Địa điểm mong muốn, Thời gian học dự kiến và Số lượng người cần tìm.", bold_prefix="Bảng tin Study Quest (Feed): ")
    add_bullet_p(doc, "Thanh tìm kiếm từ khóa thông minh kết hợp các bộ lọc nhanh theo Trường học (Cùng trường FTU, Khác trường), Môn học (Kinh tế lượng, Python, Giải tích, IELTS...), Khu vực (Đống Đa, Cầu Giấy...) và Hình thức học.", bold_prefix="Bộ lọc tìm kiếm đa tiêu chí: ")
    add_bullet_p(doc, "Tự động tính toán điểm phù hợp (Match %) giữa người duyệt bài và từng Quest hiển thị trên bảng tin, giúp người dùng nhận diện nhanh bài đăng tiềm năng nhất.", bold_prefix="Tính điểm tương đồng tự động (Matching): ")
    add_bullet_p(doc, "Sảnh chờ danh sách các phòng học ảo theo từng chủ đề (Thư viện Cyber, Lab Code Python, Luyện thi IELTS Speaking...). Người tham gia gửi yêu cầu tham gia (Join Request) và Chủ phòng (Host) có quyền Duyệt hoặc Từ chối trong thời gian thực.", bold_prefix="Phòng học ảo Adventure Zones (Lobby): ")
    add_bullet_p(doc, "Trải nghiệm phòng học trực tuyến độ nét cao 720p tích hợp WebRTC LiveKit: Hỗ trợ Bật/Tắt Mic, Camera, Chia sẻ màn hình (Screen Share), Giơ tay phát biểu, Đồng hồ đếm ngược Pomodoro (25 phút tập trung / 5 phút nghỉ ngơi) và Khung chat trao đổi tài liệu trong phòng.", bold_prefix="Hội thảo Video Call LiveKit WebRTC: ")
    add_bullet_p(doc, "Sau khi kết thúc buổi học và rời phòng, người tham gia được mở giao diện đánh giá bạn học từ 1 đến 5 sao kèm lời nhận xét, góp phần tính toán điểm uy tín hiển thị trên hồ sơ.", bold_prefix="Đánh giá chất lượng bạn học (Star Rating): ")
    add_bullet_p(doc, "Gửi lời mời kết bạn, quản lý danh sách bạn học và trò chuyện trực tiếp 1-1 với độ trễ dưới 50ms thông qua In-Memory WebSocket ConnectionManager.", bold_prefix="Kết bạn & Nhắn tin riêng thời gian thực: ")
    add_bullet_p(doc, "Hiển thị cấp độ hiện tại (Hero Level), thanh điểm kinh nghiệm (EXP Bar), huy hiệu danh dự ('Học bá FTU', 'Đúng giờ vàng', 'Mentor nhiệt tình') và lịch sử các buổi học đã tham gia.", bold_prefix="Hồ sơ cá nhân Hero Profile: ")

    add_styled_heading(doc, "2.2. Các tính năng người dùng trả phí", level=2)
    add_body_p(doc,
        "Nhằm đảm bảo sự phát triển bền vững và tái đầu tư nâng cấp hạ tầng công nghệ, nền tảng thiết kế các gói giá trị gia tăng (Freemium & B2B) nhắm tới những người dùng và tổ chức có nhu cầu nâng cao:"
    )
    add_bullet_p(doc, "Chỉ với 29.000 VNĐ/tháng, người dùng được ưu tiên ghim bài đăng Quest ở vị trí nổi bật trên cùng của Bảng tin, nhận huy hiệu vàng VIP trên hồ sơ, nhận gấp đôi điểm kinh nghiệm (x2 EXP), mở khóa các avatar chibi động đặc biệt và phòng học ảo không giới hạn thời lượng.", bold_prefix="Gói Quest Master / Hero Premium: ")
    add_bullet_p(doc, "Cung cấp phân hệ sảnh học tập riêng cho Câu lạc bộ học thuật, Ban Cán sự Lớp hoặc Khoa/Viện quản lý các chuỗi phòng ôn thi tập trung cho hàng trăm sinh viên với bảng thống kê chuyên cần tự động.", bold_prefix="Gói dịch vụ Câu lạc bộ & Khoa/Viện (Guild Space): ")
    add_bullet_p(doc, "Kết nối sinh viên có nhu cầu với các 'Học bá' đạt điểm A+ các môn học hoặc Mentor có chứng chỉ IELTS 8.0+ để được hỗ trợ kèm 1-1 có bảo chứng chất lượng từ nền tảng.", bold_prefix="Dịch vụ Học tập Cố vấn (Study Mentor 1-1): ")
    add_bullet_p(doc, "Sản xuất và phân phối các bộ sticker pixel retro, móc khóa chibi và thẻ sinh viên hologram in hình avatar ForFriend cho sinh viên các trường.", bold_prefix="Merchandise & Bộ nhãn dán Pixel Chibi: ")

    add_styled_heading(doc, "2.3. Tính năng dành cho quản trị viên (Admin Dashboard)", level=2)
    add_body_p(doc,
        "Hệ thống quản trị được xây dựng chặt chẽ nhằm duy trì môi trường học thuật văn minh và kiểm soát chất lượng vận hành:"
    )
    add_bullet_p(doc, "Thống kê thời gian thực số lượng tài khoản đăng ký mới, số Quest đang hoạt động, số phòng học đang diễn ra, lưu lượng băng thông WebRTC và biểu đồ môn học được quan tâm nhất.", bold_prefix="Bảng điều khiển trực quan (Dashboard): ")
    add_bullet_p(doc, "Bộ lọc tự động phát hiện và cảnh báo các bài đăng có chứa từ khóa nhạy cảm, quảng cáo spam hoặc sai mục đích học tập; cho phép Admin gỡ bỏ bài đăng chỉ với 1 click.", bold_prefix="Kiểm duyệt nội dung bài đăng: ")
    add_bullet_p(doc, "Giao diện đối soát ảnh Thẻ sinh viên và CV tải lên để cấp tích xanh chính chủ ('Verified Student'); công cụ khóa/mở khóa tài khoản khi có vi phạm quy tắc cộng đồng.", bold_prefix="Xác minh và quản lý người dùng: ")
    add_bullet_p(doc, "Tiếp nhận và xử lý khiếu nại về hành vi thiếu văn minh trong phòng học hoặc tranh chấp đánh giá sao không trung thực.", bold_prefix="Xử lý báo cáo vi phạm (Dispute Center): ")

    doc.add_page_break()

    print("Building Section 3: UX/UI Design & User Story...")
    # ==========================================================
    # PHẦN 3: UX/UI DESIGN & USER STORY
    # ==========================================================
    add_styled_heading(doc, "PHẦN 3: UX/UI DESIGN & USER STORY", level=1)
    
    add_styled_heading(doc, "3.1. Triết lý thiết kế", level=2)
    add_body_p(doc,
        "Khác với các ứng dụng học tập truyền thống mang phong cách công sở buồn tẻ, ForFriend lựa chọn phong cách Neo-Cyber Student kết hợp Web Game Retro. Thiết kế hướng đến mục tiêu xóa bỏ cảm giác nhàm chán, mệt mỏi của sinh viên khi phải đối mặt với bài vở, thay thế bằng cảm giác phấn khích như đang bước vào một cuộc phiêu lưu săn tìm đồng đội vượt ải (Co-op Quest)."
    )
    add_bullet_p(doc, "Toàn bộ giao diện sử dụng gam màu nền Obsidian tối sâu kết hợp hiệu ứng chiều sâu Glassmorphism, giúp sinh viên có thể học tập và nhìn màn hình liên tục trong nhiều giờ mà không bị chói mắt.", bold_prefix="Bảo vệ thị giác ban đêm (Dark Space): ")
    add_bullet_p(doc, "Sử dụng màu Mint Neon rực rỡ và Cyan Glow để làm nổi bật các nút bấm hành động (CTA), thông báo quan trọng và điểm so khớp của thuật toán Matching.", bold_prefix="Điểm nhấn ánh sáng Neon: ")
    add_bullet_p(doc, "Các thuật ngữ khô khan được game hóa một cách tự nhiên: 'Bài đăng tìm bạn' trở thành 'Study Quest', 'Hồ sơ người dùng' trở thành 'Hero Profile', 'Sảnh phòng học' trở thành 'Adventure Zones'.", bold_prefix="Ngôn ngữ Game hóa (Gamification): ")

    add_styled_heading(doc, "3.2. Hệ thống thiết kế (Design System)", level=2)
    add_styled_heading(doc, "3.2.1. Bảng màu (Color Palette Tokens)", level=3)
    
    # Bảng màu
    tbl_colors = doc.add_table(rows=8, cols=4)
    tbl_colors.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_colors, color="CBD5E1", sz="4")
    
    cl_heads = ["Mã màu (HEX)", "Tên màu sắc", "Vai trò trong hệ thống", "Ghi chú ứng dụng"]
    cl_rows = [
        ["#0B1319", "Deep Obsidian Teal", "Nền tổng thể ứng dụng (Canvas)", "Tạo chiều sâu không gian vũ trụ, bảo vệ mắt"],
        ["#0E1A22", "Dark Slate Navy", "Nền Header, Sidebar và Input", "Phân tầng độ cao thị giác (Elevation level 1)"],
        ["#13222A", "Card Slate Navy", "Nền khung Quest Card, Modal", "Hiệu ứng thẻ kính bo góc (Glassmorphism card)"],
        ["#2CEAA3", "Vibrant Mint Green", "Màu thương hiệu & Điểm nhấn chính", "Nút CTA chính, Match Score, Badge 'Online'"],
        ["#00D2FF", "Cyan Glow", "Màu điểm nhấn phụ & Công nghệ", "Tiêu đề khu vực, LiveKit SFU Badge, Link"],
        ["#FBBF24", "Retro Gold", "Màu đánh giá sao & Huy hiệu", "Hệ thống Star Rating 1-5★, Danh hiệu VIP"],
        ["#F43F5E", "Cyber Berry Pink", "Màu cảnh báo & Nút thoát", "Nút rời phòng học, Báo vi phạm, Tag giới hạn"],
    ]
    for c_idx, h in enumerate(cl_heads):
        cell = tbl_colors.cell(0, c_idx)
        set_cell_background(cell, "101D24")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, row in enumerate(cl_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_colors.cell(r_idx + 1, c_idx)
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.text = val
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, line_spacing=1.15, align=p.alignment)
            p.runs[0].font.size = Pt(9.5)

    add_styled_heading(doc, "3.2.2. Typography & Component Games", level=3)
    add_bullet_p(doc, "'Press Start 2P' — được áp dụng có chọn lọc cho Logo, Cấp độ Level, Điểm Match Score và Nhãn sự kiện game nhằm giữ trọn vẹn chất Retro hoài niệm.", bold_prefix="Pixel Typography: ")
    add_bullet_p(doc, "'Outfit' và 'Plus Jakarta Sans' — bộ font sans-serif hiện đại, độ tương phản sắc nét, hỗ trợ 100% tiếng Việt có dấu, dùng cho toàn bộ tiêu đề bài đăng và nội dung trao đổi.", bold_prefix="Nội dung chính & UI Typography: ")
    add_bullet_p(doc, "Toàn bộ khung thẻ sử dụng viền phát sáng nhẹ `1px solid rgba(44, 234, 163, 0.16)` kết hợp đổ bóng sâu `0 8px 30px rgba(0, 0, 0, 0.4)`, tạo cảm giác nổi khối sinh động khi hover chuột.", bold_prefix="Hệ thống Game Cards & Micro-interactions: ")

    add_styled_heading(doc, "3.3. Sơ đồ điều hướng (Navigation Flow)", level=2)
    add_body_p(doc,
        "Luồng trải nghiệm người dùng trên ForFriend được thiết kế liền mạch xoay quanh 5 hành trình chính:"
    )
    add_bullet_p(doc, "Trang chủ → Chọn 'Khởi tạo Hero' → Nhập thông tin sinh viên & Trường → Chọn 1 trong 15 Avatar Chibi → Tải thẻ sinh viên/CV → Chuyển hướng ngay tới Bảng tin Quest.", bold_prefix="1. Luồng Khởi tạo tài khoản: ")
    add_bullet_p(doc, "Bảng tin Feed → Nhấn 'Đăng Quest Mới' → Chọn hình thức (Offline/Online) → Nhập môn học & địa điểm → Xem trước hiển thị → Kích hoạt bài đăng và thuật toán ghép bạn.", bold_prefix="2. Luồng Tạo Study Quest: ")
    add_bullet_p(doc, "Bảng tin Feed → Sử dụng bộ lọc Trường/Môn/Khu vực → Xem Quest Card có Match Score cao → Bấm 'Xin tham gia Quest' → Hệ thống gửi thông báo WebSocket tới tác giả.", bold_prefix="3. Luồng Tra cứu & Ghép bạn: ")
    add_bullet_p(doc, "Sảnh Adventure Zones → Chọn phòng học theo chủ đề → Bấm 'Xin vào phòng' → Host chấp nhận → Bật WebRTC Video Call + Bật đồng hồ Pomodoro 25 phút → Kết thúc buổi học → Chấm điểm 1-5 sao.", bold_prefix="4. Luồng Phòng học ảo LiveKit: ")
    add_bullet_p(doc, "Menu Bạn bè → Mở cửa sổ Chat 1-1 → Nhắn tin trao đổi tài liệu real-time → Xem Hero Profile của bạn học (EXP, Badges, Đánh giá) → Bấm gọi video trực tiếp.", bold_prefix="5. Luồng Trò chuyện & Hồ sơ Hero: ")

    add_styled_heading(doc, "3.4. Thiết kế từng màn hình (Screen Design)", level=2)
    add_body_p(doc,
        "Dưới đây là hình ảnh chụp thực tế và phân tích chi tiết từng màn hình chính trong nền tảng ForFriend:"
    )

    # 1. Screen 1
    add_image_with_caption(
        doc,
        os.path.join(ASSETS_DIR, "screen_01_register_avatars.png"),
        "Hình 3.1: Giao diện Khởi tạo tài khoản Hero & Lưới chọn 1 trong 15 Avatar Chibi phong cách Retro Pixel (Giao diện Tiếng Anh)",
        width_inch=6.0
    )
    add_body_p(doc,
        "Màn hình Khởi tạo tài khoản (Hero Registration) được thiết kế hiện đại với ngôn ngữ giao diện Tiếng Anh chuẩn quốc tế: Cột bên trái gồm các trường thông tin học thuật chuẩn xác (Full Student Name, University Email .edu.vn, Student ID, Major, Area, và khu vực tải minh chứng thẻ sinh viên/CV). Cột bên phải là bộ sưu tập 15 Avatar Chibi Pixel độc quyền. Khi người dùng nhấp chọn avatar, khung viền sẽ lập tức phát sáng ánh Mint Neon và hiển thị huy hiệu 'SELECTED', tạo cảm giác nhập vai nhân vật trước khi bắt đầu hành trình học tập."
    )

    # 2. Screen 2
    add_image_with_caption(
        doc,
        os.path.join(ASSETS_DIR, "screen_02_quest_feed.png"),
        "Hình 3.2: Giao diện Bảng tin Home Page / Discover Partners với Logo Green Owl chính thức, Bộ lọc và danh sách Study Quest Cards",
        width_inch=6.2
    )
    add_body_p(doc,
        "Trang chủ / Bảng tin (Discover Partners) thể hiện trọn vẹn phong cách Neo-Cyber Student của ForFriend: Góc trên bên trái là biểu tượng Green Owl chính thức và thương hiệu ForFriend; thanh điều hướng bên trái gồm Dashboard, Discover Partners, Study Groups, Messages, Profile, Settings và thẻ người dùng Online ở góc dưới. Thanh tìm kiếm trung tâm hỗ trợ tra cứu 'Search for partners, subjects, or quests...'. Thanh bộ lọc thông minh phân loại theo Subject, Level, Time Zone và Schedule Weekly cùng nút '+ Post Quest'. Các thẻ Study Quest Card hiển thị đa dạng môn học (Python Project AI Chatbot, History Essay, Math Prep Calculus II) kèm thông tin trường, điểm đánh giá sao, nhãn tag và các nút hành động [View Details], [Request Join]. Cột bên phải tích hợp widget 'Level 14 Study Hero' cùng danh sách Active Quests và Recent Contacts."
    )

    # 3. Screen 3
    add_image_with_caption(
        doc,
        os.path.join(ASSETS_DIR, "screen_03_create_quest_modal.png"),
        "Hình 3.3: Giao diện Modal Đăng Quest Mới (Create Study Quest) & Khung xem trước trực quan Live Preview",
        width_inch=5.8
    )
    add_body_p(doc,
        "Modal Đăng Quest mới (Create Study Quest) hỗ trợ người dùng dễ dàng chuyển đổi giữa hai chế độ học tập Offline (In-Person: Library, Cafe) và Online (Virtual Room: LiveKit Video Call). Form nhập liệu Tiếng Anh cho phép gắn thẻ môn học và kỹ năng để hệ sinh thái thuật toán tự động phân phối bài viết đến đúng các sinh viên có nhu cầu tương tự. Khung bên phải hiển thị bản xem trước trực quan (Feed Display Live Preview) giúp người dùng kiểm tra bài đăng trước khi phát hành lên bảng tin."
    )

    # 4. Screen 4
    add_image_with_caption(
        doc,
        os.path.join(ASSETS_DIR, "screen_04_virtual_rooms_lobby.png"),
        "Hình 3.4: Giao diện Phòng học ảo Adventure Zones tích hợp LiveKit WebRTC Video Call & Đồng hồ Pomodoro 25 phút",
        width_inch=6.0
    )
    add_body_p(doc,
        "Phòng học ảo tích hợp trực tiếp công nghệ WebRTC LiveKit Cloud cho phép truyền phát video HD 720p với độ trễ cực thấp (< 20ms). Màn hình hiển thị lưới camera các thành viên tham gia, khung nhận diện người đang phát biểu (Active Speaker Tag: TALKING), đồng hồ bấm giờ Pomodoro 25 phút giúp duy trì kỷ luật nhóm, thanh công cụ điều khiển (Mic, Video, Screen Share, Raise Hand, Leave Room) và khung chat trao đổi tài liệu trong phòng (In-Room Chat & Study Notes)."
    )

    # 5. Screen 5
    add_image_with_caption(
        doc,
        os.path.join(ASSETS_DIR, "screen_05_hero_profile_chat.png"),
        "Hình 3.5: Giao diện Hồ sơ Hero Profile (Cấp độ EXP, Đánh giá sao, Gamified Badges) & Cửa sổ Chat 1-1 Real-time",
        width_inch=6.0
    )
    add_body_p(doc,
        "Màn hình Hồ sơ cá nhân kết hợp cùng khung trò chuyện riêng: Cột trái thể hiện hồ sơ 'Hero' với avatar chibi kích thước lớn, tích xanh xác thực 'VERIFIED FTU', điểm uy tín 4.95/5.0★ (dựa trên 38 lượt đánh giá khách quan), thanh tiến trình EXP thăng cấp và bộ sưu tập huy hiệu danh dự Gamified Badges (Top Scholar, Punctual Master, Peer Mentor, Night Owl). Cột phải là hộp thoại Chat 1-1 real-time vận hành qua In-Memory WebSocket, hỗ trợ sinh viên trao đổi riêng tư và hẹn lịch học tập trực tiếp."
    )

    doc.add_page_break()

    print("Building Section 4: Technical Plan...")
    # ==========================================================
    # PHẦN 4: TECHNICAL PLAN
    # ==========================================================
    add_styled_heading(doc, "PHẦN 4: TECHNICAL PLAN", level=1)
    
    add_styled_heading(doc, "4.1. Tổng quan kiến trúc kỹ thuật (Pure Python Stack)", level=2)
    add_body_p(doc,
        "Nhằm đáp ứng yêu cầu khắt khe về tính độc lập, dễ bảo trì, dễ triển khai tại máy cá nhân sinh viên hoặc máy chấm đồ án mà không đòi hỏi cài đặt các dịch vụ phụ trợ phức tạp (như Docker Desktop, PostgreSQL Server hay Redis), ForFriend được xây dựng dựa trên triết lý Pure Python Stack (100% Python từ tầng Giao diện đến tầng Nghiệp vụ và Cơ sở dữ liệu nhúng)."
    )

    # Architecture diagram
    add_image_with_caption(
        doc,
        os.path.join(ASSETS_DIR, "architecture_diagram.png"),
        "Hình 4.1: Sơ đồ Kiến trúc phân tầng ForFriend (Reflex Python Frontend, FastAPI Backend, SQLite nhúng & In-Memory Hub)",
        width_inch=6.0
    )

    add_styled_heading(doc, "4.2. Tech Stack chi tiết", level=2)
    add_styled_heading(doc, "4.2.1. Frontend — Reflex (Python-first UI)", level=3)
    add_body_p(doc,
        "Reflex là framework web thế hệ mới của Python, cho phép biên dịch mã nguồn thuần Python thành ứng dụng React Single Page Application (SPA) hiệu năng cao. Toàn bộ logic giao diện, chuyển trang (Routing) và quản lý trạng thái (State Management) đều được viết hoàn toàn bằng Python:"
    )
    add_bullet_p(doc, "Mỗi luồng nghiệp vụ được đóng gói trong một lớp kế thừa từ `rx.State` (AuthState, FeedState, RoomState, ChatState, ProfileState), hỗ trợ Type Hints chặt chẽ và cơ chế đồng bộ biến tự động qua WebSocket.", bold_prefix="Quản lý State tập trung (State Pattern): ")
    add_bullet_p(doc, "Không phụ thuộc vào các thư viện tiện ích cồng kềnh như Tailwind CSS, toàn bộ hệ thống sử dụng Vanilla CSS Tokens kết hợp CSS Variables trong `theme.py` và `global.css`, đảm bảo tốc độ render siêu tốc và chuẩn phong cách game retro.", bold_prefix="Hệ thống Design Tokens thuần CSS: ")
    add_bullet_p(doc, "Thư viện LiveKit React SDK được bao bọc thành một Reflex Custom Component (`livekit_component.py`) với chưa đầy 5% mã JavaScript, cho phép kết nối luồng WebRTC trực tiếp trong giao diện Python.", bold_prefix="LiveKit WebRTC Component Wrapper: ")

    add_styled_heading(doc, "4.2.2. Backend & Database (FastAPI, SQLite & In-Memory Hub)", level=3)
    add_bullet_p(doc, "Sử dụng FastAPI (Python 3.11+) với kiến trúc Asynchronous I/O toàn diện (`async` / `await`), cung cấp tài liệu tự động Swagger UI chuẩn OpenAPI tại đường dẫn `/docs`.", bold_prefix="FastAPI Service Layer: ")
    add_bullet_p(doc, "Toàn bộ dữ liệu được lưu trữ trong tệp cơ sở dữ liệu nhúng `forfriend.db` thông qua trình điều khiển bất đồng bộ `aiosqlite` và ORM `SQLAlchemy 2.0`. Không cần cài đặt bất kỳ server database độc lập nào.", bold_prefix="Cơ sở dữ liệu SQLite 3 Async: ")
    add_bullet_p(doc, "Thay thế hoàn toàn Redis bằng lớp `ConnectionManager` viết bằng Python thuần, sử dụng `dict` lưu trữ các phiên WebSocket hoạt động và `dict` có thời gian hết hạn (TTL) để cache bảng tin feed và kết quả tính toán matching.", bold_prefix="In-Memory Hub (Bộ nhớ RAM nội tại): ")

    # Database ERD diagram
    add_image_with_caption(
        doc,
        os.path.join(ASSETS_DIR, "database_erd.png"),
        "Hình 4.2: Sơ đồ Thực thể Liên kết (Entity Relationship Diagram) 10 bảng dữ liệu quan hệ của ForFriend",
        width_inch=6.0
    )

    add_body_p(doc,
        "Cơ sở dữ liệu bao gồm 10 bảng quan hệ được thiết kế chuẩn hóa mức 3NF, bảo đảm tính toàn vẹn dữ liệu và hỗ trợ truy vấn bất đồng bộ tốc độ cao: `user` (Hồ sơ sinh viên, mật khẩu bcrypt, điểm rating), `user_subject` (Danh sách môn học đang theo), `post` (Study Quest tìm bạn), `post_tag` (Thẻ môn học), `room` (Phòng học ảo), `room_category` (Khu vực Adventure Zones), `room_participant` (Danh sách thành viên phòng), `rating` (Chấm điểm 1-5 sao), `friendship` (Quan hệ kết bạn) và `message` (Tin nhắn chat riêng 1-1)."
    )

    add_styled_heading(doc, "4.3. Tính năng đã hoàn thiện vs. Kế hoạch Roadmap", level=2)
    
    # Bảng tính năng
    tbl_feat = doc.add_table(rows=6, cols=3)
    tbl_feat.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_feat, color="CBD5E1", sz="4")
    
    f_heads = ["Hạng mục nghiệp vụ", "Trạng thái hoàn thiện", "Mô tả triển khai chi tiết"]
    f_rows = [
        ["Xác thực & Người dùng (Auth & Hero Profile)", "Đã hoàn thành 100% (MVP)", "Đăng ký, Đăng nhập JWT, Bcrypt hash, Chọn 15 avatar chibi, Upload thẻ SV & CV, Đổi avatar trong profile."],
        ["Bảng tin Quest & Bộ lọc (Feed & Filter)", "Đã hoàn thành 100% (MVP)", "Tạo Quest Offline/Online, Bộ lọc môn/trường/vị trí, Tìm kiếm từ khóa, Xem chi tiết Quest, Hủy bài đăng."],
        ["Thuật toán Ghép bạn (Matching Engine)", "Đã hoàn thành 100% (MVP)", "Tính toán Relevance Score dựa trên 5 chiều trọng số, In-memory feed cache tự động làm mới khi có tin mới."],
        ["Phòng học ảo & Video Call (Rooms & LiveKit)", "Đã hoàn thành 100% (MVP)", "Tạo phòng theo chủ đề, Sảnh Adventure Zones, In-Memory WebSocket xin vào/duyệt, LiveKit WebRTC Video/Audio/Screen."],
        ["Đánh giá & Bạn bè Chat (Rating & Social)", "Đã hoàn thành 100% (MVP)", "Chấm điểm 1-5 sao sau phòng học, Cập nhật rating trung bình, Kết bạn, Chat 1-1 real-time qua ConnectionManager."],
    ]
    for c_idx, h in enumerate(f_heads):
        cell = tbl_feat.cell(0, c_idx)
        set_cell_background(cell, "101D24")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, row in enumerate(f_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_feat.cell(r_idx + 1, c_idx)
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.text = val
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, line_spacing=1.15, align=p.alignment)
            p.runs[0].font.size = Pt(9.5)

    add_styled_heading(doc, "4.4. Thuật toán tính toán (Matching & Gamification Engine)", level=2)
    add_body_p(doc,
        "Để đảm bảo chất lượng ghép nối tối ưu giữa nhu cầu của người học và bài đăng Quest, ForFriend triển khai thuật toán tính điểm tương đồng (Relevance Score) đa yếu tố:"
    )

    # Matching diagram
    add_image_with_caption(
        doc,
        os.path.join(ASSETS_DIR, "matching_algorithm_diagram.png"),
        "Hình 4.3: Công thức và cấu trúc 5 thành phần trọng số của Thuật toán Matching Engine",
        width_inch=5.8
    )

    add_body_p(doc,
        "Công thức tổng quát tính điểm tương đồng giữa sinh viên U và bài đăng Quest P được định nghĩa như sau:"
    )
    
    p_form = doc.add_paragraph()
    format_paragraph(p_form, space_before=4, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_f = p_form.add_run("Score(U, P) = W1·Same_School + W2·Same_Area + W3·Jaccard(Subjects) + W4·e^(-λ·Δt) + W5·Rating_Norm")
    r_f.font.name = "Courier New"
    r_f.font.size = Pt(11)
    r_f.font.bold = True
    r_f.font.color.rgb = RGBColor(0x0E, 0x5A, 0x64)

    add_bullet_p(doc, "W1 = 3.0. Nếu sinh viên và tác giả cùng học tại một trường (ví dụ FTU = FTU), điểm cộng là 3.0; nếu khác trường điểm cộng là 0.", bold_prefix="1. Trọng số cùng Trường (Same School): ")
    add_bullet_p(doc, "W2 = 2.0. Phân bổ 70% (1.4 điểm) nếu cùng Thành phố và 30% (0.6 điểm) nếu cùng Quận/Huyện (ví dụ cùng ở Đống Đa, Chùa Láng).", bold_prefix="2. Trọng số Khu vực Địa lý (Same Area): ")
    add_bullet_p(doc, "W3 = 2.5. Đo lường tỷ lệ trùng khớp giữa danh sách môn học của sinh viên và các Tags của Quest bằng chỉ số tương đồng Jaccard: J(A, B) = |A ∩ B| / |A ∪ B|.", bold_prefix="3. Trọng số Môn học (Subject Overlap): ")
    add_bullet_p(doc, "W4 = 1.0. Áp dụng hàm suy giảm số mũ theo thời gian exp(-0.029 × Δt) với chu kỳ bán rã t_half = 24 giờ. Đảm bảo các bài đăng mới luôn được ưu tiên hơn các bài đã đăng nhiều ngày.", bold_prefix="4. Trọng số Độ mới (Recency Decay): ")
    add_bullet_p(doc, "W5 = 1.5. Chuẩn hóa điểm sao đánh giá của tác giả về thang đo 0–1 (Rating / 5.0), khuyến khích sinh viên kết nối với các bạn học có uy tín cao.", bold_prefix="5. Trọng số Tín nhiệm Tác giả (Author Rating): ")

    add_styled_heading(doc, "4.5. Tự động hóa & Hạ tầng Real-time Hub", level=2)
    add_body_p(doc,
        "Lớp In-Memory Hub đảm nhiệm vai trò điều phối thông điệp thời gian thực (Pub/Sub) và quản lý kết nối socket mà không cần phụ thuộc vào broker ngoài như Redis:"
    )
    add_bullet_p(doc, "Mỗi kết nối WebSocket của sinh viên được định danh theo `user_id` và quản lý trong `dict[str, WebSocket]`. Hỗ trợ các phương thức `send_personal_message()`, `broadcast_room()` và `push_notification()` với độ trễ cực thấp (< 30ms).", bold_prefix="In-Memory ConnectionManager: ")
    add_bullet_p(doc, "Một tác vụ nền (Background Task) chạy định kỳ mỗi 5 phút quét các phòng học không còn người tham gia hoặc đã kết thúc để tự động chuyển trạng thái `status = 'closed'`, giải phóng tài nguyên hệ thống.", bold_prefix="Cơ chế tự động dọn dẹp phòng trống (Auto-cleanup Worker): ")

    add_styled_heading(doc, "4.6. Dự toán chi phí vận hành", level=2)
    add_body_p(doc,
        "Nhờ việc loại bỏ hoàn toàn các dịch vụ phụ trợ nặng nề và tận dụng tối đa kiến trúc nhúng thuần Python, chi phí vận hành hàng tháng của ForFriend được tối ưu hóa ở mức kỷ lục, cực kỳ phù hợp cho đồ án sinh viên và giai đoạn khởi nghiệp ban đầu:"
    )

    # Bảng chi phí
    tbl_cost = doc.add_table(rows=6, cols=4)
    tbl_cost.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cost, color="CBD5E1", sz="4")
    
    cs_heads = ["Hạng mục hạ tầng", "Nhà cung cấp dự kiến", "Gói dịch vụ / Thông số", "Chi phí ước tính / Tháng"]
    cs_rows = [
        ["Máy chủ ứng dụng (Web & API)", "Cloud VPS / Hetzner / Vietnix", "1 vCPU, 2GB RAM, 20GB SSD", "90.000 – 150.000 VNĐ (~4 - 6 USD)"],
        ["Cơ sở dữ liệu & Bộ nhớ Cache", "SQLite 3 & In-Memory RAM", "Nhúng trực tiếp trong VPS", "0 VNĐ (Không tốn thêm chi phí)"],
        ["Hạ tầng Video SFU WebRTC", "LiveKit Cloud", "Free Tier (100GB Băng thông / tháng)", "0 VNĐ (Đủ cho 5.000 giờ phòng học)"],
        ["Lưu trữ Thẻ SV & Avatar", "Local Disk VPS / Cloudflare R2", "Dung lượng ~10GB", "0 – 25.000 VNĐ (~0 - 1 USD)"],
        ["Tên miền chính thức", "Nhà đăng ký tên miền (.vn / .com)", "Bản quyền 1 năm", "25.000 VNĐ / tháng (Quy đổi)"],
    ]
    for c_idx, h in enumerate(cs_heads):
        cell = tbl_cost.cell(0, c_idx)
        set_cell_background(cell, "101D24")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, row in enumerate(cs_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_cost.cell(r_idx + 1, c_idx)
            set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.text = val
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 3 else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, line_spacing=1.15, align=p.alignment)
            p.runs[0].font.size = Pt(9.5)

    add_styled_heading(doc, "4.7. Bảo mật & Privacy", level=2)
    add_bullet_p(doc, "Toàn bộ mật khẩu tài khoản được băm một chiều (Hashing) bằng thuật toán Bcrypt với Salt ngẫu nhiên qua `passlib.context.CryptContext`, tuyệt đối không lưu trữ plaintext.", bold_prefix="Mã hóa mật khẩu: ")
    add_bullet_p(doc, "Sử dụng JSON Web Token với thuật toán mã hóa HS256, thời hạn truy cập (Access Token Expiry) 24 giờ và Refresh Token để làm mới phiên đăng nhập an toàn.", bold_prefix="Xác thực phân quyền JWT Bearer: ")
    add_bullet_p(doc, "Toàn bộ dữ liệu nhập liệu từ người dùng (nội dung bài viết Quest, tin nhắn chat) đều được lọc và khử độc (Sanitization) qua `bleach` và Schema Pydantic v2, ngăn chặn triệt để tấn công XSS (Cross-Site Scripting) và SQL Injection.", bold_prefix="Làm sạch dữ liệu & Phòng chống XSS: ")
    add_bullet_p(doc, "Các luồng media WebRTC giữa trình duyệt và SFU LiveKit được mã hóa đầu-cuối qua giao thức SRTP (Secure Real-time Transport Protocol) kết hợp chứng chỉ TLS 1.3.", bold_prefix="Bảo mật đường truyền Video Call: ")
    add_bullet_p(doc, "Chỉ hiển thị công khai thông tin liên hệ khi người dùng chủ động cho phép; hệ thống avatar chibi giúp bảo vệ danh tính cá nhân sinh viên khỏi nguy cơ bị làm phiền.", bold_prefix="Bảo vệ quyền riêng tư sinh viên: ")

    doc.add_page_break()

    print("Building Section 5: Conclusion...")
    # ==========================================================
    # PHẦN 5: KẾT LUẬN TỔNG KẾT DỰ ÁN
    # ==========================================================
    add_styled_heading(doc, "PHẦN 5: KẾT LUẬN TỔNG KẾT DỰ ÁN", level=1)
    
    add_styled_heading(doc, "5.1. Tổng kết những thành quả đạt được", level=2)
    add_body_p(doc,
        "Sau quá trình nghiên cứu, khảo sát thực tế và triển khai kỹ thuật nghiêm túc, Nhóm 10 đã hoàn thiện trọn vẹn nền tảng ForFriend đáp ứng đầy đủ ba trụ cột chính của một dự án công nghệ hoàn chỉnh:"
    )
    add_bullet_p(doc, "Xác lập rõ ràng bài toán nhức nhối của sinh viên khi học tập độc lập; thiết kế mô hình kinh doanh Lean Canvas có tiềm năng thương mại hóa thực tế; định lượng thị trường TAM/SAM/SOM rõ ràng và xây dựng lộ trình phát triển 4 giai đoạn mạch lạc.", bold_prefix="Trụ cột Kế hoạch Kinh doanh (Business Plan): ")
    add_bullet_p(doc, "Đột phá với phong cách Web Game Retro Neo-Cyber Student, kết hợp bộ sưu tập 15 Avatar Chibi Pixel độc quyền và hệ thống ngôn ngữ game hóa (Quest, Hero, EXP, Adventure Zones), tạo nên giao diện cuốn hút, giảm tải áp lực học tập cho sinh viên.", bold_prefix="Trụ cột Thiết kế Trải nghiệm (UX/UI Design): ")
    add_bullet_p(doc, "Hiện thực hóa 100% tính năng bằng Pure Python Stack (Reflex + FastAPI + SQLite Async + In-Memory Hub), chứng minh tính khả thi vượt trội của kiến trúc không phụ thuộc Docker/Redis, chi phí hạ tầng tiệm cận 0 VNĐ nhưng vẫn đảm bảo độ tin cậy và khả năng gọi video call WebRTC trực tiếp.", bold_prefix="Trụ cột Kỹ thuật Công nghệ (Technical Implementation): ")

    add_styled_heading(doc, "5.2. Đánh giá và định hướng phát triển trong tương lai", level=2)
    add_body_p(doc,
        "Dự án ForFriend không chỉ là một sản phẩm học phần mẫu mực của môn Lập trình ứng dụng Web (TIN314) tại Trường Đại học Ngoại Thương mà còn là một giải pháp EdTech có tính ứng dụng xã hội sâu sắc. Hướng đi tiếp theo của nhóm tác giả bao gồm:"
    )
    add_bullet_p(doc, "Phối hợp cùng Hội Sinh viên và các Câu lạc bộ học thuật tại FTU Cơ sở Hà Nội để đưa sản phẩm vào sử dụng thực tế trong kỳ thi sắp tới, thu thập dữ liệu phản hồi từ hơn 1.000 sinh viên.", bold_prefix="1. Triển khai thí điểm thực tế: ")
    add_bullet_p(doc, "Sử dụng dữ liệu hành vi tìm bạn và tham gia phòng học thực tế để tinh chỉnh các hệ số trọng số W1 – W5 trong Matching Engine, tiến tới tích hợp thuật toán gợi ý bằng học máy (Machine Learning Recommendation).", bold_prefix="2. Nâng cấp thuật toán thông minh: ")
    add_bullet_p(doc, "Tiếp tục hoàn thiện các phân hệ trả phí dành cho cá nhân (Quest Master) và các tổ chức câu lạc bộ (Guild Space) nhằm hiện thực hóa các mốc doanh thu đã đề ra.", bold_prefix="3. Thương mại hóa bền vững: ")

    p_final = doc.add_paragraph()
    format_paragraph(p_final, space_before=20, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_fin = p_final.add_run("--- HẾT BÁO CÁO DỰ ÁN FORFRIEND ---")
    r_fin.font.name = "Times New Roman"
    r_fin.font.size = Pt(11)
    r_fin.font.bold = True
    r_fin.font.color.rgb = RGBColor(0x8A, 0x15, 0x38)

    try:
        doc.save(OUTPUT_DOCX)
        print(f"Report document successfully created at: {OUTPUT_DOCX}")
        print(f"File size: {os.path.getsize(OUTPUT_DOCX)} bytes")
    except PermissionError:
        fallback_path = os.path.abspath("Bao_Cao_Du_An_ForFriend_Updated.docx")
        doc.save(fallback_path)
        print(f"Original file is opened in Word. Saved updated report at: {fallback_path}")
        print(f"File size: {os.path.getsize(fallback_path)} bytes")

if __name__ == "__main__":
    create_report_document()
