import streamlit as st
from io import BytesIO
from pydub import AudioSegment
from utils import get_file_path, get_base64_image, render_common_menu, generate_play_scenario, play_bgm
import os
import time

def village_page():
    """시작의 마을 페이지 (확장 가능한 구조)"""
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 메인 콘텐츠를 감싸는 컨테이너
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    # 배경음악 버튼을 가장 먼저 렌더링 (dialog 닫힐 때 커서가 여기로 오도록)
    st.markdown('<div id="village-audio-top"></div>', unsafe_allow_html=True)
    
    
    # 초대장 이미지 표시
    invitation_path = get_file_path("사진 모음/초대장/1_시작의 마을 초대장.png")
    invitation_image = get_base64_image(invitation_path)
    
    if invitation_image:
        # 오디오 플레이어들을 배치
        col1, col2, col3 = st.columns([1, 5, 1])
        
        # 배경음악 (첫 번째 컬럼) - 가장 먼저 렌더링
        with col1:
            st.markdown("🎵 배경음악 듣기", help="- 배경음악이 필요할 때는 재생해 보세요. 상황에 따라 재생 속도를 조절하거나 음소거 기능도 활용할 수 있어요!")
            try:
                with open(get_file_path("브금 모음/1. 시작의 마을.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"BGM 파일을 불러올 수 없습니다: {str(e)}")
        
        
        # 초대장 듣기 (마지막 컬럼)
        with col3:
            st.markdown("📜 초대장 듣기", help="- 시작의 마을에서 여러분을 따뜻하게 맞이하는 초대장을 읽어주는 친구의 목소리를 들어보세요! 이 마을에서 무엇을 할 수 있는지 알아볼 수 있어요.")
            try:
                with open(get_file_path("나레이션 소리 모음/1.시작의 마을.mp3"), "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3",autoplay=True)
            except Exception as e:
                st.error(f"초대장 파일을 불러올 수 없습니다: {str(e)}")
        
        # 공백 추가
        st.markdown("")
        st.markdown("")
        st.image(f"data:image/png;base64,{invitation_image}",width="stretch")
    else:
        st.error("초대장 이미지를 불러올 수 없습니다.")
        st.write(f"파일 경로: {invitation_path}")
        st.write(f"파일 존재 여부: {os.path.exists(invitation_path)}")
    
    # 초대장 내용 컨테이너화
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin: 20px 0;">
        <h3 style="text-align: center; color: #333; margin-bottom: 15px;">📜 시작의 마을 초대장</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #555; text-align: center;">
            안녕하세요~ 시작의 마을에 오신 여러분을 환영합니다!<br><br>
            시작의 마을에서는 여러분들이 모둠 회의를 통해 대본에 필요한 여러 가지 항목들을 함께 정하고 기록할 것입니다.<br><br>
            그럼 시작해 볼까요? 무대를 설계해 봅시다. 참! <strong>잔인한 내용이나 욕설 사용은 절대 금지입니다^^</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    

    
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
        default_character_count = 1
        if 'village_inputs' in st.session_state and 'character_count' in st.session_state.village_inputs:
            default_character_count = st.session_state.village_inputs['character_count']
        
        character_count = st.number_input(
            "👥 등장인물의 수\n(해설 역할은 제외하고 적어 주세요. 예. 해설, 흥부, 놀부 -> 2)",
            min_value=1,
            max_value=20,
            value=default_character_count,
            help="연극에 등장할 인물의 수를 입력하세요."
        )
        
        # 등장인물의 이름
        st.markdown("📝 **등장인물의 이름**")
        default_character_names = ""
        if 'village_inputs' in st.session_state and 'character_names' in st.session_state.village_inputs:
            default_character_names = st.session_state.village_inputs['character_names']
        
        character_names = st.text_area(
            "등장인물들의 이름을 쉼표(,)로 구분하여 입력하세요.",
            value=default_character_names,
            placeholder="예: 홍길동, 김철수, 이영희...",
            help="여러 등장인물의 이름을 쉼표(,)로 구분하여 입력하세요."
        )
        
        # 연극 장르 입력
        default_genre = ""
        if 'village_inputs' in st.session_state and 'genre' in st.session_state.village_inputs:
            default_genre = st.session_state.village_inputs['genre']
        
        genre = st.text_input(
            "🎬 연극 장르",
            value=default_genre,
            placeholder="예: 드라마, 코미디, 로맨스, 스릴러, 판타지, 역사극, 뮤지컬, 실험극, 기타...",
            help="연극의 장르를 직접 입력하세요."
        )
        
        # 연극 주제 입력 (왼쪽 칼럼 제일 아래)
        default_theme = ""
        if 'village_inputs' in st.session_state and 'theme' in st.session_state.village_inputs:
            default_theme = st.session_state.village_inputs['theme']
        
        theme = st.text_input(
            "🎯 연극 주제",
            value=default_theme,
            placeholder="예: 착한 일을 하면 복을 받는다",
            help="'착한 일을 하면 복을 받는다.' '이야기 흐름 예시는 '가난하지만 마음씨 착한 주인공이 길에서 잃어버린 지갑을 주워 주인에게 돌려준다. 지갑 주인이 선행에 감동해 주인공이 위기에 처했을 때 도와준다.'"
        )
    
    with col2:
        # 시간적 배경
        default_time_background = ""
        if 'village_inputs' in st.session_state and 'time_background' in st.session_state.village_inputs:
            default_time_background = st.session_state.village_inputs['time_background']
        
        time_background = st.text_input(
            "⏰ 시간적 배경",
            value=default_time_background,
            placeholder="예: 2025 년, 조선시대, 미래...",
            help="연극이 일어나는 시대나 시간을 입력하세요. 배경이 여러 개라면 쉼표로 구분하여 적어주세요."
        )
        
        # 공간적 배경
        default_space_background = ""
        if 'village_inputs' in st.session_state and 'space_background' in st.session_state.village_inputs:
            default_space_background = st.session_state.village_inputs['space_background']
        
        space_background = st.text_input(
            "🏛️ 공간적 배경",
            value=default_space_background,
            placeholder="예: 교실, 강당, 시청각실, 울산 대공원...",
            help="연극이 일어나는 장소나 공간을 입력하세요. 시간이 여러 개라면 쉼표로 구분하여 적어주세요."
        )
        
        # 공연 시간 (분 단위)
        default_performance_time = 10
        if 'village_inputs' in st.session_state and 'performance_time' in st.session_state.village_inputs:
            default_performance_time = st.session_state.village_inputs['performance_time']
        
        performance_time = st.number_input(
            "⏱️ 공연 시간 (분)",
            min_value=1,
            max_value=60,
            value=default_performance_time,
            help="예상 공연 시간을 분 단위로 입력하세요."
        )
        
        # 장면 수 (오른쪽 칼럼으로 이동)
        default_scene_count = 1
        if 'village_inputs' in st.session_state and 'scene_count' in st.session_state.village_inputs:
            default_scene_count = st.session_state.village_inputs['scene_count']
        
        scene_count = st.number_input(
            "🎭 장면 수",
            min_value=1,
            max_value=10,
            value=default_scene_count,
            help="연극의 총 장면 수를 입력하세요"
        )
        
        # 이야기 흐름 입력 (오른쪽 칼럼 가장 밑)
        st.markdown("<br>", unsafe_allow_html=True)
        default_story_flow = ""
        if 'village_inputs' in st.session_state and 'story_flow' in st.session_state.village_inputs:
            default_story_flow = st.session_state.village_inputs['story_flow']
        
        story_flow = st.text_area(
            "📖 이야기 흐름",
            value=default_story_flow,
            placeholder="예: 가난하지만 마음씨 착한 주인공이 길에서 잃어버린 지갑을 주워 주인에게 돌려준다. 지갑 주인이 선행에 감동해 주인공이 위기에 처했을 때 도와준다.",
            help="연극의 주요 이야기 흐름을 자세히 설명해 주세요.",
            height=100
        )
    
    # 입력 완료 버튼 (양쪽 칼럼을 합쳐서 큰 버튼)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ 입력 완료 (반드시 입력 완료 버튼으로 저장하세요!)", key="submit_form", 
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
                
                # 3. 쉼표로 구분된 항목들의 내용 길이 확인
                if character_names.strip() != "":
                    name_list = [name.strip() for name in character_names.split(',') if name.strip()]
                    for i, name in enumerate(name_list):
                        if len(name) < 2:
                            validation_errors.append(f"등장인물 {i+1}번째 이름이 너무 짧습니다.")
                
                if genre.strip() != "":
                    genre_list = [g.strip() for g in genre.split(',') if g.strip()]
                    for i, g in enumerate(genre_list):
                        if len(g) < 2:
                            validation_errors.append(f"연극 장르 {i+1}번째 항목이 너무 짧습니다.")
                
                if time_background.strip() != "":
                    time_list = [t.strip() for t in time_background.split(',') if t.strip()]
                    for i, t in enumerate(time_list):
                        if len(t) < 2:
                            validation_errors.append(f"시간적 배경 {i+1}번째 항목이 너무 짧습니다.")
                
                if space_background.strip() != "":
                    space_list = [s.strip() for s in space_background.split(',') if s.strip()]
                    for i, s in enumerate(space_list):
                        if len(s) < 2:
                            validation_errors.append(f"공간적 배경 {i+1}번째 항목이 너무 짧습니다.")
                
                # 4. 주제와 이야기 흐름 길이 확인
                if theme.strip() != "" and len(theme.strip()) < 5:
                    validation_errors.append("연극 주제가 너무 짧습니다. 더 자세히 작성해 주세요.")
                
                if story_flow.strip() != "" and len(story_flow.strip()) < 10:
                    validation_errors.append("이야기 흐름이 너무 짧습니다. 더 자세히 작성해 주세요.")
                
                # 5. 공연시간과 장면 수 비율 확인 (5분당 1장면 이상이면 경고)
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
    
    # 대본 설정 다운로드/업로드 버튼들
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 대본 설정 다운로드", key="download_settings",
                    help="현재 입력된 설정을 txt 파일로 다운로드합니다.",
                    use_container_width=True):
            # 다운로드할 내용 생성
            download_content = ""
            if 'village_inputs' in st.session_state:
                inputs = st.session_state.village_inputs
                download_content += f"### 등장인물 수 ###\n{inputs.get('character_count', '')}\n\n"
                download_content += f"### 등장인물의 이름 ###\n{inputs.get('character_names', '')}\n\n"
                download_content += f"### 연극 장르 ###\n{inputs.get('genre', '')}\n\n"
                download_content += f"### 시간적 배경 ###\n{inputs.get('time_background', '')}\n\n"
                download_content += f"### 공간적 배경 ###\n{inputs.get('space_background', '')}\n\n"
                download_content += f"### 공연 시간 ###\n{inputs.get('performance_time', '')}\n\n"
                download_content += f"### 장면 수 ###\n{inputs.get('scene_count', '')}\n\n"
                download_content += f"### 연극 주제 ###\n{inputs.get('theme', '')}\n\n"
                download_content += f"### 이야기 흐름 ###\n{inputs.get('story_flow', '')}\n\n"
            else:
                download_content = "저장된 설정이 없습니다."
            
            # 다운로드 버튼 생성
            st.download_button(
                label="📥 설정 파일 다운로드",
                data=download_content,
                file_name="연극_대본_설정.txt",
                mime="text/plain",
                key="download_file"
            )
    
    with col2:
        # 업로드 완료되지 않은 경우에만 파일 업로더 표시
        if not st.session_state.get('upload_completed', False):
            uploaded_file = st.file_uploader("📤 대본 설정 업로드", 
                                           type=['txt'],
                                           help="이전에 다운로드한 설정 파일을 업로드하여 자동으로 입력합니다.",
                                           key="upload_settings")
            
            if uploaded_file is not None:
                try:
                    # 파일 내용 읽기
                    content = uploaded_file.read().decode('utf-8')
                    
                    # 파싱하여 세션 상태에 저장
                    parsed_data = {}
                    sections = content.split('### ')
                    
                    for section in sections[1:]:  # 첫 번째 빈 섹션 제외
                        if '###' in section:
                            lines = section.split('\n')
                            title = lines[0].replace('###', '').strip()
                            value = '\n'.join(lines[1:]).strip()
                            
                            # 제목을 세션 상태 키로 매핑
                            if title == "등장인물 수":
                                parsed_data['character_count'] = int(value) if value.isdigit() else 1
                            elif title == "등장인물의 이름":
                                parsed_data['character_names'] = value
                            elif title == "연극 장르":
                                parsed_data['genre'] = value
                            elif title == "시간적 배경":
                                parsed_data['time_background'] = value
                            elif title == "공간적 배경":
                                parsed_data['space_background'] = value
                            elif title == "공연 시간":
                                parsed_data['performance_time'] = int(value) if value.isdigit() else 10
                            elif title == "장면 수":
                                parsed_data['scene_count'] = int(value) if value.isdigit() else 1
                            elif title == "연극 주제":
                                parsed_data['theme'] = value
                            elif title == "이야기 흐름":
                                parsed_data['story_flow'] = value
                    
                    # 세션 상태에 저장
                    st.session_state.village_inputs = parsed_data
                    st.success("✅ 설정 파일이 성공적으로 업로드되었습니다!")
                    # 업로드 완료 플래그 설정
                    st.session_state.upload_completed = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ 파일 업로드 중 오류가 발생했습니다: {str(e)}")
        else:
            # 업로드 완료된 경우 성공 메시지 표시
            st.success("✅ 설정 파일이 성공적으로 업로드되었습니다!")
            if st.button("🔄 다시 업로드하기", key="reupload_button"):
                st.session_state.upload_completed = False
                st.rerun()
    
    # 다음 마을로 모험 떠나기 버튼 (검증 통과 후에만 표시)
    if 'village_inputs' in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 다음 마을로 모험 떠나기", key="next_village", 
                    help="다음 마을로 이동합니다.",
                    use_container_width=True):
            # 다음 페이지에 표시할 뱃지 설정 (시작의 마을 뱃지)
            st.session_state.badge_image_filename = "1_뱃지_시작의 마을.png"
            st.session_state.show_badge_dialog = True
            # feedback_page.py 페이지로 이동
            st.session_state.current_page = "feedback_page"
            st.rerun()
    
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
