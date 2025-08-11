import streamlit as st
from utils import play_bgm, get_file_path, get_base64_image, render_common_menu
import os
import openai

def memory_page():
    """추억의 언덕 페이지"""
    # 추억의 언덕 뱃지 획득 (4번째 마을 클리어)
    if 'cleared_villages' not in st.session_state:
        st.session_state.cleared_villages = []
    
    if 4 not in st.session_state.cleared_villages:
        st.session_state.cleared_villages.append(4)
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
    
    # BGM 재생 - 추억의 언덕 BGM
    bgm_path = get_file_path("브금 모음/5. 추억의 언덕.mp3")
    play_bgm(bgm_path)
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 초대장 이미지를 적절한 크기로 표시
    invitation_path = get_file_path("사진 모음/초대장/5_추억의 언덕 초대장.png")
    invitation_image = get_base64_image(invitation_path)
    
    if invitation_image:
        # 이미지를 CSS 클래스를 사용하여 적절한 크기로 표시
        st.markdown(f"""
        <div class="image-container">
            <img src="data:image/png;base64,{invitation_image}" alt="추억의 언덕 초대장">
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
                with open(get_file_path("나레이션 소리 모음/5.추억의 언덕.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                
                # 나레이션 텍스트 내용 출력
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📖 초대장 듣기:**")
                try:
                    with open(get_file_path("나레이션/5.추억의 언덕.txt"), "r", encoding="utf-8") as text_file:
                        narration_text = text_file.read()
                        st.write(narration_text)
                except Exception as e:
                    st.error(f"나레이션 텍스트 파일을 불러올 수 없습니다: {str(e)}")
                
            except Exception as e:
                st.error(f"나레이션 파일을 불러올 수 없습니다: {str(e)}")
                st.write(f"파일 경로: 나레이션 소리 모음/5. 추억의 언덕.mp3")
    
    # 메인 콘텐츠
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    # 추억의 언덕 제목
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">🌅 추억의 언덕에 오신 것을 환영합니다!</h2>
        <p style="color: #666; font-size: 1.1rem; margin-bottom: 2rem;">
            연극 대모험을 통해 얻은 소중한 경험과 추억을 돌아보는 시간입니다.<br>
            아래 질문들에 답해보며 나만의 특별한 상을 받아보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 질문과 답변 입력 폼
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 질문 리스트
    questions = [
        "이번 연극 준비나 공연에서 내가 가장 잘했다고 생각하는 것은 무엇인가요?",
        "다음에 연극을 한다면 고치거나 더 연습하고 싶은 부분은 무엇인가요?",
        "연극을 하면서 가장 기억에 남는 순간은 언제였나요?",
        "이번 연극을 통해 내가 새롭게 배우거나 더 잘하게 된 것은 무엇인가요?",
        "연극대모험 여정을 하면서 느낀 점과 생각을 적어 보세요."
    ]
    
    # 답변을 저장할 딕셔너리 초기화
    if 'memory_answers' not in st.session_state:
        st.session_state.memory_answers = {}
    
    # 각 질문에 대한 답변 입력
    for i, question in enumerate(questions):
        st.markdown(f"**{i+1}. {question}**")
        answer = st.text_area(
            f"답변 {i+1}",
            value=st.session_state.memory_answers.get(f"answer_{i}", ""),
            key=f"memory_answer_{i}",
            height=100,
            placeholder="여기에 답변을 입력해주세요...",
            help="자유롭게 답변해주세요"
        )
        st.session_state.memory_answers[f"answer_{i}"] = answer
        st.markdown("<br>", unsafe_allow_html=True)
    
    # 상 생성하기 버튼
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 활동 마무리하기", key="generate_award", 
                    help="재미있는 활동이었나요?",
                    use_container_width=True):
            
            # 모든 답변이 입력되었는지 확인
            all_answered = all(st.session_state.memory_answers.get(f"answer_{i}", "").strip() for i in range(5))
            
            if not all_answered:
                st.warning("💡 모든 질문에 답변해주세요!")
                st.info("빈 답변이 있는 질문이 있어요. 모든 질문에 답변하고 다시 시도해보세요.")
            else:
                # 로딩 표시
                with st.spinner("잠깐만요..? 어디선가 날아온 메시지가 있어요."):
                    try:
                        # 프롬프트 파일 읽기
                        prompt_path = get_file_path("프롬프트/5.추억의 언덕.txt")
                        with open(prompt_path, "r", encoding="utf-8") as f:
                            prompt_content = f.read()
                        
                        # 답변들을 하나의 문자열로 결합
                        answers_text = "\n".join([
                            f"질문 {i+1}: {questions[i]}\n답변 {i+1}: {st.session_state.memory_answers[f'answer_{i}']}"
                            for i in range(5)
                        ])
                        
                        # 완성된 프롬프트 생성
                        full_prompt = f"{prompt_content}\n{answers_text}\n\n<생성한 상>"
                        
                        # OpenAI API 호출 (환경변수에서 API 키 가져오기)
                        api_key = os.getenv("OPENAI_API_KEY")
                        if not api_key:
                            st.error("OpenAI API 키가 설정되지 않았습니다.")
                            return
                        
                        client = openai.OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": "당신은 초등학생 연극 활동의 심사위원이자 칭찬 선생님입니다."},
                                {"role": "user", "content": full_prompt+"\n반드시 특별한 상이름, 재치있는 내용으로 생성하세요."}
                            ],
                            max_tokens=500,
                            temperature=0.7
                        )
                        
                        # 생성된 상 내용
                        generated_award = response.choices[0].message.content
                        st.session_state.generated_award = generated_award
                        st.session_state.award_generated = True
                        
                        st.success("🎉 나만의 특별한 상이 생성되었습니다!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"상 생성 중 오류가 발생했습니다: {str(e)}")
                        st.info("잠시 후 다시 시도해보세요.")
    
    # 생성된 상 표시
    if st.session_state.get('award_generated', False) and 'generated_award' in st.session_state:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white; margin: 2rem 0;">
            <h3 style="color: white; margin-bottom: 1rem;">🏆 나만의 특별한 상</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 생성된 상 내용을 예쁘게 표시
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 15px; 
                    border: 3px solid #667eea; margin: 2rem 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <div style="white-space: pre-line; font-size: 1.1rem; line-height: 1.6; color: #333;">
                {st.session_state.generated_award}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 다음 마을로 이동 버튼
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📋 활동 돌아보기", key="next_village", 
                        help="활동 내용을 돌아봅니다",
                        use_container_width=True):
                st.session_state.current_page = "summary_page"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
