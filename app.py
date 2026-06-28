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
    page_title="Workload & Roaster System",
    page_icon="📋",
    layout="wide"
)

# ==========================================
# 2. PROFESSIONAL ACADEMIC STYLING
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .main { padding: 0 0.5rem !important; }
    .block-container { padding: 0.5rem 0.5rem 1rem 0.5rem !important; max-width: 100% !important; }
    
    /* Academic Header */
    .academic-header {
        background: #1a2a4a;
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-bottom: 4px solid #c9a84c;
    }
    .academic-header h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .academic-header .subtitle {
        font-size: 0.95rem;
        color: #a8b8d0;
        margin-top: 0.2rem;
    }
    .academic-header .meta {
        font-size: 0.75rem;
        color: #8899b0;
        margin-top: 0.3rem;
        letter-spacing: 0.3px;
    }
    .academic-header .badge {
        display: inline-block;
        background: rgba(201,168,76,0.2);
        padding: 0.15rem 0.8rem;
        border-radius: 4px;
        font-size: 0.7rem;
        border: 1px solid rgba(201,168,76,0.3);
        color: #c9a84c;
    }
    
    /* WAM Card - Professional */
    .wam-professional {
        background: #1a2a4a;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        border-bottom: 3px solid #c9a84c;
        margin: 0.5rem 0;
    }
    .wam-professional .number {
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1.2;
        color: #ffffff;
    }
    .wam-professional .label {
        font-size: 0.8rem;
        color: #a8b8d0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 1.5rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.3px;
    }
    
    /* Module Cards - Academic */
    .module-academic {
        background: #ffffff;
        border: 1px solid #e8ecf0;
        border-radius: 6px;
        padding: 0.8rem 1.2rem;
        margin: 0.3rem 0;
        border-left: 3px solid #1a2a4a;
        transition: all 0.2s ease;
    }
    .module-academic:hover {
        border-left-color: #c9a84c;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .module-academic .code {
        font-weight: 600;
        color: #1a2a4a;
        font-size: 0.95rem;
    }
    .module-academic .name {
        font-size: 0.9rem;
        color: #2c3e50;
    }
    .module-academic .details {
        font-size: 0.78rem;
        color: #7f8c8d;
        margin-top: 0.1rem;
    }
    
    /* Stats Grid - Academic */
    .stats-academic {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.5rem;
        background: #f8f9fa;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        border: 1px solid #e8ecf0;
        margin: 0.3rem 0;
    }
    .stats-academic .item { text-align: center; }
    .stats-academic .value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a2a4a;
    }
    .stats-academic .label {
        font-size: 0.6rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Threshold Guide */
    .threshold-academic {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        background: #f8f9fa;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        border: 1px solid #e8ecf0;
        margin: 0.3rem 0;
    }
    .threshold-academic .item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
        color: #2c3e50;
    }
    .threshold-academic .dot {
        width: 12px;
        height: 12px;
        border-radius: 2px;
        display: inline-block;
        flex-shrink: 0;
    }
    
    /* Admin Zone */
    .admin-academic {
        background: #1a2a4a;
        padding: 1rem 1.5rem;
        border-radius: 6px;
        border-left: 4px solid #c9a84c;
        color: #ffffff;
        margin: 0.5rem 0;
    }
    .admin-academic .title { font-weight: 600; font-size: 1.1rem; }
    .admin-academic .sub { font-size: 0.85rem; opacity: 0.7; }
    
    /* Buttons */
    .stButton > button {
        border-radius: 4px;
        font-weight: 600;
        background: #1a2a4a;
        color: white;
        border: none;
        padding: 0.35rem 0.8rem;
        transition: all 0.2s ease;
        width: 100%;
        font-size: 0.85rem;
    }
    .stButton > button:hover {
        background: #2a4a6a;
        box-shadow: 0 2px 8px rgba(26,42,74,0.2);
    }
    
    /* Timetable Card */
    .timetable-academic {
        background: #ffffff;
        border: 1px solid #e8ecf0;
        border-radius: 6px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    .timetable-academic .header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a2a4a;
        border-bottom: 2px solid #1a2a4a;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .timetable-entry {
        display: grid;
        grid-template-columns: 1fr 2fr 1fr 1fr 1.2fr;
        gap: 0.5rem;
        padding: 0.4rem 0;
        border-bottom: 1px solid #f1f3f5;
        font-size: 0.82rem;
    }
    .timetable-entry .label { font-weight: 600; color: #495057; }
    .timetable-entry .value { color: #212529; }
    
    /* Sidebar */
    .css-1d391kg {
        background: #f8f9fa;
        padding: 0.5rem !important;
    }
    
    /* Mobile */
    @media (max-width: 768px) {
        .academic-header h1 { font-size: 1.4rem; }
        .wam-professional .number { font-size: 2.5rem; }
        .stats-academic { grid-template-columns: repeat(2, 1fr); }
        .threshold-academic { flex-direction: column; align-items: center; gap: 0.2rem; }
        .timetable-entry { grid-template-columns: 1fr; gap: 0.1rem; padding: 0.6rem 0; }
    }
    
    /* PRINT STYLES - Print everything */
    @media print {
        /* Hide Streamlit elements */
        .stApp { background: white !important; }
        .stSidebar { display: none !important; }
        .stButton { display: none !important; }
        .stTabs { display: none !important; }
        .stSelectbox { display: none !important; }
        .stTextInput { display: none !important; }
        .stSlider { display: none !important; }
        .stRadio { display: none !important; }
        .stMarkdown .threshold-academic { display: none !important; }
        .admin-academic { display: none !important; }
        .no-print { display: none !important; }
        .stats-academic { display: none !important; }
        .stAlert { display: none !important; }
        .stInfo { display: none !important; }
        .stWarning { display: none !important; }
        .stSuccess { display: none !important; }
        .stException { display: none !important; }
        .stSpinner { display: none !important; }
        
        /* Show print content */
        .print-content { display: block !important; }
        
        /* Print styling */
        .academic-header { 
            background: #1a2a4a !important; 
            -webkit-print-color-adjust: exact !important; 
            print-color-adjust: exact !important;
            padding: 1rem 1.5rem !important;
        }
        .wam-professional { 
            background: #1a2a4a !important; 
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        .status-badge { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        .module-academic { break-inside: avoid; border: 1px solid #ddd !important; }
        .timetable-academic { break-inside: avoid; border: 1px solid #ddd !important; }
        .timetable-entry { break-inside: avoid; }
        
        /* Page setup */
        @page {
            size: A4;
            margin: 1.5cm;
        }
        body { font-size: 11pt !important; }
        .print-container { padding: 0 !important; }
    }
    
    .print-content { display: none; }
    .no-print { display: block; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. COMPLETE MODULE DATABASE
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
            ],
            'Semester II': [
                {'code': 'PHW101', 'name': 'Oscillations and Waves', 'theory': 3, 'lab': 2},
                {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
                {'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'LAC102', 'name': 'རྫོང་ཁ་རྩྫོམ་རིག།', 'theory': 2, 'lab': 0},
                {'code': 'Elective I', 'name': 'Elective I', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 2': {
            'Semester I': [
                {'code': 'APH201', 'name': 'Physics of Space and Satellites', 'theory': 3, 'lab': 2},
                {'code': 'EMT201', 'name': 'Electricity and Magnetism', 'theory': 3, 'lab': 3},
                {'code': 'MMP201', 'name': 'Essential Mathematics for Physics', 'theory': 3, 'lab': 0},
                {'code': 'APH202', 'name': 'Introduction to Electronic Systems', 'theory': 2, 'lab': 3},
                {'code': 'Elective II', 'name': 'Elective II', 'theory': 2, 'lab': 0},
            ],
            'Semester II': [
                {'code': 'MMP202', 'name': 'Mathematical Methods in Physics', 'theory': 3, 'lab': 0},
                {'code': 'FMP201', 'name': 'Modern Physics', 'theory': 3, 'lab': 2},
                {'code': 'PHW202', 'name': 'Optics', 'theory': 3, 'lab': 3},
                {'code': 'TPH201', 'name': 'Thermal Physics', 'theory': 3, 'lab': 2},
                {'code': 'Elective III', 'name': 'Elective III', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 3': {
            'Semester I': [
                {'code': 'APH303', 'name': 'Computational Physics', 'theory': 3, 'lab': 3},
                {'code': 'APH304', 'name': 'Applied Integrated Circuits and Logic Design', 'theory': 3, 'lab': 3},
                {'code': 'EPH301', 'name': 'Atmospheric Physics', 'theory': 3, 'lab': 2},
                {'code': 'QME301', 'name': 'Quantum Mechanics', 'theory': 4, 'lab': 0},
                {'code': 'Elective IV', 'name': 'Elective IV', 'theory': 2, 'lab': 0},
            ],
            'Semester II': [
                {'code': 'ANP301', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3},
                {'code': 'ANP302', 'name': 'Nuclear Physics', 'theory': 3, 'lab': 2},
                {'code': 'SSP301', 'name': 'Condensed Matter Physics', 'theory': 3, 'lab': 3},
                {'code': 'APH305', 'name': 'Machine Learning for Physics', 'theory': 3, 'lab': 3},
                {'code': 'Elective V', 'name': 'Elective V', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 4': {
            'Semester I': [
                {'code': 'THP402', 'name': 'Statistical Physics', 'theory': 4, 'lab': 0},
                {'code': 'EMT402', 'name': 'Electromagnetic Theory', 'theory': 4, 'lab': 0},
                {'code': 'SSP402', 'name': 'Advanced Condensed Matter Physics', 'theory': 3, 'lab': 3},
                {'code': 'QME402', 'name': 'Advanced Quantum Mechanics', 'theory': 4, 'lab': 0},
                {'code': 'CRD403', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
            ],
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
                {'code': 'Elective I', 'name': 'Elective I', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 2': {
            'Semester I': [
                {'code': 'BTS202', 'name': 'Plant Anatomy and Physiology', 'theory': 3, 'lab': 3},
                {'code': 'BCH201', 'name': 'Biochemistry', 'theory': 3, 'lab': 4},
                {'code': 'ZLS201', 'name': 'Invertebrate Biology and Parasitology', 'theory': 3, 'lab': 3},
                {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
                {'code': 'Elective II', 'name': 'Elective II', 'theory': 2, 'lab': 0},
            ],
            'Semester II': [
                {'code': 'BTS203', 'name': 'Embryology of Angiosperms', 'theory': 3, 'lab': 6},
                {'code': 'BTZ202', 'name': 'Genetics', 'theory': 3, 'lab': 4},
                {'code': 'ZLS202', 'name': 'Cell and Molecular Biology', 'theory': 3, 'lab': 4},
                {'code': 'ZLS203', 'name': 'Chordate Biology', 'theory': 3, 'lab': 3},
                {'code': 'Elective III', 'name': 'Elective III', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 3': {
            'Semester I': [
                {'code': 'BTS304', 'name': 'Fungi and Plant Pathology', 'theory': 3, 'lab': 3},
                {'code': 'GRS301', 'name': 'GIS and Remote Sensing', 'theory': 2, 'lab': 3},
                {'code': 'ZLS304', 'name': 'Anatomy and Physiology of Vertebrates', 'theory': 3, 'lab': 3},
                {'code': 'ZLS305', 'name': 'Developmental Biology', 'theory': 3, 'lab': 3},
                {'code': 'Elective IV', 'name': 'Elective IV', 'theory': 2, 'lab': 0},
            ],
            'Semester II': [
                {'code': 'BTS305', 'name': 'Principles of Plant Systematics', 'theory': 3, 'lab': 3},
                {'code': 'BTS306', 'name': 'Horticulture and Postharvest Management', 'theory': 3, 'lab': 3},
                {'code': 'BTZ303', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
                {'code': 'BTZ304', 'name': 'Bioinformatics', 'theory': 2, 'lab': 4},
                {'code': 'Elective V', 'name': 'Elective V', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 4': {
            'Semester I': [
                {'code': 'BTS407', 'name': 'Ethnobotany and Phytochemistry', 'theory': 3, 'lab': 4},
                {'code': 'BTZ405', 'name': 'Biotechnology and Tissue Culture', 'theory': 3, 'lab': 4},
                {'code': 'BTZ406', 'name': 'Ecology and Biodiversity Conservation', 'theory': 3, 'lab': 3},
                {'code': 'ZLS406', 'name': 'Freshwater Biology', 'theory': 3, 'lab': 3},
                {'code': 'CRD403', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
            ],
            'Semester II': [
                {'code': 'ZLS407', 'name': 'Animal Behaviour', 'theory': 3, 'lab': 3},
                {'code': 'BTZ407', 'name': 'Immunology and Forensic Biology', 'theory': 3, 'lab': 4},
                {'code': 'CRD404', 'name': 'Capstone Project II', 'theory': 2, 'lab': 4},
            ]
        }
    },
    'Chemistry_New': {
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
        },
        'Year 4': {
            'Semester I': [
                {'code': 'THP402', 'name': 'Statistical Physics', 'theory': 4, 'lab': 0},
                {'code': 'EMT402', 'name': 'Electromagnetic Theory', 'theory': 4, 'lab': 0},
                {'code': 'SSP402', 'name': 'Advanced Condensed Matter Physics', 'theory': 3, 'lab': 3},
                {'code': 'QME402', 'name': 'Advanced Quantum Mechanics', 'theory': 4, 'lab': 0},
                {'code': 'CRD403', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
            ],
            'Semester II': [
                {'code': 'CME402', 'name': 'Lagrangian and Hamiltonian Mechanics', 'theory': 3, 'lab': 0},
                {'code': 'EPH402', 'name': 'Physics of Renewable Energy', 'theory': 3, 'lab': 2},
                {'code': 'CRD404', 'name': 'Capstone Project II', 'theory': 2, 'lab': 4},
            ]
        }
    }
}

# ==========================================
# 4. FACULTY LIST
# ==========================================
FACULTY_LIST = [
    "Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan",
    "Ms. Kuenzang Choki", "Ms. Sangay Yuden", "Mr. Tashi Dendup",
    "Shacha Thinley", "Nachiketa Homchaudhuri", "Mon B Ghalley",
    "Dr. Karma Tenzin", "Rit Wik Sharma", "Ugyen D Tamang",
    "Asst. Prof. Karma Wangchuck", "Mohan S Rana", "Tshering Dekar",
    "Dr. Bimal K Chetri", "Sonam Tobgay", "Dechen Lhendup",
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
    if wam == 0:
        return 'No Load', '⚪', '#6c757d', 'Select modules to begin'
    elif wam < 12:
        return 'Light Load', '🟡', '#ffc107', 'Capacity available for additional modules'
    elif wam <= 16:
        return 'Balanced', '🟢', '#28a745', 'Workload is within optimal range'
    else:
        return 'Heavy Load', '🔴', '#dc3545', 'Consider redistributing workload'

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

def get_history(name):
    log_file = 'workload_logs.json'
    if not os.path.exists(log_file):
        return []
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
        return [l for l in logs if l['faculty'] == name]
    except:
        return []

# ==========================================
# 6. SESSION STATE
# ==========================================
if 'modules' not in st.session_state:
    st.session_state.modules = []
if 'counts' not in st.session_state:
    st.session_state.counts = {}
if 'rooms' not in st.session_state:
    st.session_state.rooms = {}
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'admin' not in st.session_state:
    st.session_state.admin = False

# ==========================================
# 7. ACADEMIC HEADER
# ==========================================
st.markdown(f"""
<div class="academic-header">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">
        <div>
            <h1>Workload & Roaster System</h1>
            <div class="subtitle">Department of Natural Sciences • Sherubtse College •Royal University of Bhutan</div>
            <div class="meta">
                <span class="badge">📅 {datetime.now().strftime('%B %d, %Y')}</span>
                <span class="badge" style="margin-left:0.5rem;">📚 Autumn 2026</span>
                <span class="badge" style="margin-left:0.5rem;">🏛️ Academic Year 2026-2027</span>
            </div>
        </div>
        <div style="text-align:right; font-size:0.8rem; color:#8899b0;">
            <div>Faculty Self-Service Portal</div>
            <div>Workload Allocation Module</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 8. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### Faculty Profile")
    
    name_opt = st.radio("Select Option", ["From Directory", "Enter Manually"], index=0)
    
    if name_opt == "From Directory":
        name = st.selectbox(
            "Select Faculty Name",
            [""] + sorted(FACULTY_LIST),
            help="Select your name from the directory"
        )
    else:
        name = st.text_input(
            "Enter Full Name",
            value=st.session_state.name,
            placeholder="e.g., Dr. Jas Raj Subba"
        )
    
    if name:
        st.session_state.name = name
        st.success(f"Welcome, {name}")
    
    st.selectbox(
        "Designation",
        ["Professor", "Associate Professor", "Assistant Professor", "Senior Lecturer", "Lecturer"]
    )
    
    st.divider()
    st.markdown("### Module Selection")
    
    prog = st.selectbox("Programme", ["Physics", "Chemistry", "Life Sciences"])
    curr = st.selectbox("Curriculum", ["Old (3-Year)", "New (4-Year)"])
    
    prog_key = {"Physics":"Physics", "Chemistry":"Chemistry", "Life Sciences":"LifeSciences"}[prog]
    curr_key = "Old" if curr == "Old (3-Year)" else "New"
    key = f"{prog_key}_{curr_key}"
    
    year = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
    sem = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI"])
    
    modules = []
    try:
        modules = MODULE_DATABASE[key][year][sem]
    except:
        st.warning("No modules available for the selected parameters")
    
    if modules:
        opts = [f"{m['code']} - {m['name']}" for m in modules]
        sel = st.selectbox("Select Module", ["-- Select --"] + opts)
        
        if sel != "-- Select --":
            code = sel.split(" - ")[0]
            mod = next(m for m in modules if m['code'] == code)
            
            students = st.slider("Student Enrolment", 25, 40, 30)
            
            room = st.text_input(
                "Room / Laboratory",
                value=st.session_state.rooms.get(code, ""),
                placeholder="e.g., Science Hall 1, Lab 203"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Add Module", use_container_width=True):
                    if not any(m['code'] == code for m in st.session_state.modules):
                        st.session_state.modules.append(mod)
                        st.session_state.counts[code] = students
                        if room:
                            st.session_state.rooms[code] = room
                        st.success(f"Added: {code}")
                        st.rerun()
                    else:
                        st.warning("Module already in list")
            with col_b:
                if st.button("Clear All", use_container_width=True):
                    st.session_state.modules = []
                    st.session_state.counts = {}
                    st.session_state.rooms = {}
                    st.rerun()
    
    st.divider()
    if st.session_state.modules:
        st.metric("Modules Selected", len(st.session_state.modules))
        st.metric("Total Students", sum(st.session_state.counts.values()))
    
    st.divider()
    st.markdown("### Administrative Access")
    pin = st.text_input("PIN", type="password")
    if pin == "DNS777":
        st.session_state.admin = True
        st.success("Administrator access granted")

# ==========================================
# 9. MAIN CONTENT
# ==========================================
if not st.session_state.name:
    st.info("👈 Please select or enter your name in the sidebar to proceed")
    st.stop()

col_main, col_wam = st.columns([2, 1])

with col_main:
    st.markdown("### Selected Modules")
    
    if not st.session_state.modules:
        st.info("No modules selected. Use the sidebar to add modules.")
    else:
        total_t, total_l = 0, 0
        
        for mod in st.session_state.modules:
            students = st.session_state.counts.get(mod['code'], 25)
            room = st.session_state.rooms.get(mod['code'], "Not Assigned")
            total_t += mod['theory']
            total_l += mod['lab']
            
            w = calculate_wam([{**mod, 'students': students}])
            
            st.markdown(f"""
            <div class="module-academic">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                    <div>
                        <span class="code">{mod['code']}</span>
                        <span class="name"> - {mod['name']}</span>
                        <div class="details">
                            Theory: {mod['theory']}h • Laboratory: {mod['lab']}h • Students: {students}
                            <span style="margin-left:0.8rem;">Room: <strong>{room}</strong></span>
                        </div>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                        <span style="background:#1a2a4a; color:white; padding:0.15rem 0.6rem; border-radius:4px; font-size:0.75rem;">{mod['theory'] + mod['lab']}h</span>
                        <span style="font-weight:600; color:#1a2a4a;">WAM: {w:.1f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_r, col_rm = st.columns([4, 1])
            with col_rm:
                if st.button("✏️ Room", key=f"edit_room_{mod['code']}"):
                    new_room = st.text_input("Update Room", value=room, key=f"room_input_{mod['code']}")
                    if new_room:
                        st.session_state.rooms[mod['code']] = new_room
                        st.rerun()
            
            if st.button(f"Remove {mod['code']}", key=f"rm_{mod['code']}"):
                st.session_state.modules.remove(mod)
                if mod['code'] in st.session_state.counts:
                    del st.session_state.counts[mod['code']]
                if mod['code'] in st.session_state.rooms:
                    del st.session_state.rooms[mod['code']]
                st.rerun()
        
        st.markdown(f"""
        <div class="stats-academic">
            <div class="item"><div class="value">{len(st.session_state.modules)}</div><div class="label">Modules</div></div>
            <div class="item"><div class="value">{total_t}h</div><div class="label">Theory Hours</div></div>
            <div class="item"><div class="value">{total_l}h</div><div class="label">Lab Hours</div></div>
            <div class="item"><div class="value">{sum(st.session_state.counts.values())}</div><div class="label">Students</div></div>
        </div>
        """, unsafe_allow_html=True)

with col_wam:
    st.markdown("### Workload Allocation Score")
    
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
        <div class="wam-professional">
            <div class="number">{wam}</div>
            <div class="label">Workload Allocation Model Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align:center;">
            <span class="status-badge" style="background:{color};color:white;">{emoji} {status}</span>
            <p style="font-size:0.8rem; color:#7f8c8d; margin-top:0.3rem;">{msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Workload Distribution")
        progress = min(wam / 16, 1.0)
        st.progress(progress)
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
            df_chart = pd.DataFrame(data)
            fig = px.bar(df_chart, x='Module', y='WAM', color='WAM', 
                        color_continuous_scale='Blues', height=250)
            fig.update_layout(
                showlegend=False,
                margin=dict(l=0, r=0, t=20, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add modules to calculate your workload score")

# ==========================================
# 10. THRESHOLD GUIDE
# ==========================================
st.markdown("""
<div class="threshold-academic">
    <div class="item"><span class="dot" style="background:#ffc107;"></span> Light (WAM &lt; 12)</div>
    <div class="item"><span class="dot" style="background:#28a745;"></span> Balanced (12 - 16)</div>
    <div class="item"><span class="dot" style="background:#dc3545;"></span> Heavy (WAM &gt; 16)</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 11. PRINTABLE CONTENT - COMPLETE PAGE
# ==========================================
# This section contains everything that will be printed
st.markdown('<div class="print-content">', unsafe_allow_html=True)

# Print Header
st.markdown(f"""
<div style="text-align:center; padding:1rem 0; border-bottom:3px solid #1a2a4a; margin-bottom:1.5rem;">
    <h1 style="color:#1a2a4a; font-size:1.8rem; margin:0;">Workload & Roaster Report</h1>
    <p style="color:#495057; margin:0.2rem 0;">Department of Natural Sciences • Royal University of Bhutan</p>
    <p style="color:#7f8c8d; font-size:0.85rem; margin:0;">{datetime.now().strftime('%B %d, %Y')} • Autumn 2026</p>
</div>
""", unsafe_allow_html=True)

# Faculty Info
st.markdown(f"""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-bottom:1.5rem; padding:1rem; background:#f8f9fa; border-radius:6px;">
    <div><strong>Faculty Name:</strong> {st.session_state.name}</div>
    <div><strong>Designation:</strong> {st.session_state.get('designation', 'Not Specified')}</div>
    <div><strong>Programme:</strong> {st.session_state.get('programme', 'Not Specified')}</div>
    <div><strong>Semester:</strong> Autumn 2026</div>
</div>
""", unsafe_allow_html=True)

# Modules Table
if st.session_state.modules:
    st.markdown("### Teaching Assignment")
    
    data = []
    for m in st.session_state.modules:
        students = st.session_state.counts.get(m['code'], 25)
        room = st.session_state.rooms.get(m['code'], "Not Assigned")
        w = calculate_wam([{**m, 'students': students}])
        data.append({
            'Code': m['code'],
            'Module': m['name'],
            'Theory': m['theory'],
            'Lab': m['lab'],
            'Students': students,
            'Room': room,
            'WAM': w
        })
    df_print = pd.DataFrame(data)
    
    # Display as table
    st.table(df_print)
    
    # Summary
    st.markdown(f"""
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:0.5rem; margin-top:1rem; padding:1rem; background:#f8f9fa; border-radius:6px; text-align:center;">
        <div><strong>Total Modules</strong><br>{len(st.session_state.modules)}</div>
        <div><strong>Total Theory</strong><br>{df_print['Theory'].sum()}h</div>
        <div><strong>Total Lab</strong><br>{df_print['Lab'].sum()}h</div>
        <div><strong>Total Students</strong><br>{df_print['Students'].sum()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # WAM Score
    wam_total = calculate_wam([
        {**m, 'students': st.session_state.counts.get(m['code'], 25)}
        for m in st.session_state.modules
    ])
    status, emoji, color, msg = get_status(wam_total)
    
    st.markdown(f"""
    <div style="background:#1a2a4a; color:white; padding:1rem; border-radius:6px; margin-top:1rem; text-align:center;">
        <div style="font-size:1.5rem; font-weight:700;">{wam_total}</div>
        <div style="font-size:0.8rem; opacity:0.8;">Workload Allocation Model Score</div>
        <div style="margin-top:0.3rem; background:{color}; display:inline-block; padding:0.2rem 1rem; border-radius:4px; color:white; font-weight:600;">{emoji} {status}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No modules selected")

# Footer
st.markdown("""
<div style="text-align:center; margin-top:2rem; padding-top:1rem; border-top:2px solid #e8ecf0; color:#7f8c8d; font-size:0.75rem;">
    Generated by Workload & Roaster System • Royal University of Bhutan
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End print-content

# ==========================================
# 12. DETAILED SECTIONS (Non-printable)
# ==========================================
if st.session_state.modules:
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Detailed Breakdown", "Analytics", "History", "Timetable"])
    
    with tab1:
        data = []
        for m in st.session_state.modules:
            students = st.session_state.counts.get(m['code'], 25)
            room = st.session_state.rooms.get(m['code'], "Not Assigned")
            w = calculate_wam([{**m, 'students': students}])
            data.append({
                'Code': m['code'],
                'Module': m['name'],
                'Theory': m['theory'],
                'Lab': m['lab'],
                'Students': students,
                'Room': room,
                'WAM': w,
                'Type': 'Theory + Lab' if m['lab'] > 0 else 'Theory Only'
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, f"workload_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(values=[df['Theory'].sum(), df['Lab'].sum()], 
                        names=['Theory Hours', 'Lab Hours'], 
                        title="Theory vs Laboratory Distribution",
                        color_discrete_sequence=['#1a2a4a', '#c9a84c'])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.bar(df, x='Code', y='WAM', title="WAM Distribution by Module", 
                        color='WAM', color_continuous_scale='Blues', height=300)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Summary Statistics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Average WAM", f"{df['WAM'].mean():.1f}")
        c2.metric("Maximum WAM", f"{df['WAM'].max():.1f}")
        c3.metric("Minimum WAM", f"{df['WAM'].min():.1f}")
        c4.metric("Total Students", df['Students'].sum())
    
    with tab3:
        st.subheader("Workload History")
        history = get_history(st.session_state.name)
        if history:
            df_h = pd.DataFrame(history)
            df_h['timestamp'] = pd.to_datetime(df_h['timestamp'])
            df_h = df_h.sort_values('timestamp', ascending=False)
            st.dataframe(df_h[['timestamp', 'wam', 'status']], use_container_width=True, hide_index=True)
        else:
            st.info("No historical records found")
    
    with tab4:
        st.subheader("Timetable View")
        st.caption("Academic schedule with room allocations")
        
        st.markdown(f"""
        <div class="timetable-academic">
            <div class="header">
                Teaching Timetable
                <span style="font-size:0.8rem; font-weight:400; color:#7f8c8d; float:right;">
                    {st.session_state.name} • {datetime.now().strftime('%B %d, %Y')}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        for i, row in df.iterrows():
            st.markdown(f"""
            <div class="timetable-entry">
                <div><span class="label">Module:</span> <span class="value">{row['Code']}</span></div>
                <div><span class="label">Title:</span> <span class="value">{row['Module']}</span></div>
                <div><span class="label">Hours:</span> <span class="value">{row['Theory']}T + {row['Lab']}L</span></div>
                <div><span class="label">Students:</span> <span class="value">{row['Students']}</span></div>
                <div><span class="label">Room:</span> <span class="value" style="color:#1a2a4a; font-weight:600;">{row['Room']}</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="margin-top:1rem; padding-top:0.5rem; border-top:2px solid #e8ecf0; text-align:center; font-size:0.75rem; color:#7f8c8d;">
                Generated by Workload & Roaster System • Royal University of Bhutan
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 13. PRINT BUTTON - AT BOTTOM OF PAGE
# ==========================================
st.divider()
st.markdown("""
<div class="no-print" style="text-align:center; padding:0.5rem 0;">
    <button onclick="window.print()" style="
        background: #1a2a4a;
        color: white;
        border: none;
        padding: 0.7rem 3rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(26,42,74,0.2);
    " onmouseover="this.style.background='#2a4a6a'; this.style.boxShadow='0 4px 12px rgba(26,42,74,0.3)';" 
    onmouseout="this.style.background='#1a2a4a'; this.style.boxShadow='0 2px 8px rgba(26,42,74,0.2)';">
        🖨️ Print Complete Report
    </button>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 14. ADMIN SECTION
# ==========================================
if st.session_state.admin:
    st.divider()
    st.markdown("""
    <div class="admin-academic">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <div>
                <span class="title">🔐 Administrative Dashboard</span>
                <span class="sub"> • Master Workload Records</span>
            </div>
            <div style="font-size:0.8rem; opacity:0.6;">Secure Access</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    log_file = 'workload_logs.json'
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            if logs:
                df_a = pd.DataFrame(logs)
                df_a['timestamp'] = pd.to_datetime(df_a['timestamp'])
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Submissions", len(df_a))
                c2.metric("Unique Faculty", df_a['faculty'].nunique())
                c3.metric("Average WAM", round(df_a['wam'].mean(), 2))
                c4.metric("Heavy Load Cases", len(df_a[df_a['status'] == 'Heavy Load']))
                
                st.dataframe(df_a.sort_values('timestamp', ascending=False), use_container_width=True, hide_index=True)
                
                csv_a = df_a.to_csv(index=False).encode('utf-8')
                st.download_button("Download Full Report", csv_a, f"DNS_Report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
                
                if st.button("Purge Database", use_container_width=True):
                    os.remove(log_file)
                    st.rerun()
        except:
            st.info("No data available")

# ==========================================
# 15. FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style="text-align:center; color:#7f8c8d; font-size:0.75rem; padding:0.5rem 0;">
    Department of Natural Sciences • Royal University of Bhutan • Autumn 2026
</div>
""", unsafe_allow_html=True)
