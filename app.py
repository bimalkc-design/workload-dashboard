import streamlit as st
import pandas as pd
from datetime import datetime
import os
import streamlit.components.v1 as components

# ==========================================
# 1. PAGE SETUP & ACADEMIC THEME
# ==========================================
st.set_page_config(page_title="DNS Workload Command", page_icon="⚖️", layout="wide")

MASTER_LOG = "dns_workload_master.csv"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    :root { 
        --rub-blue: #1a2a6c; 
        --rub-red: #b21f1f; 
        --rub-gold: #daa520; 
        --parchment: #fdfbf7;
    }
    
    .stApp { background-color: var(--parchment); }
    
    .main-header {
        background: linear-gradient(135deg, var(--rub-blue) 0%, var(--rub-red) 100%);
        padding: 2rem; color: white; border-bottom: 5px solid var(--rub-gold);
        text-align: center; margin: -4rem -4rem 2rem -4rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .section-head {
        background: var(--rub-blue); color: var(--rub-gold);
        padding: 10px 15px; border-radius: 4px; font-weight: 700; margin-bottom: 1rem;
        font-family: 'Playfair Display', serif; border-left: 5px solid var(--rub-gold);
    }

    .tutor-card-print {
        background: white; border: 2px solid var(--rub-blue);
        padding: 1rem; border-radius: 10px; margin-bottom: 1rem;
        min-height: 240px; font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .card-header {
        background: var(--rub-blue); color: var(--rub-gold);
        padding: 5px; text-align: center; font-weight: bold;
        border-radius: 5px 5px 0 0; margin: -1rem -1rem 10px -1rem;
        font-size: 0.8rem; letter-spacing: 1px;
    }
    .card-label { color: var(--rub-red); font-weight: 700; font-size: 0.7rem; text-transform: uppercase; }
    .card-value { color: var(--rub-blue); font-weight: 700; font-size: 1rem; line-height: 1.2; }

    div.stButton > button {
        background-color: var(--rub-blue); color: white; border-radius: 6px;
        font-weight: 700; width: 100%; border: none; padding: 0.6rem;
        transition: all 0.3s;
    }
    div.stButton > button:hover { background-color: var(--rub-gold); color: black; }

    @media print { .no-print { display: none !important; } .stApp { background: white !important; } }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. COMPLETE DATA INTEGRATION
# ==========================================
FACULTY_LIST = sorted([
    "Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan", "Ms. Kuenzang Choki", 
    "Ms. Sangay Yuden", "Mr. Tashi Dendup", "Shacha Thinley", "Nachiketa Homchaudhuri", 
    "Mon Bahadur Ghalley", "Dr. Karma Tenzin", "Rit Wik Sharma", "Ugyen Dorji Tamang", 
    "Karma Wangchuck", "Mohan Singh Rana", "Tshering Dekar", "Bimal Kumar Chetri", 
    "Sonam Tobgay", "Dechen Lhendup", "S. Chitra", "DS-Y", "Paul Raj"
])

MODULE_DATABASE = {
    'Chemistry_Old': {
        'Year 1': {
            'Semester I': [{'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0}, {'code': 'FCH101', 'name': 'Fundamentals of Inorganic Chemistry', 'theory': 3, 'lab': 2}, {'code': 'FPH101', 'name': 'Foundations of Physics I', 'theory': 2, 'lab': 3}, {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0}],
            'Semester II': [{'code': 'FCH102', 'name': 'Fundamentals of Physical Chemistry', 'theory': 3, 'lab': 2}, {'code': 'FCH103', 'name': 'Fundamentals of Organic Chemistry', 'theory': 3, 'lab': 2}]
        },
        'Year 2': {
            'Semester III': [{'code': 'ICH101', 'name': 'Inorganic Chemistry I', 'theory': 3, 'lab': 3}, {'code': 'PCH201', 'name': 'Physical Chemistry I', 'theory': 3, 'lab': 3}],
            'Semester IV': [{'code': 'OCH202', 'name': 'Organic Chemistry II', 'theory': 3, 'lab': 3}, {'code': 'PCH202', 'name': 'Physical Chemistry II', 'theory': 3, 'lab': 3}]
        },
        'Year 3': {
            'Semester V': [{'code': 'OCH303', 'name': 'Organic Chemistry III', 'theory': 3, 'lab': 3}, {'code': 'PCH303', 'name': 'Physical Chemistry III', 'theory': 3, 'lab': 3}]
        }
    },
    'Physics_Old': {
        'Year 1': { 'Semester I': [{'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0}, {'code': 'MEC101', 'name': 'Mechanics I', 'theory': 3, 'lab': 2}] },
        'Year 3': { 'Semester V': [{'code': 'MPH303', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3}, {'code': 'MPH304', 'name': 'Quantum Physics', 'theory': 4, 'lab': 0}] }
    },
    'LifeSciences_Old': {
        'Year 1': { 'Semester I': [{'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4}, {'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2}] },
        'Year 2': { 'Semester III': [{'code': 'BTS202', 'name': 'Plant Anatomy', 'theory': 3, 'lab': 3}] },
        'Year 3': { 'Semester V': [{'code': 'BTS304', 'name': 'Fungi/Plant Pathology', 'theory': 3, 'lab': 3}, {'code': 'GRS301', 'name': 'GIS and Remote Sensing', 'theory': 2, 'lab': 3}, {'code': 'ZLS304', 'name': 'Vertebrate Physiology', 'theory': 3, 'lab': 3}] }
    },
    'Physics_New': { 'Year 1': { 'Semester I': [{'code': 'CME101', 'name': 'Newtonian Mechanics', 'theory': 3, 'lab': 2}] } },
    'LifeSciences_New': { 'Year 1': { 'Semester I': [{'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4}] } }
}

# ==========================================
# 3. UTILITIES
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
# 4. SIDEBAR IDENTITY
# ==========================================
with st.sidebar:
    st.markdown("### 🏛️ Faculty Identity")
    user_name = st.selectbox("Your Identity", ["-- Select --", "➕ New Name..."] + FACULTY_LIST)
    if user_name == "➕ New Name...": user_name = st.text_input("Enter Full Name")
    
    user_rank = st.selectbox("Position", ["Assistant Lecturer", "Associate Lecturer", "Lecturer", "Senior Lecturer", "Assistant Professor", "Associate Professor", "Dean", "HoD"])
    
    st.divider()
    st.markdown("### 🔒 Administrative")
    admin_pass = st.text_input("HoD PIN", type="password")
    is_admin = (admin_pass == "DNS777")

# ==========================================
# 5. ADMIN COMMAND CENTER (HoD VIEW)
# ==========================================
if is_admin:
    st.markdown("<div class='main-header'><h1>Department Audit Console</h1></div>", unsafe_allow_html=True)
    if os.path.isfile(MASTER_LOG):
        m_df = pd.read_csv(MASTER_LOG)
        st.dataframe(m_df, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1: st.download_button("📥 Export Master Log", m_df.to_csv(index=False), "DNS_MASTER.csv")
        with c2: 
            if st.button("🔥 PURGE ALL RECORDS"): 
                if os.path.exists(MASTER_LOG): os.remove(MASTER_LOG)
                st.success("Database Reset."); st.rerun()
    else: st.info("Database empty.")
    st.stop()

# ==========================================
# 6. TUTOR PORTAL
# ==========================================
st.markdown(f"""
<div class="main-header">
    <div style="font-size: 0.8rem; letter-spacing: 3px; color: var(--rub-gold); font-weight: 700;">ROYAL UNIVERSITY OF BHUTAN</div>
    <h1>Department of Natural Sciences</h1>
    <p>Academic Resource & Workload Portal — Autumn 2026</p>
</div>
""", unsafe_allow_html=True)

if user_name == "-- Select --" or not user_name:
    st.info("👋 Please select your identity in the sidebar to begin.")
    st.stop()

if 'basket' not in st.session_state: st.session_state.basket = []

tab_plan, tab_cards = st.tabs(["🎯 Drafting Canvas", "📋 My Printable Cards"])

with tab_plan:
    c_in, c_pre = st.columns([1.1, 1.5])
    with c_in:
        st.markdown('<div class="section-head">🖊️ Selection Filters</div>', unsafe_allow_html=True)
        prog_display = st.selectbox("Program Area", ["Physics", "Chemistry", "Life Sciences", "➕ New..."])
        prog_map = {"Physics": "Physics", "Chemistry": "Chemistry", "Life Sciences": "LifeSciences"}
        prog = prog_map.get(prog_display, prog_display)
        
        curr = st.selectbox("Curriculum", ["New", "Old"])
        yr = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
        sem = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI"])
        
        db_key = f"{prog}_{curr}"
        m_code, m_name, d_th, d_lb = "", "", 3, 0
        
        if db_key in MODULE_DATABASE and yr in MODULE_DATABASE[db_key] and sem in MODULE_DATABASE[db_key][yr]:
            mods = MODULE_DATABASE[db_key][yr][sem]
            mod_names = [f"{m['code']} - {m['name']}" for m in mods]
            sel_mod = st.selectbox("Select Module", mod_names + ["➕ Manual Entry"])
            if sel_mod != "➕ Manual Entry":
                entry = next(m for m in mods if f"{m['code']} - {m['name']}" == sel_mod)
                m_code, m_name, d_th, d_lb = entry['code'], entry['name'], entry['theory'], entry['lab']
        else:
            st.warning("Filters not found in database. Manual entry enabled.")
            sel_mod = "➕ Manual Entry"

        st.markdown('<div class="section-head" style="background:#b21f1f;">📝 Specific Details</div>', unsafe_allow_html=True)
        if sel_mod == "➕ Manual Entry":
            m_code = st.text_input("Manual Code", placeholder="e.g. BIO101")
            m_name = st.text_input("Manual Name", placeholder="e.g. Microbiology")
        else: st.write(f"**Target:** {m_code} - {m_name}")
        
        m_type = st.selectbox("Component", ["Theory + Lab", "Theory Only", "Lab Only"])
        m_room = st.text_input("Classroom / Venue")
        c3, c4 = st.columns(2)
        with c3: m_th = st.number_input("Theory Hours", 0, 12, d_th)
        with c4: m_lb = st.number_input("Lab Hours", 0, 12, d_lb)
        m_st = st.number_input("Enrollment", 1, 300, 30)

        if st.button("➕ Add to My Draft", type="primary"):
            st.session_state.basket.append({'code': m_code, 'name': m_name, 'type': m_type, 'room': m_room, 'theory': m_th, 'lab': m_lb, 'students': m_st})
            st.rerun()

    with c_pre:
        st.markdown('<div class="section-head">📋 Drafting Canvas</div>', unsafe_allow_html=True)
        if st.session_state.basket:
            if st.button("🗑️ Clear Entire Draft"): st.session_state.basket = []; st.rerun()
            for i, m in enumerate(st.session_state.basket):
                wam = (m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045)
                st.markdown(f"✅ **{m['code']}**: {m['name']} ({m['room']}) - WAM: {wam:.2f}")
                if st.button(f"Remove {m['code']}", key=f"r_{i}"): st.session_state.basket.pop(i); st.rerun()
            
            st.divider()
            if st.button("🚀 SUBMIT FINAL PLAN", type="primary"):
                commit_to_master(user_name, user_rank, st.session_state.basket)
                st.balloons(); st.session_state.basket = []; st.rerun()
        else: st.info("Canvas is empty.")

# ==========================================
# 7. PRINTABLE CARDS
# ==========================================
with tab_cards:
    if os.path.isfile(MASTER_LOG):
        all_data = pd.read_csv(MASTER_LOG).fillna("Not Specified")
        my_data = all_data[all_data['Faculty'] == user_name]
        
        if not my_data.empty:
            # AUTO-REPAIR Logic for older CSV formats
            if 'Timestamp' in my_data.columns:
                latest = my_data['Timestamp'].max()
                display_data = my_data[my_data['Timestamp'] == latest]
            else:
                st.warning("⚠️ Database format is older. Showing all historical records.")
                display_data = my_data
            
            if st.button("🖨️ Print My Tutor Cards", type="primary"):
                components.html("<script>window.print();</script>", height=0)

            grid = st.columns(3)
            for idx, row in display_data.reset_index().iterrows():
                with grid[idx % 3]:
                    st.markdown(f"""<div class="tutor-card-print"><div class="card-header">{row['Rank'].upper()} REFERENCE</div>
                        <span class="card-label">Tutor</span><br><span class="card-value">{row['Faculty']}</span><br>
                        <span class="card-label">Module</span><br><span class="card-value">{row['Code']} - {row['Module']}</span><br>
                        <span class="card-label">Venue</span><br><span class="card-value" style="color:var(--rub-red);">{row['Classroom']}</span><br>
                        <hr style="margin: 8px 0; border: 0.5px solid #eee;"><div style="display:flex; justify-content:space-between; font-size:0.8rem;">
                        <div><b>{row['Type']}</b></div><div>{row['Theory']}T | {row['Lab']}L</div></div></div>""", unsafe_allow_html=True)
        else: st.info("No submitted entries found.")
    else: st.info("Database empty.")
