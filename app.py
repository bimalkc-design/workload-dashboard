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
# 2. PREMIUM STYLING
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .main { padding: 0 0.5rem !important; }
    .block-container { padding: 0.5rem 0.5rem 1rem 0.5rem !important; max-width: 100% !important; }
    
    /* Premium Header */
    .premium-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 1.8rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    .premium-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .premium-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #fff, #a8b5ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .premium-header .sub {
        font-size: 0.95rem;
        opacity: 0.7;
        margin-top: 0.2rem;
        -webkit-text-fill-color: #ccc;
    }
    .premium-header .badge {
        display: inline-block;
        background: rgba(102,126,234,0.2);
        padding: 0.2rem 1rem;
        border-radius: 20px;
        font-size: 0.7rem;
        border: 1px solid rgba(102,126,234,0.3);
        margin-top: 0.3rem;
        -webkit-text-fill-color: #a8b5ff;
    }
    
    /* WAM Card */
    .wam-premium {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.8rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(102,126,234,0.35);
        margin: 0.5rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    .wam-premium:hover { transform: scale(1.02); }
    .wam-premium .number {
        font-size: 3.8rem;
        font-weight: 800;
        line-height: 1.2;
        position: relative;
        z-index: 1;
    }
    .wam-premium .label {
        font-size: 0.85rem;
        opacity: 0.85;
        position: relative;
        z-index: 1;
    }
    
    /* Status Badge */
    .status-premium {
        display: inline-block;
        padding: 0.4rem 1.8rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Module Cards */
    .module-premium {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.4rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    .module-premium:hover {
        box-shadow: 0 4px 20px rgba(102,126,234,0.15);
        transform: translateX(4px);
    }
    .module-premium .code { font-weight: 700; color: #667eea; font-size: 1rem; }
    .module-premium .name { font-size: 0.9rem; color: #333; }
    .module-premium .details { font-size: 0.78rem; color: #888; margin-top: 0.1rem; }
    
    /* Stats Grid */
    .stats-premium {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.6rem;
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin: 0.4rem 0;
    }
    .stats-premium .item { text-align: center; }
    .stats-premium .value { font-size: 1.5rem; font-weight: 800; color: #1a1a2e; }
    .stats-premium .label { font-size: 0.65rem; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Threshold Guide */
    .threshold-premium {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        background: white;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin: 0.4rem 0;
    }
    .threshold-premium .item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 500; }
    .threshold-premium .dot { width: 14px; height: 14px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
    
    /* Admin Zone */
    .admin-premium {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #daa520;
        color: #daa520;
        margin: 0.8rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.4rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102,126,234,0.25);
        width: 100%;
        font-size: 0.85rem;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.35);
    }
    
    /* Print Button - Special */
    .print-btn > button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        box-shadow: 0 4px 15px rgba(40,167,69,0.3);
    }
    .print-btn > button:hover {
        box-shadow: 0 8px 25px rgba(40,167,69,0.4);
    }
    
    /* Timetable Card */
    .timetable-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }
    .timetable-card .header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a1a2e;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .timetable-entry {
        display: grid;
        grid-template-columns: 1fr 2fr 1fr 1fr 1fr;
        gap: 0.5rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f1f3f5;
        font-size: 0.85rem;
    }
    .timetable-entry .label { font-weight: 600; color: #495057; }
    .timetable-entry .value { color: #212529; }
    
    /* Mobile */
    @media (max-width: 768px) {
        .premium-header h1 { font-size: 1.5rem; }
        .wam-premium .number { font-size: 2.8rem; }
        .stats-premium { grid-template-columns: repeat(2, 1fr); }
        .threshold-premium { flex-direction: column; align-items: center; gap: 0.3rem; }
        .timetable-entry { grid-template-columns: 1fr; gap: 0.2rem; padding: 0.8rem 0; }
        .timetable-entry .label { font-weight: 700; }
    }
    
    /* Print Styles */
    @media print {
        .stApp { background: white !important; }
        .premium-header { background: #1a1a2e !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        .wam-premium { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; -webkit-print-color-adjust: exact !important; }
        .status-premium { -webkit-print-color-adjust: exact !important; }
        .module-premium { break-inside: avoid; }
        .stSidebar { display: none !important; }
        .stButton { display: none !important; }
        .stTabs { display: none !important; }
        .threshold-premium { display: none !important; }
        .admin-premium { display: none !important; }
        .no-print { display: none !important; }
        .print-only { display: block !important; }
        .timetable-card { break-inside: avoid; border: 1px solid #ddd !important; }
    }
    .print-only { display: none; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. COMPLETE MODULE DATABASE (YOUR DATA)
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
    if wam == 0:
        return 'No Load', '⚪', '#6c757d', 'Select modules to begin'
    elif wam < 12:
        return 'Light Load', '🟡', '#ffc107', 'You have capacity for more modules'
    elif wam <= 16:
        return 'Balanced', '🟢', '#28a745', 'Your workload is optimally balanced!'
    else:
        return 'Heavy Load', '🔴', '#dc3545', 'Consider sharing modules with colleagues'

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
# 7. HEADER
# ==========================================
st.markdown(f"""
<div class="premium-header">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; position:relative; z-index:1;">
        <div>
            <h1>📋 Workload & Roaster System</h1>
            <div class="sub">Department of Natural Sciences • Royal University of Bhutan</div>
            <span class="badge">📅 {datetime.now().strftime('%B %d, %Y')} • Autumn 2026</span>
        </div>
        <div class="top-right" style="text-align:right; font-size:0.8rem; opacity:0.6; -webkit-text-fill-color:#aaa;">
            <div>⚡ Faculty Self-Service</div>
            <div>📊 Real-time WAM</div>
            <div>🏫 Room Allocation</div>
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
        name = st.text_input("Your Name", value=st.session_state.name, placeholder="e.g., Dr. Jas Raj Subba")
    
    if name:
        st.session_state.name = name
        st.success(f"✅ Welcome, {name}!")
    
    st.selectbox("Designation", ["Professor", "Associate Professor", "Assistant Professor", "Senior Lecturer", "Lecturer"])
    
    st.divider()
    st.markdown("### 📚 Module Selection")
    
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
            
            # Room/Lab Entry - NEW FEATURE
            room = st.text_input(
                "Room/Lab Name/Number",
                value=st.session_state.rooms.get(code, ""),
                placeholder="e.g., Sc. Hall 1, Lab 203"
            )
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("➕ Add", use_container_width=True):
                    if not any(m['code'] == code for m in st.session_state.modules):
                        st.session_state.modules.append(mod)
                        st.session_state.counts[code] = students
                        if room:
                            st.session_state.rooms[code] = room
                        st.success(f"✅ Added {code}")
                        st.rerun()
                    else:
                        st.warning("⚠️ Already added")
            with c2:
                if st.button("🗑️ Clear", use_container_width=True):
                    st.session_state.modules = []
                    st.session_state.counts = {}
                    st.session_state.rooms = {}
                    st.rerun()
    
    st.divider()
    if st.session_state.modules:
        st.metric("📦 Modules", len(st.session_state.modules))
        st.metric("👨‍🎓 Students", sum(st.session_state.counts.values()))
    
    st.divider()
    st.markdown("### 🔒 Admin")
    pin = st.text_input("PIN", type="password")
    if pin == "DNS777":
        st.session_state.admin = True
        st.success("🔓 Admin mode ON")

# ==========================================
# 9. MAIN CONTENT
# ==========================================
if not st.session_state.name:
    st.info("👈 Please select or enter your name in the sidebar to get started")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Your Selected Modules")
    
    if not st.session_state.modules:
        st.info("👈 Select modules from the sidebar")
    else:
        total_t, total_l = 0, 0
        
        for mod in st.session_state.modules:
            students = st.session_state.counts.get(mod['code'], 25)
            room = st.session_state.rooms.get(mod['code'], "Not Assigned")
            total_t += mod['theory']
            total_l += mod['lab']
            
            w = calculate_wam([{**mod, 'students': students}])
            
            st.markdown(f"""
            <div class="module-premium">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                    <div>
                        <span class="code">{mod['code']}</span>
                        <span class="name"> - {mod['name']}</span>
                        <div class="details">
                            📖 {mod['theory']}h Theory • 🧪 {mod['lab']}h Lab • 👨‍🎓 {students} students
                            <span style="margin-left:0.8rem;">🏫 <strong>{room}</strong></span>
                        </div>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.8rem; flex-wrap:wrap;">
                        <span style="background:#667eea; color:white; padding:0.2rem 0.8rem; border-radius:20px; font-size:0.8rem; font-weight:600;">{mod['theory'] + mod['lab']}h</span>
                        <span style="font-weight:600; color:#764ba2;">WAM: {w:.1f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Edit Room Button
            col_a, col_b = st.columns([4, 1])
            with col_b:
                if st.button(f"✏️ Room", key=f"edit_room_{mod['code']}"):
                    new_room = st.text_input("Update Room", value=room, key=f"room_input_{mod['code']}")
                    if new_room:
                        st.session_state.rooms[mod['code']] = new_room
                        st.rerun()
            
            if st.button(f"✖ Remove {mod['code']}", key=f"rm_{mod['code']}"):
                st.session_state.modules.remove(mod)
                if mod['code'] in st.session_state.counts:
                    del st.session_state.counts[mod['code']]
                if mod['code'] in st.session_state.rooms:
                    del st.session_state.rooms[mod['code']]
                st.rerun()
        
        st.markdown(f"""
        <div class="stats-premium">
            <div class="item"><div class="value">{len(st.session_state.modules)}</div><div class="label">Modules</div></div>
            <div class="item"><div class="value">{total_t}h</div><div class="label">Theory</div></div>
            <div class="item"><div class="value">{total_l}h</div><div class="label">Lab</div></div>
            <div class="item"><div class="value">{sum(st.session_state.counts.values())}</div><div class="label">Students</div></div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 Your WAM Score")
    
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
        <div class="wam-premium">
            <div class="number">{wam}</div>
            <div class="label">Workload Allocation Model Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align:center;">
            <span class="status-premium" style="background:{color};color:white;">{emoji} {status}</span>
            <p style="font-size:0.85rem;color:#888;margin-top:0.3rem;">{msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Workload Level")
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
<div class="threshold-premium">
    <div class="item"><span class="dot" style="background:#ffc107;"></span> Light (WAM &lt; 12)</div>
    <div class="item"><span class="dot" style="background:#28a745;"></span> Balanced (12 - 16)</div>
    <div class="item"><span class="dot" style="background:#dc3545;"></span> Heavy (WAM &gt; 16)</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 11. TIMETABLE & ROASTER - NEW FEATURE
# ==========================================
if st.session_state.modules:
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Detailed Breakdown", "📈 Analytics", "📜 Your History", "📋 Timetable & Roaster"])
    
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
                'Type': 'T+L' if m['lab'] > 0 else 'Theory'
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, f"workload_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(values=[df['Theory'].sum(), df['Lab'].sum()], 
                        names=['Theory', 'Lab'], title="Theory vs Lab Distribution")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.bar(df, x='Code', y='WAM', title="WAM by Module", color='WAM',
                        color_continuous_scale='Viridis', height=300)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 Summary Statistics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg WAM", f"{df['WAM'].mean():.1f}")
        c2.metric("Max WAM", f"{df['WAM'].max():.1f}")
        c3.metric("Min WAM", f"{df['WAM'].min():.1f}")
        c4.metric("Total Students", df['Students'].sum())
    
    with tab3:
        st.subheader("📜 Your Workload History")
        history = get_history(st.session_state.name)
        if history:
            df_h = pd.DataFrame(history)
            df_h['timestamp'] = pd.to_datetime(df_h['timestamp'])
            df_h = df_h.sort_values('timestamp', ascending=False)
            st.dataframe(df_h[['timestamp', 'wam', 'status']], use_container_width=True, hide_index=True)
        else:
            st.info("No history found")
    
    with tab4:
        st.subheader("📋 Timetable & Roaster")
        st.caption("Your complete teaching schedule with room allocations")
        
        # Generate Timetable Card
        st.markdown(f"""
        <div class="timetable-card" id="timetable-print">
            <div class="header">
                📋 Teaching Timetable & Roaster
                <span style="font-size:0.8rem; font-weight:400; color:#888; float:right;">
                    {st.session_state.name} • {datetime.now().strftime('%B %d, %Y')}
                </span>
            </div>
            <div style="margin-bottom:0.8rem;">
                <span style="font-weight:600; color:#495057;">Department:</span> Natural Sciences
                <span style="margin-left:1.5rem; font-weight:600; color:#495057;">Semester:</span> Autumn 2026
            </div>
        """, unsafe_allow_html=True)
        
        # Timetable entries
        for i, row in df.iterrows():
            st.markdown(f"""
            <div class="timetable-entry">
                <div><span class="label">Module:</span> <span class="value">{row['Code']}</span></div>
                <div><span class="label">Name:</span> <span class="value">{row['Module']}</span></div>
                <div><span class="label">Hours:</span> <span class="value">{row['Theory']}T + {row['Lab']}L</span></div>
                <div><span class="label">Students:</span> <span class="value">{row['Students']}</span></div>
                <div><span class="label">Room:</span> <span class="value" style="color:#667eea; font-weight:600;">{row['Room']}</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="margin-top:1rem; padding-top:0.5rem; border-top:2px solid #e9ecef; text-align:center; font-size:0.8rem; color:#888;">
                Generated by Workload & Roaster System • Royal University of Bhutan
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Print Button - Using JavaScript
        st.markdown("""
        <div class="no-print" style="margin-top:1rem;">
            <button onclick="window.print()" style="
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                border: none;
                padding: 0.6rem 2rem;
                border-radius: 10px;
                font-weight: 700;
                font-size: 1rem;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(40,167,69,0.3);
                transition: all 0.3s ease;
                width: 100%;
            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(40,167,69,0.4)';" 
            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(40,167,69,0.3)';">
                🖨️ Print Timetable & Roaster
            </button>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 12. ADMIN
# ==========================================
if st.session_state.admin:
    st.divider()
    st.markdown("""
    <div class="admin-premium">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <div>
                <span style="font-size:1.2rem; font-weight:700;">🔐 ADMIN COMMAND CENTER</span>
                <span style="font-size:0.85rem; opacity:0.7;"> • Master Workload Records</span>
            </div>
            <div style="font-size:0.8rem; opacity:0.6;">🔒 Secure Access</div>
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
                c3.metric("Avg WAM", round(df_a['wam'].mean(), 2))
                c4.metric("Heavy Load", len(df_a[df_a['status'] == 'Heavy Load']))
                
                st.dataframe(df_a.sort_values('timestamp', ascending=False), use_container_width=True, hide_index=True)
                
                csv_a = df_a.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Full Report", csv_a, f"DNS_Report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
                
                if st.button("🗑️ Purge Database", use_container_width=True):
                    os.remove(log_file)
                    st.rerun()
        except:
            st.info("No data")

# ==========================================
# 13. FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style="text-align:center;color:#888;font-size:0.8rem;padding:0.5rem 0;">
    Department of Natural Sciences • Royal University of Bhutan • Autumn 2026
</div>
""", unsafe_allow_html=True)
