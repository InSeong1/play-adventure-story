import streamlit as st
import streamlit.components.v1 as components
from utils import get_file_path, get_base64_image, render_common_menu



def summary_page():
    """활동 요약 페이지"""
    
    
    
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # # 인쇄 버튼 (페이지 상단)
    # st.markdown("""
    # <div style="text-align: center; margin-bottom: 2rem;">
    #     <button onclick="window.print()" style="
    #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    #         color: white;
    #         border: none;
    #         padding: 12px 24px;
    #         border-radius: 25px;
    #         font-size: 16px;
    #         font-weight: bold;
    #         cursor: pointer;
    #         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    #         transition: all 0.3s ease;
    #     " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(102, 126, 234, 0.6)'" 
    #        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(102, 126, 234, 0.4)'">
    #         완주 증서
    #     </button>
    # </div>
    # """, unsafe_allow_html=True)
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content" id="summary-page-top">', unsafe_allow_html=True)
    
    # 시상식 상 이미지
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1 style="color: #2E86AB; font-weight: bold; margin-bottom: 2rem;">🏆 연극 대모험 완주 축하합니다!</h1>
        <p style="color: #666; font-size: 1.2rem; margin-bottom: 3rem;">
            연극 대모험 여정을 돌아보는 시간입니다.<br>
            스크롤을 아래로 내리면서 연극 대모험의 여정을 돌아보아요! <br>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 시상식 상 이미지
    award_image_path = get_file_path("사진 모음/시상식 상.png")
    award_image = get_base64_image(award_image_path)
    
    if award_image:
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <img src="data:image/png;base64,{award_image}" alt="시상식 상" 
                 style="max-width: 80%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("시상식 상 이미지를 불러올 수 없습니다.")
    
    # 마무리 편지 이미지
    st.markdown("<br><br>", unsafe_allow_html=True)
    letter_image_path = get_file_path("사진 모음/마무리 편지.png")
    letter_image = get_base64_image(letter_image_path)
    
    if letter_image:
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <img src="data:image/png;base64,{letter_image}" alt="마무리 편지" 
                 style="max-width: 80%; height: auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("마무리 편지 이미지를 불러올 수 없습니다.")
    

    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 2rem;">📚 나의 연극 대모험 여정</h2>
        <p style="color: #666; font-size: 1.1rem;">
            아래로 스크롤하여 여정의 모든 순간을 돌아보세요
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. 시작의 마을 - 입력 내용
    st.markdown("---")
    st.markdown("### 🏠 시작의 마을 - 나의 입력")
    
    if 'village_inputs' in st.session_state:
        village_data = st.session_state.village_inputs
        st.markdown("**📝 입력한 내용들:**")
        
        # 시작의 마을 입력 항목들
        village_items = [
            ("연극의 주제", "theme"),
            ("등장인물 수", "character_count"),
            ("등장인물 이름들", "character_names"),
            ("장르", "genre"),
            ("시간적 배경", "time_background"),
            ("공간적 배경", "space_background"),
            ("공연 시간", "performance_time"),
            ("장면 수", "scene_count"),
            ("이야기 흐름", "story_flow")
        ]
        
        for display_name, key in village_items:
            if key in village_data and village_data[key]:
                if key == "character_names" and isinstance(village_data[key], list):
                    names_str = ", ".join(village_data[key])
                    st.markdown(f"**{display_name}:** {names_str}")
                else:
                    st.markdown(f"**{display_name}:** {village_data[key]}")
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("시작의 마을에서 입력한 내용이 없습니다.")
    
    # 2. 이야기 숲 - 대본 작성
    st.markdown("---")
    st.markdown("### 🌲 이야기 숲 - 나의 대본")
    
    # 장면별 대본이 있으면 표시
    if 'scene_inputs' in st.session_state and st.session_state.scene_inputs:
        st.markdown("**📝 장면별 대본:**")
        
        # 장면 수 계산 (village_inputs에서 가져오기)
        scene_count = 0
        if 'village_inputs' in st.session_state and 'scene_count' in st.session_state.village_inputs:
            scene_count = st.session_state.village_inputs['scene_count']
        
        if scene_count > 0:
            for scene_num in range(1, scene_count + 1):
                stage_key = f"stage_{scene_num}"
                script_key = f"script_{scene_num}"
                
                stage = st.session_state.scene_inputs.get(stage_key, "")
                script = st.session_state.scene_inputs.get(script_key, "")
                
                if stage.strip() or script.strip():
                    st.markdown(f"**🎬 장면 {scene_num}:**")
                    if stage.strip():
                        st.markdown(f"**무대:** {stage}")
                    if script.strip():
                        st.markdown(f"**대본:** {script.replace(chr(10), chr(10) + chr(10))}")
                    st.markdown("---")
        else:
            st.info("장면 수 정보를 찾을 수 없습니다.")
    else:
        st.info("이야기 숲에서 작성한 대본이 없습니다.")
    
    # AI 피드백이 있으면 표시
    if 'generated_feedback' in st.session_state and st.session_state.generated_feedback.strip():
        st.markdown("**🤖 AI 피드백:**")
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #007bff; color: #333;">
            {st.session_state.generated_feedback.replace(chr(10), chr(10) + chr(10))}
        </div>
        """, unsafe_allow_html=True)
    
    # 3. 준비의 광장 - 체크리스트
    st.markdown("---")
    st.markdown("### 🎭 준비의 광장 - 연극 준비 체크리스트")
    
    if 'prepare_checklist' in st.session_state:
        st.markdown("**✅ 준비 완료 항목들:**")
        checklist_data = st.session_state.prepare_checklist
        
        # 체크리스트 항목들 표시
        checklist_items = [
            "연극의 주제와 내용을 이해했다",
            "내가 맡은 역할을 명확히 알고 있다",
            "대사를 외웠다",
            "소품과 의상을 준비했다",
            "무대에서의 위치와 동선을 연습했다",
            "음악과 조명을 확인했다",
            "친구들과 함께 연습했다"
        ]
        
        for i, item in enumerate(checklist_items):
            yes_key = f"yes_{i}"
            no_key = f"no_{i}"
            
            if checklist_data.get(yes_key, False):
                st.markdown(f"✅ {item}")
            elif checklist_data.get(no_key, False):
                st.markdown(f"❌ {item}")
            else:
                st.markdown(f"⭕ {item}")
    else:
        st.info("준비의 광장에서 체크한 항목이 없습니다.")
    
    # 4. 환호의 극장 - 공연 체크리스트
    st.markdown("---")
    st.markdown("### 🎪 환호의 극장 - 공연 체크리스트")
    
    if 'performance_checklist' in st.session_state:
        st.markdown("**🎭 공연자 체크리스트:**")
        performance_data = st.session_state.performance_checklist
        
        performer_items = [
            "대사를 또박또박 자연스럽게 말했다",
            "인물의 마음을 생각하며 대사를 자연스럽게 말했다",
            "표정과 몸짓으로 인물의 감정과 상황을 잘 나타냈다",
            "소품·의상·음악을 장면에 맞게 준비하고 활용했다",
            "연극을 준비하고 공연하는 동안 친구들과 잘 협력했다"
        ]
        
        for i, item in enumerate(performer_items):
            yes_key = f"performer_yes_{i}"
            no_key = f"performer_no_{i}"
            
            if performance_data.get(yes_key, False):
                st.markdown(f"✅ {item}")
            elif performance_data.get(no_key, False):
                st.markdown(f"❌ {item}")
            else:
                st.markdown(f"⭕ {item}")
        
        st.markdown("**👥 관람자 체크리스트:**")
        audience_items = [
            "공연을 끝까지 집중해서 보았다",
            "공연 중에 박수·웃음·호응을 예의 바르게 했다",
            "무대에 오른 친구들의 연기를 존중하며 방해하지 않았다",
            "연극의 주제가 무엇인지 생각하며 공연을 보았다",
            "공연이 끝난 후, 잘한 점이나 인상 깊었던 부분을 구체적으로 말할 수 있다"
        ]
        
        for i, item in enumerate(audience_items):
            yes_key = f"audience_yes_{i}"
            no_key = f"audience_no_{i}"
            
            if performance_data.get(yes_key, False):
                st.markdown(f"✅ {item}")
            elif performance_data.get(no_key, False):
                st.markdown(f"❌ {item}")
            else:
                st.markdown(f"⭕ {item}")
    else:
        st.info("환호의 극장에서 체크한 항목이 없습니다.")
    
    # 5. 추억의 언덕 - 나만의 상
    st.markdown("---")
    st.markdown("### 🌅 추억의 언덕 - 나만의 특별한 상")
    
    if 'generated_award' in st.session_state:
        st.markdown("**🏆 AI가 주는 특별한 상:**")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
            <div style="white-space: pre-line; font-size: 1.1rem; line-height: 1.6;">
                {st.session_state.generated_award.replace('**', '').replace('*', '').replace(chr(10), chr(10) + chr(10))}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("추억의 언덕에서 받은 상이 없습니다.")
    
    # 6. 답변 내용들
    st.markdown("---")
    st.markdown("### 💭 나의 생각과 느낌")
    
    if 'memory_answers' in st.session_state:
        questions = [
            "이번 연극 준비나 공연에서 내가 가장 잘했다고 생각하는 것은 무엇인가요?",
            "다음에 연극을 한다면 고치거나 더 연습하고 싶은 부분은 무엇인가요?",
            "연극을 하면서 가장 기억에 남는 순간은 언제였나요?",
            "이번 연극을 통해 내가 새롭게 배우거나 더 잘하게 된 것은 무엇인가요?",
            "연극대모험 여정을 하면서 느낀 점과 생각을 적어 보세요."
        ]
        
        for i, question in enumerate(questions):
            answer = st.session_state.memory_answers.get(f"answer_{i}", "")
            if answer.strip():
                st.markdown(f"**질문 {i+1}:** {question}")
                st.markdown(f"**답변:** {answer.replace(chr(10), chr(10) + chr(10))}")
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("추억의 언덕에서 작성한 답변이 없습니다.")
    

    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; color: white; margin: 2rem 0;">
        <h2 style="color: white; margin-bottom: 1rem;">🎉 축하합니다!</h2>
        <p style="font-size: 1.2rem; line-height: 1.6;">
            연극 대모험을 성공적으로 완주했습니다!<br>
            이번 경험을 통해 연극의 즐거움과 협력의 중요성을 배웠을 것입니다.<br>
            앞으로도 더 많은 연극 활동을 통해 꿈을 키워나가세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 간단한 인쇄 안내
    st.markdown("""
    <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 15px; border-left: 4px solid #2E86AB; margin: 2rem 0;">
        <h4 style="color: #2E86AB; margin-bottom: 1rem;">💡 PDF 저장 팁</h4>
        
        <div style="margin-bottom: 1rem;">
            <h5 style="color: #1976D2; margin-bottom: 0.5rem;">🖥️ PC에서:</h5>
            <p style="margin-bottom: 0.5rem; color: #333;"><strong>위의 버튼을 클릭하거나</strong> <kbd style="background: #f0f0f0; color: #333; padding: 2px 6px; border-radius: 3px;">Ctrl</kbd> + <kbd style="background: #f0f0f0; color: #333; padding: 2px 6px; border-radius: 3px;">P</kbd> (Windows/Linux) 또는 <kbd style="background: #f0f0f0; color: #333; padding: 2px 6px; border-radius: 3px;">Cmd</kbd> + <kbd style="background: #f0f0f0; color: #333; padding: 2px 6px; border-radius: 3px;">P</kbd> (Mac)을 눌러주세요!</p>
            <p style="margin-bottom: 0; color: #333;"><strong>인쇄 창에서:</strong> 대상을 "PDF로 저장"으로 변경하고, "배경 그래픽" 옵션을 체크하면 색상과 이미지가 포함된 완벽한 PDF를 만들 수 있습니다.</p>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <h5 style="color: #1976D2; margin-bottom: 0.5rem;">📱 태블릿에서:</h5>
            <p style="margin-bottom: 0.5rem; color: #333;"><strong>iPad:</strong> 화면을 길게 누르고 "공유" → "PDF로 저장" 또는 Safari에서 <kbd style="background: #f0f0f0; color: #333; padding: 2px 6px; border-radius: 3px;">Cmd</kbd> + <kbd style="background: #f0f0f0; color: #333; padding: 2px 6px; border-radius: 3px;">P</kbd> → "PDF로 저장"</p>
            <p style="margin-bottom: 0.5rem; color: #333;"><strong>Android 태블릿:</strong> Chrome에서 ⋮ 메뉴 → "공유" → "인쇄" → "PDF로 저장" 또는 화면 캡처 후 "PDF로 변환" 앱 사용</p>
            <p style="margin-bottom: 0; color: #333;"><strong>공통:</strong> 브라우저 설정에서 "데스크톱 모드"로 전환하면 PC와 동일한 방법으로 PDF 저장이 가능합니다!</p>
        </div>
        
        <p style="margin-bottom: 0; color: #666; font-size: 0.9rem; font-style: italic;">💡 왼쪽 메뉴 바를 닫고 저장을 시도해서 pdf 파일로 증서를 얻어볼까요?</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
