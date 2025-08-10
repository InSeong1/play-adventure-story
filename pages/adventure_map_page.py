import streamlit as st
from utils import play_bgm, get_file_path, get_base64_image, render_common_menu

def adventure_map_page():
    """연극 대모험 지도 페이지"""
    # BGM 계속 재생 (intro와 같은 BGM)
    if 'current_bgm' in st.session_state:
        # 기존 BGM 계속 재생
        bgm_path = st.session_state.current_bgm
        play_bgm(bgm_path)
    else:
        # 새로운 BGM 시작
        bgm_path = get_file_path("브금 모음/첫 시작 bgm.mp3")
        play_bgm(bgm_path)
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 메인 콘텐츠
    # 제목과 설명 제거 - 지도 이미지만 표시
    
    # 전체 지도 이미지 표시 - 엄청 크게
    map_image = get_base64_image(get_file_path("사진 모음/전체 지도.png"))
    
    if map_image:
        # 이미지를 CSS 클래스를 사용하여 표시
        st.markdown(f"""
        <div class="image-container">
            <img src="data:image/png;base64,{map_image}" alt="연극 대모험 지도">
        </div>
        """, unsafe_allow_html=True)
    
    # 시작의 마을로 출발하기 버튼 - 나중에 추가할 버튼들을 위한 위치 확보
    st.markdown("<br><br><br>", unsafe_allow_html=True)  # 이미지와 버튼 사이 간격
    
    # 버튼들을 세로로 배치하여 나중에 추가하기 쉽게 구성
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏘️ 시작의 마을로 출발하기", 
                    key="go_to_village",
                    help="시작의 마을로 이동합니다",
                    use_container_width=True):
            st.session_state.current_page = "village"
            st.rerun()
        
        # 나중에 추가할 버튼들을 위한 공간
        st.markdown("<br>", unsafe_allow_html=True)
        # 예시: 다음 버튼이 추가될 위치
        # if st.button("🌲 이야기 숲으로 출발하기", key="go_to_forest", use_container_width=True):
        #     st.session_state.current_page = "forest"
        #     st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
