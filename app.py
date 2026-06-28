import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ==========================================
# 1. PAGE SETUP & THEME
# ==========================================
st.set_page_config(page_title="DNS Workload Command", page_icon="🎓", layout="wide")

# Persistent Log Path
MASTER_LOG = "dns_workload_master.csv"

# Styling Logic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    :root { --rub-blue: #1a2a6c; --rub-red: #b21f1f; --rub-gold: #daa520; --card-bg: #ffffff; }
    
    .stApp { background-color: #f8f9fa; }
    
    /* Executive Header */
    .dean-header {
        background: linear-gradient(135deg, var(--rub-blue) 0%, var(--rub-red) 100%);
        padding: 2.5rem; color: white; border-bottom: 5px solid var(--rub-gold);
        text-align: center; margin: -4rem -4rem 2rem -4rem;
    }
    
    /* Academic Card Styling for Tutors */
    .tutor-card {
        background: white; border-top: 5px solid var(--rub-blue);
        padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-right: 1px solid #eee;
    }
    .card-label { color: var(--rub-red); font-weight: 700; font-size: 0.7rem; text-transform: uppercase; }
    .card-value { color: var(--rub-blue); font-weight: 700; font-size: 1.1rem; }
    
    /* Admin Section */
    .admin-zone {
        background: #000; color: #daa520; padding: 1rem;
        border-radius: 5px; font-family: monospace; margin-bottom: 2rem;
    }
    
    div.stButton > button {
        background-color: var(--rub-blue); color: white; border-radius: 4px;
        font-weight: 700; width: 100%; border: none;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PERSISTENCE LOGIC (For HoD/Dean)
# ==========================================
def commit_to_master(faculty, position, basket):
    """Saves records to the permanent server file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    data = []
    for m in basket:
        data.append({
            "Date": timestamp, "Faculty": faculty, "Rank": position,
            "Code": m['code'], "Module": m['name'], "Type": m['type'],
            "Classroom": m['room'], "Theory": m['theory'], "Lab": m['lab'],
            "Students": m['students'], "WAM": round((m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045), 2)
        })
    df = pd.DataFrame(data)
    if not os.path.isfile(MASTER_LOG):
        df.to_csv(MASTER_LOG, index=False)
    else:
        df.to_csv(MASTER_LOG, mode='a', header=False, index=False)

# ==========================================
# 3. SIDEBAR & ACCESS CONTROL
# ==========================================
with st.sidebar:
    st.markdown("### 👤 User Identification")
    user_name = st.selectbox("Select Name", ["-- Select --", "➕ New..."] + ["Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan", "Ms. Kuenzang Choki", "Mr. Tashi Dendup"])
    if user_name == "➕ New...": user_name = st.text_input("Enter Full Name")
    
    user_rank = st.selectbox("Designation", ["Assistant Lecturer", "Associate Lecturer", "Lecturer", "Senior Lecturer", "Assistant Professor", "Associate Professor"])
    
    st.divider()
    st.markdown("### 🔒 Dean / HoD Access")
    admin_pass = st.text_input("Admin PIN", type="password")
    is_admin = (admin_pass == "DNS777") # Example Secure Code

# ==========================================
# 4. ADMIN DASHBOARD (HoD/DEAN VIEW)
# ==========================================
if is_admin:
    st.markdown("<div class='dean-header'><h1>Administrative Command Center</h1><p>Master Workload Records & Export</p></div>", unsafe_allow_html=True)
    if os.path.isfile(MASTER_LOG):
        m_df = pd.read_csv(MASTER_LOG)
        
        # Dashboard Overview
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Submissions", len(m_df))
        c2.metric("Total Faculty Logged", m_df['Faculty'].nunique())
        c3.metric("Avg Dept WAM", round(m_df['WAM'].mean(), 2))
        
        st.markdown("### 📄 Master Audit Log")
        st.dataframe(m_df, use_container_width=True)
        
        # Download Provison
        csv_data = m_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD COMPLETE DEPARTMENTAL CSV", csv_data, f"DNS_Master_Report_{datetime.now().year}.csv", "text/csv")
        
        if st.button("Purge Database (Caution!)"):
            os.remove(MASTER_LOG)
            st.rerun()
    else:
        st.info("The Master Log is currently empty. No submissions recorded.")
    st.stop()

# ==========================================
# 5. TUTOR PLANNER VIEW
# ==========================================
st.markdown("""
<div class="dean-header">
    <div style="font-size: 0.8rem; letter-spacing: 3px; color: #daa520; font-weight: 700;">ROYAL UNIVERSITY OF BHUTAN</div>
    <h1>Department of Natural Sciences</h1>
    <p>Academic Resource & Workload Portal</p>
</div>
""", unsafe_allow_html=True)

if user_name == "-- Select --" or not user_name:
    st.warning("📜 Authentication required. Please identify yourself in the sidebar.")
    st.stop()

if 'basket' not in st.session_state: st.session_state.basket = []

tab_plan, tab_cards = st.tabs(["🎯 Drafting Plan", "📋 My Printable Cards"])

with tab_plan:
    col_in, col_pre = st.columns([1, 1.5])
    
    with col_in:
        st.markdown("### 🖊️ Entry Details")
        with st.container(border=True):
            m_code = st.text_input("Module Code", placeholder="e.g. CHE101")
            m_name = st.text_input("Module Name", placeholder="e.g. Organic Chemistry")
            
            c1, c2 = st.columns(2)
            with c1: m_type = st.selectbox("Module Type", ["Theory Only", "Lab Only", "Theory + Lab"])
            with c2: m_room = st.text_input("Classroom Name", placeholder="e.g. Sc. Hall 1")
            
            c3, c4, c5 = st.columns(3)
            with c3: m_th = st.number_input("Theory (h)", 0, 12, 3)
            with c4: m_lb = st.number_input("Lab (h)", 0, 12, 0)
            with c5: m_st = st.number_input("Students", 1, 300, 30)
            
            if st.button("➕ ADD TO MY LIST"):
                st.session_state.basket.append({
                    'code': m_code.upper(), 'name': m_name, 'type': m_type,
                    'room': m_room, 'theory': m_th, 'lab': m_lb, 'students': m_st
                })
                st.rerun()

    with col_pre:
        st.markdown("### 📋 Current Draft")
        if not st.session_state.basket:
            st.info("Your draft is currently empty.")
        else:
            for i, m in enumerate(st.session_state.basket):
                wam = (m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045)
                st.markdown(f"""
                <div class="tutor-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <span class="card-label">Module:</span> <span class="card-value">{m['code']}</span><br>
                            <span class="card-label">Type:</span> <span style="font-size:0.9rem;">{m['type']}</span> | 
                            <span class="card-label">Room:</span> <span style="font-size:0.9rem;">{m['room']}</span>
                        </div>
                        <div style="text-align:right">
                            <span class="card-label">WAM weight</span><br><span style="font-size:1.5rem; color:var(--rub-red); font-weight:800;">{wam:.2f}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🚀 SUBMIT FOR FINAL APPROVAL"):
                commit_to_master(user_name, user_rank, st.session_state.basket)
                st.balloons()
                st.success("Workload successfully committed to the Master Departmental Log.")
                st.session_state.basket = []

# ==========================================
# 6. PRINTABLE TUTOR CARDS
# ==========================================
with tab_cards:
    st.markdown("### 💳 Workload Reference Cards")
    st.caption("Instructions: These cards are designed for print/carry. Right-click page and 'Print to PDF' to save them.")
    
    if os.path.isfile(MASTER_LOG):
        all_data = pd.read_csv(MASTER_LOG)
        my_data = all_data[all_data['Faculty'] == user_name]
        
        if my_data.empty:
            st.warning("No submitted modules found for your name in the database.")
        else:
            grid = st.columns(3)
            for idx, row in my_data.iterrows():
                with grid[idx % 3]:
                    st.markdown(f"""
                    <div style="background: white; border: 2px solid var(--rub-blue); border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <div style="background: var(--rub-blue); color: var(--rub-gold); padding: 5px; text-align: center; font-weight: bold; border-radius: 5px 5px 0 0; margin: -15px -15px 10px -15px;">
                            DNS TUTOR CARD
                        </div>
                        <span class="card-label">Module</span><br><span class="card-value">{row['Code']}</span><br>
                        <span class="card-label">Room</span><br><span class="card-value" style="color:var(--rub-red);">{row['Classroom']}</span><br>
                        <hr style="margin: 10px 0;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
                            <div><b>{row['Type']}</b></div>
                            <div>{row['Theory']}T | {row['Lab']}L</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.download_button("📥 Download My Submitted List (CSV)", my_data.to_csv(index=False), f"My_Workload_{user_name}.csv", "text/csv")
    else:
        st.info("Submit your plan first to generate printable cards.")

# ==========================================
# 7. FOOTER
# ==========================================
st.markdown("<br><hr><div style='text-align: center; color: #7f8c8d; font-size: 0.8rem;'>Department of Natural Sciences • Dean's Command Portal • Cycle 2026</div>", unsafe_allow_html=True)
