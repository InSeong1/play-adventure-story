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
                    help="클릭하여 초대장을 들을 수 있습니다",
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
        <h2 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">🎭 연극 대본 계획서 작성하기</h2>
        <p style="color: #666; font-size: 1.1rem;">연극 대본 작성을 위한 기본 정보를 입력해 주세요.</p>
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
            help="연극에 등장할 인물의 수를 입력하세요."
        )
        
        # 등장인물의 이름
        st.markdown("📝 **등장인물의 이름**")
        character_names = st.text_area(
            "등장인물들의 이름을 쉼표(,)로 구분하여 입력하세요.",
            placeholder="예: 홍길동, 김철수, 이영희...",
            help="여러 등장인물의 이름을 쉼표(,)로 구분하여 입력하세요."
        )
        
        # 연극 장르 입력
        genre = st.text_input(
            "🎬 연극 장르",
            placeholder="예: 드라마, 코미디, 로맨스, 스릴러, 판타지, 역사극, 뮤지컬, 실험극, 기타...",
            help="연극의 장르를 직접 입력하세요."
        )
        
        # 연극 주제 입력 (왼쪽 칼럼 제일 아래)
        theme = st.text_input(
            "🎯 연극 주제",
            placeholder="예: 착한 일을 하면 복을 받는다",
            help="'착한 일을 하면 복을 받는다.' '이야기 흐름 예시는 '가난하지만 마음씨 착한 주인공이 길에서 잃어버린 지갑을 주워 주인에게 돌려준다. 지갑 주인이 선행에 감동해 주인공이 위기에 처했을 때 도와준다.'"
        )
    
    with col2:
        # 시간적 배경
        time_background = st.text_input(
            "⏰ 시간적 배경",
            placeholder="예: 2025 년, 조선시대, 미래...",
            help="연극이 일어나는 시대나 시간을 입력하세요. 배경이 여러 개라면 쉼표로 구분하여 적어주세요."
        )
        
        # 공간적 배경
        space_background = st.text_input(
            "🏛️ 공간적 배경",
            placeholder="예: 교실, 강당, 시청각실실...",
            help="연극이 일어나는 장소나 공간을 입력하세요. 시간이 여러 개라면 쉼표로 구분하여 적어주세요."
        )
        
        # 공연 시간 (분 단위)
        performance_time = st.number_input(
            "⏱️ 공연 시간 (분)",
            min_value=1,
            max_value=60,
            value=10,
            help="예상 공연 시간을 분 단위로 입력하세요."
        )
        
        # 장면 수 (오른쪽 칼럼으로 이동)
        scene_count = st.number_input(
            "🎭 장면 수",
            min_value=1,
            max_value=10,
            value=1,
            help="연극의 총 장면 수를 입력하세요"
        )
        
        # 이야기 흐름 입력 (오른쪽 칼럼 가장 밑)
        st.markdown("<br>", unsafe_allow_html=True)
        story_flow = st.text_area(
            "📖 이야기 흐름",
            placeholder="예: 가난하지만 마음씨 착한 주인공이 길에서 잃어버린 지갑을 주워 주인에게 돌려준다. 지갑 주인이 선행에 감동해 주인공이 위기에 처했을 때 도와준다.",
            help="연극의 주요 이야기 흐름을 자세히 설명해 주세요.",
            height=100
        )
    
    # 입력 완료 버튼 (양쪽 칼럼을 합쳐서 큰 버튼)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ 입력 완료", key="submit_form", 
                help="입력한 정보를 저장합니다.",
                use_container_width=True):
                
                # 검증 로직
                validation_errors = []
                
                # 1. 필수 입력 확인
                if character_names.strip() == "":
                    validation_errors.append("등장인물 이름을 입력해 주세요.")
                if genre.strip() == "":
                    validation_errors.append("연극 장르를 입력해 주세요.")
                if time_background.strip() == "":
                    validation_errors.append("시간적 배경을 입력해 주세요.")
                if space_background.strip() == "":
                    validation_errors.append("공간적 배경을 입력해 주세요.")
                if theme.strip() == "":
                    validation_errors.append("연극 주제를 입력해 주세요.")
                if story_flow.strip() == "":
                    validation_errors.append("이야기 흐름을 입력해 주세요.")
                
                # 2. 등장인물 수와 이름 개수 확인
                if character_names.strip() != "":
                    name_list = [name.strip() for name in character_names.split(',') if name.strip()]
                    if len(name_list) != character_count:
                        validation_errors.append(f"등장인물 수({character_count}명)와 입력한 이름 개수({len(name_list)}명)가 일치하지 않습니다.")
                
                # 3. 공연시간과 장면 수 비율 확인 (5분당 1장면 이상이면 경고)
                max_recommended_scenes = performance_time // 5
                if scene_count > max_recommended_scenes:
                    validation_errors.append(f"공연시간 {performance_time}분에 비해 장면 수({scene_count}개)가 많습니다. 권장 장면 수는 {max_recommended_scenes}개 이하입니다.")
                
                # 검증 오류가 있으면 탭으로 구분해서 표시
                if validation_errors:
                    st.error("⚠️ 입력 정보를 확인해 주세요:")
                    
                    # 오류 유형별로 탭 생성
                    tab_names = []
                    if any("등장인물" in error for error in validation_errors):
                        tab_names.append("👥 등장인물")
                    if any("장르" in error or "배경" in error or "주제" in error or "이야기" in error for error in validation_errors):
                        tab_names.append("📝 기본 정보")
                    if any("장면" in error for error in validation_errors):
                        tab_names.append("🎭 공연 설정")
                    
                    if len(tab_names) > 1:
                        tabs = st.tabs(tab_names)
                        
                        # 등장인물 탭
                        if "👥 등장인물" in tab_names:
                            tab_index = tab_names.index("👥 등장인물")
                            with tabs[tab_index]:
                                for error in validation_errors:
                                    if "등장인물" in error:
                                        st.write(f"• {error}")
                        
                        # 기본 정보 탭
                        if "📝 기본 정보" in tab_names:
                            tab_index = tab_names.index("📝 기본 정보")
                            with tabs[tab_index]:
                                for error in validation_errors:
                                    if any(keyword in error for keyword in ["장르", "배경", "주제", "이야기"]):
                                        st.write(f"• {error}")
                        
                        # 공연 설정 탭
                        if "🎭 공연 설정" in tab_names:
                            tab_index = tab_names.index("🎭 공연 설정")
                            with tabs[tab_index]:
                                for error in validation_errors:
                                    if "장면" in error:
                                        st.write(f"• {error}")
                    else:
                        # 탭이 하나만 필요한 경우
                        for error in validation_errors:
                            st.write(f"• {error}")
                    
                    # 주의사항 표시
                    st.markdown("""
                    <div style="background-color: #FFF3CD; border: 1px solid #FFEAA7; border-radius: 5px; padding: 1rem; margin: 1rem 0;">
                        <p style="color: #856404; font-weight: bold; margin: 0;">⚠️ 주의사항:</p>
                        <ul style="color: #856404; margin: 0.5rem 0 0 0;">
                            <li>잔인하거나 폭력적인 내용은 포함하지 마세요.</li>
                            <li>모든 필수 항목을 정확히 입력해 주세요.</li>
                            <li>등장인물 수와 이름 개수를 일치시켜 주세요.</li>
                            <li>공연시간에 비해 장면 수가 너무 많지 않도록 설정해 주세요.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 검증 통과 시 다음 마을로 진행
                else:
                    st.success("🎉 연극에 필요한 기본 정보들을 입력 받았어요!\n다음 마을로 모험을 계속해 볼까요?")
                    
                    # 입력된 값들을 세션에 저장
                    st.session_state.village_inputs = {
                        'character_count': character_count,
                        'character_names': character_names,
                        'genre': genre,
                        'time_background': time_background,
                        'space_background': space_background,
                        'performance_time': performance_time,
                        'scene_count': scene_count,
                        'theme': theme,
                        'story_flow': story_flow
                    }
    
            # 다음 마을로 모험 떠나기 버튼 (검증 통과 후에만 표시)
    if 'village_inputs' in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 다음 마을로 모험 떠나기", key="next_village", 
                    help="다음 마을로 이동합니다.",
                    use_container_width=True):
            # 시작의 마을 클리어 (자동으로)
            if 'cleared_villages' not in st.session_state:
                st.session_state.cleared_villages = []
            if 1 not in st.session_state.cleared_villages:
                st.session_state.cleared_villages.append(1)
            
            # feedback_age.py 페이지로 이동
            st.session_state.current_page = "feedback_age"
            st.rerun()
    
  
