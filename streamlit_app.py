import streamlit as st
import os
import base64
from pages.intro_page import intro_page
from pages.adventure_map_page import adventure_map_page
from pages.village_page import village_page
from pages.story_forest_page import story_forest_page
from pages.feedback_age import feedback_age_page

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
    
    .audio-player-container {
        position: fixed;
        top: 5px;
        right: 5px;
        z-index: 1000;
        background: rgba(0, 0, 0, 0.7);
        border-radius: 3px;
        padding: 2px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        max-width: 40px;
        text-align: center;
        font-size: 6px;
    }
    
    .audio-player-container .audio-label {
        font-size: 6px;
        color: white;
        margin-bottom: 1px;
        font-weight: bold;
    }
    
    .audio-player-container audio {
        width: 35px;
        height: 20px;
        transform: scale(0.8);
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
    
    # Determine badge image path
    if not cleared_villages:
        badge_image_path = "assets/뱃지 보드/0_빈 뱃지 화면.png"
    else:
        # Village name mapping
        village_names = {
            1: "시작의 마을 뱃지 획득",
            2: "이야기 숲 뱃지 획득", 
            3: "준비의 광장 뱃지 획득",
            4: "환호의 극장 뱃지 획득",
            5: "추억의 언덕 뱃지 획득"
        }
        if cleared_villages[0] in village_names:
            badge_image_path = f"assets/뱃지 보드/{cleared_villages[0]}_{village_names[cleared_villages[0]]}.png"
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
                "🏆 뱃지 보드",
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
                <img src="data:image/png;base64,{badge_image}" alt="뱃지">
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**클리어한 마을: {len(cleared_villages)}개**")
    else:
        # Clear the container when hidden
        badge_container.empty()

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
                # Display audio player in top right (minimal size)
                st.markdown(f"""
                <div class="audio-player-container">
                    <div class="audio-label">🎵</div>
                    <audio controls autoplay loop style="width: 35px; height: 20px;">
                        <source src="data:audio/mp3;base64,{base64.b64encode(open(bgm_path, 'rb').read()).decode()}" type="audio/mp3">
                    </audio>
                </div>
                """, unsafe_allow_html=True)
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
    else:
        st.session_state.current_page = "intro"
        intro_page()

if __name__ == "__main__":
    main()
