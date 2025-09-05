import streamlit as st
import base64
import os
import openai

def get_openai_api_key():
    """Streamlit secrets에서 OpenAI API 키를 가져오는 함수"""
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception as e:
        st.error(f"⚠️ Streamlit secrets에서 OPENAI_API_KEY를 찾을 수 없습니다: {str(e)}")
        st.info("`.streamlit/secrets.toml` 파일에 OPENAI_API_KEY를 추가해주세요.")
        return None

def get_file_path(file_path):
    """파일 경로를 반환하는 함수"""
    # 현재 스크립트의 디렉토리를 기준으로 assets 폴더 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, "assets", file_path)
    

    
    return full_path

def get_base64_audio(file_path):
    """오디오 파일을 base64로 인코딩하는 함수"""
    try:
        with open(file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode()
            return audio_base64
    except:
        return None

def get_base64_image(file_path):
    """이미지 파일을 base64로 인코딩하는 함수"""
    try:

        with open(file_path, "rb") as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode()

            return image_base64
    except Exception as e:

        return None



def render_common_menu():
    """공통 메뉴를 렌더링하는 함수"""
    st.sidebar.title("🎭 메뉴")
    
    if st.sidebar.button("🏠 홈으로", use_container_width=True):
        st.session_state.current_page = "intro"
        st.rerun()
    
    if st.sidebar.button("📖 사용 방법", use_container_width=True):
        # 사용 방법 팝업 표시 상태를 토글
        if 'show_help_popup' not in st.session_state:
            st.session_state.show_help_popup = False
        st.session_state.show_help_popup = not st.session_state.show_help_popup
        st.rerun()
    
    if st.sidebar.button("🗺️ 지도 보기", use_container_width=True):
        # 지도 팝업 표시 상태를 토글
        if 'show_map_popup' not in st.session_state:
            st.session_state.show_map_popup = False
        st.session_state.show_map_popup = not st.session_state.show_map_popup
        st.rerun()
        
    if st.sidebar.button("🎭 연극의 특성", use_container_width=True):
        # 연극의 특성 팝업 표시 상태를 토글
        if 'show_theater_popup' not in st.session_state:
            st.session_state.show_theater_popup = False
        st.session_state.show_theater_popup = not st.session_state.show_theater_popup
        st.rerun()
    
    if st.sidebar.button("📝 극본의 특성", use_container_width=True):
        # 극본의 특성 팝업 표시 상태를 토글
        if 'show_script_popup' not in st.session_state:
            st.session_state.show_script_popup = False
        st.session_state.show_script_popup = not st.session_state.show_script_popup
        st.rerun()
    
    if st.sidebar.button("❓ 자주하는 질문", use_container_width=True):
        # 자주하는 질문 팝업 표시 상태를 토글
        if 'show_faq_popup' not in st.session_state:
            st.session_state.show_faq_popup = False
        st.session_state.show_faq_popup = not st.session_state.show_faq_popup
        st.rerun()
    
    # 메뉴 하단에 안내 문구 추가
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<p style='text-align: center; color: #666; font-size: 0.9rem; margin: 10px 0;'>"
        "💡 버튼을 클릭해 정보 보기/닫기</p>", 
        unsafe_allow_html=True
    )

def clear_village(village_number):
    """마을을 클리어했을 때 호출하는 함수"""
    if 'cleared_villages' not in st.session_state:
        st.session_state.cleared_villages = []
    
    # 마을 클리어 상태 업데이트 (중복 방지)
    if village_number not in st.session_state.cleared_villages:
        st.session_state.cleared_villages.append(village_number)
        
        # 뱃지 보드 업데이트를 위한 세션 상태 설정
        st.session_state.village_cleared = True
        st.session_state.last_cleared_village = village_number
        
        # 성공 메시지는 표시하지 않음 (페이지 이동이 즉시 일어나므로)
        # st.success(f"🎉 {village_number}번째 마을을 클리어했습니다!")

def show_badge_popup(village_number):
    """뱃지를 팝업처럼 표시하는 함수"""
    # 뱃지 이미지 경로 설정
    badge_paths = {
        1: "뱃지 모음/1_뱃지_시작의 마을.png",
        2: "뱃지 모음/2_이야기 숲 뱃지 획득.png",
        3: "뱃지 모음/3_준비의 광장 뱃지 획득.png",
        4: "뱃지 모음/4_뱃지_환호의 극장.png",
        5: "뱃지 모음/5_뱃지_추억의 언덕.png"
    }
    
    badge_path = badge_paths.get(village_number, "뱃지 모음/1_뱃지_시작의 마을.png")
    full_badge_path = get_file_path(badge_path)
    
    if os.path.exists(full_badge_path):
        # 뱃지 이미지를 base64로 인코딩
        badge_image = get_base64_image(full_badge_path)
        
        if badge_image:
            # Streamlit 내장 기능을 사용한 뱃지 표시
            st.markdown("---")
            st.markdown("### 🏆 축하합니다!")
            
            # 뱃지 이미지 표시
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{badge_image}" 
                     style="max-width: 100%; height: auto; border-radius: 15px; 
                            box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);" 
                     alt="뱃지">
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**🎉 마을을 성공적으로 클리어했습니다!**")
            
            # 넘어가기 버튼
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🌲 다음 마을로 넘어가기", 
                            help="피드백 나이 페이지로 이동합니다",
                            use_container_width=True):
                    st.session_state.current_page = "feedback_page"
                    st.switch_page("pages/feedback_page.py")
        else:
            st.error("뱃지 이미지를 불러올 수 없습니다.")
    else:
        st.error(f"뱃지 파일을 찾을 수 없습니다: {badge_path}")

def generate_play_scenario(prompt):
    """OpenAI API를 사용하여 연극 시나리오를 생성하는 함수"""
    # API 키를 자동으로 가져오기
    api_key = get_openai_api_key()
    if not api_key:
        return "OpenAI API 키를 찾을 수 없습니다. Streamlit secrets를 확인해주세요."
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 창의적이고 전문적인 연극 대본 작가입니다. 사용자의 요구사항에 맞는 흥미롭고 완성도 높은 연극 시나리오를 작성해주세요."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.8
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"시나리오 생성 중 오류가 발생했습니다: {str(e)}"
