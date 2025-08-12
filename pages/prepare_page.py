import streamlit as st
from utils import play_bgm, get_file_path, get_base64_image, render_common_menu, clear_village
import os

def prepare_page():
    """준비의 광장 페이지"""
    # 이야기 숲 뱃지 획득 (2번째 마을 클리어)
    if 'cleared_villages' not in st.session_state:
        st.session_state.cleared_villages = []
    
    if 2 not in st.session_state.cleared_villages:
        st.session_state.cleared_villages.append(2)
        st.session_state.badge_updated = True
    
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
    
    # BGM 재생 - 준비의 광장 BGM
    bgm_path = get_file_path("브금 모음/3. 준비의 광장.mp3")
    play_bgm(bgm_path)
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 초대장 이미지를 적절한 크기로 표시 (배경이 아닌 일반 이미지)
    invitation_path = get_file_path("사진 모음/초대장/3_준비의 광장 초대장.png")
    invitation_image = get_base64_image(invitation_path)
    
    if invitation_image:
        # 이미지를 CSS 클래스를 사용하여 적절한 크기로 표시
        st.markdown(f"""
        <div class="image-container">
            <img src="data:image/png;base64,{invitation_image}" alt="준비의 광장 초대장">
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
                with open(get_file_path("나레이션 소리 모음/3.준비의 광장.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                
                # 나레이션 텍스트 내용 출력
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📖 초대장 내용:**")
                try:
                    with open(get_file_path("나레이션/3.준비의 광장.txt"), "r", encoding="utf-8") as text_file:
                        narration_text = text_file.read()
                        st.write(narration_text)
                except Exception as e:
                    st.error(f"나레이션 텍스트 파일을 불러올 수 없습니다: {str(e)}")
                
            except Exception as e:
                st.error(f"나레이션 파일을 불러올 수 없습니다: {str(e)}")
                st.write(f"파일 경로: 나레이션 소리 모음/3.준비의 광장.mp3")
    
    # 메인 콘텐츠
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    # 이야기 숲 뱃지 표시
    badge_path = get_file_path("뱃지 모음/2_뱃지_이야기숲.png")
    badge_image = get_base64_image(badge_path)
    
    if badge_image:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background-color: #f0f8ff; border-radius: 15px; 
                         box-shadow: 0 4px 15px rgba(46, 134, 171, 0.2); margin: 1rem 0;">
                <h3 style="color: #2E86AB; margin-bottom: 1rem;">🏆 이야기 숲 뱃지 획득!</h3>
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{badge_image}" 
                         style="max-width: 150px; height: auto; border-radius: 10px; 
                                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);" 
                         alt="이야기 숲 뱃지">
                </div>
                <p style="color: #666; font-size: 1rem; margin-top: 1rem; font-weight: bold;">
                    🎉 이야기 숲을 성공적으로 클리어했습니다!
                </p>
            </div>
            """.format(badge_image=badge_image), unsafe_allow_html=True)
    else:
        st.error("뱃지 이미지를 불러올 수 없습니다.")
    
    # 준비의 광장 제목
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">🎭 준비의 광장에 오신 것을 환영합니다!</h2>
        <p style="color: #666; font-size: 1.1rem;">이야기 숲에서 작성한 극본을 바탕으로 연극을 준비해보아요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 연극 공연 연습의 과정 이미지
    process_image_path = get_file_path("사진 모음/연극 공연 연습의 과정.png")
    process_image = get_base64_image(process_image_path)
    
    if process_image:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="image-container">
                <img src="data:image/png;base64,{process_image}" alt="연극 공연 연습의 과정" style="max-width: 100%; height: auto;">
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("연극 공연 연습의 과정 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {process_image_path}")
        st.write(f"파일 존재 여부: {os.path.exists(process_image_path)}")
    
    # 출처 표시
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; font-style: italic; margin-top: 1rem;">
        출처: 구민정·권재원(2012), 『학교에서 연극하자』, 다른.
    </div>
    """, unsafe_allow_html=True)
    
    # 최종 극본 표시 및 다운로드 섹션
    if 'scene_inputs' in st.session_state and st.session_state.scene_inputs:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 📖 최종 극본")
        st.markdown("---")
        
        # 극본 내용 구성 - village_inputs에서 기본 정보 가져오기
        final_script = ""
        
        # village_inputs에서 기본 정보 가져오기
        if 'village_inputs' in st.session_state:
            village_data = st.session_state.village_inputs
            final_script += f"**등장인물 수:** {village_data.get('character_count', '')}명\n\n"
            final_script += f"**등장인물:** {village_data.get('character_names', '')}\n\n"
            final_script += f"**장르:** {village_data.get('genre', '')}\n\n"
            final_script += f"**시간 배경:** {village_data.get('time_background', '')}\n\n"
            final_script += f"**공간 배경:** {village_data.get('space_background', '')}\n\n"
            final_script += f"**공연 시간:** {village_data.get('performance_time', '')}분\n\n"
            final_script += f"**장면 수:** {village_data.get('scene_count', '')}개\n\n"
            final_script += f"**주제:** {village_data.get('theme', '')}\n\n"
            final_script += f"**이야기 흐름:** {village_data.get('story_flow', '')}\n\n"
        
        # 장면별 대본 추가 (feedback_age에서 입력한 내용)
        # village_inputs에서 scene_count를 가져와서 사용
        scene_count = 0
        if 'village_inputs' in st.session_state and 'scene_count' in st.session_state.village_inputs:
            scene_count = st.session_state.village_inputs['scene_count']
        
        for scene_num in range(1, scene_count + 1):
            stage_key = f"stage_{scene_num}"
            script_key = f"script_{scene_num}"
            stage = st.session_state.scene_inputs.get(stage_key, "")
            script = st.session_state.scene_inputs.get(script_key, "")
            
            if stage or script:
                final_script += f"## 장면 {scene_num}\n\n"
                if stage:
                    final_script += f"**무대:** {stage}\n\n"
                if script:
                    # 대본의 줄바꿈 한 개를 줄바꿈 두 개로 변환하여 마크다운에서 제대로 줄 구분되도록 함
                    formatted_script = script.replace('\n', '\n\n')
                    final_script += f"**대본:**\n{formatted_script}\n\n"
        
        # AI 피드백이 있다면 추가
        if 'generated_feedback' in st.session_state:
            # AI 피드백의 줄바꿈 한 개를 줄바꿈 두 개로 변환
            formatted_feedback = st.session_state.generated_feedback.replace('\n', '\n\n')
            final_script += f"## AI 피드백\n\n{formatted_feedback}\n\n"
        
        # 극본 내용 표시
        st.markdown(final_script)
        
        # 장면별 대본 미리보기 (선택사항)
        if scene_count > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📖 장면별 대본 미리보기")
            st.markdown("---")
            
            for scene_num in range(1, scene_count + 1):
                stage_key = f"stage_{scene_num}"
                script_key = f"script_{scene_num}"
                stage = st.session_state.scene_inputs.get(stage_key, "")
                script = st.session_state.scene_inputs.get(script_key, "")
                
                if stage or script:
                    with st.expander(f"🎬 장면 {scene_num}", expanded=False):
                        if stage:
                            st.markdown(f"**무대:** {stage}")
                        if script:
                            # 대본의 줄바꿈 한 개를 줄바꿈 두 개로 변환
                            formatted_script = script.replace('\n', '\n\n')
                            st.markdown(f"**대본:**\n{formatted_script}")
        
        # 다운로드 버튼들
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # TXT 파일 다운로드 (극본만, AI 피드백 제외)
            txt_content = final_script
            st.download_button(
                label="📄 TXT 다운로드",
                data=txt_content,
                file_name="최종극본.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # 극본 복사하기
            st.button(
                label="📋 극본 복사",
                help="극본 내용을 클립보드에 복사합니다",
                use_container_width=True,
                on_click=lambda: st.write("극본이 클립보드에 복사되었습니다!")
            )
        
        st.markdown("---")
    
    # 체크리스트 섹션
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📋 연극 준비 체크리스트")
    st.markdown("---")
    
    # 체크리스트 상태 초기화
    if 'prepare_checklist' not in st.session_state:
        st.session_state.prepare_checklist = {}
    
    # 체크리스트 항목들
    checklist_items = [
        "내가 맡은 배역의 성격과 상황을 이해하고 있다.",
        "무대에 등장하고 퇴장하는 위치와 순서를 알고 있다.",
        "대사를 이야기 흐름에 맞춰 자연스럽게 말할 수 있다.",
        "공연할 장면의 시간과 장소(배경)를 알고 있다.",
        "무대의 동선을 알고, 다른 사람과 부딪히지 않도록 연습했다.",
        "장면에 필요한 소품·의상 또는 음악을 준비했다.",
        "장면에서 인물의 감정과 분위기를 잘 표현할 수 있도록 연습했다.",
        "모둠 친구들과 배역과 준비 역할을 고르게 나누었다.",
        "연출 일지에 의상·소품·음악·등장·퇴장 순서를 정리하고 공유했다.",
        "공연 전에 모둠원과 함께 전체 준비 내용을 점검했다."
    ]
    
    # 체크리스트 표시
    for i, item in enumerate(checklist_items):
        col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
        with col1:
            st.markdown(f"**{i+1}.** {item}")
        with col2:
            if st.checkbox("예", key=f"yes_{i}", value=st.session_state.prepare_checklist.get(f"yes_{i}", False)):
                st.session_state.prepare_checklist[f"yes_{i}"] = True
                st.session_state.prepare_checklist[f"no_{i}"] = False
        with col3:
            if st.checkbox("아니오", key=f"no_{i}", value=st.session_state.prepare_checklist.get(f"no_{i}", False)):
                st.session_state.prepare_checklist[f"no_{i}"] = True
                st.session_state.prepare_checklist[f"yes_{i}"] = False
    
    # 완료하기 버튼
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ 체크리스트 완료하기", key="complete_checklist", 
                    help="체크리스트를 완료하고 다음 마을로 이동할 수 있습니다",
                    use_container_width=True):
            
            # 체크리스트 완료 여부 확인
            all_completed = True
            incomplete_items = []
            
            for i in range(len(checklist_items)):
                yes_key = f"yes_{i}"
                no_key = f"no_{i}"
                
                if not st.session_state.prepare_checklist.get(yes_key, False) and not st.session_state.prepare_checklist.get(no_key, False):
                    all_completed = False
                    incomplete_items.append(f"{i+1}번 항목")
                elif st.session_state.prepare_checklist.get(no_key, False):
                    all_completed = False
                    incomplete_items.append(f"{i+1}번 항목 (아니오)")
            
            if all_completed:
                st.success("🎉 체크리스트가 완료되었습니다!")
                st.session_state.checklist_completed = True
                st.rerun()
            else:
                st.warning("💡 아직 준비가 안 된 것들이 있어요!")
                st.info(f"**{', '.join(incomplete_items)}** 같은 것들이 준비가 안되어 있으니 모두 준비하고 다음 마을로 가볼까요? 😊")
    
    # 체크리스트 완료 후 다음 마을로 이동 버튼
    if st.session_state.get('checklist_completed', False):
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌲 다음 마을로", key="next_village", 
                        help="환호의 극장으로 이동합니다",
                        use_container_width=True):
                st.session_state.current_page = "hwanho_page"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
