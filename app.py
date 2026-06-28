import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ==========================================
# 1. PAGE SETUP & THEME
# ==========================================
st.set_page_config(page_title="DNS Workload Command", page_icon="🎓", layout="wide")

# Persistent Log Path (This is where HoD downloads the data)
MASTER_LOG = "dns_workload_master.csv"

# Styling Logic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    :root { --rub-blue: #1a2a6c; --rub-red: #b21f1f; --rub-gold: #daa520; }
    
    .stApp { background-color: #fdfbf7; }
    
    /* Executive Header */
    .dean-header {
        background: linear-gradient(135deg, var(--rub-blue) 0%, var(--rub-red) 100%);
        padding: 2.5rem; color: white; border-bottom: 5px solid var(--rub-gold);
        text-align: center; margin: -4rem -4rem 2rem -4rem;
    }
    
    .section-head {
        background: var(--rub-blue); color: var(--rub-gold);
        padding: 10px 15px; border-radius: 4px; font-weight: 700; margin-bottom: 1rem;
    }

    /* Academic Card Styling for Tutors */
    .tutor-card {
        background: white; border-top: 5px solid var(--rub-blue);
        padding: 1.2rem; border-radius: 8px; margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #eee;
    }
    .card-label { color: var(--rub-red); font-weight: 700; font-size: 0.7rem; text-transform: uppercase; }
    .card-value { color: var(--rub-blue); font-weight: 700; font-size: 1rem; }
    
    div.stButton > button {
        background-color: var(--rub-blue); color: white; border-radius: 4px;
        font-weight: 700; width: 100%; border: none; padding: 0.5rem;
    }
    div.stButton > button:hover { background-color: var(--rub-gold); color: black; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. THE COMPLETE MODULE DATABASE
# ==========================================
MODULE_DATABASE = {
    'Chemistry_Old': {
        'Year 1': {
            'Semester I': [
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
                {'code': 'FCH101', 'name': 'Fundamentals of Inorganic Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'FPH101', 'name': 'Foundations of Physics I', 'theory': 2, 'lab': 3},
                {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0},
            ],
            'Semester II': [
                {'code': 'FCH102', 'name': 'Fundamentals of Physical Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'APC101', 'name': 'IT Skills', 'theory': 2, 'lab': 2},
                {'code': 'FCH103', 'name': 'Fundamentals of Organic Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'FPH102', 'name': 'Foundations of Physics II', 'theory': 2, 'lab': 3},
                {'code': 'FMT103', 'name': 'Foundations of Mathematics II', 'theory': 3, 'lab': 0},
                {'code': 'DZG101', 'name': 'Dzongkha Communication', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 2': {
            'Semester III': [
                {'code': 'ICH101', 'name': 'Inorganic Chemistry I', 'theory': 3, 'lab': 3},
                {'code': 'PCH201', 'name': 'Physical Chemistry I', 'theory': 3, 'lab': 3},
                {'code': 'FMT204', 'name': 'Foundations of Mathematics III', 'theory': 3, 'lab': 0},
                {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
                {'code': 'OCH201', 'name': 'Organic Chemistry I', 'theory': 3, 'lab': 3},
            ],
            'Semester IV': [
                {'code': 'OCH202', 'name': 'Organic Chemistry II', 'theory': 3, 'lab': 3},
                {'code': 'PCH202', 'name': 'Physical Chemistry II', 'theory': 3, 'lab': 3},
                {'code': 'AMT202', 'name': 'Foundations of Statistics', 'theory': 3, 'lab': 0},
                {'code': 'ACH201', 'name': 'Introduction to Analytical Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'ICH202', 'name': 'Inorganic Chemistry II', 'theory': 3, 'lab': 3},
            ]
        },
        'Year 3': {
            'Semester V': [
                {'code': 'OCH303', 'name': 'Organic Chemistry III', 'theory': 3, 'lab': 3},
                {'code': 'PCH303', 'name': 'Physical Chemistry III', 'theory': 3, 'lab': 3},
                {'code': 'OCH304', 'name': 'Spectroscopic Methods in Chemistry', 'theory': 4, 'lab': 0},
                {'code': 'BCH301', 'name': 'Principles of Biochemistry I', 'theory': 3, 'lab': 3},
                {'code': 'ICH203', 'name': 'Inorganic Chemistry III', 'theory': 3, 'lab': 3},
            ],
            'Semester VI': [
                {'code': 'ECH301', 'name': 'Environmental Chemistry', 'theory': 3, 'lab': 3},
                {'code': 'BAC301', 'name': 'Basic Applied Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'PCH304', 'name': 'Quantum Chemistry and Spectroscopy', 'theory': 4, 'lab': 0},
                {'code': 'NCH301', 'name': 'Chemistry of Natural Product', 'theory': 3, 'lab': 3},
                {'code': 'BCH302', 'name': 'Principles of Biochemistry II', 'theory': 3, 'lab': 3},
            ]
        }
    },
    'Physics_Old': {
        'Year 1': {
            'Semester I': [
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
                {'code': 'MEC101', 'name': 'Mechanics I', 'theory': 3, 'lab': 2},
                {'code': 'GCH101', 'name': 'General Chemistry I', 'theory': 3, 'lab': 2},
                {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0},
                {'code': 'MPH101', 'name': 'Foundations of Practical Physics', 'theory': 2, 'lab': 3},
            ],
            'Semester II': [
                {'code': 'FMT102', 'name': 'Mathematical Software', 'theory': 2, 'lab': 2},
                {'code': 'MEC102', 'name': 'Waves and Oscillations', 'theory': 3, 'lab': 2},
                {'code': 'GCH102', 'name': 'General Chemistry II', 'theory': 3, 'lab': 2},
                {'code': 'FMT103', 'name': 'Foundations of Mathematics II', 'theory': 3, 'lab': 0},
                {'code': 'DZG101', 'name': 'Dzongkha Communication', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 2': {
            'Semester III': [
                {'code': 'MEC203', 'name': 'Electromagnetism', 'theory': 3, 'lab': 3},
                {'code': 'MEC204', 'name': 'Mechanics II', 'theory': 3, 'lab': 3},
                {'code': 'FMT204', 'name': 'Foundations of Mathematics III', 'theory': 3, 'lab': 0},
                {'code': 'PLT101', 'name': 'Programming Fundamentals', 'theory': 2, 'lab': 3},
                {'code': 'MMP201', 'name': 'Mathematical Physics I', 'theory': 3, 'lab': 0},
            ],
            'Semester IV': [
                {'code': 'MPH202', 'name': 'Foundations of Modern Physics', 'theory': 3, 'lab': 2},
                {'code': 'OPH201', 'name': 'Optics', 'theory': 3, 'lab': 3},
                {'code': 'AMT202', 'name': 'Foundations of Statistics', 'theory': 3, 'lab': 0},
                {'code': 'TPH201', 'name': 'Thermal Physics', 'theory': 3, 'lab': 2},
                {'code': 'ELE201', 'name': 'Electronic Circuits and Devices', 'theory': 3, 'lab': 3},
            ]
        },
        'Year 3': {
            'Semester V': [
                {'code': 'MPH303', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3},
                {'code': 'MPH304', 'name': 'Quantum Physics', 'theory': 4, 'lab': 0},
                {'code': 'MMP302', 'name': 'Computational Physics', 'theory': 3, 'lab': 3},
                {'code': 'TPH302', 'name': 'Statistical Mechanics', 'theory': 4, 'lab': 0},
                {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
            ],
            'Semester VI': [
                {'code': 'MMP303', 'name': 'Mathematical Physics II', 'theory': 3, 'lab': 0},
                {'code': 'MPH305', 'name': 'Solid State Physics I', 'theory': 3, 'lab': 2},
                {'code': 'MPH306', 'name': 'Nuclear Physics', 'theory': 3, 'lab': 2},
                {'code': 'ELE302', 'name': 'Analogue and Digital Electronics', 'theory': 3, 'lab': 3},
                {'code': 'MEC305', 'name': 'Electromagnetic Theory', 'theory': 4, 'lab': 0},
            ]
        }
    },
    'LifeSciences_Old': {
        'Year 1': {
            'Semester I': [
                {'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4},
                {'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'FMT101', 'name': 'Fundamentals of Mathematics', 'theory': 3, 'lab': 0},
                {'code': 'LAC101', 'name': 'རྫོང་ཁ་ཤེས་ཡྫོན་འབྲི་རྩལ།', 'theory': 2, 'lab': 0},
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
            ],
            'Semester II': [
                {'code': 'BTS101', 'name': 'Plant Diversity', 'theory': 3, 'lab': 3},
                {'code': 'PLS101', 'name': 'Fundamentals of Physics for Life Sciences', 'theory': 2, 'lab': 2},
                {'code': 'CSP101', 'name': 'Foundations of Python Programming', 'theory': 2, 'lab': 3},
                {'code': 'LAC102', 'name': 'རྫོང་ཁ་རྩྫོམ་རིག།', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 2': {
            'Semester III': [
                {'code': 'BTS202', 'name': 'Plant Anatomy and Physiology', 'theory': 3, 'lab': 3},
                {'code': 'BCH201', 'name': 'Biochemistry', 'theory': 3, 'lab': 4},
                {'code': 'ZLS201', 'name': 'Invertebrate Biology and Parasitology', 'theory': 3, 'lab': 3},
                {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
                {'code': 'ZLS204', 'name': 'Developmental Biology', 'theory': 3, 'lab': 0},
            ],
            'Semester IV': [
                {'code': 'BTS203', 'name': 'Embryology of Angiosperms', 'theory': 3, 'lab': 6},
                {'code': 'BTZ202', 'name': 'Genetics', 'theory': 3, 'lab': 4},
                {'code': 'ZLS202', 'name': 'Cell and Molecular Biology', 'theory': 3, 'lab': 4},
                {'code': 'ZLS203', 'name': 'Chordate Biology', 'theory': 3, 'lab': 3},
                {'code': 'BTZ202', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
            ]
        },
        'Year 3': {
            'Semester V': [
                {'code': 'BTS304', 'name': 'Fungi and Plant Pathology', 'theory': 3, 'lab': 3},
                {'code': 'GRS301', 'name': 'GIS and Remote Sensing', 'theory': 2, 'lab': 3},
                {'code': 'ZLS304', 'name': 'Anatomy and Physiology of Vertebrates', 'theory': 3, 'lab': 3},
                {'code': 'ZLS305', 'name': 'Developmental Biology', 'theory': 3, 'lab': 3},
                {'code': 'BTS306', 'name': 'Plant Breeding and Horticulture', 'theory': 3, 'lab': 6},
            ],
            'Semester VI': [
                {'code': 'BTS305', 'name': 'Principles of Plant Systematics', 'theory': 3, 'lab': 3},
                {'code': 'BTS306', 'name': 'Horticulture and Postharvest Management', 'theory': 3, 'lab': 3},
                {'code': 'BTZ303', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
                {'code': 'BTZ304', 'name': 'Bioinformatics', 'theory': 2, 'lab': 4},
                {'code': 'ZLS307', 'name': 'Freshwater Biology', 'theory': 3, 'lab': 6},
                {'code': 'ZLS308', 'name': 'Animal Physiology', 'theory': 3, 'lab': 6},
                {'code': 'BTS307', 'name': 'Economic Botany', 'theory': 3, 'lab': 6},
                {'code': 'BTS308', 'name': 'Plant Biotechnology and Tissue Culture', 'theory': 3, 'lab': 3},
            ]
        }
    },
    'Physics_New': {
        'Year 1': {
            'Semester I': [
                {'code': 'CME101', 'name': 'Newtonian Mechanics', 'theory': 3, 'lab': 2},
                {'code': 'CSP101', 'name': 'Foundations of Python Programming', 'theory': 2, 'lab': 3},
                {'code': 'FMT101', 'name': 'Fundamentals of Mathematics', 'theory': 4, 'lab': 0},
                {'code': 'LAC101', 'name': 'རྫོང་ཁ་ཤེས་ཡྫོན་འབྲི་རྩལ།', 'theory': 2, 'lab': 0},
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 4': {
            'Semester II': [
                {'code': 'CME402', 'name': 'Lagrangian and Hamiltonian Mechanics', 'theory': 3, 'lab': 0},
                {'code': 'EPH402', 'name': 'Physics of Renewable Energy', 'theory': 3, 'lab': 2},
                {'code': 'CRD404', 'name': 'Capstone Project II', 'theory': 2, 'lab': 4},
            ]
        }
    },
    'LifeSciences_New': {
        'Year 1': {
            'Semester I': [
                {'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4}
            ]
        }
    },
    'Chemistry_New': {
        'Year 1': {
            'Semester I': [
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
                {'code': 'MEC101', 'name': 'Mechanics I', 'theory': 3, 'lab': 2}
            ]
        }
    }
}

FACULTY_LIST = sorted([
    "Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan", "Ms. Kuenzang Choki", 
    "Ms. Sangay Yuden", "Mr. Tashi Dendup", "Shacha Thinley", "Nachiketa Homchaudhuri", 
    "Mon Bahadur Ghalley", "Dr. Karma Tenzin", "Rit Wik Sharma", "Ugyen Dorji Tamang", 
    "Karma Wangchuck", "Mohan Singh Rana", "Tshering Dekar", "Bimal Kumar Chetri", 
    "Sonam Tobgay", "Dechen Lhendup", "S. Chitra", "DS-Y", "Paul Raj"
])

# ==========================================
# 3. PERSISTENCE LOGIC
# ==========================================
def commit_to_master(faculty, position, basket):
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
# 4. SIDEBAR & ACCESS CONTROL
# ==========================================
with st.sidebar:
    st.markdown("### 🏛️ Faculty Profile")
    user_name = st.selectbox("Select Your Identity", ["-- Select --", "➕ New..."] + FACULTY_LIST)
    if user_name == "➕ New...": user_name = st.text_input("Enter Full Name")
    
    user_rank = st.selectbox("Designation", [
        "Assistant Lecturer", "Associate Lecturer", "Lecturer", "Senior Lecturer", 
        "Assistant Professor", "Associate Professor", "Dean", "HoD"
    ])
    
    st.divider()
    st.markdown("### 🔒 Administrative Access")
    admin_pass = st.text_input("Admin PIN", type="password", help="Contact HoD for access")
    is_admin = (admin_pass == "DNS777")

# ==========================================
# 5. ADMIN COMMAND CENTER (HoD VIEW)
# ==========================================
if is_admin:
    st.markdown("<div class='dean-header'><h1>Departmental Command Center</h1><p>Master Workload Audit & Strategic Planning</p></div>", unsafe_allow_html=True)
    if os.path.isfile(MASTER_LOG):
        m_df = pd.read_csv(MASTER_LOG)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Submissions", len(m_df))
        c2.metric("Faculty Participating", m_df['Faculty'].nunique())
        c3.metric("Average Dept. WAM", round(m_df['WAM'].mean(), 2))
        
        st.markdown("### 📋 Master Log (Persistent Database)")
        st.dataframe(m_df, use_container_width=True)
        
        csv_data = m_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD COMPLETE MASTER CSV", csv_data, "DNS_MASTER_WORKLOAD.csv", "text/csv")
        
        if st.button("🗑️ Reset Database (Permanent)"):
            os.remove(MASTER_LOG)
            st.rerun()
    else:
        st.info("No records submitted to the persistent database yet.")
    st.stop()

# ==========================================
# 6. TUTOR PLANNER VIEW
# ==========================================
st.markdown("""
<div class="dean-header">
    <div style="font-size: 0.8rem; letter-spacing: 3px; color: #daa520; font-weight: 700;">ROYAL UNIVERSITY OF BHUTAN</div>
    <h1>Department of Natural Sciences</h1>
    <p>Workload Selection & Planning Portal — Autumn 2026</p>
</div>
""", unsafe_allow_html=True)

if user_name == "-- Select --" or not user_name:
    st.info("👋 Select your name in the sidebar to begin drafting your workload.")
    st.stop()

if 'basket' not in st.session_state: st.session_state.basket = []

tab_plan, tab_cards = st.tabs(["🎯 Drafting Canvas", "📋 My Visual Reference Cards"])

with tab_plan:
    col_entry, col_preview = st.columns([1, 1.5])
    
    with col_entry:
        st.markdown('<div class="section-head">🖊️ Module Assignment</div>', unsafe_allow_html=True)
        
        # 1. Program & Curriculum Selection
        prog_opt = st.selectbox("Program Area", ["Physics", "Chemistry", "LifeSciences", "➕ Add New..."])
        curr_opt = st.selectbox("Curriculum Version", ["New", "Old", "➕ Add New..."])
        
        # Mapping for database
        db_key = f"{prog_opt}_{curr_opt}"
        
        # 2. Year & Semester
        c1, c2 = st.columns(2)
        with c1: yr = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
        with c2: sem = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI"])
        
        # 3. Module Selection Logic
        m_code, m_name, m_th, m_lb = "", "", 3, 0
        
        if db_key in MODULE_DATABASE and yr in MODULE_DATABASE[db_key] and sem in MODULE_DATABASE[db_key][yr]:
            mods = MODULE_DATABASE[db_key][yr][sem]
            mod_options = [f"{m['code']} - {m['name']}" for m in mods] + ["➕ Manual Entry"]
            sel_mod = st.selectbox("Select Module from Database", mod_options)
            
            if sel_mod != "➕ Manual Entry":
                entry = next(m for m in mods if f"{m['code']} - {m['name']}" == sel_mod)
                m_code, m_name, m_th, m_lb = entry['code'], entry['name'], entry['theory'], entry['lab']
            else:
                m_code = st.text_input("Manual Code")
                m_name = st.text_input("Manual Name")
        else:
            st.warning("Filters not in database. Enter details manually.")
            m_code = st.text_input("Module Code")
            m_name = st.text_input("Module Name")
        
        # 4. Logistics & Student Volume
        st.divider()
        m_type = st.selectbox("Component Type", ["Theory + Lab", "Theory Only", "Lab Only"])
        m_room = st.text_input("Classroom/Lab Name", placeholder="e.g. Science Hall 2")
        
        c3, c4 = st.columns(2)
        with c3: m_th = st.number_input("Theory Hours", 0, 10, m_th)
        with c4: m_lb = st.number_input("Lab Hours", 0, 10, m_lb)
        
        m_st = st.number_input("Student Enrollment", 1, 300, 30)

        if st.button("➕ ADD TO MY DRAFT"):
            st.session_state.basket.append({
                'code': m_code, 'name': m_name, 'type': m_type,
                'room': m_room, 'theory': m_th, 'lab': m_lb, 'students': m_st
            })
            st.rerun()

    with col_preview:
        st.markdown('<div class="section-head">📋 Current Selection</div>', unsafe_allow_html=True)
        if not st.session_state.basket:
            st.markdown("<div style='text-align:center; padding:5rem; color:#999; border:2px dashed #eee;'>Your drafting canvas is empty.</div>", unsafe_allow_html=True)
        else:
            for i, m in enumerate(st.session_state.basket):
                wam = (m['theory']*1.1 + m['lab']*0.8 + m['students']*0.045)
                st.markdown(f"""
                <div class="tutor-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <span class="card-label">Module:</span> <span class="card-value">{m['code']}</span><br>
                            <span class="card-value" style="font-size:0.9rem; color:#666;">{m['name']}</span><br>
                            <span class="card-label">Room:</span> <span class="card-value" style="color:var(--rub-red);">{m['room']}</span>
                        </div>
                        <div style="text-align:right">
                            <span class="card-label">WAM weight</span><br><span style="font-size:1.5rem; color:var(--rub-blue); font-weight:800;">{wam:.2f}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🗑️ Remove {m['code']}", key=f"del_{i}"):
                    st.session_state.basket.pop(i)
                    st.rerun()
            
            if st.button("🚀 SUBMIT FINAL PLAN TO DEPARTMENT"):
                commit_to_master(user_name, user_rank, st.session_state.basket)
                st.balloons()
                st.success("Workload successfully committed to the Master Log.")
                st.session_state.basket = []

# ==========================================
# 7. PRINTABLE REFERENCE CARDS
# ==========================================
with tab_cards:
    st.markdown("### 💳 Personal Reference Cards (Submitted)")
    if os.path.isfile(MASTER_LOG):
        all_data = pd.read_csv(MASTER_LOG)
        my_data = all_data[all_data['Faculty'] == user_name]
        
        if not my_data.empty:
            grid = st.columns(3)
            for idx, row in my_data.iterrows():
                with grid[idx % 3]:
                    st.markdown(f"""
                    <div style="background: white; border: 2px solid var(--rub-blue); border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <div style="background: var(--rub-blue); color: var(--rub-gold); padding: 5px; text-align: center; font-weight: bold; border-radius: 5px 5px 0 0; margin: -15px -15px 10px -15px;">
                            {user_rank} REFERENCE
                        </div>
                        <span class="card-label">Module</span><br><span class="card-value">{row['Code']}</span><br>
                        <span class="card-label">Venue</span><br><span class="card-value" style="color:var(--rub-red);">{row['Classroom']}</span><br>
                        <hr style="margin: 10px 0;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
                            <div><b>{row['Type']}</b></div>
                            <div>{row['Theory']}T | {row['Lab']}L</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No submissions found for your identity.")
    else:
        st.info("Master database is currently empty.")

# ==========================================
# 8. FOOTER
# ==========================================
st.markdown("<br><hr><div style='text-align: center; color: #7f8c8d; font-size: 0.8rem;'>Department of Natural Sciences • Dean's Command Suite • Cycle 2026</div>", unsafe_allow_html=True)
