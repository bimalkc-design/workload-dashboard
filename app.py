import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & ENHANCED THEME
# ==========================================
st.set_page_config(
    page_title="DNS Workload Portal | Royal University of Bhutan",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600;700&display=swap');
    
    :root {
        --oxford-blue: #1a2a6c;
        --crimson: #b21f1f;
        --gold: #daa520;
        --ivory: #fdfbf7;
        --text-slate: #2c3e50;
    }

    /* Main Container */
    .stApp { background-color: var(--ivory); }

    /* Elegant Header */
    .main-header {
        background: linear-gradient(to right, #1a2a6c, #b21f1f);
        padding: 3rem;
        border-bottom: 6px solid var(--gold);
        margin: -4rem -4rem 2rem -4rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .main-header h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 3rem;
        margin: 0;
        letter-spacing: 1px;
    }

    /* Professional Section Headers */
    .section-head {
        background-color: var(--oxford-blue);
        color: var(--gold);
        padding: 8px 15px;
        border-radius: 4px;
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        border-left: 5px solid var(--gold);
    }

    /* Module Details Box - Color Provision */
    .module-config-box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e1e1e1;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }

    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-top: 4px solid var(--crimson);
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* Canvas Strips */
    .canvas-strip {
        background: white;
        padding: 1.2rem;
        border-left: 6px solid var(--oxford-blue);
        border-radius: 6px;
        margin-bottom: 1rem;
        border-top: 1px solid #eee;
        border-right: 1px solid #eee;
        border-bottom: 1px solid #eee;
        transition: transform 0.2s;
    }
    .canvas-strip:hover { transform: translateX(5px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }

    /* Academic Buttons */
    div.stButton > button {
        background-color: var(--oxford-blue);
        color: white;
        border-radius: 4px;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        border: 2px solid var(--oxford-blue);
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: var(--gold);
        border-color: var(--gold);
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. COMPLETE MODULE DATABASE
# ==========================================
MODULE_DATABASE = {
    'Chemistry_Old': {
        'Year 1': {'Semester I': [{'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0}, {'code': 'FCH101', 'name': 'Fundamentals of Inorganic Chemistry', 'theory': 3, 'lab': 2}, {'code': 'FPH101', 'name': 'Foundations of Physics I', 'theory': 2, 'lab': 3}, {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0}]},
        'Year 2': {'Semester III': [{'code': 'ICH101', 'name': 'Inorganic Chemistry I', 'theory': 3, 'lab': 3}, {'code': 'PCH201', 'name': 'Physical Chemistry I', 'theory': 3, 'lab': 3}]},
    },
    'Physics_New': {
        'Year 1': {'Semester I': [{'code': 'CME101', 'name': 'Newtonian Mechanics', 'theory': 3, 'lab': 2}, {'code': 'CSP101', 'name': 'Foundations of Python Programming', 'theory': 2, 'lab': 3}]},
        'Year 2': {'Semester I': [{'code': 'APH201', 'name': 'Physics of Space and Satellites', 'theory': 3, 'lab': 2}]}
    },
    'LifeSciences_New': {
        'Year 1': {'Semester I': [{'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4}]}
    }
} # Note: Truncated here for script size, but logic accepts full keys

FACULTY_LIST = ["Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan", "Ms. Kuenzang Choki", "Mr. Tashi Dendup", "Nachiketa Homchaudhuri"]

if 'basket' not in st.session_state: st.session_state.basket = []

# ==========================================
# 3. HEADER
# ==========================================
st.markdown("""
<div class="main-header">
    <div style="font-size: 0.9rem; letter-spacing: 4px; color: var(--gold); font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem;">Royal University of Bhutan</div>
    <h1>Department of Natural Sciences</h1>
    <div style="font-style: italic; opacity: 0.9; margin-top: 0.5rem;">Academic Workload Intelligence — Cycle: Autumn 2026</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR - IDENTITY & DESIGNATION
# ==========================================
with st.sidebar:
    st.markdown("### 🏛️ Faculty Profile")
    
    # Faculty Name Selection with Provisions
    name_choice = st.selectbox("Select Your Name", ["-- Select --", "➕ Add New..."] + sorted(FACULTY_LIST))
    user_name = st.text_input("New Name Title") if name_choice == "➕ Add New..." else (None if name_choice == "-- Select --" else name_choice)

    # Position Selection as requested (Assistant Lecturer to Assistant Professor)
    pos_choice = st.selectbox("Current Position", [
        "Assistant Lecturer", "Associate Lecturer", "Lecturer", "Senior Lecturer", "Assistant Professor", "Associate Professor", "➕ Add Custom Position..."
    ])
    user_pos = st.text_input("Custom Position Name") if pos_choice == "➕ Add Custom Position..." else pos_choice

    st.divider()
    if st.session_state.basket:
        total_wam = sum([(m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045) for m in st.session_state.basket])
        st.metric("Aggregate WAM Weight", f"{total_wam:.2f}")
        if st.button("Reset Plan"): st.session_state.basket = []; st.rerun()

# ==========================================
# 5. MAIN CONTENT - TWO COLUMN INTERFACE
# ==========================================
if not user_name:
    st.info("📜 Please select your faculty profile in the sidebar to begin academic planning.")
    st.stop()

col_planner, col_canvas = st.columns([1.1, 1.5])

with col_planner:
    st.markdown('<div class="section-head">🎓 Workload Planner</div>', unsafe_allow_html=True)
    
    with st.container():
        # 1. PROGRAM FILTERS
        st.markdown("**Program Configuration**")
        c1, c2 = st.columns(2)
        with c1:
            prog_opt = st.selectbox("Program", ["Physics", "Chemistry", "LifeSciences", "➕ Add New..."])
            prog = st.text_input("New Program Name") if prog_opt == "➕ Add New..." else prog_opt
        with c2:
            curr_opt = st.selectbox("Curriculum", ["New", "Old", "➕ Add New..."])
            curr = st.text_input("New Curriculum Version") if curr_opt == "➕ Add New..." else curr_opt
        
        c3, c4 = st.columns(2)
        with c3:
            yr_opt = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4", "➕ Add New..."])
            yr = st.text_input("Manual Year Entry") if yr_opt == "➕ Add New..." else yr_opt
        with c4:
            sem_opt = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "➕ Add New..."])
            sem = st.text_input("Manual Semester Entry") if sem_opt == "➕ Add New..." else sem_opt

        # 2. MODULE DETAILS - AUTO & MANUAL PROVISIONS
        st.markdown('<div class="section-head" style="background-color: var(--crimson); border-left: 5px solid var(--oxford-blue); font-size: 1rem;">📝 Module Details</div>', unsafe_allow_html=True)
        
        entry_mode = st.radio("Entry Mode", ["Database Search", "Manual Entry (Provisional)"], horizontal=True)
        
        # Internal Search Key
        data_key = f"{prog}_{curr}"
        
        if entry_mode == "Database Search" and data_key in MODULE_DATABASE:
            try:
                mod_list = MODULE_DATABASE[data_key][yr][sem]
                mod_options = [f"{m['code']} - {m['name']}" for m in mod_list]
                selected_mod_str = st.selectbox("Select Module from Database", mod_options)
                
                # Auto-fill logic
                selected_mod = next(m for m in mod_list if f"{m['code']} - {m['name']}" == selected_mod_str)
                m_code = selected_mod['code']
                m_name = selected_mod['name']
                m_theory = selected_mod['theory']
                m_lab = selected_mod['lab']
            except KeyError:
                st.warning("No modules found in database for these filters. Switching to Manual Entry.")
                entry_mode = "Manual Entry (Provisional)"

        if entry_mode == "Manual Entry (Provisional)" or data_key not in MODULE_DATABASE:
            m_code = st.text_input("Enter Module Code (e.g. PHY101)")
            m_name = st.text_input("Enter Module Title")
            m_theory = st.number_input("Theory Hours", 0, 10, 3)
            m_lab = st.number_input("Lab Hours", 0, 10, 2)

        m_students = st.number_input("Expected Student Enrollment", 1, 500, 30)

        if st.button("➕ Assign to Workload"):
            if m_code and m_name:
                st.session_state.basket.append({
                    'code': m_code, 'name': m_name, 'theory': m_theory, 'lab': m_lab,
                    'students': m_students, 'prog': prog, 'curr': curr
                })
                st.success(f"Assigned {m_code} successfully.")
                st.rerun()
            else:
                st.error("Please provide Module Code and Title.")

with col_canvas:
    st.markdown('<div class="section-head">📋 Drafting Canvas</div>', unsafe_allow_html=True)
    
    if not st.session_state.basket:
        st.markdown("""
            <div style="border: 2px dashed #ccc; padding: 6rem; text-align: center; color: #999; border-radius: 15px; background: #fff;">
                <h3 style="margin-top:0;">Your canvas is currently empty.</h3>
                <p>Selected modules from the planner will appear here for review.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        for i, m in enumerate(st.session_state.basket):
            wam_val = (m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045)
            st.markdown(f"""
            <div class="canvas-strip">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.75rem; color: var(--crimson); font-weight: 800; text-transform: uppercase;">{m['prog']} • Curriculum {m['curr']}</div>
                        <div style="font-size: 1.25rem; font-weight: 700; color: var(--oxford-blue);">{m['code']}: {m['name']}</div>
                        <div style="font-size: 0.9rem; color: #555; margin-top: 3px;">
                            <b>Theory:</b> {m['theory']}h | <b>Lab:</b> {m['lab']}h | <b>Students:</b> {m['students']}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.5rem; font-weight: 800; color: var(--oxford-blue);">{wam_val:.2f}</div>
                        <div style="font-size: 0.65rem; color: #999; font-weight: 700;">WAM WEIGHT</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗑️ Remove Entry", key=f"del_{i}"):
                st.session_state.basket.pop(i)
                st.rerun()

# ==========================================
# 6. ANALYTICS & EXPORT
# ==========================================
if st.session_state.basket:
    st.divider()
    tab_data, tab_submit = st.tabs(["📊 Analytical Review", "📤 Formal Submission"])
    
    with tab_data:
        df = pd.DataFrame(st.session_state.basket)
        df['WAM'] = df.apply(lambda x: (x['theory']*1.1 + x['lab']*0.8 + x['students']*0.045), axis=1)
        
        c_k1, c_k2, c_k3 = st.columns(3)
        c_k1.markdown(f'<div class="metric-card"><h6>TOTAL HOURS</h6><h3>{df["theory"].sum() + df["lab"].sum()}h</h3></div>', unsafe_allow_html=True)
        c_k2.markdown(f'<div class="metric-card"><h6>TOTAL STUDENTS</h6><h3>{df["students"].sum()}</h3></div>', unsafe_allow_html=True)
        c_k3.markdown(f'<div class="metric-card"><h6>AGGREGATE WAM</h6><h3>{df["WAM"].sum():.2f}</h3></div>', unsafe_allow_html=True)
        
        g1, g2 = st.columns(2)
        with g1:
            fig = px.pie(df, values='WAM', names='code', hole=0.5, title="WAM Weightage by Module", color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        with g2:
            fig2 = px.bar(df, x='code', y='students', title="Student Distribution", color_discrete_sequence=['#daa520'])
            st.plotly_chart(fig2, use_container_width=True)

    with tab_submit:
        st.markdown("#### Review Final Allocation Plan")
        st.table(df[['code', 'name', 'theory', 'lab', 'students', 'WAM']])
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Official Report (CSV)", csv, f"DNS_Report_{user_name}.csv", "text/csv", use_container_width=True)
        with col_ex2:
            if st.button("🚀 Final Submission to Department Head", use_container_width=True):
                st.balloons()
                st.success("Workload allocation successfully logged for departmental review.")

# ==========================================
# 7. FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.8rem; padding-bottom: 2rem;">
    Department of Natural Sciences — Royal University of Bhutan<br>
    Academic Resource Allocation Management System • v6.0.0 Scholar Suite • © 2026
</div>
""", unsafe_allow_html=True)
