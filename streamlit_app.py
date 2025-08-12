import streamlit as st
import os
import base64
from pages.intro_page import intro_page
from pages.adventure_map_page import adventure_map_page
from pages.village_page import village_page
from pages.story_forest_page import story_forest_page
from pages.feedback_age import feedback_age_page
from pages.prepare_page import prepare_page
from pages.hwanho_page import hwanho_page
from pages.memory_page import memory_page
from pages.summary_page import summary_page

# 페이지 설정
st.set_page_config(
    page_title="연극 대모험",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit 기본 메뉴와 페이지 네비게이션 숨기기
st.markdown("""
<style>
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    .stApp > footer {display: none;}
    
    /* 상단 네비게이션 메뉴 숨기기 */
    .stApp > header {display: none;}
    .stApp > div[data-testid="stToolbar"] {display: none;}
    .stApp > div[data-testid="stDecoration"] {display: none;}
    
    /* 페이지 네비게이션 숨기기 */
    .stApp > div[data-testid="stSidebar"] > div[data-testid="stSidebarNav"] {display: none;}
    .stApp > div[data-testid="stSidebar"] > div[data-testid="stSidebarContent"] > div:first-child {display: none;}
    
    /* 추가적인 네비게이션 요소 숨기기 */
    [data-testid="stSidebarNav"] {display: none !important;}
    .stApp > div[data-testid="stSidebar"] > div:first-child {display: none !important;}
    .stApp > div[data-testid="stSidebar"] > div[data-testid="stSidebarContent"] > div:first-child {display: none !important;}
    
    /* 상단 메뉴바 완전 숨기기 */
    .stApp > div[data-testid="stToolbar"] {display: none !important;}
    .stApp > div[data-testid="stDecoration"] {display: none !important;}
    .stApp > header {display: none !important;}
    
    /* 사이드바 상단 네비게이션 완전 숨기기 */
    .stApp > div[data-testid="stSidebar"] > div[data-testid="stSidebarContent"] > div:first-child {display: none !important;}
    .stApp > div[data-testid="stSidebar"] > div[data-testid="stSidebarContent"] > div:nth-child(1) {display: none !important;}
    
    /* 사이드바 너비 조정 */
    .stApp > div[data-testid="stSidebar"] {min-width: 300px !important;}
</style>

<script>
// 페이지 로드 후 네비게이션 요소들을 강제로 숨기기
window.addEventListener('load', function() {
    setTimeout(function() {
        // 사이드바 네비게이션 숨기기
        const sidebarNav = document.querySelector('[data-testid="stSidebarNav"]');
        if (sidebarNav) sidebarNav.style.display = 'none';
        
        // 사이드바 첫 번째 요소만 숨기기 (뱃지 보드는 유지)
        const sidebarContent = document.querySelector('[data-testid="stSidebarContent"]');
        if (sidebarContent) {
            const firstChild = sidebarContent.firstElementChild;
            if (firstChild && firstChild.getAttribute('data-testid') === 'stSidebarNav') {
                firstChild.style.display = 'none';
            }
        }
        
        // 상단 툴바 숨기기
        const toolbar = document.querySelector('[data-testid="stToolbar"]');
        if (toolbar) toolbar.style.display = 'none';
        
        // 상단 장식 요소 숨기기
        const decoration = document.querySelector('[data-testid="stDecoration"]');
        if (decoration) decoration.style.display = 'none';
    }, 1000);
    
    // 지도 팝업 닫기 함수
    function closeMapPopup() {
        const popup = document.getElementById('map-popup-overlay');
        if (popup) {
            popup.style.display = 'none';
        }
    }
    
    // ESC 키로 팝업 닫기
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeMapPopup();
        }
    });
    
    // 팝업 외부 클릭으로 닫기
    document.addEventListener('click', function(event) {
        const popup = document.getElementById('map-popup-overlay');
        if (popup && event.target === popup) {
            closeMapPopup();
        }
    });
});
</script>
""", unsafe_allow_html=True)

# CSS 스타일링
st.markdown("""
<style>
    .bg-image {
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        opacity: 0.3;
        pointer-events: none;
    }
    
    /* 인트로와 초대장 페이지용 밝은 배경 이미지 */
    .bg-image-bright {
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        opacity: 0.8;
        pointer-events: none;
        filter: brightness(1.1) contrast(1.1);
    }
    
    .main-header {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        margin-bottom: 2rem;
        position: relative;
        z-index: 10;
    }
    
    .adventure-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        position: relative;
        z-index: 10;
    }
    
    .adventure-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* 메인 콘텐츠 컨테이너 */
    .main-content {
        position: relative;
        z-index: 10;
    }
    
    /* 이미지 컨테이너 */
    .image-container {
        position: relative;
        z-index: 5;
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .image-container img {
        width: 100%;
        height: auto;
        display: block;
        object-fit: contain;
        max-width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Streamlit 기본 이미지 스타일 오버라이드 */
    .stImage > img {
        width: 100% !important;
        height: auto !important;
        max-width: 100% !important;
        object-fit: contain !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    
    /* 이미지가 잘리지 않도록 보장 */
    .stImage {
        width: 100% !important;
        max-width: 100% !important;
        overflow: visible !important;
    }
    

    
    /* Streamlit 기본 컨테이너 오버플로우 방지 */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* 밝은 배경 이미지 위의 텍스트 가독성 향상 */
    .bg-image-bright + .main-content,
    .bg-image-bright ~ .main-content {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* 버튼과 텍스트가 밝은 배경에서 잘 보이도록 */
    .bg-image-bright ~ .stButton > button,
    .bg-image-bright ~ .stMarkdown {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #333 !important;
        border: 2px solid rgba(0,0,0,0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* BGM 오디오 컨트롤을 작게 만들기 위한 스타일 */
    .stAudio {
        width: 100px !important;
        height: 40px !important;
    }
    
    .stAudio > div {
        width: 100px !important;
        height: 40px !important;
    }
    
    .stAudio audio {
        width: 100px !important;
        height: 40px !important;
    }
    
    /* 오른쪽 뱃지 보드 사이드바 스타일 */
    .badge-sidebar {
        position: fixed !important;
        top: 0 !important;
        right: -400px !important;
        width: 400px !important;
        height: 100vh !important;
        background: rgba(0, 0, 0, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        transition: right 0.3s ease !important;
        z-index: 9999 !important;
        border-left: 2px solid #FFD700 !important;
        overflow-y: auto !important;
        font-family: Arial, sans-serif !important;
    }
    
    .badge-sidebar.open {
        right: 0 !important;
    }
    
    .badge-sidebar-header {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000;
        padding: 15px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        border-bottom: 2px solid #FFD700;
    }
    
    .badge-sidebar-content {
        padding: 20px;
        text-align: center;
    }
    
    .badge-image {
        max-width: 100%;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .badge-toggle-btn {
        position: fixed !important;
        top: 50% !important;
        right: 10px !important;
        transform: translateY(-50%) !important;
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        font-size: 1.5rem !important;
        cursor: pointer !important;
        z-index: 10000 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .badge-toggle-btn:hover {
        transform: translateY(-50%) scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    .page-wrapper {
        position: relative;
        min-height: 100vh;
    }
    
    .bg-image {
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    
    .invitation-image {
        max-width: 100%;
        height: auto;
        object-fit: contain;
    }
    
    /* 지도 팝업 스타일 */
    .map-popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(5px);
    }
    
    .map-popup-content {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        max-width: 70vw;
        max-height: 80vh;
        width: 800px;
        height: 600px;
        overflow: hidden;
        position: relative;
        animation: popupFadeIn 0.3s ease-out;
    }
    
    @keyframes popupFadeIn {
        from {
            opacity: 0;
            transform: scale(0.8) translateY(-20px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    .map-popup-header {
        background: linear-gradient(45deg, #4ECDC4, #44A08D);
        color: white;
        padding: 15px 20px;
        text-align: center;
        border-bottom: 2px solid #44A08D;
        position: relative;
    }
    
    .map-popup-header h3 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .map-popup-body {
        padding: 10px;
        text-align: center;
        max-height: calc(100% - 80px);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .map-popup-image {
        max-width: 100%;
        max-height: 100%;
        width: auto;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        object-fit: contain;
    }
    
    /* 사용 방법 팝업 스타일 */
    .help-popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(5px);
    }
    
    .help-popup-content {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        max-width: 70vw;
        max-height: 80vh;
        width: 800px;
        height: 600px;
        overflow: hidden;
        position: relative;
        animation: popupFadeIn 0.3s ease-out;
    }
    
    .help-popup-header {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 15px 20px;
        text-align: center;
        border-bottom: 2px solid #FF8E53;
        position: relative;
    }
    
    .help-popup-header h3 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .help-popup-body {
        padding: 10px;
        text-align: center;
        max-height: calc(100% - 80px);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .help-popup-image {
        max-width: 100%;
        max-height: 100%;
        width: auto;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        object-fit: contain;
    }
    
    /* 자주하는 질문 팝업 스타일 */
    .faq-popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(5px);
    }
    
    .faq-popup-content {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        max-width: 70vw;
        max-height: 80vh;
        width: 800px;
        height: 600px;
        overflow: hidden;
        position: relative;
        animation: popupFadeIn 0.3s ease-out;
    }
    
    .faq-popup-header {
        background: linear-gradient(45deg, #A8E6CF, #7FCDCD);
        color: white;
        padding: 15px 20px;
        text-align: center;
        border-bottom: 2px solid #7FCDCD;
        position: relative;
    }
    
    .faq-popup-header h3 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .faq-popup-body {
        padding: 10px;
        text-align: center;
        max-height: calc(100% - 80px);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 극본의 특성 팝업 스타일 */
    .script-popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(5px);
    }
    
    .script-popup-content {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        max-width: 70vw;
        max-height: 80vh;
        width: 800px;
        height: 600px;
        overflow: hidden;
        position: relative;
        animation: popupFadeIn 0.3s ease-out;
    }
    
    .script-popup-header {
        background: linear-gradient(45deg, #9B59B6, #8E44AD);
        color: white;
        padding: 15px 20px;
        text-align: center;
        border-bottom: 2px solid #8E44AD;
        position: relative;
    }
    
    .script-popup-header h3 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .script-popup-body {
        padding: 10px;
        text-align: center;
        max-height: calc(100% - 80px);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .script-popup-image {
        max-width: 100%;
        max-height: 100%;
        width: auto;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        object-fit: contain;
    }
    
    /* 연극의 특성 팝업 스타일 */
    .theater-popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(5px);
    }
    
    .theater-popup-content {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        max-width: 70vw;
        max-height: 80vh;
        width: 800px;
        height: 600px;
        overflow: hidden;
        position: relative;
        animation: popupFadeIn 0.3s ease-out;
    }
    
    .theater-popup-header {
        background: linear-gradient(45deg, #E74C3C, #C0392B);
        color: white;
        padding: 15px 20px;
        text-align: center;
        border-bottom: 2px solid #C0392B;
        position: relative;
    }
    
    .theater-popup-header h3 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .theater-popup-body {
        padding: 10px;
        text-align: center;
        max-height: calc(100% - 80px);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .theater-popup-image {
        max-width: 100%;
        max-height: 100%;
        width: auto;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        object-fit: contain;
    }
</style>
""", unsafe_allow_html=True)

# 헬퍼 함수들
def get_file_path(filename):
    """파일 경로를 반환하는 함수"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

def get_base64_image(file_path):
    """이미지 파일을 base64로 인코딩하는 함수"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        else:
            st.error(f"이미지 파일을 찾을 수 없습니다: {file_path}")
            return None
    except Exception as e:
        st.error(f"이미지 로딩 오류: {str(e)}")
        return None

def render_badge_board():
    """Function to render the badge board on the right side"""
    # Current number of cleared villages (get from session state or default to 0)
    cleared_villages = st.session_state.get('cleared_villages', [])
    
    # Current page to determine which badge to show
    current_page = st.session_state.get('current_page', 'intro')
    
    # Determine badge image path based on current page and cleared villages
    if current_page == "village" and 1 in cleared_villages:
        # 시작의 마을에서 뱃지 획득
        badge_image_path = "assets/뱃지 보드/1_시작의 마을 뱃지 획득.png"
    elif current_page == "feedback_age" and 1 in cleared_villages:
        # 이야기 숲에서 시작의 마을 뱃지 표시
        badge_image_path = "assets/뱃지 보드/1_시작의 마을 뱃지 획득.png"
    elif current_page == "prepare_page" and 2 in cleared_villages:
        # 준비의 광장에서 이야기 숲 뱃지 표시
        badge_image_path = "assets/뱃지 보드/2_이야기 숲 뱃지 획득.png"
    elif current_page == "hwanho_page" and 3 in cleared_villages:
        # 환호의 극장에서 준비의 광장 뱃지 표시
        badge_image_path = "assets/뱃지 보드/3_준비의 광장 뱃지 획득.png"
    elif current_page == "memory_page" and 4 in cleared_villages:
        # 추억의 언덕에서 환호의 극장 뱃지 표시
        badge_image_path = "assets/뱃지 보드/4_환호의 극장 뱃지 획득.png"
    elif current_page == "summary_page" and 5 in cleared_villages:
        # 요약 페이지에서 추억의 언덕 뱃지 표시
        badge_image_path = "assets/뱃지 보드/5_추억의 언덕 뱃지 획득.png"
    elif not cleared_villages:
        # 아직 클리어한 마을이 없음
        badge_image_path = "assets/뱃지 보드/0_빈 뱃지 화면.png"
    else:
        # 기본적으로 가장 높은 클리어된 마을의 뱃지 표시
        max_cleared = max(cleared_villages)
        village_names = {
            1: "시작의 마을 뱃지 획득",
            2: "이야기 숲 뱃지 획득", 
            3: "준비의 광장 뱃지 획득",
            4: "환호의 극장 뱃지 획득",
            5: "추억의 언덕 뱃지 획득"
        }
        if max_cleared in village_names:
            badge_image_path = f"assets/뱃지 보드/{max_cleared}_{village_names[max_cleared]}.png"
        else:
            badge_image_path = "assets/뱃지 보드/0_빈 뱃지 화면.png"
    
    # Load badge image only once and cache it
    if 'badge_image_cache' not in st.session_state or st.session_state.get('badge_image_cache_path') != badge_image_path:
        full_path = get_file_path(badge_image_path)
        badge_image = get_base64_image(full_path)
        if badge_image:
            st.session_state.badge_image_cache = badge_image
            st.session_state.badge_image_cache_path = badge_image_path
        else:
            st.error("뱃지 이미지를 불러올 수 없습니다.")
            return
    else:
        badge_image = st.session_state.badge_image_cache
    
    # Initialize badge visibility state
    if 'badge_visible' not in st.session_state:
        st.session_state.badge_visible = False
    
    # Create toggle button using form for better state management
    with st.form("badge_toggle_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "🏆 뱃지 보드 (진행 현황 보기)",
                type="primary" if st.session_state.badge_visible else "secondary",
                use_container_width=True,
                help="뱃지 보드를 보이거나 숨깁니다 (더블 클릭)"
            )
    
    # Handle form submission
    if submit_button:
        st.session_state.badge_visible = not st.session_state.badge_visible
    
    # Auto-show badge board when village is cleared
    if st.session_state.get('badge_updated', False):
        st.session_state.badge_visible = True
        st.session_state.badge_updated = False
    
    # Create container for badge content and update it based on state
    badge_container = st.empty()
    
    # Display badge content if visible
    if st.session_state.badge_visible:
        with badge_container.container():
            st.markdown("---")
            st.markdown("### 🏆 뱃지 보드")
            # Display base64 image using CSS classes
            st.markdown(f"""
            <div class="image-container">
                <img src="data:image/image;base64,{badge_image}" alt="뱃지">
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**모험 완료한 장소: {len(cleared_villages)}개**")
            
            # 마을 이름들 하드코딩
            village_names = ["시작의 마을", "이야기 숲", "준비의 광장", "환호의 극장", "추억의 언덕"]
            
            # 클리어된 마을들 표시
            if cleared_villages:
                st.markdown("**완료한 마을들:**")
                for i, village_id in enumerate(sorted(cleared_villages)):
                    if 1 <= village_id <= len(village_names):
                        village_name = village_names[village_id - 1]  # village_id는 1부터 시작
                        st.markdown(f"• {village_name}")
            else:
                st.markdown("*아직 완료한 마을이 없습니다.*")
    else:
        # Clear the container when hidden
        badge_container.container().empty()

def render_map_popup():
    """지도 팝업을 렌더링하는 함수"""
    # 지도 팝업 표시 상태 확인
    if st.session_state.get('show_map_popup', False):
        # 전체지도.png 이미지 로드
        map_image = get_base64_image(get_file_path("assets/사진 모음/전체 지도.png"))
        
        if map_image:
            # 팝업 오버레이와 지도 이미지 표시
            st.markdown(f"""
            <div id="map-popup-overlay" class="map-popup-overlay">
                <div class="map-popup-content">
                    <div class="map-popup-header">
                        <h3>🗺️ 연극 대모험 지도</h3>
                    </div>
                    <div class="map-popup-body">
                        <img src="data:image/png;base64,{map_image}" alt="전체 지도" class="map-popup-image">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 간단한 닫기 버튼
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("❌ 팝업 닫기", key="close_map_popup", use_container_width=True):
                st.session_state.show_map_popup = False
                st.rerun()

def render_help_popup():
    """사용 방법 팝업을 렌더링하는 함수"""
    # 사용 방법 팝업 표시 상태 확인
    if st.session_state.get('show_help_popup', False):
        # 사용 방법.png 이미지 로드
        help_image = get_base64_image(get_file_path("assets/사진 모음/사용 방법.png"))
        
        if help_image:
            # 팝업 오버레이와 사용 방법 이미지 표시
            st.markdown(f"""
            <div id="help-popup-overlay" class="help-popup-overlay">
                <div class="help-popup-content">
                    <div class="help-popup-header">
                        <h3>📖 사용 방법</h3>
                    </div>
                    <div class="help-popup-body">
                        <img src="data:image/png;base64,{help_image}" alt="사용 방법" class="help-popup-image">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 간단한 닫기 버튼
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("❌ 팝업 닫기", key="close_help_popup", use_container_width=True):
                st.session_state.show_help_popup = False
                st.rerun()

def render_faq_popup():
    """자주하는 질문 팝업을 렌더링하는 함수"""
    # 자주하는 질문 팝업 표시 상태 확인
    if st.session_state.get('show_faq_popup', False):
        # 자주하는 질문.png 이미지 로드
        faq_image = get_base64_image(get_file_path("assets/사진 모음/자주하는 질문.png"))
        
        if faq_image:
            # 팝업 오버레이와 자주하는 질문 이미지 표시
            st.markdown(f"""
            <div id="faq-popup-overlay" class="faq-popup-overlay">
                <div class="faq-popup-content">
                    <div class="faq-popup-header">
                        <h3>❓ 자주하는 질문</h3>
                    </div>
                    <div class="faq-popup-body">
                        <img src="data:image/png;base64,{faq_image}" alt="자주하는 질문" class="map-popup-image">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 간단한 닫기 버튼
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("❌ 팝업 닫기", key="close_faq_popup", use_container_width=True):
                st.session_state.show_faq_popup = False
                st.rerun()

def render_script_popup():
    """극본의 특성 팝업을 렌더링하는 함수"""
    # 극본의 특성 팝업 표시 상태 확인
    if st.session_state.get('show_script_popup', False):
        # 극본의 특성.png 이미지 로드
        script_image = get_base64_image(get_file_path("assets/사진 모음/극본의 특성.png"))
        
        if script_image:
            # 팝업 오버레이와 극본의 특성 이미지 표시
            st.markdown(f"""
            <div id="script-popup-overlay" class="script-popup-overlay">
                <div class="script-popup-content">
                    <div class="script-popup-header">
                        <h3>📝 극본의 특성</h3>
                    </div>
                    <div class="script-popup-body">
                        <img src="data:image/png;base64,{script_image}" alt="극본의 특성" class="script-popup-image">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 간단한 닫기 버튼
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("❌ 팝업 닫기", key="close_script_popup", use_container_width=True):
                st.session_state.show_script_popup = False
                st.rerun()

def render_theater_popup():
    """연극의 특성 팝업을 렌더링하는 함수"""
    # 연극의 특성 팝업 표시 상태 확인
    if st.session_state.get('show_theater_popup', False):
        # 연극의 특성.png 이미지 로드
        theater_image = get_base64_image(get_file_path("assets/사진 모음/연극의 특성.png"))
        
        if theater_image:
            # 팝업 오버레이와 연극의 특성 이미지 표시
            st.markdown(f"""
            <div id="theater-popup-overlay" class="theater-popup-overlay">
                <div class="theater-popup-content">
                    <div class="theater-popup-header">
                        <h3>🎭 연극의 특성</h3>
                    </div>
                    <div class="theater-popup-body">
                        <img src="data:image/png;base64,{theater_image}" alt="연극의 특성" class="theater-popup-image">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 간단한 닫기 버튼
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("❌ 팝업 닫기", key="close_theater_popup", use_container_width=True):
                st.session_state.show_theater_popup = False
                st.rerun()

def clear_village(village_number):
    """Function called when a village is cleared"""
    if 'cleared_villages' not in st.session_state:
        st.session_state.cleared_villages = []
    
    # Update village clear status (중복 방지)
    if village_number not in st.session_state.cleared_villages:
        st.session_state.cleared_villages.append(village_number)
        
        # Trigger badge board update
        st.session_state.badge_updated = True
        st.rerun()

def play_bgm(bgm_path):
    """Function to play BGM"""
    try:
        if os.path.exists(bgm_path):
            # Store BGM information in session state
            st.session_state.current_bgm = bgm_path
            
            # Only display audio player if it's not already displayed
            if 'bgm_displayed' not in st.session_state or not st.session_state.bgm_displayed:
                st.session_state.bgm_displayed = True
                
                # 오른쪽 위에 작은 BGM 컨트롤 배치
                col1, col2, col3 = st.columns([0.9, 0.05, 0.05])
                
                with col3:
                    # BGM 라벨과 오디오 컨트롤을 작게 표시
                    st.markdown("🎵", help="BGM")
                    st.audio(
                        open(bgm_path, 'rb').read(),
                        format='audio/mp3',
                        start_time=0,
                        sample_rate=None,
                        key="bgm_player"
                    )
        else:
            st.error(f"BGM 파일을 찾을 수 없습니다: {bgm_path}")
    except Exception as e:
        st.error(f"BGM 재생 오류: {str(e)}")

def main():
    """Main function"""
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "intro"
    if 'cleared_villages' not in st.session_state:
        st.session_state.cleared_villages = []
    

    
    # Render badge board (displayed on all pages)
    render_badge_board()
    
    # Render map popup if needed (displayed on all pages)
    render_map_popup()
    
    # Render help popup if needed (displayed on all pages)
    render_help_popup()
    
    # Render FAQ popup if needed (displayed on all pages)
    render_faq_popup()
    
    # Render script popup if needed (displayed on all pages)
    render_script_popup()
    
    # Render theater popup if needed (displayed on all pages)
    render_theater_popup()
    
    # Page routing
    if st.session_state.current_page == "intro":
        intro_page()
    elif st.session_state.current_page == "adventure_map":
        adventure_map_page()
    elif st.session_state.current_page == "village":
        village_page()
    elif st.session_state.current_page == "story_forest":
        story_forest_page()
    elif st.session_state.current_page == "feedback_age":
        feedback_age_page()
    elif st.session_state.current_page == "prepare_page":
        prepare_page()
    elif st.session_state.current_page == "hwanho_page":
        hwanho_page()
    elif st.session_state.current_page == "memory_page":
        memory_page()
    elif st.session_state.current_page == "summary_page":
        summary_page()
    else:
        st.session_state.current_page = "intro"
        intro_page()

if __name__ == "__main__":
    main()
