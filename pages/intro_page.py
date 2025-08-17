import streamlit as st
from utils import play_bgm, get_file_path, get_base64_image, render_common_menu

def intro_page():
    """인트로 페이지"""
    # BGM 재생 - 인트로 페이지 BGM
    bgm_path = get_file_path("브금 모음/첫 시작 bgm.mp3")
    play_bgm(bgm_path)
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.header("연극 대모험")
    st.subheader("초등 5‧6학년의 연극 활동을 위한 통합 학습 AI 소프트웨어")
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
    
    # 모험 시작하기 버튼 - 가운데 정렬, 크게, 그림에서 한 칸 떨어지게
    st.markdown("<br><br><br>", unsafe_allow_html=True)  # 그림에서 한 칸 떨어지게
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 모험 시작하기", key="start_adventure", 
                    help="클릭하여 연극 대모험 지도로 이동합니다",
                    use_container_width=True):
            st.session_state.current_page = "adventure_map"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
