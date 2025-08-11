import streamlit as st
import os
import base64
from utils import get_file_path, get_base64_image, render_common_menu

def story_forest_page():
    """이야기 숲 페이지"""
    
    # 햄버거 메뉴 (사이드바)
    render_common_menu()
    
    # 페이지 제목
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1 style="color: #2E86AB; font-weight: bold; margin-bottom: 1rem;">🌲 이야기 숲</h1>
        <p style="color: #666; font-size: 1.1rem;">이야기 숲에 오신 것을 환영합니다!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 초대장 이미지 표시
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📜 초대장")
        
        # 초대장 이미지 로드
        invitation_path = get_file_path("사진 모음/초대장/2_이야기 숲 초대장.png")
        if os.path.exists(invitation_path):
            invitation_image = get_base64_image(invitation_path)
            if invitation_image:
                st.markdown(f"""
                <img src="data:image/png;base64,{invitation_image}" 
                     style="width: 100%; max-width: 600px; height: auto; border-radius: 15px; 
                            box-shadow: 0 8px 25px rgba(0,0,0,0.3); margin: 0 auto; display: block;" 
                     alt="이야기 숲 초대장">
                """, unsafe_allow_html=True)
            else:
                st.error("초대장 이미지를 불러올 수 없습니다.")
        else:
            st.error("초대장 파일을 찾을 수 없습니다.")
    
    # 대본 수정 및 피드백 섹션
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### ✏️ 대본 수정 및 피드백")
    
    # 이전 마을에서 생성된 시나리오 표시 (세션 상태에서 가져오기)
    if 'generated_scenario' in st.session_state:
        st.markdown("#### 📖 현재 대본")
        st.markdown("---")
        st.text_area("시나리오 내용", value=st.session_state.generated_scenario, 
                    height=300, disabled=True, key="current_scenario")
        
        # 대본 수정 입력
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🔄 대본 수정")
        
        modified_scenario = st.text_area(
            "수정된 대본을 입력하세요",
            value=st.session_state.generated_scenario,
            height=300,
            help="대본을 수정하여 더 좋은 연극을 만들어보세요"
        )
        
        # 피드백 입력
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 💬 피드백")
        
        feedback = st.text_area(
            "대본에 대한 피드백을 입력하세요",
            placeholder="대본의 장점, 개선점, 아이디어 등을 자유롭게 작성해주세요...",
            height=150,
            help="대본을 더 좋게 만들기 위한 의견을 남겨주세요"
        )
        
        # 수정 완료 버튼
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ 수정 완료", 
                        help="대본 수정과 피드백을 완료합니다",
                        use_container_width=True):
                
                # 수정된 시나리오와 피드백을 세션 상태에 저장
                st.session_state.modified_scenario = modified_scenario
                st.session_state.feedback = feedback
                
                st.success("🎉 대본 수정과 피드백이 완료되었습니다!")
                
                # 다음 마을로 이동 버튼
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🌲 다음 마을로", 
                            help="피드백 페이지로 이동합니다",
                            use_container_width=True):
                    st.session_state.current_page = "feedback_age"
                    st.rerun()
    else:
        st.info("💡 시작의 마을에서 먼저 대본을 작성해주세요!")
        
        # 홈으로 돌아가기 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏠 홈으로 돌아가기", 
                        help="홈 페이지로 돌아갑니다",
                        use_container_width=True):
                st.session_state.current_page = "intro"
                st.rerun()
    
    # 사이드바에 네비게이션 메뉴
    st.sidebar.title("🌲 이야기 숲")
    
    if st.sidebar.button("🏠 홈으로", use_container_width=True):
        st.session_state.current_page = "intro"
        st.rerun()
    
    if st.sidebar.button("🗺️ 지도 보기", use_container_width=True):
        st.session_state.current_page = "adventure_map"
        st.rerun()
    
    if st.sidebar.button("🏘️ 시작의 마을", use_container_width=True):
        st.session_state.current_page = "village"
        st.rerun()
