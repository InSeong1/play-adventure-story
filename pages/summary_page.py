import streamlit as st
import streamlit.components.v1 as components
from utils import play_bgm, get_file_path, get_base64_image, render_common_menu
import os

def summary_page():
    """활동 요약 페이지"""
    # 추억의 언덕 뱃지 획득 (5번째 마을 클리어)
    if 'cleared_villages' not in st.session_state:
        st.session_state.cleared_villages = []
    
    if 5 not in st.session_state.cleared_villages:
        st.session_state.cleared_villages.append(5)
        st.session_state.badge_updated = True
    
    # 페이지 상단으로 스크롤
    js = '''
    <script>
        var body = window.parent.document.querySelector(".main");
        if (body) {
            body.scrollTop = 0;
        }
    </script>
    '''
    components.html(js, height=0)
    
    # BGM 재생 - 시상식 BGM
    bgm_path = get_file_path("브금 모음/시상식.mp3")
    play_bgm(bgm_path)
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 시상식 상 이미지
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1 style="color: #2E86AB; font-weight: bold; margin-bottom: 2rem;">🏆 연극 대모험 완주 축하합니다!</h1>
        <p style="color: #666; font-size: 1.2rem; margin-bottom: 3rem;">
            연극 대모험 여정을 돌아보는 시간입니다.
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
    
    # 활동 내용 요약 섹션
    st.markdown("<br><br><br>", unsafe_allow_html=True)
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
    
    # 마무리 메시지
    st.markdown("<br><br><br>", unsafe_allow_html=True)
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
    
    st.markdown('</div>', unsafe_allow_html=True)
