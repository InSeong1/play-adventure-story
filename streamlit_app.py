import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from pages.intro_page import intro_page
from pages.adventure_map_page import adventure_map_page
from pages.village_page import village_page
from pages.feedback_page import feedback_page
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
    
    // 사용 방법 팝업 닫기 함수
    function closeHelpPopup() {
        const popup = document.getElementById('help-popup-overlay');
        if (popup) {
            popup.style.display = 'none';
        }
    }
    
    // 자주하는 질문 팝업 닫기 함수
    function closeFaqPopup() {
        const popup = document.getElementById('faq-popup-overlay');
        if (popup) {
            popup.style.display = 'none';
        }
    }
    
    // 극본의 특성 팝업 닫기 함수
    function closeScriptPopup() {
        const popup = document.getElementById('script-popup-overlay');
        if (popup) {
            popup.style.display = 'none';
        }
    }
    
    // 연극의 특성 팝업 닫기 함수
    function closeTheaterPopup() {
        const popup = document.getElementById('theater-popup-overlay');
        if (popup) {
            popup.style.display = 'none';
        }
    }
    
    // ESC 키로 팝업 닫기
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeMapPopup();
            closeHelpPopup();
            closeFaqPopup();
            closeScriptPopup();
            closeTheaterPopup();
        }
    });
    
    // 팝업 외부 클릭으로 닫기
    document.addEventListener('click', function(event) {
        const mapPopup = document.getElementById('map-popup-overlay');
        const helpPopup = document.getElementById('help-popup-overlay');
        const faqPopup = document.getElementById('faq-popup-overlay');
        const scriptPopup = document.getElementById('script-popup-overlay');
        const theaterPopup = document.getElementById('theater-popup-overlay');
        
        if (mapPopup && event.target === mapPopup) {
            closeMapPopup();
        }
        if (helpPopup && event.target === helpPopup) {
            closeHelpPopup();
        }
        if (faqPopup && event.target === faqPopup) {
            closeFaqPopup();
        }
        if (scriptPopup && event.target === scriptPopup) {
            closeScriptPopup();
        }
        if (theaterPopup && event.target === theaterPopup) {
            closeTheaterPopup();
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
    
    .popup-close-btn {
        position: absolute;
        top: 10px;
        right: 15px;
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .popup-close-btn:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.1);
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

def dialog_dismiss_callback():
    """Universal dialog dismiss callback that scrolls to top"""
    # Set flag to trigger scroll after rerun
    st.session_state.dialog_dismissed = True
    st.session_state.scroll_to_top_after_dialog = True

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
    elif current_page == "feedback_page" and 1 in cleared_villages:
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

@st.dialog("🗺️ 연극 대모험 지도", width="large", on_dismiss=dialog_dismiss_callback)
def show_map_dialog():
    """지도 다이얼로그"""
    # 전체지도.png 이미지 로드
    map_image = get_base64_image(get_file_path("assets/사진 모음/전체 지도.png"))
    
    if map_image:
        # 지도 이미지 표시
        st.image(f"data:image/png;base64,{map_image}")
    else:
        st.error("지도 이미지를 불러올 수 없습니다.")

def village_dialog_callback():
    """village_page dialog dismiss callback"""
    dialog_dismiss_callback()
    if st.session_state.get('current_page') == 'village':
        st.session_state.dialog_dismissed = True

@st.dialog("알림", width="medium", on_dismiss=village_dialog_callback)
def show_arrival_dialog(message: str = ""):
    if message:
        st.markdown(message)

@st.dialog("🌟 모험의 시작", width="medium", on_dismiss=dialog_dismiss_callback)
def show_adventure_start_dialog():
    """모험 시작 다이얼로그"""
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h3 style='color: #4ECDC4; margin-bottom: 20px;'>🎭 연극 대모험에 오신 것을 환영해요!</h3>
        <p style='font-size: 1.1rem; line-height: 1.6; color: #333; margin-bottom: 15px;'>
            이제 정말 신나는 모험이 시작돼요! 🚀
        </p>
        <p style='font-size: 1rem; line-height: 1.6; color: #666;'>
            지도에서 원하는 마을을 선택해서<br>
            멋진 연극 이야기를 만들어보세요! ✨
        </p>
        <p style='font-size: 0.9rem; color: #888; margin-top: 20px;'>
            준비되셨나요? 그럼 함께 떠나요! 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)

@st.dialog("🏆 뱃지 획득", width="large", on_dismiss=village_dialog_callback)
def show_badge_dialog(image_filename: str = ""):
    if not image_filename:
        return
    full_path = get_file_path(f"assets/뱃지 모음/{image_filename}")
    badge_image = get_base64_image(full_path)
    captions = {
        "1_뱃지_시작의 마을.png": "시작의 마을 뱃지를 획득했어요! 다음 모험도 힘차게 떠나볼까요?",
        "2_뱃지_이야기숲.png": "이야기 숲 뱃지를 획득했어요! 멋진 아이디어가 숲처럼 자라고 있어요!",
        "3_뱃지_준비의 광장.png": "준비의 광장 뱃지를 획득했어요! 차근차근 준비한 만큼 더 멋진 공연이 될 거예요!",
        "4_뱃지_환호의 극장.png": "환호의 극장 뱃지를 획득했어요! 최고의 무대였어요, 정말 자랑스러워요!",
        "5_뱃지_추억의 언덕.png": "마지막 뱃지까지 모두 모았어요! 오늘의 모험을 멋지게 마무리했네요. 정말 잘했어요!"
    }
    if badge_image:
        st.markdown(f"<div style='text-align:center'><img src='data:image/png;base64,{badge_image}' alt='뱃지' style='max-width: 90%; height: auto; border-radius: 14px; box-shadow: 0 12px 36px rgba(0,0,0,0.25);'></div>", unsafe_allow_html=True)
        caption = captions.get(image_filename, "멋진 성과예요! 계속해서 즐겁게 모험을 이어가요!")
        st.markdown(f"<div style='text-align:center; margin-top: 12px; font-size: 1.05rem;'>✨ {caption}</div>", unsafe_allow_html=True)
    else:
        st.error("뱃지 이미지를 불러올 수 없습니다.")

def scroll_to_top():
    """페이지 상단으로 스크롤하는 함수"""
    import streamlit.components.v1 as components
    
    # 현재 페이지에 따라 적절한 div ID 선택
    current_page = st.session_state.get('current_page', 'intro')
    page_div_ids = {
        'adventure_map': 'adventure-map-top',
        'village': 'village-audio-top',
        'story_forest': 'feedback-page-top',  # feedback_page의 div ID
        'feedback_page': 'feedback-page-top',
        'prepare_page': 'prepare-page-top',
        'hwanho_page': 'hwanho-page-top',
        'memory_page': 'memory-page-top',
        'summary_page': 'summary-page-top'
    }
    
    target_div_id = page_div_ids.get(current_page, None)
    
    if target_div_id:
        components.html(f"""
        <script>
            // 여러 방법으로 스크롤을 맨 위로 이동
            function scrollToTop() {{
                // 1. 먼저 기본 스크롤
                window.parent.scrollTo(0, 0);
                
                // 2. 특정 div로 스크롤 시도
                var element = window.parent.document.getElementById('{target_div_id}');
                if (element) {{
                    element.scrollIntoView({{behavior: 'smooth', block: 'start'}});
                }}
                
                // 3. 강제로 상단으로 이동
                setTimeout(function() {{
                    window.parent.scrollTo(0, 0);
                    // 추가 보장
                    window.parent.document.documentElement.scrollTop = 0;
                    window.parent.document.body.scrollTop = 0;
                }}, 50);
            }}
            
            // 즉시 실행
            scrollToTop();
            
            // DOM 로드 후에도 실행
            setTimeout(scrollToTop, 100);
            setTimeout(scrollToTop, 300);
        </script>
        """, height=0)
    else:
        # 기본 스크롤 (intro 페이지 등)
        components.html("""
        <script>
            // 여러 방법으로 스크롤을 맨 위로 이동
            function scrollToTop() {
                window.parent.scrollTo(0, 0);
                window.parent.document.documentElement.scrollTop = 0;
                window.parent.document.body.scrollTop = 0;
                
                // iframe 내부 스크롤도 처리
                var iframes = window.parent.document.querySelectorAll('iframe');
                iframes.forEach(function(iframe) {
                    try {
                        iframe.contentWindow.scrollTo(0, 0);
                    } catch(e) {}
                });
            }
            
            // 즉시 실행
            scrollToTop();
            
            // DOM이 로드된 후에도 실행
            setTimeout(scrollToTop, 100);
            setTimeout(scrollToTop, 300);
            setTimeout(scrollToTop, 500);
        </script>
        """, height=0)

def scroll_to_element(element_id):
    """특정 요소로 스크롤하는 함수"""
    import streamlit.components.v1 as components
    components.html(f"""
    <script>
        var element = window.parent.document.getElementById('{element_id}');
        if (element) {{
            element.scrollIntoView({{behavior: 'smooth', block: 'start'}});
        }}
    </script>
    """, height=0)

def render_map_popup():
    """지도 팝업을 렌더링하는 함수"""
    # 지도 팝업 표시 상태 확인
    if st.session_state.get('show_map_popup', False):
        show_map_dialog()
        # 다이얼로그가 닫히면 상태 초기화
        st.session_state.show_map_popup = False
            

@st.dialog("📖 사용 방법", width="large", on_dismiss=dialog_dismiss_callback)
def show_help_dialog():
    """사용 방법 다이얼로그"""
    # 사용 방법.png 이미지 로드
    help_image = get_base64_image(get_file_path("assets/사진 모음/사용 방법.png"))
    
    if help_image:
        # 사용 방법 이미지 표시
        st.image(f"data:image/png;base64,{help_image}")
    else:
        st.error("사용 방법 이미지를 불러올 수 없습니다.")

def render_help_popup():
    """사용 방법 팝업을 렌더링하는 함수"""
    # 사용 방법 팝업 표시 상태 확인
    if st.session_state.get('show_help_popup', False):
        show_help_dialog()
        # 다이얼로그가 닫히면 상태 초기화
        st.session_state.show_help_popup = False
            

@st.dialog("❓ 자주하는 질문", width="large", on_dismiss=dialog_dismiss_callback)
def show_faq_dialog():
    """자주하는 질문 다이얼로그"""
    # 자주하는 질문.png 이미지 로드
    faq_image = get_base64_image(get_file_path("assets/사진 모음/자주하는 질문.png"))
    
    if faq_image:
        # 자주하는 질문 이미지 표시
        st.image(f"data:image/png;base64,{faq_image}")
    else:
        st.error("자주하는 질문 이미지를 불러올 수 없습니다.")

def render_faq_popup():
    """자주하는 질문 팝업을 렌더링하는 함수"""
    # 자주하는 질문 팝업 표시 상태 확인
    if st.session_state.get('show_faq_popup', False):
        show_faq_dialog()
        # 다이얼로그가 닫히면 상태 초기화
        st.session_state.show_faq_popup = False
            

@st.dialog("📝 극본의 특성", width="large", on_dismiss=dialog_dismiss_callback)
def show_script_dialog():
    """극본의 특성 다이얼로그"""
    # 극본의 특성.png 이미지 로드
    script_image = get_base64_image(get_file_path("assets/사진 모음/극본의 특성.png"))
    
    if script_image:
        # 극본의 특성 이미지 표시
        st.image(f"data:image/png;base64,{script_image}")
    else:
        st.error("극본의 특성 이미지를 불러올 수 없습니다.")

def render_script_popup():
    """극본의 특성 팝업을 렌더링하는 함수"""
    # 극본의 특성 팝업 표시 상태 확인
    if st.session_state.get('show_script_popup', False):
        show_script_dialog()
        # 다이얼로그가 닫히면 상태 초기화
        st.session_state.show_script_popup = False
            

@st.dialog("🎭 연극의 특성", width="large", on_dismiss=dialog_dismiss_callback)
def show_theater_dialog():
    """연극의 특성 다이얼로그"""
    # 연극의 특성.png 이미지 로드
    theater_image = get_base64_image(get_file_path("assets/사진 모음/연극의 특성.png"))
    
    if theater_image:
        # 연극의 특성 이미지 표시
        st.image(f"data:image/png;base64,{theater_image}")
    else:
        st.error("연극의 특성 이미지를 불러올 수 없습니다.")

def render_theater_popup():
    """연극의 특성 팝업을 렌더링하는 함수"""
    # 연극의 특성 팝업 표시 상태 확인
    if st.session_state.get('show_theater_popup', False):
        show_theater_dialog()
        # 다이얼로그가 닫히면 상태 초기화
        st.session_state.show_theater_popup = False
            

    

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
    
    # Check if dialog was dismissed and scroll to top
    if st.session_state.get('scroll_to_top_after_dialog', False):
        scroll_to_top()
        st.session_state.scroll_to_top_after_dialog = False
    
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
    # Show badge dialog if requested (one-at-a-time)
    if st.session_state.get('show_badge_dialog', False):
        show_badge_dialog(st.session_state.get('badge_image_filename', ''))
        st.session_state.show_badge_dialog = False

    # Show adventure start dialog if transitioning to adventure_map
    if st.session_state.get('show_adventure_start_dialog', False):
        show_adventure_start_dialog()
        st.session_state.show_adventure_start_dialog = False

    if st.session_state.current_page == "intro":
        intro_page()
    elif st.session_state.current_page == "adventure_map":
        adventure_map_page()
    elif st.session_state.current_page == "village":
        if st.session_state.get('show_village_dialog'):
            show_arrival_dialog(st.session_state.get('village_dialog_message', ''))
            st.session_state.show_village_dialog = False
        village_page()
    elif st.session_state.current_page == "story_forest":
        feedback_page()
    elif st.session_state.current_page == "feedback_page":
        if st.session_state.get('show_feedback_dialog'):
            show_arrival_dialog(st.session_state.get('feedback_dialog_message', ''))
            st.session_state.show_feedback_dialog = False
            # 다이얼로그 닫힌 후 초대장 듣기 버튼으로 스크롤
            scroll_to_element("초대장-듣기-버튼")
        feedback_page()
    elif st.session_state.current_page == "prepare_page":
        if st.session_state.get('show_prepare_dialog'):
            show_arrival_dialog(st.session_state.get('prepare_dialog_message', ''))
            st.session_state.show_prepare_dialog = False
            # 다이얼로그 닫힌 후 초대장 듣기 버튼으로 스크롤
            scroll_to_element("초대장-듣기-버튼")
        prepare_page()
    elif st.session_state.current_page == "hwanho_page":
        if st.session_state.get('show_hwanho_dialog'):
            show_arrival_dialog(st.session_state.get('hwanho_dialog_message', ''))
            st.session_state.show_hwanho_dialog = False
            # 다이얼로그 닫힌 후 초대장 듣기 버튼으로 스크롤
            scroll_to_element("초대장-듣기-버튼")
        hwanho_page()
    elif st.session_state.current_page == "memory_page":
        if st.session_state.get('show_memory_dialog'):
            show_arrival_dialog(st.session_state.get('memory_dialog_message', ''))
            st.session_state.show_memory_dialog = False
            # 다이얼로그 닫힌 후 초대장 듣기 버튼으로 스크롤
            scroll_to_element("초대장-듣기-버튼")
        memory_page()
    elif st.session_state.current_page == "summary_page":
        if st.session_state.get('show_summary_dialog'):
            show_arrival_dialog(st.session_state.get('summary_dialog_message', ''))
            st.session_state.show_summary_dialog = False
        summary_page()
    else:
        st.session_state.current_page = "intro"
        intro_page()

if __name__ == "__main__":
    main()
