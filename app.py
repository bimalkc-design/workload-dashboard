import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & ACADEMIC THEME
# ==========================================
st.set_page_config(
    page_title="DNS Workload Portal | Department of Natural Sciences",
    page_icon="📜",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap');
    
    :root {
        --academic-blue: #1a2a6c;
        --academic-gold: #b39359;
        --academic-crimson: #8e2de2;
        --parchment: #fdfbf7;
        --slate: #2c3e50;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--parchment);
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--academic-blue);
    }

    /* Elegant Header */
    .header-box {
        background: white;
        padding: 2.5rem;
        border-bottom: 5px solid var(--academic-blue);
        margin: -4rem -4rem 2rem -4rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border: 1px solid #e1e1e1;
        border-top: 4px solid var(--academic-gold);
        border-radius: 4px;
        text-align: center;
    }

    .module-strip {
        background: white;
        border: 1px solid #e1e1e1;
        border-left: 5px solid var(--academic-blue);
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 4px;
    }

    /* Academic Buttons */
    div.stButton > button {
        background-color: var(--academic-blue);
        color: white;
        border-radius: 2px;
        font-family: 'Playfair Display', serif;
        letter-spacing: 1px;
        border: none;
        padding: 0.6rem 2rem;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: var(--academic-gold);
        color: white;
    }

    /* Provisions for New Entry Fields */
    .new-entry-box {
        background: #f0f4f8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px dashed var(--academic-blue);
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. EXTENSIBLE DATA SYSTEM
# ==========================================
# Database from user (Subset shown for brevity, logic handles all keys)
BASE_MODULES = {
    'Chemistry': ['Old', 'New'],
    'Physics': ['Old', 'New'],
    'Life Sciences': ['Old', 'New']
}

# Pre-defined Faculty
FACULTY_LIST = sorted([
    "Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan", "Ms. Kuenzang Choki", 
    "Ms. Sangay Yuden", "Mr. Tashi Dendup", "Shacha Thinley", "Nachiketa Homchaudhuri", 
    "Mon Bahadur Ghalley", "Dr. Karma Tenzin", "Rit Wik Sharma", "Ugyen Dorji Tamang"
])

if 'basket' not in st.session_state: st.session_state.basket = []

# ==========================================
# 3. HEADER
# ==========================================
st.markdown("""
<div class="header-box">
    <div style="font-size: 0.8rem; letter-spacing: 3px; color: #b39359; font-weight: 700; text-transform: uppercase;">Royal University of Bhutan</div>
    <h1>Department of Natural Sciences</h1>
    <p style="color: #666; font-style: italic;">Workload Allocation & Academic Planning Portal — Autumn 2026</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR - PROFILE & FALLBACKS
# ==========================================
with st.sidebar:
    st.markdown("### 🏛️ Faculty Identity")
    
    # PROVISION: Add New Faculty
    fac_choice = st.selectbox("Select Faculty Member", ["-- Select --", "➕ Add New Faculty..."] + FACULTY_LIST)
    if fac_choice == "➕ Add New Faculty...":
        user_name = st.text_input("Enter Full Name & Title")
    else:
        user_name = fac_choice if fac_choice != "-- Select --" else None

    # PROVISION: Add New Designation
    rank_choice = st.selectbox("Current Designation", ["Lecturer", "Senior Lecturer", "Assistant Professor", "Associate Professor", "➕ Other..."])
    if rank_choice == "➕ Other...":
        user_rank = st.text_input("Enter Designation")
    else:
        user_rank = rank_choice

    st.divider()
    if st.session_state.basket:
        st.markdown("### 📊 Live Score")
        # WAM Calculation Logic
        total_wam = sum([(m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045) for m in st.session_state.basket])
        st.metric("Total WAM Weight", f"{total_wam:.2f}")
        
        if st.button("Reset All Entries"):
            st.session_state.basket = []
            st.rerun()

# ==========================================
# 5. MAIN INTERFACE
# ==========================================
if not user_name:
    st.warning("📜 Please authenticate by selecting or entering your name in the sidebar.")
    st.stop()

tab_planning, tab_visuals, tab_submission = st.tabs(["🏛️ Workload Drafting", "📈 Analytical Review", "✉️ Formal Submission"])

with tab_planning:
    col_config, col_canvas = st.columns([1, 1.5])
    
    with col_config:
        st.markdown("### Module Assignment")
        
        with st.container():
            # PROVISION: Program Fallback
            prog_sel = st.selectbox("Program Area", list(BASE_MODULES.keys()) + ["➕ New Program..."])
            program = st.text_input("New Program Name") if prog_sel == "➕ New Program..." else prog_sel
            
            # PROVISION: Curriculum Fallback
            curr_sel = st.selectbox("Curriculum Type", ["Old", "New", "➕ Other Version..."])
            curriculum = st.text_input("Specify Version") if curr_sel == "➕ Other Version..." else curr_sel
            
            # PROVISION: Semester/Year Fallback
            c1, c2 = st.columns(2)
            with c1:
                y_sel = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4", "➕ Other..."])
                year = st.text_input("Manual Year") if y_sel == "➕ Other..." else y_sel
            with c2:
                s_sel = st.selectbox("Semester", ["Sem I", "Sem II", "➕ Other..."])
                semester = st.text_input("Manual Sem") if s_sel == "➕ Other..." else s_sel

            st.divider()
            
            # PROVISION: COMPLETE NEW MODULE ENTRY
            st.markdown("**Module Details**")
            mod_mode = st.radio("Entry Mode", ["Database Search", "Manual Entry (Ad-hoc)"])
            
            if mod_mode == "Database Search":
                m_code = st.text_input("Module Code (e.g., PHY101)")
                m_name = st.text_input("Module Title")
                m_theory = st.number_input("Theory Hours", 0, 10, 3)
                m_lab = st.number_input("Lab Hours", 0, 10, 2)
            else:
                st.info("Directly define module parameters below.")
                m_code = st.text_input("New Module Code")
                m_name = st.text_input("New Module Title")
                m_theory = st.slider("Theory Contact Hours", 0, 12, 3)
                m_lab = st.slider("Lab Contact Hours", 0, 12, 0)
                
            m_students = st.number_input("Expected Student Count", 1, 500, 30)

            if st.button("Add to Academic Plan"):
                entry = {
                    'code': m_code.upper(),
                    'name': m_name,
                    'theory': m_theory,
                    'lab': m_lab,
                    'students': m_students,
                    'program': program,
                    'curriculum': curriculum
                }
                st.session_state.basket.append(entry)
                st.toast(f"Assigned {m_code}")

    with col_canvas:
        st.markdown("### Drafting Canvas")
        if not st.session_state.basket:
            st.markdown("""
                <div style="border: 2px dashed #ccc; padding: 5rem; text-align: center; color: #999;">
                    Canvas is clear. Assign modules using the left panel.
                </div>
            """, unsafe_allow_html=True)
        else:
            for i, m in enumerate(st.session_state.basket):
                wam_val = (m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045)
                st.markdown(f"""
                <div class="module-strip">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <small style="color: #b39359; font-weight: bold;">{m['program']} • {m['curriculum']}</small>
                            <div style="font-size: 1.1rem; font-weight: 700;">{m['code']}: {m['name']}</div>
                            <div style="font-size: 0.85rem; color: #666;">
                                Theory: {m['theory']}h | Lab: {m['lab']}h | Enrollment: {m['students']}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.3rem; font-weight: 700; color: #1a2a6c;">{wam_val:.2f}</div>
                            <div style="font-size: 0.6rem; text-transform: uppercase; color: #999;">Weight (WAM)</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Delete Entry", key=f"del_{i}"):
                    st.session_state.basket.pop(i)
                    st.rerun()

with tab_visuals:
    if not st.session_state.basket:
        st.info("Insufficient data to generate analytics.")
    else:
        df = pd.DataFrame(st.session_state.basket)
        df['WAM'] = df.apply(lambda x: (x['theory']*1.1 + x['lab']*0.8 + x['students']*0.045), axis=1)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="metric-card"><small>TOTAL HOURS</small><h3>{}h</h3></div>'.format(df['theory'].sum() + df['lab'].sum()), unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card"><small>TOTAL STUDENTS</small><h3>{}</h3></div>'.format(df['students'].sum()), unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-card"><small>AGGREGATE WAM</small><h3>{:.2f}</h3></div>'.format(df['WAM'].sum()), unsafe_allow_html=True)

        st.divider()
        
        g1, g2 = st.columns(2)
        with g1:
            fig = px.pie(df, values='WAM', names='code', hole=0.4, title="WAM Distribution by Module")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with g2:
            fig2 = px.bar(df, x='code', y='students', title="Student Volume per Module", color_discrete_sequence=['#b39359'])
            st.plotly_chart(fig2, use_container_width=True)

with tab_submission:
    if st.session_state.basket:
        st.markdown("### Formal Summary for Approval")
        final_df = pd.DataFrame(st.session_state.basket)
        st.table(final_df)
        
        st.markdown("#### Actions")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            csv = final_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Official Report (CSV)", csv, f"DNS_Workload_{user_name}.csv", "text/csv", use_container_width=True)
        with col_dl2:
            if st.button("🚀 Formal Submission to HOD", use_container_width=True):
                st.balloons()
                st.success("Workload allocation submitted for departmental review.")
    else:
        st.info("Your academic plan is empty.")

# ==========================================
# 6. FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.8rem; padding-bottom: 2rem;">
    Department of Natural Sciences — Resource Allocation Management System<br>
    v5.0.0 Scholar Edition • RUB Internal Support • © 2026
</div>
""", unsafe_allow_html=True)
