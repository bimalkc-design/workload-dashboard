import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="DNS Workload Calculator",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. CLEAN CSS - PROPER FRAMING
# ==========================================
st.markdown("""
<style>
    /* Reset and base */
    .main {
        padding: 0 1rem !important;
    }
    .block-container {
        padding: 1rem 1rem 2rem 1rem !important;
        max-width: 100% !important;
    }
    
    /* Header */
    .header-box {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .header-box h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .header-box p {
        margin: 0.3rem 0 0 0;
        opacity: 0.85;
        font-size: 0.95rem;
    }
    .header-box .badge {
        display: inline-block;
        background: rgba(255,215,0,0.2);
        padding: 0.2rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        margin-top: 0.5rem;
        border: 1px solid rgba(255,215,0,0.3);
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 0.8rem;
        border-left: 4px solid #1a237e;
    }
    .card .code {
        font-weight: 700;
        color: #1a237e;
        font-size: 1rem;
    }
    .card .name {
        font-size: 0.9rem;
        color: #333;
    }
    .card .details {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.2rem;
    }
    
    /* WAM Display */
    .wam-box {
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    .wam-box .number {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .wam-box .label {
        font-size: 0.85rem;
        opacity: 0.85;
    }
    
    /* Status */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 1.5rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.9rem;
        text-align: center;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.8rem;
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stats-grid .item {
        text-align: center;
    }
    .stats-grid .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a237e;
    }
    .stats-grid .label {
        font-size: 0.7rem;
        color: #666;
        text-transform: uppercase;
    }
    
    /* Threshold Guide */
    .threshold-box {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        background: #f5f5f5;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .threshold-box .item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
    }
    .threshold-box .dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
        flex-shrink: 0;
    }
    
    /* Admin */
    .admin-box {
        background: #1a1a2e;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border: 1px solid #daa520;
        color: #daa520;
        margin: 1rem 0;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        background: #1a237e;
        color: white;
        border: none;
        padding: 0.4rem 1rem;
        width: 100%;
    }
    .stButton button:hover {
        background: #0d47a1;
    }
    
    /* Sidebar */
    .css-1d391kg {
        padding: 1rem !important;
    }
    
    /* Mobile */
    @media (max-width: 768px) {
        .header-box h1 { font-size: 1.5rem; }
        .wam-box .number { font-size: 2.5rem; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .threshold-box { flex-direction: column; align-items: center; gap: 0.3rem; }
    }
    
    /* Fix for columns */
    .row-widget.stColumns {
        gap: 1rem;
    }
    
    /* Ensure text fits */
    .stMarkdown {
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DATA - COMPLETE MODULE DATABASE
# ==========================================
MODULE_DATABASE = {
    'Chemistry_Old': {
        'Year 1': {'Semester I': [
            {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
            {'code': 'FCH101', 'name': 'Fundamentals of Inorganic Chem', 'theory': 3, 'lab': 2},
            {'code': 'FPH101', 'name': 'Foundations of Physics I', 'theory': 2, 'lab': 3},
            {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0},
        ], 'Semester II': [
            {'code': 'FCH102', 'name': 'Fundamentals of Physical Chem', 'theory': 3, 'lab': 2},
            {'code': 'APC101', 'name': 'IT Skills', 'theory': 2, 'lab': 2},
            {'code': 'FCH103', 'name': 'Fundamentals of Organic Chem', 'theory': 3, 'lab': 2},
            {'code': 'FPH102', 'name': 'Foundations of Physics II', 'theory': 2, 'lab': 3},
            {'code': 'FMT103', 'name': 'Foundations of Mathematics II', 'theory': 3, 'lab': 0},
        ]},
        'Year 2': {'Semester III': [
            {'code': 'ICH101', 'name': 'Inorganic Chemistry I', 'theory': 3, 'lab': 3},
            {'code': 'PCH201', 'name': 'Physical Chemistry I', 'theory': 3, 'lab': 3},
            {'code': 'FMT204', 'name': 'Foundations of Mathematics III', 'theory': 3, 'lab': 0},
            {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
        ], 'Semester IV': [
            {'code': 'OCH201', 'name': 'Organic Chemistry I', 'theory': 3, 'lab': 3},
            {'code': 'OCH202', 'name': 'Organic Chemistry II', 'theory': 3, 'lab': 3},
            {'code': 'PCH202', 'name': 'Physical Chemistry II', 'theory': 3, 'lab': 3},
            {'code': 'AMT202', 'name': 'Foundations of Statistics', 'theory': 3, 'lab': 0},
            {'code': 'ACH201', 'name': 'Intro to Analytical Chem', 'theory': 3, 'lab': 2},
        ]},
        'Year 3': {'Semester V': [
            {'code': 'OCH303', 'name': 'Organic Chemistry III', 'theory': 3, 'lab': 3},
            {'code': 'PCH303', 'name': 'Physical Chemistry III', 'theory': 3, 'lab': 3},
            {'code': 'OCH304', 'name': 'Spectroscopic Methods', 'theory': 4, 'lab': 0},
            {'code': 'BCH301', 'name': 'Principles of Biochemistry I', 'theory': 3, 'lab': 3},
            {'code': 'ICH203', 'name': 'Inorganic Chemistry III', 'theory': 3, 'lab': 3},
        ], 'Semester VI': [
            {'code': 'ECH301', 'name': 'Environmental Chemistry', 'theory': 3, 'lab': 3},
            {'code': 'BAC301', 'name': 'Basic Applied Chemistry', 'theory': 3, 'lab': 2},
            {'code': 'PCH304', 'name': 'Quantum Chem & Spectroscopy', 'theory': 4, 'lab': 0},
            {'code': 'NCH301', 'name': 'Chemistry of Natural Product', 'theory': 3, 'lab': 3},
            {'code': 'BCH302', 'name': 'Principles of Biochemistry II', 'theory': 3, 'lab': 3},
        ]}
    },
    'Physics_Old': {
        'Year 1': {'Semester I': [
            {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
            {'code': 'MEC101', 'name': 'Mechanics I', 'theory': 3, 'lab': 2},
            {'code': 'GCH101', 'name': 'General Chemistry I', 'theory': 3, 'lab': 2},
            {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0},
            {'code': 'MPH101', 'name': 'Foundations of Practical Physics', 'theory': 2, 'lab': 3},
        ], 'Semester II': [
            {'code': 'FMT102', 'name': 'Mathematical Software', 'theory': 2, 'lab': 2},
            {'code': 'MEC102', 'name': 'Waves and Oscillations', 'theory': 3, 'lab': 2},
            {'code': 'GCH102', 'name': 'General Chemistry II', 'theory': 3, 'lab': 2},
            {'code': 'FMT103', 'name': 'Foundations of Mathematics II', 'theory': 3, 'lab': 0},
        ]},
        'Year 2': {'Semester III': [
            {'code': 'MEC203', 'name': 'Electromagnetism', 'theory': 3, 'lab': 3},
            {'code': 'MEC204', 'name': 'Mechanics II', 'theory': 3, 'lab': 3},
            {'code': 'FMT204', 'name': 'Foundations of Mathematics III', 'theory': 3, 'lab': 0},
            {'code': 'PLT101', 'name': 'Programming Fundamentals', 'theory': 2, 'lab': 3},
            {'code': 'MMP201', 'name': 'Mathematical Physics I', 'theory': 3, 'lab': 0},
        ], 'Semester IV': [
            {'code': 'MPH202', 'name': 'Foundations of Modern Physics', 'theory': 3, 'lab': 2},
            {'code': 'OPH201', 'name': 'Optics', 'theory': 3, 'lab': 3},
            {'code': 'AMT202', 'name': 'Foundations of Statistics', 'theory': 3, 'lab': 0},
            {'code': 'TPH201', 'name': 'Thermal Physics', 'theory': 3, 'lab': 2},
            {'code': 'ELE201', 'name': 'Electronic Circuits & Devices', 'theory': 3, 'lab': 3},
        ]},
        'Year 3': {'Semester V': [
            {'code': 'MPH303', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3},
            {'code': 'MPH304', 'name': 'Quantum Physics', 'theory': 4, 'lab': 0},
            {'code': 'MMP302', 'name': 'Computational Physics', 'theory': 3, 'lab': 3},
            {'code': 'TPH302', 'name': 'Statistical Mechanics', 'theory': 4, 'lab': 0},
            {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
        ], 'Semester VI': [
            {'code': 'MMP303', 'name': 'Mathematical Physics II', 'theory': 3, 'lab': 0},
            {'code': 'MPH305', 'name': 'Solid State Physics I', 'theory': 3, 'lab': 2},
            {'code': 'MPH306', 'name': 'Nuclear Physics', 'theory': 3, 'lab': 2},
            {'code': 'ELE302', 'name': 'Analogue & Digital Electronics', 'theory': 3, 'lab': 3},
            {'code': 'MEC305', 'name': 'Electromagnetic Theory', 'theory': 4, 'lab': 0},
        ]}
    },
    'LifeSciences_Old': {
        'Year 1': {'Semester I': [
            {'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4},
            {'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2},
            {'code': 'FMT101', 'name': 'Foundations of Mathematics', 'theory': 3, 'lab': 0},
            {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
        ], 'Semester II': [
            {'code': 'BTS101', 'name': 'Plant Diversity', 'theory': 3, 'lab': 3},
            {'code': 'PLS101', 'name': 'Physics for Life Sciences', 'theory': 2, 'lab': 2},
            {'code': 'CSP101', 'name': 'Python Programming', 'theory': 2, 'lab': 3},
        ]},
        'Year 2': {'Semester III': [
            {'code': 'BTS202', 'name': 'Plant Anatomy & Physiology', 'theory': 3, 'lab': 3},
            {'code': 'BCH201', 'name': 'Biochemistry', 'theory': 3, 'lab': 4},
            {'code': 'ZLS201', 'name': 'Invertebrate Biology', 'theory': 3, 'lab': 3},
            {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
        ], 'Semester IV': [
            {'code': 'BTS203', 'name': 'Embryology of Angiosperms', 'theory': 3, 'lab': 6},
            {'code': 'BTZ202', 'name': 'Genetics', 'theory': 3, 'lab': 4},
            {'code': 'ZLS202', 'name': 'Cell & Molecular Biology', 'theory': 3, 'lab': 4},
            {'code': 'ZLS203', 'name': 'Chordate Biology', 'theory': 3, 'lab': 3},
        ]},
        'Year 3': {'Semester V': [
            {'code': 'BTS304', 'name': 'Fungi & Plant Pathology', 'theory': 3, 'lab': 3},
            {'code': 'GRS301', 'name': 'GIS & Remote Sensing', 'theory': 2, 'lab': 3},
            {'code': 'ZLS304', 'name': 'Anatomy of Vertebrates', 'theory': 3, 'lab': 3},
            {'code': 'ZLS305', 'name': 'Developmental Biology', 'theory': 3, 'lab': 3},
        ], 'Semester VI': [
            {'code': 'BTS305', 'name': 'Plant Systematics', 'theory': 3, 'lab': 3},
            {'code': 'BTS306', 'name': 'Horticulture Management', 'theory': 3, 'lab': 3},
            {'code': 'BTZ303', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
            {'code': 'BTZ304', 'name': 'Bioinformatics', 'theory': 2, 'lab': 4},
        ]}
    },
    'Physics_New': {
        'Year 1': {'Semester I': [
            {'code': 'CME101', 'name': 'Newtonian Mechanics', 'theory': 3, 'lab': 2},
            {'code': 'CSP101', 'name': 'Python Programming', 'theory': 2, 'lab': 3},
            {'code': 'FMT101', 'name': 'Fundamentals of Mathematics', 'theory': 4, 'lab': 0},
            {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
        ], 'Semester II': [
            {'code': 'PHW101', 'name': 'Oscillations & Waves', 'theory': 3, 'lab': 2},
            {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
            {'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2},
        ]},
        'Year 2': {'Semester I': [
            {'code': 'APH201', 'name': 'Physics of Space & Satellites', 'theory': 3, 'lab': 2},
            {'code': 'EMT201', 'name': 'Electricity & Magnetism', 'theory': 3, 'lab': 3},
            {'code': 'MMP201', 'name': 'Essential Mathematics', 'theory': 3, 'lab': 0},
            {'code': 'APH202', 'name': 'Electronic Systems', 'theory': 2, 'lab': 3},
        ], 'Semester II': [
            {'code': 'MMP202', 'name': 'Mathematical Methods', 'theory': 3, 'lab': 0},
            {'code': 'FMP201', 'name': 'Modern Physics', 'theory': 3, 'lab': 2},
            {'code': 'PHW202', 'name': 'Optics', 'theory': 3, 'lab': 3},
            {'code': 'TPH201', 'name': 'Thermal Physics', 'theory': 3, 'lab': 2},
        ]},
        'Year 3': {'Semester I': [
            {'code': 'APH303', 'name': 'Computational Physics', 'theory': 3, 'lab': 3},
            {'code': 'APH304', 'name': 'Applied Integrated Circuits', 'theory': 3, 'lab': 3},
            {'code': 'EPH301', 'name': 'Atmospheric Physics', 'theory': 3, 'lab': 2},
            {'code': 'QME301', 'name': 'Quantum Mechanics', 'theory': 4, 'lab': 0},
        ], 'Semester II': [
            {'code': 'ANP301', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3},
            {'code': 'ANP302', 'name': 'Nuclear Physics', 'theory': 3, 'lab': 2},
            {'code': 'SSP301', 'name': 'Condensed Matter Physics', 'theory': 3, 'lab': 3},
            {'code': 'APH305', 'name': 'Machine Learning for Physics', 'theory': 3, 'lab': 3},
        ]},
        'Year 4': {'Semester I': [
            {'code': 'THP402', 'name': 'Statistical Physics', 'theory': 4, 'lab': 0},
            {'code': 'EMT402', 'name': 'Electromagnetic Theory', 'theory': 4, 'lab': 0},
            {'code': 'SSP402', 'name': 'Advanced Condensed Matter', 'theory': 3, 'lab': 3},
            {'code': 'QME402', 'name': 'Advanced Quantum Mechanics', 'theory': 4, 'lab': 0},
            {'code': 'CRD403', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
        ], 'Semester II': [
            {'code': 'CME402', 'name': 'Lagrangian & Hamiltonian Mech', 'theory': 3, 'lab': 0},
            {'code': 'EPH402', 'name': 'Renewable Energy Physics', 'theory': 3, 'lab': 2},
            {'code': 'CRD404', 'name': 'Capstone Project II', 'theory': 2, 'lab': 4},
        ]}
    },
    'LifeSciences_New': {
        'Year 1': {'Semester I': [
            {'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4},
            {'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2},
            {'code': 'FMT101', 'name': 'Fundamentals of Mathematics', 'theory': 3, 'lab': 0},
            {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
        ], 'Semester II': [
            {'code': 'BTS101', 'name': 'Plant Diversity', 'theory': 3, 'lab': 3},
            {'code': 'PLS101', 'name': 'Physics for Life Sciences', 'theory': 2, 'lab': 2},
            {'code': 'CSP101', 'name': 'Python Programming', 'theory': 2, 'lab': 3},
        ]},
        'Year 2': {'Semester I': [
            {'code': 'BTS202', 'name': 'Plant Anatomy & Physiology', 'theory': 3, 'lab': 3},
            {'code': 'BCH201', 'name': 'Biochemistry', 'theory': 3, 'lab': 4},
            {'code': 'ZLS201', 'name': 'Invertebrate Biology', 'theory': 3, 'lab': 3},
            {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
        ], 'Semester II': [
            {'code': 'BTS203', 'name': 'Embryology of Angiosperms', 'theory': 3, 'lab': 6},
            {'code': 'BTZ202', 'name': 'Genetics', 'theory': 3, 'lab': 4},
            {'code': 'ZLS202', 'name': 'Cell & Molecular Biology', 'theory': 3, 'lab': 4},
            {'code': 'ZLS203', 'name': 'Chordate Biology', 'theory': 3, 'lab': 3},
        ]},
        'Year 3': {'Semester I': [
            {'code': 'BTS304', 'name': 'Fungi & Plant Pathology', 'theory': 3, 'lab': 3},
            {'code': 'GRS301', 'name': 'GIS & Remote Sensing', 'theory': 2, 'lab': 3},
            {'code': 'ZLS304', 'name': 'Anatomy & Physiology', 'theory': 3, 'lab': 3},
            {'code': 'ZLS305', 'name': 'Developmental Biology', 'theory': 3, 'lab': 3},
        ], 'Semester II': [
            {'code': 'BTS305', 'name': 'Plant Systematics', 'theory': 3, 'lab': 3},
            {'code': 'BTS306', 'name': 'Horticulture Management', 'theory': 3, 'lab': 3},
            {'code': 'BTZ303', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
            {'code': 'BTZ304', 'name': 'Bioinformatics', 'theory': 2, 'lab': 4},
        ]},
        'Year 4': {'Semester I': [
            {'code': 'BTS407', 'name': 'Ethnobotany & Phytochemistry', 'theory': 3, 'lab': 4},
            {'code': 'BTZ405', 'name': 'Biotechnology & Tissue Culture', 'theory': 3, 'lab': 4},
            {'code': 'BTZ406', 'name': 'Ecology & Conservation', 'theory': 3, 'lab': 3},
            {'code': 'ZLS406', 'name': 'Freshwater Biology', 'theory': 3, 'lab': 3},
            {'code': 'CRD403', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
        ], 'Semester II': [
            {'code': 'ZLS407', 'name': 'Animal Behaviour', 'theory': 3, 'lab': 3},
            {'code': 'BTZ407', 'name': 'Immunology & Forensic Biology', 'theory': 3, 'lab': 4},
            {'code': 'CRD404', 'name': 'Capstone Project II', 'theory': 2, 'lab': 4},
        ]}
    },
    'Chemistry_New': {
        'Year 1': {'Semester I': [
            {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
            {'code': 'MEC101', 'name': 'Mechanics I', 'theory': 3, 'lab': 2},
            {'code': 'GCH101', 'name': 'General Chemistry I', 'theory': 3, 'lab': 2},
            {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0},
            {'code': 'MPH101', 'name': 'Practical Physics', 'theory': 2, 'lab': 3},
        ], 'Semester II': [
            {'code': 'FMT102', 'name': 'Mathematical Software', 'theory': 2, 'lab': 2},
            {'code': 'MEC102', 'name': 'Waves & Oscillations', 'theory': 3, 'lab': 2},
            {'code': 'GCH102', 'name': 'General Chemistry II', 'theory': 3, 'lab': 2},
            {'code': 'FMT103', 'name': 'Mathematics II', 'theory': 3, 'lab': 0},
        ]},
        'Year 2': {'Semester III': [
            {'code': 'MEC203', 'name': 'Electromagnetism', 'theory': 3, 'lab': 3},
            {'code': 'MEC204', 'name': 'Mechanics II', 'theory': 3, 'lab': 3},
            {'code': 'FMT204', 'name': 'Mathematics III', 'theory': 3, 'lab': 0},
            {'code': 'PLT101', 'name': 'Programming Fundamentals', 'theory': 2, 'lab': 3},
            {'code': 'MMP201', 'name': 'Mathematical Physics I', 'theory': 3, 'lab': 0},
        ], 'Semester IV': [
            {'code': 'MPH202', 'name': 'Modern Physics', 'theory': 3, 'lab': 2},
            {'code': 'OPH201', 'name': 'Optics', 'theory': 3, 'lab': 3},
            {'code': 'AMT202', 'name': 'Foundations of Statistics', 'theory': 3, 'lab': 0},
            {'code': 'TPH201', 'name': 'Thermal Physics', 'theory': 3, 'lab': 2},
            {'code': 'ELE201', 'name': 'Electronic Circuits', 'theory': 3, 'lab': 3},
        ]},
        'Year 3': {'Semester V': [
            {'code': 'MPH303', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3},
            {'code': 'MPH304', 'name': 'Quantum Physics', 'theory': 4, 'lab': 0},
            {'code': 'MMP302', 'name': 'Computational Physics', 'theory': 3, 'lab': 3},
            {'code': 'TPH302', 'name': 'Statistical Mechanics', 'theory': 4, 'lab': 0},
            {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
        ], 'Semester VI': [
            {'code': 'MMP303', 'name': 'Mathematical Physics II', 'theory': 3, 'lab': 0},
            {'code': 'MPH305', 'name': 'Solid State Physics I', 'theory': 3, 'lab': 2},
            {'code': 'MPH306', 'name': 'Nuclear Physics', 'theory': 3, 'lab': 2},
            {'code': 'ELE302', 'name': 'Analogue & Digital Electronics', 'theory': 3, 'lab': 3},
            {'code': 'MEC305', 'name': 'Electromagnetic Theory', 'theory': 4, 'lab': 0},
        ]},
        'Year 4': {'Semester I': [
            {'code': 'THP402', 'name': 'Statistical Physics', 'theory': 4, 'lab': 0},
            {'code': 'EMT402', 'name': 'Electromagnetic Theory', 'theory': 4, 'lab': 0},
            {'code': 'SSP402', 'name': 'Advanced Condensed Matter', 'theory': 3, 'lab': 3},
            {'code': 'QME402', 'name': 'Advanced Quantum Mechanics', 'theory': 4, 'lab': 0},
            {'code': 'CRD403', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
        ], 'Semester II': [
            {'code': 'CME402', 'name': 'Lagrangian & Hamiltonian Mech', 'theory': 3, 'lab': 0},
            {'code': 'EPH402', 'name': 'Renewable Energy Physics', 'theory': 3, 'lab': 2},
            {'code': 'CRD404', 'name': 'Capstone Project II', 'theory': 2, 'lab': 4},
        ]}
    }
}

# ==========================================
# 4. FACULTY LIST
# ==========================================
FACULTY_LIST = [
    "Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan",
    "Ms. Kuenzang Choki", "Ms. Sangay Yuden", "Mr. Tashi Dendup",
    "Shacha Thinley", "Nachiketa Homchaudhuri", "Mon Bahadur Ghalley",
    "Dr. Karma Tenzin", "Rit Wik Sharma", "Ugyen Dorji Tamang",
    "Karma Wangchuck", "Mohan Singh Rana", "Tshering Dekar",
    "Bimal Kumar Chetri", "Sonam Tobgay", "Dechen Lhendup",
    "S. Chitra", "DS-Y", "Paul Raj"
]

# ==========================================
# 5. CORE FUNCTIONS
# ==========================================
def calculate_wam(modules):
    total = 0
    for m in modules:
        base = m['theory'] + m['lab']
        student_load = (m.get('students', 25) * 4) * 0.04
        total += base + student_load
    return round(total, 1)

def get_status(wam):
    if wam == 0: return 'No Load', '⚪', '#6c757d', 'Select modules to begin'
    if wam < 12: return 'Light Load', '🟡', '#ffc107', 'You can add more modules'
    if wam <= 16: return 'Balanced', '🟢', '#28a745', 'Workload is optimal'
    return 'Heavy Load', '🔴', '#dc3545', 'Consider sharing modules'

def log_activity(name, modules, wam, status):
    log_file = 'workload_logs.json'
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except:
            pass
    logs.append({
        'timestamp': datetime.now().isoformat(),
        'faculty': name,
        'modules': modules,
        'wam': wam,
        'status': status
    })
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

# ==========================================
# 6. SESSION STATE
# ==========================================
if 'modules' not in st.session_state:
    st.session_state.modules = []
if 'counts' not in st.session_state:
    st.session_state.counts = {}
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'admin' not in st.session_state:
    st.session_state.admin = False

# ==========================================
# 7. HEADER
# ==========================================
st.markdown(f"""
<div class="header-box">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">
        <div>
            <h1>📊 DNS Workload Calculator</h1>
            <p>Department of Natural Sciences • Royal University of Bhutan</p>
            <span class="badge">📅 {datetime.now().strftime('%B %d, %Y')}</span>
        </div>
        <div style="text-align:right; font-size:0.85rem; opacity:0.7;">
            <div>🎓 Faculty Self-Service</div>
            <div>⚡ Real-time WAM</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 8. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    
    name_opt = st.radio("Choose", ["From List", "Enter Name"], index=0)
    
    if name_opt == "From List":
        name = st.selectbox("Select", [""] + sorted(FACULTY_LIST))
    else:
        name = st.text_input("Your Name", value=st.session_state.name)
    
    if name:
        st.session_state.name = name
        st.success(f"✅ {name}")
    
    st.selectbox("Designation", ["Professor", "Associate Professor", "Assistant Professor", "Senior Lecturer", "Lecturer"])
    
    st.divider()
    st.markdown("### 📚 Select Modules")
    
    prog = st.selectbox("Program", ["Physics", "Chemistry", "Life Sciences"])
    curr = st.selectbox("Curriculum", ["Old", "New"])
    
    prog_key = {"Physics":"Physics", "Chemistry":"Chemistry", "Life Sciences":"LifeSciences"}[prog]
    key = f"{prog_key}_{curr}"
    
    year = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
    sem = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI"])
    
    modules = []
    try:
        modules = MODULE_DATABASE[key][year][sem]
    except:
        st.warning("No modules found")
    
    if modules:
        opts = [f"{m['code']} - {m['name']}" for m in modules]
        sel = st.selectbox("Module", ["-- Select --"] + opts)
        
        if sel != "-- Select --":
            code = sel.split(" - ")[0]
            mod = next(m for m in modules if m['code'] == code)
            
            students = st.slider("Students", 25, 40, 30)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("➕ Add", use_container_width=True):
                    if not any(m['code'] == code for m in st.session_state.modules):
                        st.session_state.modules.append(mod)
                        st.session_state.counts[code] = students
                        st.success(f"Added {code}")
                        st.rerun()
                    else:
                        st.warning("Already added")
            with c2:
                if st.button("🗑️ Clear", use_container_width=True):
                    st.session_state.modules = []
                    st.session_state.counts = {}
                    st.rerun()
    
    st.divider()
    if st.session_state.modules:
        st.metric("Modules", len(st.session_state.modules))
        st.metric("Students", sum(st.session_state.counts.values()))
    
    st.divider()
    st.markdown("### 🔒 Admin")
    pin = st.text_input("PIN", type="password")
    if pin == "DNS777":
        st.session_state.admin = True
        st.success("Admin mode ON")

# ==========================================
# 9. MAIN CONTENT
# ==========================================
if not st.session_state.name:
    st.info("👈 Please select or enter your name in the sidebar")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Your Modules")
    
    if not st.session_state.modules:
        st.info("👈 Select modules from the sidebar")
    else:
        total_t, total_l = 0, 0
        
        for mod in st.session_state.modules:
            students = st.session_state.counts.get(mod['code'], 25)
            total_t += mod['theory']
            total_l += mod['lab']
            
            c_a, c_b, c_c, c_d = st.columns([3, 1, 1, 0.5])
            with c_a:
                st.markdown(f"""
                <div class="card">
                    <span class="code">{mod['code']}</span>
                    <span class="name">{mod['name']}</span>
                    <div class="details">📖 {mod['theory']}h Theory • 🧪 {mod['lab']}h Lab • 👨‍🎓 {students} students</div>
                </div>
                """, unsafe_allow_html=True)
            with c_b:
                st.metric("", f"{mod['theory'] + mod['lab']}h", label_visibility="collapsed")
            with c_c:
                w = calculate_wam([{**mod, 'students': students}])
                st.metric("WAM", f"{w:.1f}", label_visibility="collapsed")
            with c_d:
                if st.button("✖", key=f"rm_{mod['code']}"):
                    st.session_state.modules.remove(mod)
                    del st.session_state.counts[mod['code']]
                    st.rerun()
        
        st.markdown(f"""
        <div class="stats-grid">
            <div class="item"><div class="value">{len(st.session_state.modules)}</div><div class="label">Modules</div></div>
            <div class="item"><div class="value">{total_t}h</div><div class="label">Theory</div></div>
            <div class="item"><div class="value">{total_l}h</div><div class="label">Lab</div></div>
            <div class="item"><div class="value">{sum(st.session_state.counts.values())}</div><div class="label">Students</div></div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 Your WAM")
    
    if st.session_state.modules:
        wam = calculate_wam([
            {**m, 'students': st.session_state.counts.get(m['code'], 25)}
            for m in st.session_state.modules
        ])
        status, emoji, color, msg = get_status(wam)
        
        log_activity(st.session_state.name, [
            {'code': m['code'], 'name': m['name'], 'students': st.session_state.counts.get(m['code'], 25)}
            for m in st.session_state.modules
        ], wam, status)
        
        st.markdown(f"""
        <div class="wam-box">
            <div class="number">{wam}</div>
            <div class="label">Workload Allocation Model Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align:center;">
            <span class="status-badge" style="background:{color};color:white;">{emoji} {status}</span>
            <p style="font-size:0.9rem;color:#666;margin-top:0.5rem;">{msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(min(wam/16, 1.0))
        st.caption("0" + " " * 50 + "16+")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Theory", f"{total_t}h")
        c2.metric("Lab", f"{total_l}h")
        c3.metric("Total", f"{total_t + total_l}h")
        
        if len(st.session_state.modules) > 1:
            data = []
            for m in st.session_state.modules:
                w = calculate_wam([{**m, 'students': st.session_state.counts.get(m['code'], 25)}])
                data.append({'Module': m['code'], 'WAM': w})
            df = pd.DataFrame(data)
            fig = px.bar(df, x='Module', y='WAM', color='WAM', 
                        color_continuous_scale='Viridis', height=250)
            fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 Add modules to calculate")

# ==========================================
# 10. THRESHOLD GUIDE
# ==========================================
st.markdown("""
<div class="threshold-box">
    <div class="item"><span class="dot" style="background:#ffc107;"></span> Light (WAM &lt; 12)</div>
    <div class="item"><span class="dot" style="background:#28a745;"></span> Balanced (12 - 16)</div>
    <div class="item"><span class="dot" style="background:#dc3545;"></span> Heavy (WAM &gt; 16)</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 11. DETAILS & HISTORY
# ==========================================
if st.session_state.modules:
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📊 Details", "📈 Charts", "📜 History"])
    
    with tab1:
        data = []
        for m in st.session_state.modules:
            students = st.session_state.counts.get(m['code'], 25)
            w = calculate_wam([{**m, 'students': students}])
            data.append({
                'Code': m['code'], 'Module': m['name'],
                'Theory': m['theory'], 'Lab': m['lab'],
                'Students': students, 'WAM': w
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, f"workload_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(values=[df['Theory'].sum(), df['Lab'].sum()], 
                        names=['Theory', 'Lab'], title="Theory vs Lab")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.bar(df, x='Code', y='WAM', title="WAM by Module", color='WAM',
                        color_continuous_scale='Viridis', height=300)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        log_file = 'workload_logs.json'
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    all_logs = json.load(f)
                my_logs = [l for l in all_logs if l['faculty'] == st.session_state.name]
                if my_logs:
                    df = pd.DataFrame(my_logs)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df = df.sort_values('timestamp', ascending=False)
                    st.dataframe(df[['timestamp', 'wam', 'status']], use_container_width=True, hide_index=True)
            except:
                st.info("No history")

# ==========================================
# 12. ADMIN
# ==========================================
if st.session_state.admin:
    st.divider()
    st.markdown('<div class="admin-box">🔐 ADMIN COMMAND CENTER</div>', unsafe_allow_html=True)
    
    log_file = 'workload_logs.json'
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            if logs:
                df = pd.DataFrame(logs)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total", len(df))
                c2.metric("Faculty", df['faculty'].nunique())
                c3.metric("Avg WAM", round(df['wam'].mean(), 2))
                c4.metric("Heavy Load", len(df[df['status'] == 'Heavy Load']))
                
                st.dataframe(df.sort_values('timestamp', ascending=False), use_container_width=True, hide_index=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Full Report", csv, f"DNS_Report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
                
                if st.button("🗑️ Purge Database"):
                    os.remove(log_file)
                    st.rerun()
        except:
            st.info("No data")

# ==========================================
# 13. FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style="text-align:center;color:#666;font-size:0.8rem;padding:0.5rem 0;">
    Department of Natural Sciences • Royal University of Bhutan
</div>
""", unsafe_allow_html=True)
