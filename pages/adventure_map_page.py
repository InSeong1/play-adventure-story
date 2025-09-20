import streamlit as st
import os
from utils import get_file_path, get_base64_image, render_common_menu

def adventure_map_page():
    """연극 대모험 지도 페이지"""
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 페이지 상단으로 스크롤 (dialog 닫힐 때 커서가 여기로 오도록)
    st.markdown('<div id="adventure-map-top"></div>', unsafe_allow_html=True)
    
    # 전체 지도 이미지 표시
    map_image = get_base64_image(get_file_path("사진 모음/전체 지도.png"))
    
    if map_image:
        # 오디오 플레이어들을 배치
        col1, col2, col3 = st.columns([1, 5, 1])
        
        # 배경음악 (첫 번째 컬럼)
        with col1:
            st.markdown("🎵 배경음악 듣기", help="배경음악")
            try:
                with open(get_file_path("브금 모음/0. 인트로 지도.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
            except Exception as e:
                st.error(f"BGM 파일을 불러올 수 없습니다: {str(e)}")
        
        # 지도 설명 듣기 (마지막 컬럼)
        with col3:
            st.markdown("🗺️ 지도 설명 듣기", help="지도 설명 듣기")
            try:
                with open(get_file_path("나레이션 소리 모음/지도 나레이션.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
            except Exception as e:
                st.error(f"지도 설명 파일을 불러올 수 없습니다: {str(e)}")
        
        # 공백 추가
        st.markdown("")
        st.markdown("")
        # 지도 이미지를 중앙에 배치
        st.image(f"data:image/png;base64,{map_image}")
    else:
        st.error("지도 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {get_file_path('사진 모음/전체 지도.png')}")
        st.write(f"파일 존재 여부: {os.path.exists(get_file_path('사진 모음/전체 지도.png'))}")
    
    # 스크립트 텍스트 추가
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin: 20px 0;">
        <h3 style="text-align: center; color: #333; margin-bottom: 15px;">🗺️ 연극 대모험의 전체 지도입니다!</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #555; text-align: center;">
            <strong>첫 번째, 시작의 마을</strong>에서는 여러분의 아이디어를 담아 연극 대본 계획서를 작성합니다.<br>
            <strong>두 번째, 이야기 숲</strong>에서는 AI 피드백을 참고하여 직접 극본을 완성합니다.<br>
            <strong>세 번째, 준비의 광장</strong>에서는 완성한 극본으로 연습하며 무대를 준비합니다.<br>
            <strong>네 번째, 환호의 극장</strong>에서는 드디어 무대에 올라 연기를 펼칩니다.<br>
            <strong>마지막으로, 추억의 언덕</strong>에서 우리의 모험을 돌아보고 경험을 정리하며 추억을 남깁니다.<br>
            이 지도를 따라 차근차근 모험을 이어가 보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 시작의 마을로 출발하기 버튼
    if st.button("🏘️ 시작의 마을로 출발하기", 
                key="go_to_village",
                help="시작의 마을로 이동합니다",
                use_container_width=True):
        st.session_state.village_dialog_message = "🏘️ 시작의 마을에 도착했어요! 이제 연극 대본 계획을 세워볼까요?"
        st.session_state.show_village_dialog = True
        st.session_state.current_page = "village"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
