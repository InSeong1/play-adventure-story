import streamlit as st
from utils import get_file_path, get_base64_image, render_common_menu
import os

def hwanho_page():
    """환호의 극장 페이지"""
    
    
    
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 초대장 이미지를 적절한 크기로 표시 (배경이 아닌 일반 이미지)
    invitation_path = get_file_path("사진 모음/초대장/4_환호의 극장 초대장.png")
    invitation_image = get_base64_image(invitation_path)
    
    if invitation_image:
        # 이미지를 CSS 클래스를 사용하여 적절한 크기로 표시
        st.markdown(f"""
        <div class="image-container">
            <img src="data:image/png;base64,{invitation_image}" alt="환호의 극장 초대장">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("초대장 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {invitation_path}")
        st.write(f"파일 존재 여부: {os.path.exists(invitation_path)}")
    
    st.markdown('<div id="초대장-듣기-버튼"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📜 초대장 듣기", key="listen_invitation_hwanho", 
                    help="클릭하여 초대장 나레이션을 보이기/숨기기",
                    use_container_width=True):
            st.session_state["show_narration_hwanho"] = not st.session_state.get("show_narration_hwanho", False)
            st.rerun()
    
    # 나레이션 오디오 플레이어 (버튼 클릭 시 표시)
    if st.session_state.get('show_narration_hwanho', False):
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("**🎧 초대장 듣기**")
            # 나레이션 오디오 파일 재생 (BGM과 함께)
            try:
                with open(get_file_path("나레이션 소리 모음/4.환호의 극장.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                
                # 나레이션 텍스트 내용 출력
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📖 초대장 듣기:**")
                try:
                    with open(get_file_path("나레이션/4.환호의 극장.txt"), "r", encoding="utf-8") as text_file:
                        narration_text = text_file.read()
                        st.write(narration_text)
                except Exception as e:
                    st.error(f"나레이션 텍스트 파일을 불러올 수 없습니다: {str(e)}")
                
            except Exception as e:
                st.error(f"나레이션 파일을 불러올 수 없습니다: {str(e)}")
                st.write(f"파일 경로: 나레이션 소리 모음/4.환호의 극장.mp3")
    
    
    # 환호의 극장 제목
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">🎭 환호의 극장에 오신 것을 환영합니다!</h2>
        <p style="color: #666; font-size: 1.1rem;">준비의 광장에서 연습한 연극을 공연해보아요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 연극 공연 예절 이미지
    etiquette_image_path = get_file_path("사진 모음/연극 공연 예절.png")
    etiquette_image = get_base64_image(etiquette_image_path)
    
    if etiquette_image:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="image-container">
                <img src="data:image/png;base64,{etiquette_image}" alt="연극 공연 예절" style="max-width: 100%; height: auto;">
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("연극 공연 예절 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {etiquette_image_path}")
        st.write(f"파일 존재 여부: {os.path.exists(etiquette_image_path)}")
    
    # 체크리스트 섹션

    st.markdown("### 📋 연극 공연 체크리스트")
    st.markdown("---")
    
    # 체크리스트 상태 초기화
    if 'performance_checklist' not in st.session_state:
        st.session_state.performance_checklist = {}
    
    # 공연자 체크리스트
    st.markdown("#### 🎭 공연자")
    performer_items = [
        "내가 맡은 역할에 맞게 무대에 나가고 들어오는 순서를 잘 지켰다.",
        "인물의 마음을 생각하며 대사를 자연스럽게 말했다.",
        "표정과 몸짓으로 인물의 감정과 상황을 잘 나타냈다.",
        "소품·의상·음악을 장면에 맞게 준비하고 활용했다.",
        "연극을 준비하고 공연하는 동안 친구들과 잘 협력했다."
    ]
    
    for i, item in enumerate(performer_items):
        col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
        with col1:
            st.markdown(f"**{i+1}.** {item}")
        with col2:
            # 예 체크박스 - 현재 상태 확인
            yes_current = st.session_state.performance_checklist.get(f"performer_yes_{i}", False)
            yes_checked = st.checkbox("예", key=f"performer_yes_{i}", value=yes_current)
            
            # 예가 체크되면 아니오 해제
            if yes_checked and not yes_current:
                st.session_state.performance_checklist[f"performer_yes_{i}"] = True
                st.session_state.performance_checklist[f"performer_no_{i}"] = False
                st.rerun()
            elif not yes_checked and yes_current:
                st.session_state.performance_checklist[f"performer_yes_{i}"] = False
                
        with col3:
            # 아니오 체크박스 - 현재 상태 확인
            no_current = st.session_state.performance_checklist.get(f"performer_no_{i}", False)
            no_checked = st.checkbox("아니오", key=f"performer_no_{i}", value=no_current)
            
            # 아니오가 체크되면 예 해제
            if no_checked and not no_current:
                st.session_state.performance_checklist[f"performer_no_{i}"] = True
                st.session_state.performance_checklist[f"performer_yes_{i}"] = False
                st.rerun()
            elif not no_checked and no_current:
                st.session_state.performance_checklist[f"performer_no_{i}"] = False
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 관람자 체크리스트
    st.markdown("#### 👥 관람자")
    audience_items = [
        "공연을 끝까지 집중해서 보았다.",
        "공연 중에 박수·웃음·호응을 예의 바르게 했다.",
        "무대에 오른 친구들의 연기를 존중하며 방해하지 않았다.",
        "연극의 주제가 무엇인지 생각하며 공연을 보았다.",
        "공연이 끝난 후, 잘한 점이나 인상 깊었던 부분을 구체적으로 말할 수 있다."
    ]
    
    for i, item in enumerate(audience_items):
        col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
        with col1:
            st.markdown(f"**{i+1}.** {item}")
        with col2:
            # 예 체크박스 - 현재 상태 확인
            yes_current = st.session_state.performance_checklist.get(f"audience_yes_{i}", False)
            yes_checked = st.checkbox("예", key=f"audience_yes_{i}", value=yes_current)
            
            # 예가 체크되면 아니오 해제
            if yes_checked and not yes_current:
                st.session_state.performance_checklist[f"audience_yes_{i}"] = True
                st.session_state.performance_checklist[f"audience_no_{i}"] = False
                st.rerun()
            elif not yes_checked and yes_current:
                st.session_state.performance_checklist[f"audience_yes_{i}"] = False
                
        with col3:
            # 아니오 체크박스 - 현재 상태 확인
            no_current = st.session_state.performance_checklist.get(f"audience_no_{i}", False)
            no_checked = st.checkbox("아니오", key=f"audience_no_{i}", value=no_current)
            
            # 아니오가 체크되면 예 해제
            if no_checked and not no_current:
                st.session_state.performance_checklist[f"audience_no_{i}"] = True
                st.session_state.performance_checklist[f"audience_yes_{i}"] = False
                st.rerun()
            elif not no_checked and no_current:
                st.session_state.performance_checklist[f"audience_no_{i}"] = False
    
    # 완료하기 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ 체크리스트 완료하기", key="complete_performance_checklist", 
                    help="체크리스트를 완료하고 다음 마을로 이동할 수 있습니다",
                    use_container_width=True):
            
            # 체크리스트 완료 여부 확인
            all_completed = True
            incomplete_items = []
            
            # 공연자 체크리스트 확인
            for i in range(len(performer_items)):
                yes_key = f"performer_yes_{i}"
                no_key = f"performer_no_{i}"
                
                if not st.session_state.performance_checklist.get(yes_key, False) and not st.session_state.performance_checklist.get(no_key, False):
                    all_completed = False
                    incomplete_items.append(f"공연자 {i+1}번 항목")
                elif st.session_state.performance_checklist.get(no_key, False):
                    all_completed = False
                    incomplete_items.append(f"공연자 {i+1}번 항목 (아니오)")
            
            # 관람자 체크리스트 확인
            for i in range(len(audience_items)):
                yes_key = f"audience_yes_{i}"
                no_key = f"audience_no_{i}"
                
                if not st.session_state.performance_checklist.get(yes_key, False) and not st.session_state.performance_checklist.get(no_key, False):
                    all_completed = False
                    incomplete_items.append(f"관람자 {i+1}번 항목")
                elif st.session_state.performance_checklist.get(no_key, False):
                    all_completed = False
                    incomplete_items.append(f"관람자 {i+1}번 항목 (아니오)")
            
            if all_completed:
                st.success("🎉 체크리스트가 완료되었습니다!")
                st.session_state.performance_checklist_completed = True
                st.rerun()
            else:
                st.warning("💡 아직 준비가 안 된 것들이 있어요!")
                st.info(f"**{', '.join(incomplete_items)}** 같은 것들이 준비가 안되어 있으니 모두 준비하고 다음 마을로 가볼까요? 😊")
    
    # 체크리스트 완료 후 다음 마을로 이동 버튼
    if st.session_state.get('performance_checklist_completed', False):
        st.success("✅ 연극 공연 체크리스트가 완료되었습니다!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌲 다음 마을로", key="next_village", 
                        help="다음 마을로 이동합니다",
                        use_container_width=True):
                # 다음 페이지 뱃지 설정 (환호의 극장 뱃지)
                st.session_state.badge_image_filename = "4_뱃지_환호의 극장.png"
                st.session_state.show_badge_dialog = True
                st.session_state.current_page = "memory_page"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 페이지 상단으로 스크롤 (모든 콘텐츠 로드 후 실행)
    import streamlit.components.v1 as components
    
    def scroll_to_top():
        components.html("""
        <script>
            // 모든 콘텐츠가 로드된 후 스크롤 실행
            setTimeout(function() {
                window.parent.scrollTo(0, 0);
                window.parent.scrollTo(0, -1000);
            }, 1000);
            
            setTimeout(function() {
                window.parent.scrollTo(0, 0);
                window.parent.scrollTo(0, -1000);
            }, 2000);
        </script>
        """, height=0)
    
    scroll_to_top()
