import streamlit as st
import os
from utils import get_file_path, get_base64_image, render_common_menu

def adventure_map_page():
    """연극 대모험 지도 페이지"""
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 메인 콘텐츠
    # 제목과 설명 제거 - 지도 이미지만 표시
    
    # 전체 지도 이미지 표시 - 적당한 크기로
    map_image = get_base64_image(get_file_path("사진 모음/전체 지도.png"))
    
    if map_image:
        # 이미지를 CSS 클래스를 사용하여 적당한 크기로 표시
        st.markdown(f"""
        <div class="image-container">
            <img src="data:image/png;base64,{map_image}" alt="연극 대모험 지도" style="max-width: 100%; height: auto;">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("지도 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {get_file_path('사진 모음/전체 지도.png')}")
        st.write(f"파일 존재 여부: {os.path.exists(get_file_path('사진 모음/전체 지도.png'))}")
    
    # 시작의 마을로 출발하기 버튼 - 나중에 추가할 버튼들을 위한 위치 확보
    st.markdown(
    """
    <div style="text-align: center;">
        <b>연극 대모험을 떠날 준비가 되었나요? 오늘 탐험할 마을들이에요.</b><br>
        시작의 마을에서 먼저 연극 대본을 구성해볼 거예요.<br>
        모험을 떠날 준비가 되었다면 아래의 버튼을 눌러 출발해봐요요!
    </div>
    """,
    unsafe_allow_html=True
    )
    
    # 버튼들을 세로로 배치하여 나중에 추가하기 쉽게 구성
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏘️ 시작의 마을로 출발하기", 
                    key="go_to_village",
                    help="시작의 마을로 이동합니다",
                    use_container_width=True):
            st.session_state.village_dialog_message = "🏘️ 시작의 마을에 도착했어요! 이제 연극 대본 계획을 세워볼까요?"
            st.session_state.show_village_dialog = True
            st.session_state.current_page = "village"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
