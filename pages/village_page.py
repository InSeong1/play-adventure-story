import streamlit as st
from utils import play_bgm, get_file_path, get_base64_image, render_common_menu, generate_play_scenario
import os

def village_page():
    """시작의 마을 페이지 (확장 가능한 구조)"""
    # BGM 재생 - 시작의 마을 BGM (새로운 BGM)
    bgm_path = get_file_path("브금 모음/1. 시작의 마을.mp3")
    play_bgm(bgm_path)
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 초대장 이미지를 적절한 크기로 표시 (배경이 아닌 일반 이미지)
    invitation_path = get_file_path("사진 모음/초대장/1_시작의 마을 초대장.png")
    # st.write(f"DEBUG 초대장 경로: {invitation_path}")
    invitation_image = get_base64_image(invitation_path)
    
    if invitation_image:
        # 이미지를 CSS 클래스를 사용하여 적절한 크기로 표시
        st.markdown(f"""
        <div class="image-container">
            <img src="data:image/png;base64,{invitation_image}" alt="시작의 마을 초대장">
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
                with open(get_file_path("나레이션 소리 모음/1.시작의 마을.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                
                # 나레이션 텍스트 내용 출력
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📖 나레이션 내용:**")
                try:
                    with open(get_file_path("나레이션/1.시작의 마을.txt"), "r", encoding="utf-8") as text_file:
                        narration_text = text_file.read()
                        st.write(narration_text)
                except Exception as e:
                    st.error(f"나레이션 텍스트 파일을 불러올 수 없습니다: {str(e)}")
                
            except Exception as e:
                st.error(f"나레이션 파일을 불러올 수 없습니다: {str(e)}")
                st.write(f"파일 경로: 나레이션 소리 모음/1.시작의 마을.mp3")
    
    # 사용자 입력 폼 (스크롤 아래에 배치)
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    # 입력 폼 제목
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">🎭 연극 대본 계획서 작성</h2>
        <p style="color: #666; font-size: 1.1rem;">연극 대본 작성을 위한 기본 정보를 입력해주세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 입력 폼을 2열로 배치
    col1, col2 = st.columns(2)
    
    with col1:
        # 등장인물의 수
        character_count = st.number_input(
            "👥 등장인물의 수",
            min_value=1,
            max_value=20,
            value=1,
            help="연극에 등장할 인물의 수를 입력하세요"
        )
        
        # 등장인물의 이름
        st.markdown("📝 **등장인물의 이름** (쉼표로 구분)")
        character_names = st.text_area(
            "등장인물들의 이름을 쉼표(,)로 구분하여 입력하세요",
            placeholder="예: 홍길동, 김철수, 이영희...",
            help="여러 등장인물의 이름을 쉼표(,)로 구분하여 입력하세요"
        )
        
        # 연극 장르 입력
        genre = st.text_input(
            "🎬 연극 장르",
            placeholder="예: 드라마, 코미디, 로맨스, 스릴러, 판타지, 역사극, 뮤지컬, 실험극, 기타...",
            help="연극의 장르를 직접 입력하세요"
        )
    
    with col2:
        # 시간적 배경
        time_background = st.text_input(
            "⏰ 시간적 배경",
            placeholder="예: 2024년, 조선시대, 미래...",
            help="연극이 일어나는 시대나 시간을 입력하세요"
        )
        
        # 공간적 배경
        space_background = st.text_input(
            "🏛️ 공간적 배경",
            placeholder="예: 서울, 판타지 세계, 우주선...",
            help="연극이 일어나는 장소나 공간을 입력하세요"
        )
        
        # 공연 시간 (분 단위)
        performance_time = st.number_input(
            "⏱️ 공연 시간 (분)",
            min_value=10,
            max_value=180,
            value=60,
            help="예상 공연 시간을 분 단위로 입력하세요"
        )
        
        # 장면 수 (오른쪽 칼럼으로 이동)
        scene_count = st.number_input(
            "🎭 장면 수",
            min_value=1,
            max_value=10,
            value=1,
            help="연극의 총 장면 수를 입력하세요"
        )
    
    # 입력 완료 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # 모든 필수 입력 확인
        required_fields_filled = (
            character_names.strip() != "" and
            genre != "" and
            time_background.strip() != "" and
            space_background.strip() != ""
        )
        
        if required_fields_filled:
            if st.button("✅ 입력 완료", key="submit_form", 
                        help="모든 정보가 입력되었습니다. 시나리오를 생성합니다.",
                        use_container_width=True):
                
                st.success("🎉 모든 정보가 입력되었습니다! 시나리오 생성 중...")
                
                # 프롬프트 파일 읽기
                try:
                    with open(get_file_path("프롬프트/1.시작의 마을.txt"), "r", encoding="utf-8") as prompt_file:
                        prompt_template = prompt_file.read()
                    
                    # 프롬프트에 입력값 치환
                    prompt = prompt_template.format(
                        character_names=character_names,
                        genre=genre,
                        time_background=time_background,
                        space_background=space_background,
                        performance_time=performance_time,
                        scene_count=scene_count
                    )
                    
                    # OpenAI API를 사용하여 시나리오 생성
                    with st.spinner("🤖 주어진 내용을 바탕으로 시나리오를 생성하고 있어요..."):
                        generated_scenario = generate_play_scenario(prompt)
                    
                    # 생성된 시나리오 표시
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 🎭 생성된 연극 시나리오")
                    st.markdown("---")
                    
                    # 생성된 시나리오를 표시
                    st.markdown(generated_scenario)
                    
                    # 생성된 시나리오를 세션 상태에 저장
                    st.session_state.generated_scenario = generated_scenario
                    
                except Exception as e:
                    st.error(f"프롬프트 파일을 불러올 수 없습니다: {str(e)}")
    
    # 마을 클리어 버튼을 항상 표시 (필수 입력과 관계없이)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🏆 마을 클리어")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏆 마을 클리어하기", key="clear_village", 
                    help="이 마을을 클리어하고 뱃지를 획득합니다",
                    use_container_width=True):
            # 시작의 마을 클리어 (1번 마을)
            from utils import clear_village
            clear_village(1)
            
            st.session_state.current_page = "feedback_age"
            st.rerun()
    
    # 필수 입력 확인 메시지
    if not required_fields_filled:
        st.warning("⚠️ 필수 입력 정보를 모두 채워주세요!")
        st.info("등장인물 이름, 연극 장르, 시간적 배경, 공간적 배경은 반드시 입력해야 합니다.")
    
    # 네비게이션 버튼들은 사이드바에 있으므로 제거
