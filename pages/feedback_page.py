import streamlit as st
from io import BytesIO
from pydub import AudioSegment
from utils import get_file_path, get_base64_image, render_common_menu, generate_play_scenario, play_bgm
import os

def feedback_page():
    """피드백 페이지 (이야기 숲)"""
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 페이지 상단으로 스크롤 (dialog 닫힐 때 커서가 여기로 오도록)
    st.markdown('<div id="feedback-page-top"></div>', unsafe_allow_html=True)
    
    # 초대장 이미지 표시
    invitation_path = get_file_path("사진 모음/초대장/2_이야기 숲 초대장.png")
    invitation_image = get_base64_image(invitation_path)
    
    if invitation_image:
        # 오디오 플레이어들을 배치
        col1, col2, col3 = st.columns([1, 5, 1])
        
        # 배경음악 (첫 번째 컬럼) - 가장 먼저 렌더링
        with col1:
            st.markdown("🎵 배경음악 듣기", help="- 배경음악이 필요할 때는 재생해 보세요. 상황에 따라 재생 속도를 조절하거나 음소거 기능도 활용할 수 있어요!")
            try:
                with open(get_file_path("브금 모음/2. 이야기 숲.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"BGM 파일을 불러올 수 없습니다: {str(e)}")
        
        # 초대장 듣기 (마지막 컬럼)
        with col3:
            st.markdown("📜 초대장 듣기", help="- 이야기 숲에서 여러분을 신비롭게 초대하는 초대장을 읽어주는 친구의 목소리를 들어보세요! 여기서 어떤 특별한 모험을 할 수 있는지 알아볼 수 있어요.")
            try:
                with open(get_file_path("나레이션 소리 모음/2.이야기 숲.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3",autoplay=True)
            except Exception as e:
                st.error(f"초대장 파일을 불러올 수 없습니다: {str(e)}")
        
        # 공백 추가
        st.markdown("")
        st.markdown("")
        st.image(f"data:image/png;base64,{invitation_image}", width="stretch")
    else:
        st.error("초대장 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {invitation_path}")
        st.write(f"파일 존재 여부: {os.path.exists(invitation_path)}")

    
    # 입력 폼 제목
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">✏️ 극본 작성하기</h2>
        <p style="color: #666; font-size: 1.1rem;">이전 마을에서 입력한 정보를 확인하고 대본을 작성해 보아요. <br>왼쪽 메뉴 혹은 아래 그림에서 극본의 구성 요소를 확인해 보아요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 극본의 특성 이미지 표시
    script_characteristics_path = get_file_path("사진 모음/극본의 특성.png")
    script_characteristics_image = get_base64_image(script_characteristics_path)
    
    if script_characteristics_image:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image(f"data:image/png;base64,{script_characteristics_image}", width="stretch")
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
        st.markdown('<div id="장면별-대본-작성"></div>', unsafe_allow_html=True)
        
        # 제목과 외부 링크 버튼을 2열로 배치
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🎭 장면별 대본 작성")
        with col2:
            st.link_button("🐉 대본 작성에 도움이 필요하다면?", "https://play-adventure-sub.streamlit.app/", help="연극 용과 함께 대본 작성을 시작해 볼까요?")
        
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
                help=f"시간, 공간적 배경에 맞는 해당 장면의 무대를 입력해 주세요.",
                key=f"stage_input_{scene_num}"
            )
            
            # 대본 입력
            script_key = f"script_{scene_num}"
            script_input = st.text_area(
                f"대본 내용 (장면 {scene_num})",
                value=st.session_state.scene_inputs.get(script_key, ""),
                placeholder=f"장면 {scene_num}의 대본을 입력해 주세요...",
                height=150,
                help=f"장면 {scene_num}의 대사와 행동을 포함한 대본을 작성해 주세요.",
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
            validation_errors = []
            
            for scene_num in range(1, inputs['scene_count'] + 1):
                stage_key = f"stage_{scene_num}"
                script_key = f"script_{scene_num}"
                
                stage_content = st.session_state.scene_inputs.get(stage_key, "").strip()
                script_content = st.session_state.scene_inputs.get(script_key, "").strip()
                
                # 무대 설정 확인
                if not stage_content:
                    all_inputs_filled = False
                    missing_inputs.append(f"장면 {scene_num} 무대")
                elif len(stage_content) < 2:
                    all_inputs_filled = False
                    validation_errors.append(f"장면 {scene_num} 무대 설정이 너무 짧습니다.")
                
                # 대본 내용 확인
                if not script_content:
                    all_inputs_filled = False
                    missing_inputs.append(f"장면 {scene_num} 대본")
                elif len(script_content) < 15:
                    all_inputs_filled = False
                    validation_errors.append(f"장면 {scene_num} 대본 내용이 너무 짧습니다.")
            
            if all_inputs_filled and not validation_errors:
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
                if missing_inputs:
                    st.warning("⚠️ 모든 장면의 무대와 대본을 입력해 주세요!")
                    st.info(f"아직 입력되지 않은 항목: {', '.join(missing_inputs)}")
                
                if validation_errors:
                    st.error("⚠️ 입력 내용을 더 자세히 작성해 주세요:")
                    for error in validation_errors:
                        st.write(f"• {error}")
                
                # 비활성화된 AI 피드백 버튼
                st.button("🤖 AI 피드백 받기", key="get_feedback_disabled", 
                         help="모든 장면의 무대와 대본을 충분히 입력해야 합니다",
                         use_container_width=True, disabled=True)
        
        # 생성된 피드백 표시
        if 'generated_feedback' in st.session_state:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 💬 AI 피드백")
            st.markdown("**👍 표시는 잘한점, ✏ 표시는 고쳐야할 점 입니다.**")
            st.markdown("---")
            
            # AI 응답을 더 보기 좋게 포맷팅
            feedback_text = st.session_state.generated_feedback
            
            # 질문 부분을 헤더로 변환
            import re
            
            # 더 정확한 질문 패턴 찾기 (줄의 시작에서 시작하는 질문만)
            lines = feedback_text.split('\n')
            formatted_lines = []
            
            for line in lines:
                line = line.strip()
                # 줄의 시작이 질문인지 확인 (한글 + 물음표로 끝나는 문장)
                if line and line.endswith('?') and len(line) > 10:
                    # 질문을 HTML 헤더로 변환 (일관된 크기, 기본 색상 유지)
                    formatted_lines.append(f"<h4 style='margin: 1rem 0 0.5rem 0; font-size: 1.2rem;'>{line}</h4>")
                elif line.startswith("총평:"):
                    # 총평 부분을 헤더로 변환하고 나머지 내용도 포함
                    remaining_content = line[3:].strip()  # "총평:" 제거
                    if remaining_content:
                        formatted_lines.append(f"<h3 style='margin: 1.5rem 0 1rem 0; font-size: 1.4rem;'>총평</h3>")
                        formatted_lines.append(f"<p style='margin: 0.5rem 0;'>{remaining_content}</p>")
                    else:
                        formatted_lines.append(f"<h3 style='margin: 1.5rem 0 1rem 0; font-size: 1.4rem;'>총평</h3>")
                else:
                    formatted_lines.append(line)
            
            formatted_feedback = '\n'.join(formatted_lines)
            
            # HTML로 표시 (헤딩 크기 일관성 보장)
            st.markdown(formatted_feedback, unsafe_allow_html=True)
            
            # 피드백을 바탕으로 대본 수정 안내
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background-color: #f0f8ff; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: #2E86AB; margin-bottom: 0.5rem;">📝 대본 수정 안내</h4>
                <p style="color: #666; margin: 0;">
                    위의 AI 피드백을 바탕으로 <a href="#장면별-대본-작성" style="color: #2E86AB; text-decoration: none; font-weight: bold; cursor: pointer;">🎭 장면별 대본 작성</a> 에서 대본을 수정해 보세요.<br>
                    수정 후 다시 AI 피드백을 받을 수 있습니다.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 다음 마을로 이동 버튼 (피드백을 최소 1번 받았을 때만 표시)
            if st.session_state.get('feedback_count', 0) > 0:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🌲 다음 마을로", key="next_village", 
                                help="준비의 광장으로 이동합니다",
                                use_container_width=True):
                        # 다음 페이지 뱃지 설정 (이야기 숲 뱃지)
                        st.session_state.badge_image_filename = "2_뱃지_이야기숲.png"
                        st.session_state.show_badge_dialog = True
                        st.session_state.current_page = "prepare_page"
                        st.rerun()
            else:
                st.info("💡 AI 피드백을 최소 1번 받은 후 다음 마을로 이동할 수 있습니다.")
    
    else:
        st.warning("⚠️ 이전 마을에서 입력한 정보를 찾을 수 없습니다.")
        st.info("시작의 마을에서 연극 정보를 먼저 입력해 주세요.")
        
        # 홈으로 돌아가기 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏠 홈으로 돌아가기", key="go_home", 
                        help="홈 페이지로 돌아갑니다",
                        use_container_width=True):
                st.session_state.current_page = "intro"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

