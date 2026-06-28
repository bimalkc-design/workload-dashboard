import streamlit as st
import pandas as pd
from datetime import datetime
import os
import streamlit.components.v1 as components

# ==========================================
# 1. PAGE SETUP & THEME
# ==========================================
st.set_page_config(page_title="DNS Workload Command", page_icon="🎓", layout="wide")

MASTER_LOG = "dns_workload_master.csv"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    :root { --rub-blue: #1a2a6c; --rub-red: #b21f1f; --rub-gold: #daa520; }
    .stApp { background-color: #fdfbf7; }
    
    .dean-header {
        background: linear-gradient(135deg, var(--rub-blue) 0%, var(--rub-red) 100%);
        padding: 2rem; color: white; border-bottom: 5px solid var(--rub-gold);
        text-align: center; margin: -4rem -4rem 2rem -4rem;
    }
    
    .section-head {
        background: var(--rub-blue); color: var(--rub-gold);
        padding: 10px 15px; border-radius: 4px; font-weight: 700; margin-bottom: 1rem;
    }

    .tutor-card-print {
        background: white; border: 2px solid var(--rub-blue);
        padding: 1rem; border-radius: 10px; margin-bottom: 1rem;
        min-height: 220px; font-family: 'Inter', sans-serif;
    }
    .card-header {
        background: var(--rub-blue); color: var(--rub-gold);
        padding: 5px; text-align: center; font-weight: bold;
        border-radius: 5px 5px 0 0; margin: -1rem -1rem 10px -1rem;
        font-size: 0.8rem;
    }
    .card-label { color: var(--rub-red); font-weight: 700; font-size: 0.7rem; text-transform: uppercase; }
    .card-value { color: var(--rub-blue); font-weight: 700; font-size: 1rem; line-height: 1.2; }

    @media print {
        .no-print { display: none !important; }
        .stApp { background: white !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MODULE DATABASE (Truncated for readability)
# ==========================================
MODULE_DATABASE = {
    'Chemistry_Old': {
        'Year 1': {
            'Semester I': [
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
                {'code': 'FCH101', 'name': 'Fundamentals of Inorganic Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'FPH101', 'name': 'Foundations of Physics I', 'theory': 2, 'lab': 3},
                {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0},
            ]
        }
    },
    'Physics_New': { 'Year 1': { 'Semester I': [{'code': 'CME101', 'name': 'Newtonian Mechanics', 'theory': 3, 'lab': 2}] } },
    'LifeSciences_New': { 'Year 1': { 'Semester I': [{'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4}] } }
}

FACULTY_LIST = sorted(["Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan", "Ms. Kuenzang Choki", "Ms. Sangay Yuden", "Mr. Tashi Dendup"])

# ==========================================
# 3. UTILITIES & PERSISTENCE
# ==========================================
def commit_to_master(faculty, position, basket):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = []
    for m in basket:
        data.append({
            "Timestamp": timestamp, "Faculty": faculty, "Rank": position,
            "Code": m['code'], "Module": m['name'], "Type": m['type'],
            "Classroom": m['room'] if m['room'] else "Not Specified", 
            "Theory": m['theory'], "Lab": m['lab'],
            "Students": m['students'], 
            "WAM": round((m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045), 2)
        })
    df = pd.DataFrame(data)
    if not os.path.isfile(MASTER_LOG):
        df.to_csv(MASTER_LOG, index=False)
    else:
        df.to_csv(MASTER_LOG, mode='a', header=False, index=False)

# ==========================================
# 4. SIDEBAR & ADMIN
# ==========================================
with st.sidebar:
    st.markdown("### 🏛️ Faculty Profile")
    user_name = st.selectbox("Your Identity", ["-- Select --", "➕ New..."] + FACULTY_LIST)
    if user_name == "➕ New...": user_name = st.text_input("Enter Full Name")
    
    user_rank = st.selectbox("Designation", ["Assistant Lecturer", "Associate Lecturer", "Lecturer", "Senior Lecturer", "Assistant Professor", "Associate Professor"])
    
    st.divider()
    st.markdown("### 🔒 HoD/Dean Access")
    admin_pass = st.text_input("Admin PIN", type="password")
    is_admin = (admin_pass == "DNS777")

# ==========================================
# 5. ADMIN COMMAND CENTER (CLEAR RECORDS HERE)
# ==========================================
if is_admin:
    st.markdown("<div class='dean-header'><h1>HoD Master Audit Terminal</h1></div>", unsafe_allow_html=True)
    if os.path.isfile(MASTER_LOG):
        m_df = pd.read_csv(MASTER_LOG)
        st.markdown("### All Departmental Submissions")
        st.dataframe(m_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Export Master CSV", m_df.to_csv(index=False), "MASTER_WORKLOAD.csv")
        with col2:
            if st.button("🔥 PURGE ALL RECORDS (PERMANENT)", type="secondary"):
                os.remove(MASTER_LOG)
                st.success("Database cleared successfully.")
                st.rerun()
    else:
        st.info("Database file not found. It will be created upon the first submission.")
    st.stop()

# ==========================================
# 6. TUTOR PLANNER VIEW
# ==========================================
st.markdown("""
<div class="dean-header">
    <div style="font-size: 0.8rem; letter-spacing: 3px; color: #daa520; font-weight: 700;">ROYAL UNIVERSITY OF BHUTAN</div>
    <h1>Department of Natural Sciences</h1>
    <p>Workload Selection Portal — Cycle 2026</p>
</div>
""", unsafe_allow_html=True)

if user_name == "-- Select --" or not user_name:
    st.info("👋 Please authenticate via the sidebar to access the planner.")
    st.stop()

if 'basket' not in st.session_state: st.session_state.basket = []

tab_plan, tab_cards = st.tabs(["🎯 Workload Drafting", "📋 My Printable Cards"])

with tab_plan:
    c_in, c_pre = st.columns([1, 1.5])
    with c_in:
        st.markdown('<div class="section-head">🖊️ Entry Details</div>', unsafe_allow_html=True)
        prog = st.selectbox("Program", ["Physics", "Chemistry", "LifeSciences"])
        curr = st.selectbox("Curriculum", ["New", "Old"])
        yr = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
        sem = st.selectbox("Semester", ["Semester I", "Semester II"])
        
        db_key = f"{prog}_{curr}"
        m_code, m_name = "", ""
        if db_key in MODULE_DATABASE and yr in MODULE_DATABASE[db_key] and sem in MODULE_DATABASE[db_key][yr]:
            mods = MODULE_DATABASE[db_key][yr][sem]
            sel_mod = st.selectbox("Select Module", [f"{m['code']} - {m['name']}" for m in mods] + ["Manual Entry"])
            if sel_mod != "Manual Entry":
                entry = next(m for m in mods if f"{m['code']} - {m['name']}" == sel_mod)
                m_code, m_name = entry['code'], entry['name']
        
        if m_code == "":
            m_code = st.text_input("Module Code")
            m_name = st.text_input("Module Name")
            
        m_type = st.selectbox("Component", ["Theory + Lab", "Theory Only", "Lab Only"])
        m_room = st.text_input("Classroom/Venue")
        m_st = st.number_input("Students", 1, 300, 30)
        m_th = st.number_input("Theory Hours", 0, 10, 3)
        m_lb = st.number_input("Lab Hours", 0, 10, 0)

        if st.button("➕ Add to My Draft", type="primary"):
            st.session_state.basket.append({'code': m_code, 'name': m_name, 'type': m_type, 'room': m_room, 'theory': m_th, 'lab': m_lb, 'students': m_st})
            st.rerun()

    with c_pre:
        st.markdown('<div class="section-head">📋 My Draft Canvas</div>', unsafe_allow_html=True)
        
        if st.session_state.basket:
            # CLEAR DRAFT BUTTON
            if st.button("🗑️ Clear Entire Draft"):
                st.session_state.basket = []
                st.rerun()
                
            for i, m in enumerate(st.session_state.basket):
                st.markdown(f"✅ **{m['code']}** - {m['name']} ({m['room']})")
            
            st.divider()
            if st.button("🚀 SUBMIT FINAL PLAN TO MASTER LOG", type="primary"):
                commit_to_master(user_name, user_rank, st.session_state.basket)
                st.balloons()
                st.session_state.basket = []
                st.success("Submitted successfully! Go to the 'Printable Cards' tab to see your reference.")
                st.rerun()
        else:
            st.info("Draft is empty.")

# ==========================================
# 7. PRINTABLE REFERENCE CARDS
# ==========================================
with tab_cards:
    st.markdown('<div class="no-print"><h3>💳 Reference Cards</h3><p>Submit your drafting plan to update these cards.</p></div>', unsafe_allow_html=True)
    
    if os.path.isfile(MASTER_LOG):
        all_data = pd.read_csv(MASTER_LOG).fillna("Not Specified")
        my_data = all_data[all_data['Faculty'] == user_name]
        
        if not my_data.empty:
            # Filter to show only the MOST RECENT submission session to avoid clutter
            latest_timestamp = my_data['Timestamp'].max()
            display_data = my_data[my_data['Timestamp'] == latest_timestamp]
            
            st.markdown(f"**Showing Cards for Submission Date:** `{latest_timestamp}`")
            
            if st.button("🖨️ Print These Cards", type="primary"):
                components.html("<script>window.print();</script>", height=0)

            grid = st.columns(3)
            for idx, row in display_data.iterrows():
                with grid[idx % 3]:
                    st.markdown(f"""
                    <div class="tutor-card-print">
                        <div class="card-header">{row['Rank'].upper()} REFERENCE</div>
                        <span class="card-label">Faculty</span><br><span class="card-value">{row['Faculty']}</span><br>
                        <span class="card-label">Module</span><br><span class="card-value">{row['Code']} - {row['Module']}</span><br>
                        <span class="card-label">Venue</span><br><span class="card-value" style="color:var(--rub-red);">{row['Classroom']}</span><br>
                        <hr style="margin: 8px 0; border: 0.5px solid #eee;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
                            <div><b>{row['Type']}</b></div>
                            <div>{row['Theory']}T | {row['Lab']}L</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No submitted entries found for your identity.")
    else:
        st.info("The master database is currently empty.")

# ==========================================
# 8. FOOTER
# ==========================================
st.markdown("<br><hr><div style='text-align: center; color: #7f8c8d; font-size: 0.8rem;'>Department of Natural Sciences • Dean's Command Portal • Cycle 2026</div>", unsafe_allow_html=True)
