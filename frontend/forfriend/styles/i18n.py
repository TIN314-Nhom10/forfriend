"""Hệ thống từ điển đa ngôn ngữ (i18n) hỗ trợ tiếng Việt (VIE) và tiếng Anh (ENG) cho ForFriend."""

TRANSLATIONS = {
    # Navigation & Sidebar
    "nav_dashboard": {"vie": "Bảng Điều Khiển", "eng": "Dashboard"},
    "nav_feed": {"vie": "Bảng Tin Quest", "eng": "Study Quests"},
    "nav_rooms": {"vie": "Phòng Học Ảo", "eng": "Study Rooms"},
    "nav_friends": {"vie": "Bạn Bè & Chat", "eng": "Friends & Chat"},
    "nav_profile": {"vie": "Hồ Sơ Cá Nhân", "eng": "Profile"},
    "nav_logout": {"vie": "Đăng Xuất", "eng": "Logout"},
    "nav_login": {"vie": "Đăng Nhập", "eng": "Login"},
    "nav_register": {"vie": "Đăng Ký", "eng": "Register"},

    # Brand & Tagline
    "brand_name": {"vie": "ForFriend", "eng": "ForFriend"},
    "tagline": {"vie": "Nền tảng kết nối tìm bạn học nhóm sinh viên", "eng": "Student Study Partner & Virtual Study Hub"},

    # Quest Feed & Dashboard
    "quest_feed_title": {"vie": "Bảng Tin Quest Tìm Bạn Học", "eng": "Study Quest Board"},
    "quest_feed_subtitle": {"vie": "Khám phá các nhiệm vụ học tập từ sinh viên toàn quốc", "eng": "Discover study missions from fellow students nationwide"},
    "btn_create_quest": {"vie": "+ Tạo Quest Mới", "eng": "+ Post New Quest"},
    "filter_all": {"vie": "Tất Cả", "eng": "All Quests"},
    "filter_online": {"vie": "🌐 Trực Tuyến", "eng": "🌐 Online"},
    "filter_offline": {"vie": "📍 Gặp Mặt", "eng": "📍 Offline"},
    "search_placeholder": {"vie": "Tìm theo môn học, trường, từ khóa...", "eng": "Search by subject, university, keyword..."},
    "match_score": {"vie": "Độ Tương Đồng", "eng": "Match Score"},
    "btn_join_quest": {"vie": "Nhận Quest / Chat", "eng": "Accept Quest / Chat"},
    "btn_details": {"vie": "Chi Tiết", "eng": "View Details"},
    "empty_feed": {"vie": "Chưa có Quest nào phù hợp. Hãy là người đầu tiên đăng!", "eng": "No quests found. Be the first to create one!"},

    # Create Quest Modal
    "modal_create_title": {"vie": "+ TẠO QUEST MỚI", "eng": "+ CREATE NEW QUEST"},
    "input_quest_title": {"vie": "Tiêu Đề Quest:", "eng": "Quest Title:"},
    "input_quest_title_ph": {"vie": "Ví dụ: Tìm bạn cùng học Lập Trình Python & Web FastAPI...", "eng": "e.g., Finding partner for Python & FastAPI project..."},
    "input_quest_content": {"vie": "Nội Dung Chi Tiết:", "eng": "Detailed Content:"},
    "input_quest_content_ph": {"vie": "Mục tiêu học tập, thời gian rảnh, kiến thức cần ôn tập...", "eng": "Study goals, free time schedule, subjects to review..."},
    "input_quest_tags": {"vie": "Thẻ Môn Học (cách nhau bởi dấu phẩy):", "eng": "Subject Tags (comma separated):"},
    "input_quest_tags_ph": {"vie": "Python, Toán Giải Tích, AI", "eng": "Python, Calculus, Machine Learning"},
    "input_format": {"vie": "Hình Thức:", "eng": "Study Format:"},
    "format_online": {"vie": "🌐 Online", "eng": "🌐 Online"},
    "format_offline": {"vie": "📍 Offline", "eng": "📍 Offline"},
    "input_location": {"vie": "Địa Điểm Gặp Mặt:", "eng": "Meeting Location:"},
    "input_location_ph": {"vie": "Ví dụ: Thư viện Tạ Quang Bửu, Quán cà phê...", "eng": "e.g., University Library, Coffee Shop..."},
    "btn_cancel": {"vie": "Hủy", "eng": "Cancel"},
    "btn_post_now": {"vie": "🚀 Đăng Quest Ngay", "eng": "🚀 Post Quest Now"},
    "login_required_msg": {"vie": "⚠️ Bạn đang ở chế độ khách. Đăng nhập để đăng Quest:", "eng": "⚠️ You are in guest mode. Log in to post Quests:"},
    "btn_quick_demo_login": {"vie": "⚡ Đăng Nhập Demo 1-Click", "eng": "⚡ 1-Click Demo Login"},

    # User Sidebar Card
    "hero_card_welcome": {"vie": "Xin chào,", "eng": "Welcome,"},
    "hero_level": {"vie": "Cấp Độ", "eng": "Level"},
    "hero_scholar": {"vie": "Sinh Viên", "eng": "Student"},
    "hero_rating": {"vie": "Sao Uy Tín", "eng": "Rating"},
    "hero_verified": {"vie": "Đã Xác Thực SV", "eng": "Verified Student"},
    "guest_user": {"vie": "Khách", "eng": "Guest"},
    "guest_notice": {"vie": "Hãy đăng nhập để mở khóa đầy đủ tính năng!", "eng": "Log in to unlock all quests & features!"},

    # Study Rooms (Adventure Zones)
    "rooms_title": {"vie": "Sảnh Phòng Học Ảo", "eng": "Virtual Study Hub"},
    "rooms_subtitle": {"vie": "Vào phòng cùng học trực tiếp qua Video Call WebRTC", "eng": "Join collaborative rooms with real-time WebRTC Video Call"},
    "btn_create_room": {"vie": "+ Mở Phòng Học", "eng": "+ Create Study Room"},
    "room_participants": {"vie": "Thành viên", "eng": "Participants"},
    "btn_knock_room": {"vie": "🔔 Gõ Cửa Xin Vào", "eng": "🔔 Knock to Join"},
    "btn_enter_room": {"vie": "🚀 Vào Phòng Ngay", "eng": "🚀 Enter Room"},

    # Friends & Chat
    "friends_title": {"vie": "Đồng Đội & Hộp Thư", "eng": "Study Allies & Messages"},
    "chat_placeholder": {"vie": "Nhập tin nhắn... (Enter để gửi)", "eng": "Type a message... (Press Enter to send)"},
    "btn_send": {"vie": "Gửi", "eng": "Send"},

    # Language Switcher
    "lang_current": {"vie": "Tiếng Việt", "eng": "English"},
    "lang_toggle_btn": {"vie": "🇬🇧 ENG", "eng": "🇻🇳 VIE"},
}


def t(key: str, lang: str = "vie") -> str:
    """Lấy nội dung bản dịch theo key và mã ngôn ngữ (vie / eng)."""
    lang_code = "eng" if lang.lower() == "eng" else "vie"
    item = TRANSLATIONS.get(key)
    if not item:
        return key
    return item.get(lang_code, item.get("vie", key))
