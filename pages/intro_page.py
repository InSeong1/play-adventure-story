import streamlit as st
from utils import get_file_path, get_base64_image, render_common_menu, play_bgm

def intro_page():
    """인트로 페이지"""
    
    # BGM 재생
    play_bgm("0. 인트로 지도.mp3")
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 인트로 이미지를 적절한 크기로 표시 (배경이 아닌 일반 이미지)
    intro_image = get_base64_image(get_file_path("사진 모음/인트로.png"))
    
    if intro_image:
        # 이미지를 CSS 클래스를 사용하여 적절한 크기로 표시
        st.markdown(f"""
        <div class="image-container">
            <img src="data:image/png;base64,{intro_image}" alt="인트로 이미지">
        </div>
        """, unsafe_allow_html=True)
    
    # 인트로 나레이션 듣기 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎭 연극 대모험 이야기를를 들려주세요!", key="listen_intro_narration", 
                    help="클릭하여 이야기를 들을 수 있어요!",
                    use_container_width=True):
            st.session_state["show_intro_narration"] = not st.session_state.get("show_intro_narration", False)
            st.rerun()
    
    # 나레이션 오디오 플레이어 (버튼 클릭 시 표시)
    if st.session_state.get('show_intro_narration', False):
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("**🎧 이야기 듣기**")
            # 나레이션 오디오 파일 재생
            try:
                with open(get_file_path("나레이션 소리 모음/인트로 나레이션.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                
            except Exception as e:
                st.error(f"이야기 파일을 불러올 수 없습니다: {str(e)}")
                st.write(f"파일 경로: 나레이션 소리 모음/인트로 나레이션.mp3")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 모험 시작하기", key="start_adventure", 
                    help="클릭하여 연극 대모험 지도로 이동합니다",
                    use_container_width=True):
            st.session_state.current_page = "adventure_map"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
