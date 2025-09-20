import streamlit as st
from utils import get_file_path, get_base64_image, render_common_menu

def intro_page():
    """인트로 페이지"""
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 인트로 이미지를 적절한 크기로 표시 (배경이 아닌 일반 이미지)
    intro_image = get_base64_image(get_file_path("사진 모음/인트로.png"))
    
    if intro_image:
        # 먼저 오디오 플레이어들을 배치
        col1, col2, col3 = st.columns([1, 5, 1])
        
        # 배경음악 (첫 번째 컬럼)
        with col1:
            st.markdown("🎵 배경음악 듣기", help="배경음악")
            try:
                with open(get_file_path("브금 모음/0. 인트로 지도.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
            except Exception as e:
                st.error(f"BGM 파일을 불러올 수 없습니다: {str(e)}")
        
        # 나레이션 (마지막 컬럼)
        with col3:
            st.markdown("🎧 이야기 듣기", help="이야기 듣기")
            try:
                with open(get_file_path("나레이션 소리 모음/인트로 나레이션.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
            except Exception as e:
                st.error(f"이야기 파일을 불러올 수 없습니다: {str(e)}")
        
        # 공백 추가
        st.markdown("")
        st.markdown("")
        # 이미지를 중앙에 배치 (크기 조절)
        # col_left, col_center, col_right = st.columns([1, 2, 1])
        # with col_center:
        st.image(f"data:image/png;base64,{intro_image}")
    
    # 스크립트 텍스트 추가
    st.markdown("<br>", unsafe_allow_html=True)
    #col1, col2, col3 = st.columns([1, 2, 1])
    #with col2:
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin: 20px 0;">
        <h3 style="text-align: center; color: #333; margin-bottom: 15px;">🎭 연극 대모험에 오신 것을 환영합니다!</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #555; text-align: center;">
            어서 오세요! <strong>연극 대모험</strong>에 참여하게 된 여러분을 진심으로 환영합니다.<br> 
            이 모험 속에서 여러분은 아이디어를 떠올리는 순간부터 무대에 오르는 순간까지, 
            연극의 <strong>모든 과정을 직접 경험</strong>하게 될 거예요.<br>
            각 마을에서 주어진 활동을 하나씩 완수할 때마다 새로운 뱃지를 얻고, 다음 모험으로 나아갈 수 있습니다.<br>
            상상력과 협동심을 발휘해 멋진 무대를 만들어 갈 준비 되었나요?<br>
            그럼 지금부터, 연극의 세계로 함께 떠나봅시다!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    #col1, col2, col3 = st.columns([1, 2, 1])
   # with col2:
    if st.button("🚀 모험 시작하기", key="start_adventure", 
                help="클릭하여 연극 대모험 지도로 이동합니다",
                use_container_width=True):
        # Show adventure start dialog first
        st.session_state.show_adventure_start_dialog = True
        st.session_state.current_page = "adventure_map"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
