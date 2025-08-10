import streamlit as st
from utils import play_bgm, get_file_path, get_base64_image, render_common_menu, generate_play_scenario
import os

def feedback_age_page():
    """피드백 페이지 (이야기 숲)"""
    # 페이지 상단으로 스크롤
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
    </script>
    """, unsafe_allow_html=True)
    
    # BGM 재생 - 이야기 숲 BGM
    bgm_path = get_file_path("브금 모음/2. 이야기 숲.mp3")
    play_bgm(bgm_path)
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 초대장 이미지를 적절한 크기로 표시 (배경이 아닌 일반 이미지)
    invitation_path = get_file_path("사진 모음/초대장/2_이야기 숲 초대장.png")
    invitation_image = get_base64_image(invitation_path)
    
    if invitation_image:
        # 이미지를 CSS 클래스를 사용하여 적절한 크기로 표시
        st.markdown(f"""
        <div class="image-container">
            <img src="data:image/png;base64,{invitation_image}" alt="이야기 숲 초대장">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("초대장 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {invitation_path}")
        st.write(f"파일 존재 여부: {os.path.exists(invitation_path)}")
    
    # 초대장 듣기 버튼과 나레이션 오디오 플레이어
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📜 초대장 듣기", key="listen_invitation", 
                    help="클릭하여 초대장 나레이션을 들을 수 있습니다",
                    use_container_width=True):
            st.session_state.show_narration = True
            # BGM 음량을 절반으로 줄임
            if 'bgm_volume' in st.session_state:
                st.session_state.bgm_volume = 0.2
            st.rerun()
    
    # 나레이션 오디오 플레이어 (버튼 클릭 시 표시)
    if st.session_state.get('show_narration', False):
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("**🎧 나레이션 재생**")
            # 나레이션 오디오 파일 재생 (BGM과 함께)
            try:
                with open(get_file_path("나레이션 소리 모음/2.이야기 숲.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                
                # 나레이션 텍스트 내용 출력
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📖 나레이션 내용:**")
                try:
                    with open(get_file_path("나레이션/2.이야기 숲.txt"), "r", encoding="utf-8") as text_file:
                        narration_text = text_file.read()
                        st.write(narration_text)
                except Exception as e:
                    st.error(f"나레이션 텍스트 파일을 불러올 수 없습니다: {str(e)}")
                
            except Exception as e:
                st.error(f"나레이션 파일을 불러올 수 없습니다: {str(e)}")
                st.write(f"파일 경로: 나레이션 소리 모음/2.이야기 숲.mp3")
    
    # 사용자 입력 폼 (스크롤 아래에 배치)
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    # 입력 폼 제목
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">✏️ 대본 수정 및 피드백</h2>
        <p style="color: #666; font-size: 1.1rem;">이전 마을에서 생성된 시나리오를 바탕으로 피드백을 받고 수정해보세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 이전 마을에서 생성된 시나리오 표시
    if 'generated_scenario' in st.session_state:
        st.markdown("### 📖 현재 대본")
        st.markdown("---")
        st.text_area("시나리오 내용", value=st.session_state.generated_scenario, 
                    height=300, disabled=True, key="current_scenario")
        
        # 피드백 생성 버튼
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🤖 AI 피드백 받기", key="get_feedback", 
                        help="AI가 현재 시나리오에 대한 피드백을 제공합니다",
                        use_container_width=True):
                
                st.success("🤖 AI가 피드백을 생성하고 있습니다...")
                
                # 프롬프트 파일 읽기
                try:
                    with open(get_file_path("프롬프트/2.이야기 숲.txt"), "r", encoding="utf-8") as prompt_file:
                        prompt_template = prompt_file.read()
                    
                    # 프롬프트에 입력값 치환
                    prompt = prompt_template.format(
                        scenario=st.session_state.generated_scenario
                    )
                    
                    # OpenAI API를 사용하여 피드백 생성
                    with st.spinner("🤖 AI가 피드백을 생성하고 있습니다..."):
                        generated_feedback = generate_play_scenario(prompt)
                    
                    # 생성된 피드백을 세션 상태에 저장
                    st.session_state.generated_feedback = generated_feedback
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"프롬프트 파일을 불러올 수 없습니다: {str(e)}")
        
        # 생성된 피드백 표시
        if 'generated_feedback' in st.session_state:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 💬 AI 피드백")
            st.markdown("---")
            st.markdown(st.session_state.generated_feedback)
            
            # 대본 수정 입력
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🔄 대본 수정")
            
            modified_scenario = st.text_area(
                "피드백을 바탕으로 수정된 대본을 입력하세요",
                value=st.session_state.generated_scenario,
                height=300,
                help="AI 피드백을 참고하여 대본을 수정해보세요"
            )
            
            # 수정 완료 버튼
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("✅ 수정 완료", key="submit_modification", 
                            help="대본 수정을 완료합니다",
                            use_container_width=True):
                    
                    # 수정된 시나리오를 세션 상태에 저장
                    st.session_state.modified_scenario = modified_scenario
                    
                    st.success("🎉 대본 수정이 완료되었습니다!")
                    
                    # 다음 마을로 이동 버튼
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    if st.button("🌲 다음 마을로", key="next_village", 
                                help="준비의 광장으로 이동합니다",
                                use_container_width=True):
                        st.session_state.current_page = "preparation_plaza"
                        st.rerun()
    else:
        st.info("💡 시작의 마을에서 먼저 대본을 작성해주세요!")
        
        # 홈으로 돌아가기 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏠 홈으로 돌아가기", key="go_home", 
                        help="홈 페이지로 돌아갑니다",
                        use_container_width=True):
                st.session_state.current_page = "intro"
                st.rerun()
