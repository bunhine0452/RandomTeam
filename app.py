import streamlit as st
import random
import math
from typing import List, Dict
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="🎲 랜덤 팀 뽑기",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .team-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .team-name {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .member-list {
        text-align: center;
        font-size: 1.1rem;
    }
    
    .input-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        color: white;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 10px 0;
    }
    
    .shuffle-button {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border: none;
        padding: 15px 30px;
        border-radius: 25px;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .shuffle-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def shuffle_teams(names: List[str], team_size: int) -> Dict[str, List[str]]:
    """이름 리스트를 랜덤하게 섞어서 팀으로 나누는 함수"""
    shuffled_names = names.copy()
    random.shuffle(shuffled_names)
    
    teams = {}
    team_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    for i in range(0, len(shuffled_names), team_size):
        team_name = f"{team_letters[i // team_size]}팀"
        team_members = shuffled_names[i:i + team_size]
        teams[team_name] = team_members
    
    return teams

def main():
    # 메인 헤더
    st.markdown('<h1 class="main-header">🎲 랜덤 팀 뽑기</h1>', unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 🎯 설정")
        st.markdown("---")
        
        # 이름 입력
        st.markdown("#### 👥 참여자 이름")
        names_input = st.text_area(
            "이름을 쉼표(,)로 구분해서 입력하세요:",
            placeholder="김철수, 이영희, 박민수, 최지혜, 정우진, 송하나",
            height=100
        )
        
        # 팀 크기 설정
        st.markdown("#### 👨‍👩‍👧‍👦 1팀당 인원 수")
        team_size = st.number_input(
            "팀당 몇 명씩?",
            min_value=1,
            max_value=20,
            value=3,
            step=1
        )
        
        st.markdown("---")
        
        # 셔플 버튼
        shuffle_clicked = st.button(
            "🎲 팀 섞기!",
            use_container_width=True,
            type="primary"
        )
    
    # 메인 컨텐츠 영역
    if names_input.strip():
        # 이름 파싱
        names = [name.strip() for name in names_input.split(",") if name.strip()]
        
        if len(names) < 2:
            st.warning("⚠️ 최소 2명 이상의 이름을 입력해주세요!")
            return
        
        # 통계 정보
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>👥 총 인원</h3>
                <h2>{len(names)}명</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            num_teams = math.ceil(len(names) / team_size)
            st.markdown(f"""
            <div class="stats-card">
                <h3>🏆 총 팀 수</h3>
                <h2>{num_teams}팀</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <h3>👨‍👩‍👧‍👦 팀당 인원</h3>
                <h2>{team_size}명</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            remaining = len(names) % team_size
            if remaining == 0:
                remaining_text = "없음"
            else:
                remaining_text = f"{remaining}명"
            st.markdown(f"""
            <div class="stats-card">
                <h3>➕ 남는 인원</h3>
                <h2>{remaining_text}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 팀 생성 및 표시
        if 'teams' not in st.session_state or shuffle_clicked:
            st.session_state.teams = shuffle_teams(names, team_size)
        
        if 'teams' in st.session_state:
            st.markdown("## 🎉 팀 구성 결과")
            
            # 팀별로 카드 형태로 표시
            teams = st.session_state.teams
            
            # 2열로 배치
            cols = st.columns(2)
            for idx, (team_name, members) in enumerate(teams.items()):
                with cols[idx % 2]:
                    # 팀 색상을 다양하게
                    colors = [
                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                        "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                        "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
                        "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
                        "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
                    ]
                    color = colors[idx % len(colors)]
                    
                    members_str = " • ".join(members)
                    st.markdown(f"""
                    <div class="team-card" style="background: {color};">
                        <div class="team-name">🏆 {team_name}</div>
                        <div class="member-list">{members_str}</div>
                        <div style="text-align: center; margin-top: 10px; font-size: 0.9rem; opacity: 0.8;">
                            👥 {len(members)}명
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # 팀 구성 표를 데이터프레임으로도 제공
            st.markdown("### 📊 팀 구성 표")
            
            # 데이터프레임 생성
            df_data = []
            max_members = max(len(members) for members in teams.values())
            
            for team_name, members in teams.items():
                row = {'팀명': team_name, '인원수': len(members)}
                for i in range(max_members):
                    if i < len(members):
                        row[f'멤버{i+1}'] = members[i]
                    else:
                        row[f'멤버{i+1}'] = ''
                df_data.append(row)
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # CSV 다운로드 버튼
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 팀 구성 CSV 다운로드",
                data=csv,
                file_name="random_teams.csv",
                mime="text/csv"
            )
    
    else:
        # 초기 화면
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h2>👈 왼쪽 사이드바에서 설정을 시작하세요!</h2>
            <p style="font-size: 1.2rem; color: #666;">
                참여자 이름과 팀 크기를 입력하고<br>
                <strong>🎲 팀 섞기!</strong> 버튼을 눌러보세요
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🎲 Made with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
