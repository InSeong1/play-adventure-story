import streamlit as st
from utils import play_bgm, get_file_path, get_base64_image, render_common_menu, generate_play_scenario
import os

def feedback_age_page():
    """피드백 페이지 (이야기 숲)"""
    # 페이지 상단으로 스크롤
    st.markdown("""
    <script>
        // 즉시 맨 위로 스크롤
        window.scrollTo(0, 0);
        
        // 페이지 로드 완료 후에도 맨 위로 스크롤
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                window.scrollTo(0, 0);
            });
        }
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
            st.markdown("**🎧 초대장 듣기**")
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
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">✏️ 극본 작성하기</h2>
        <p style="color: #666; font-size: 1.1rem;">이전 마을에서 입력한 정보를 확인하고 대본을 작성해보아요. <br>왼쪽 메뉴에서 극본의 구성 요소를 확인해 보아요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 극본의 특성 이미지 표시
    script_characteristics_path = get_file_path("사진 모음/극본의 특성.png")
    script_characteristics_image = get_base64_image(script_characteristics_path)
    
    if script_characteristics_image:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="image-container">
                <img src="data:image/png;base64,{script_characteristics_image}" alt="극본의 특성" style="max-width: 100%; height: auto;">
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("극본의 특성 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {script_characteristics_path}")
        st.write(f"파일 존재 여부: {os.path.exists(script_characteristics_path)}")
    
    # 이전 마을에서 입력한 정보 표시
    if 'village_inputs' in st.session_state:
        inputs = st.session_state.village_inputs
        st.markdown("### 📋 입력한 연극 정보")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**👥 등장인물 수:** {inputs['character_count']}명")
            st.markdown(f"**📝 등장인물 이름:** {inputs['character_names']}")
            st.markdown(f"**🎬 연극 장르:** {inputs['genre']}")
            st.markdown(f"**🎯 연극 주제:** {inputs['theme']}")
        
        with col2:
            st.markdown(f"**⏰ 시간적 배경:** {inputs['time_background']}")
            st.markdown(f"**🏛️ 공간적 배경:** {inputs['space_background']}")
            st.markdown(f"**⏱️ 공연 시간:** {inputs['performance_time']}분")
            st.markdown(f"**🎭 장면 수:** {inputs['scene_count']}개")
        
        st.markdown(f"**📖 이야기 흐름:** {inputs['story_flow']}")
        st.markdown("---")
        
        # 극본 예시 이미지 토글 버튼
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📖 극본 예시 보기", key="toggle_script_examples", 
                        help="극본 작성 예시를 확인할 수 있습니다",
                        use_container_width=True):
                # 토글 상태를 세션에 저장 (rerun 없이)
                if 'show_script_examples' not in st.session_state:
                    st.session_state.show_script_examples = False
                st.session_state.show_script_examples = not st.session_state.show_script_examples
        
        # 극본 예시 이미지 표시 (토글 상태에 따라)
        if st.session_state.get('show_script_examples', False):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📖 극본 작성 예시")
            st.markdown("---")
            
            # 예시 이미지들을 2열로 배치
            col1, col2 = st.columns(2)
            
            with col1:
                # 극본 예시1 이미지
                example1_path = get_file_path("사진 모음/극본 예시1.png")
                example1_image = get_base64_image(example1_path)
                
                if example1_image:
                    st.markdown(f"""
                    <div class="image-container">
                        <img src="data:image/png;base64,{example1_image}" alt="극본 예시1" style="max-width: 100%; height: auto;">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("극본 예시1 이미지를 불러올 수 없습니다.")
            
            with col2:
                # 극본 예시2 이미지
                example2_path = get_file_path("사진 모음/극본 예시2.png")
                example2_image = get_base64_image(example2_path)
                
                if example2_image:
                    st.markdown(f"""
                    <div class="image-container">
                        <img src="data:image/png;base64,{example2_image}" alt="극본 예시2" style="max-width: 100%; height: auto;">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("극본 예시2 이미지를 불러올 수 없습니다.")
            
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; color: #666; font-size: 0.9rem; font-style: italic; margin-top: 1rem;">
                출처: 교육부, 《국어 6-2》, 182-185쪽.
            </div>
            """, unsafe_allow_html=True)
        
        # 장면별 무대와 대본 입력
        st.markdown("### 🎭 장면별 대본 작성")
        st.markdown("---")
        
        # 장면별 입력을 저장할 딕셔너리 초기화
        if 'scene_inputs' not in st.session_state:
            st.session_state.scene_inputs = {}
        
        # 장면 수만큼 반복하여 입력 칸 생성
        for scene_num in range(1, inputs['scene_count'] + 1):
            st.markdown(f"#### 🎬 장면 {scene_num}")
            
            # 무대 입력
            stage_key = f"stage_{scene_num}"
            stage_placeholder = f"예: 교실, 숲 속"
            stage_input = st.text_input(
                f"무대 설정 (장면 {scene_num})",
                value=st.session_state.scene_inputs.get(stage_key, ""),
                placeholder=stage_placeholder,
                help=f"시간, 공간적 배경에 맞는 해당 장면의 무대를 입력해주세요.",
                key=f"stage_input_{scene_num}"
            )
            
            # 대본 입력
            script_key = f"script_{scene_num}"
            script_input = st.text_area(
                f"대본 내용 (장면 {scene_num})",
                value=st.session_state.scene_inputs.get(script_key, ""),
                placeholder=f"장면 {scene_num}의 대본을 입력해주세요...",
                height=150,
                help=f"장면 {scene_num}의 대사와 행동을 포함한 대본을 작성해주세요.",
                key=f"script_input_{scene_num}"
            )
            
            # 입력값을 세션에 저장
            st.session_state.scene_inputs[stage_key] = stage_input
            st.session_state.scene_inputs[script_key] = script_input
            
            st.markdown("---")
        
        # AI 피드백 받기 버튼
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # 모든 장면의 무대와 대본이 입력되었는지 확인
            all_inputs_filled = True
            missing_inputs = []
            
            for scene_num in range(1, inputs['scene_count'] + 1):
                stage_key = f"stage_{scene_num}"
                script_key = f"script_{scene_num}"
                
                if not st.session_state.scene_inputs.get(stage_key, "").strip():
                    all_inputs_filled = False
                    missing_inputs.append(f"장면 {scene_num} 무대")
                
                if not st.session_state.scene_inputs.get(script_key, "").strip():
                    all_inputs_filled = False
                    missing_inputs.append(f"장면 {scene_num} 대본")
            
            if all_inputs_filled:
                if st.button("🤖 AI 피드백 받기", key="get_feedback", 
                            help="AI가 현재 시나리오에 대한 피드백을 제공합니다",
                            use_container_width=True):
                    
                    st.success("🤖 AI가 피드백을 생성하고 있습니다...")
                    
                    # 프롬프트 파일 읽기
                    try:
                        with open(get_file_path("프롬프트/2.이야기 숲.txt"), "r", encoding="utf-8") as prompt_file:
                            prompt_template = prompt_file.read()
                        
                        # 연극 기본 정보를 프롬프트에 추가
                        basic_info = f"""
# 기본 설정
등장인물: {inputs['character_names']}
연극 장르: {inputs['genre']}
연극 주제: {inputs['theme']}
시간적 배경: {inputs['time_background']}
공간적 배경: {inputs['space_background']}
공연 시간: {inputs['performance_time']}분
장면 수: {inputs['scene_count']}개
이야기 흐름: {inputs['story_flow']}
"""
                        
                        # 장면별 대본 정보를 프롬프트에 추가
                        scene_scripts = ""
                        for scene_num in range(1, inputs['scene_count'] + 1):
                            stage_key = f"stage_{scene_num}"
                            script_key = f"script_{scene_num}"
                            stage = st.session_state.scene_inputs.get(stage_key, "")
                            script = st.session_state.scene_inputs.get(script_key, "")
                            scene_scripts += f"\n장면 {scene_num}:\n무대: {stage}\n대본: {script}\n"
                        
                        # 프롬프트에 입력값 치환
                        prompt = prompt_template.format(
                            character_names=inputs['character_names'],
                            genre=inputs['genre'],
                            time_background=inputs['time_background'],
                            space_background=inputs['space_background'],
                            performance_time=inputs['performance_time'],
                            scene_count=inputs['scene_count'],
                            theme=inputs['theme'],
                            story_flow=inputs['story_flow']
                        )
                        
                        # 연극 기본 정보와 장면별 대본 정보를 프롬프트에 추가
                        prompt += basic_info + f"\n\n# 입력\n{scene_scripts}"
                        
                        # OpenAI API를 사용하여 피드백 생성
                        with st.spinner("🤖 AI가 피드백을 생성하고 있습니다..."):
                            generated_feedback = generate_play_scenario(prompt)
                        
                        # 생성된 피드백을 세션 상태에 저장
                        st.session_state.generated_feedback = generated_feedback
                        
                        # 피드백 횟수 증가
                        if 'feedback_count' not in st.session_state:
                            st.session_state.feedback_count = 0
                        st.session_state.feedback_count += 1
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"프롬프트 파일을 불러올 수 없습니다: {str(e)}")
            else:
                # 경고 메시지 표시
                st.warning("⚠️ 모든 장면의 무대와 대본을 입력해주세요!")
                st.info(f"아직 입력되지 않은 항목: {', '.join(missing_inputs)}")
                
                # 비활성화된 AI 피드백 버튼
                st.button("🤖 AI 피드백 받기", key="get_feedback_disabled", 
                         help="모든 장면의 무대와 대본을 입력해야 합니다",
                         use_container_width=True, disabled=True)
        
        # 생성된 피드백 표시
        if 'generated_feedback' in st.session_state:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 💬 AI 피드백")
            st.markdown("---")
            st.markdown(st.session_state.generated_feedback)
            
            # 피드백을 바탕으로 대본 수정 안내
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background-color: #f0f8ff; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: #2E86AB; margin-bottom: 0.5rem;">📝 대본 수정 안내</h4>
                <p style="color: #666; margin: 0;">
                    위의 AI 피드백을 바탕으로 <strong>장면별 대본 작성</strong> 섹션에서 대본을 수정해보세요.<br>
                    수정 후 다시 AI 피드백을 받을 수 있습니다.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 다음 마을로 이동 버튼 (피드백을 최소 1번 받았을 때만 표시)
            if st.session_state.get('feedback_count', 0) > 0:
                st.markdown("<br><br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🌲 다음 마을로", key="next_village", 
                                help="준비의 광장으로 이동합니다",
                                use_container_width=True):
                        st.session_state.current_page = "prepare_page"
                        st.rerun()
            else:
                st.info("💡 AI 피드백을 최소 1번 받은 후 다음 마을로 이동할 수 있습니다.")
    
    else:
        st.warning("⚠️ 이전 마을에서 입력한 정보를 찾을 수 없습니다.")
        st.info("시작의 마을에서 연극 정보를 먼저 입력해주세요.")
        
        # 홈으로 돌아가기 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏠 홈으로 돌아가기", key="go_home", 
                        help="홈 페이지로 돌아갑니다",
                        use_container_width=True):
                st.session_state.current_page = "intro"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
