import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

# Add this line to handle rerun
try:
    from streamlit import rerun as st_rerun
except ImportError:
    # For older versions of Streamlit
    def st_rerun():
        st.experimental_rerun()
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
    
    section[data-testid="stSidebar"] {
        height: 100vh !important;
        overflow: hidden !important;
        position: sticky !important;
        top: 0 !important;
        background: #f8f9fa !important;
        border-right: 1px solid #e8ecf0 !important;
        z-index: 10 !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        height: 100% !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        padding-bottom: 3rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        scroll-behavior: smooth !important;
    }
    
    .stSidebar .st-emotion-cache-1r6slb0 {
        max-height: 100vh !important;
        overflow-y: auto !important;
        padding-bottom: 2rem !important;
    }
    
    .stSidebar .st-emotion-cache-1r6slb0 {
        padding-right: 0.5rem !important;
        padding-left: 0.5rem !important;
    }
    
    .stSidebar .stRadio {
        margin-bottom: 0.5rem !important;
    }
    
    .stSidebar .stTextInput {
        margin-bottom: 0.5rem !important;
    }
    
    .stSidebar .stSlider {
        margin-bottom: 0.5rem !important;
    }
    
    .stSidebar .stButton {
        margin-bottom: 0.5rem !important;
    }
    
    .stSidebar .stNumberInput {
        margin-bottom: 0.5rem !important;
    }
    
    .stSidebar .stSelectbox {
        margin-bottom: 0.5rem !important;
    }
    
    /* Student counter styling */
    .student-counter {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: #f8f9fa;
        padding: 0.3rem 0.5rem;
        border-radius: 6px;
        border: 1px solid #e8ecf0;
        margin: 0.3rem 0;
    }
    .student-counter .counter-btn {
        background: #1a2a4a;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.2rem 0.8rem;
        font-size: 1.2rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s;
        min-width: 32px;
        min-height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .student-counter .counter-btn:hover {
        background: #2a4a6a;
        transform: scale(1.05);
    }
    .student-counter .counter-btn:active {
        transform: scale(0.95);
    }
    .student-counter .counter-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a2a4a;
        min-width: 40px;
        text-align: center;
    }
    .student-counter .counter-label {
        font-size: 0.8rem;
        color: #7f8c8d;
        margin-right: 0.5rem;
    }
    
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
    
    /* WAM Card */
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
    
    .status-badge {
        display: inline-block;
        padding: 0.3rem 1.5rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.3px;
    }
    
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
    
    .module-type-badge {
        display: inline-block;
        padding: 0.1rem 0.6rem;
        border-radius: 3px;
        font-size: 0.65rem;
        font-weight: 600;
        margin-left: 0.3rem;
    }
    .module-type-badge.theory {
        background: #e3f2fd;
        color: #1565c0;
    }
    .module-type-badge.lab {
        background: #f3e5f5;
        color: #7b1fa2;
    }
    .module-type-badge.both {
        background: #e8f5e9;
        color: #2e7d32;
    }
    
    .module-detail-box {
        background: #f8f9fa;
        padding: 0.5rem 0.8rem;
        border-radius: 4px;
        margin: 0.3rem 0;
        border-left: 3px solid #c9a84c;
        font-size: 0.8rem;
    }
    .module-detail-box strong {
        color: #1a2a4a;
    }
    
    @media (max-width: 768px) {
        .academic-header h1 { font-size: 1.4rem; }
        .wam-professional .number { font-size: 2.5rem; }
        .stats-academic { grid-template-columns: repeat(2, 1fr); }
        .threshold-academic { flex-direction: column; align-items: center; gap: 0.2rem; }
        .timetable-entry { grid-template-columns: 1fr; gap: 0.1rem; padding: 0.6rem 0; }
        .student-counter { flex-wrap: wrap; }
    }
    
    @media print {
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
        .stDataFrame { display: none !important; }
        .stPlotlyChart { display: none !important; }
        .stDownloadButton { display: none !important; }
        .stNumberInput { display: none !important; }
        .student-counter { display: none !important; }
        
        .print-content { display: block !important; }
        .print-content * { display: revert !important; }
        
        .academic-header { 
            background: #1a2a4a !important; 
            -webkit-print-color-adjust: exact !important; 
            print-color-adjust: exact !important;
            padding: 0.8rem 1.2rem !important;
            margin-bottom: 0.8rem !important;
        }
        .academic-header h1 { font-size: 1.4rem !important; }
        .academic-header .subtitle { font-size: 0.75rem !important; }
        .academic-header .meta { font-size: 0.6rem !important; }
        
        .wam-professional { 
            background: #1a2a4a !important; 
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
            padding: 0.8rem !important;
            margin: 0.3rem 0 !important;
        }
        .wam-professional .number { font-size: 2rem !important; }
        .wam-professional .label { font-size: 0.6rem !important; }
        
        .status-badge { 
            -webkit-print-color-adjust: exact !important; 
            print-color-adjust: exact !important;
            padding: 0.15rem 1rem !important;
            font-size: 0.7rem !important;
        }
        
        .module-academic { 
            break-inside: avoid; 
            border: 1px solid #ddd !important;
            padding: 0.4rem 0.8rem !important;
            margin: 0.15rem 0 !important;
        }
        .module-academic .code { font-size: 0.8rem !important; }
        .module-academic .name { font-size: 0.75rem !important; }
        .module-academic .details { font-size: 0.65rem !important; }
        
        .timetable-academic { 
            break-inside: avoid; 
            border: 1px solid #ddd !important;
            padding: 0.8rem !important;
            margin: 0.3rem 0 !important;
        }
        .timetable-academic .header { 
            font-size: 0.9rem !important;
            padding-bottom: 0.3rem !important;
            margin-bottom: 0.5rem !important;
        }
        .timetable-entry { 
            break-inside: avoid;
            padding: 0.2rem 0 !important;
            font-size: 0.7rem !important;
            grid-template-columns: 0.8fr 1.5fr 0.8fr 0.8fr 1.2fr !important;
            gap: 0.3rem !important;
        }
        
        .print-content table {
            font-size: 0.7rem !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        .print-content table th,
        .print-content table td {
            padding: 0.2rem 0.4rem !important;
            border: 1px solid #ddd !important;
        }
        .print-content table th {
            background: #f0f0f0 !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        .print-content [style*="display:grid"] {
            padding: 0.4rem !important;
            margin-top: 0.3rem !important;
            gap: 0.2rem !important;
        }
        .print-content [style*="display:grid"] div {
            font-size: 0.7rem !important;
        }
        
        .print-content [style*="background:#1a2a4a"] {
            padding: 0.5rem !important;
            margin-top: 0.5rem !important;
        }
        .print-content [style*="background:#1a2a4a"] div:first-child {
            font-size: 1.2rem !important;
        }
        .print-content [style*="background:#1a2a4a"] div:last-child {
            font-size: 0.7rem !important;
        }
        
        .print-content [style*="margin-top:2rem"] {
            margin-top: 0.8rem !important;
            padding-top: 0.5rem !important;
            font-size: 0.6rem !important;
        }
        
        .print-content [style*="display:grid; grid-template-columns:1fr 1fr"] {
            padding: 0.4rem !important;
            margin-bottom: 0.5rem !important;
            gap: 0.3rem !important;
        }
        .print-content [style*="display:grid; grid-template-columns:1fr 1fr"] div {
            font-size: 0.7rem !important;
        }
        
        .print-content [style*="text-align:center; padding:1rem 0; border-bottom:3px solid"] {
            padding: 0.4rem 0 !important;
            margin-bottom: 0.5rem !important;
        }
        .print-content [style*="text-align:center; padding:1rem 0; border-bottom:3px solid"] h1 {
            font-size: 1.2rem !important;
        }
        .print-content [style*="text-align:center; padding:1rem 0; border-bottom:3px solid"] p {
            font-size: 0.7rem !important;
        }
        
        @page {
            size: A4 portrait;
            margin: 0.8cm 0.8cm 0.8cm 0.8cm !important;
        }
        body { 
            font-size: 10pt !important; 
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
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
                {'code': 'NCH301', 'name': 'Chemistry of Natural Products', 'theory': 3, 'lab': 3},
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
                {'code': 'BTZ203', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
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
                {'code': 'BTS307', 'name': 'Horticulture and Postharvest Management', 'theory': 3, 'lab': 3},
                {'code': 'BTZ303', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
                {'code': 'BTZ304', 'name': 'Bioinformatics', 'theory': 2, 'lab': 4},
                {'code': 'ZLS307', 'name': 'Freshwater Biology', 'theory': 3, 'lab': 6},
                {'code': 'ZLS308', 'name': 'Animal Physiology', 'theory': 3, 'lab': 6},
                {'code': 'BTS308', 'name': 'Economic Botany', 'theory': 3, 'lab': 6},
                {'code': 'BTS309', 'name': 'Plant Biotechnology and Tissue Culture', 'theory': 3, 'lab': 3},
            ]
        }
    },
    'Chemistry_New': {
        'Year 1': {
            'Semester I': [
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
                {'code': 'GCH101', 'name': 'General Chemistry I', 'theory': 3, 'lab': 2},
                {'code': 'FMT101', 'name': 'Foundations of Mathematics I', 'theory': 3, 'lab': 0},
                {'code': 'LAC101', 'name': 'རྫོང་ཁ་ཤེས་ཡྫོན་འབྲི་རྩལ།', 'theory': 2, 'lab': 0},
                {'code': 'CSP101', 'name': 'Foundations of Python Programming', 'theory': 2, 'lab': 3},
            ],
            'Semester II': [
                {'code': 'GCH102', 'name': 'General Chemistry II', 'theory': 3, 'lab': 2},
                {'code': 'FCH101', 'name': 'Fundamentals of Inorganic Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'FMT102', 'name': 'Mathematical Software', 'theory': 2, 'lab': 2},
                {'code': 'LAC102', 'name': 'རྫོང་ཁ་རྩྫོམ་རིག།', 'theory': 2, 'lab': 0},
                {'code': 'PLS101', 'name': 'Fundamentals of Physics for Life Sciences', 'theory': 2, 'lab': 2},
            ]
        },
        'Year 2': {
            'Semester III': [
                {'code': 'ICH101', 'name': 'Inorganic Chemistry I', 'theory': 3, 'lab': 3},
                {'code': 'PCH201', 'name': 'Physical Chemistry I', 'theory': 3, 'lab': 3},
                {'code': 'FMT204', 'name': 'Foundations of Mathematics III', 'theory': 3, 'lab': 0},
                {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
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
                {'code': 'NCH301', 'name': 'Chemistry of Natural Products', 'theory': 3, 'lab': 3},
                {'code': 'BCH302', 'name': 'Principles of Biochemistry II', 'theory': 3, 'lab': 3},
                {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
            ]
        },
        'Year 4': {
            'Semester VII': [
                {'code': 'ACH402', 'name': 'Advanced Analytical Chemistry', 'theory': 3, 'lab': 3},
                {'code': 'ICH404', 'name': 'Advanced Inorganic Chemistry', 'theory': 3, 'lab': 3},
                {'code': 'OCH405', 'name': 'Advanced Organic Chemistry', 'theory': 3, 'lab': 3},
                {'code': 'PCH405', 'name': 'Advanced Physical Chemistry', 'theory': 3, 'lab': 3},
                {'code': 'CRD401', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
            ],
            'Semester VIII': [
                {'code': 'MCH401', 'name': 'Medicinal Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'PCH406', 'name': 'Polymer Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'NCH402', 'name': 'Nanomaterials Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'CRD402', 'name': 'Capstone Project II', 'theory': 2, 'lab': 4},
            ]
        }
    },
    'Physics_New': {
        'Year 1': {
            'Semester I': [
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
                {'code': 'CME101', 'name': 'Newtonian Mechanics', 'theory': 3, 'lab': 2},
                {'code': 'CSP101', 'name': 'Foundations of Python Programming', 'theory': 2, 'lab': 3},
                {'code': 'FMT101', 'name': 'Fundamentals of Mathematics I', 'theory': 4, 'lab': 0},
                {'code': 'LAC101', 'name': 'རྫོང་ཁ་ཤེས་ཡྫོན་འབྲི་རྩལ།', 'theory': 2, 'lab': 0},
            ],
            'Semester II': [
                {'code': 'PHW101', 'name': 'Oscillations and Waves', 'theory': 3, 'lab': 2},
                {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
                {'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'LAC102', 'name': 'རྫོང་ཁ་རྩྫོམ་རིག།', 'theory': 2, 'lab': 0},
                {'code': 'FMT102', 'name': 'Fundamentals of Mathematics II', 'theory': 3, 'lab': 0},
            ]
        },
        'Year 2': {
            'Semester III': [
                {'code': 'APH201', 'name': 'Physics of Space and Satellites', 'theory': 3, 'lab': 2},
                {'code': 'EMT201', 'name': 'Electricity and Magnetism', 'theory': 3, 'lab': 3},
                {'code': 'MMP201', 'name': 'Essential Mathematics for Physics', 'theory': 3, 'lab': 0},
                {'code': 'APH202', 'name': 'Introduction to Electronic Systems', 'theory': 2, 'lab': 3},
                {'code': 'MEC201', 'name': 'Mechanics II', 'theory': 3, 'lab': 2},
            ],
            'Semester IV': [
                {'code': 'MMP202', 'name': 'Mathematical Methods in Physics', 'theory': 3, 'lab': 0},
                {'code': 'FMP201', 'name': 'Modern Physics', 'theory': 3, 'lab': 2},
                {'code': 'PHW202', 'name': 'Optics', 'theory': 3, 'lab': 3},
                {'code': 'TPH201', 'name': 'Thermal Physics', 'theory': 3, 'lab': 2},
                {'code': 'DAT102', 'name': 'Statistical Computing II', 'theory': 2, 'lab': 3},
            ]
        },
        'Year 3': {
            'Semester V': [
                {'code': 'APH303', 'name': 'Computational Physics', 'theory': 3, 'lab': 3},
                {'code': 'APH304', 'name': 'Applied Integrated Circuits and Logic Design', 'theory': 3, 'lab': 3},
                {'code': 'EPH301', 'name': 'Atmospheric Physics', 'theory': 3, 'lab': 2},
                {'code': 'QME301', 'name': 'Quantum Mechanics I', 'theory': 4, 'lab': 0},
                {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
            ],
            'Semester VI': [
                {'code': 'ANP301', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3},
                {'code': 'ANP302', 'name': 'Nuclear Physics', 'theory': 3, 'lab': 2},
                {'code': 'SSP301', 'name': 'Condensed Matter Physics', 'theory': 3, 'lab': 3},
                {'code': 'APH305', 'name': 'Machine Learning for Physics', 'theory': 3, 'lab': 3},
                {'code': 'QME302', 'name': 'Quantum Mechanics II', 'theory': 3, 'lab': 0},
            ]
        },
        'Year 4': {
            'Semester VII': [
                {'code': 'THP402', 'name': 'Statistical Physics', 'theory': 4, 'lab': 0},
                {'code': 'EMT402', 'name': 'Electromagnetic Theory', 'theory': 4, 'lab': 0},
                {'code': 'SSP402', 'name': 'Advanced Condensed Matter Physics', 'theory': 3, 'lab': 3},
                {'code': 'QME403', 'name': 'Advanced Quantum Mechanics', 'theory': 4, 'lab': 0},
                {'code': 'CRD401', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
            ],
            'Semester VIII': [
                {'code': 'CME402', 'name': 'Lagrangian and Hamiltonian Mechanics', 'theory': 3, 'lab': 0},
                {'code': 'EPH402', 'name': 'Physics of Renewable Energy', 'theory': 3, 'lab': 2},
                {'code': 'APH406', 'name': 'Astrophysics', 'theory': 3, 'lab': 2},
                {'code': 'CRD402', 'name': 'Capstone Project II', 'theory': 2, 'lab': 4},
            ]
        }
    },
    # ========================================
    # NEW LIFE SCIENCES - CORRECTED (4 Year)
    # ========================================
    'LifeSciences_New': {
        'Year 1': {
            'Semester I': [
                {'code': 'BTS101', 'name': 'Algae & Fungi', 'theory': 3, 'lab': 3},
                {'code': 'ZLS101', 'name': 'Protistans & Invertebrate Biology', 'theory': 3, 'lab': 3},
                {'code': 'CCH101', 'name': 'Concise Chemistry', 'theory': 3, 'lab': 2},
                {'code': 'BTZ101', 'name': 'Evolution & Biogeography', 'theory': 3, 'lab': 0},
                {'code': 'APC101', 'name': 'IT Skills', 'theory': 2, 'lab': 2},
            ],
            'Semester II': [
                {'code': 'ZLS102', 'name': 'Chordate Biology', 'theory': 3, 'lab': 3},
                {'code': 'BTS102', 'name': 'Bryophyte & Pteridophyte', 'theory': 3, 'lab': 3},
                {'code': 'ZLS103', 'name': 'Cell Biology', 'theory': 3, 'lab': 3},
                {'code': 'BTS103', 'name': 'Gymnosperm & Plant Anatomy', 'theory': 3, 'lab': 3},
                {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 2': {
            'Semester III': [
                {'code': 'ZLS204', 'name': 'Developmental Biology', 'theory': 3, 'lab': 3},
                {'code': 'BTS204', 'name': 'Embryology of Angiosperms', 'theory': 3, 'lab': 6},
                {'code': 'ZLS205', 'name': 'Biochemistry', 'theory': 3, 'lab': 4},
                {'code': 'BTZ202', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
                {'code': 'AMT202', 'name': 'Foundations of Statistics', 'theory': 3, 'lab': 0},
            ],
            'Semester IV': [
                {'code': 'ZLS206', 'name': 'Parasitology', 'theory': 3, 'lab': 3},
                {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
                {'code': 'BTS205', 'name': 'Principles of Plant Systematics', 'theory': 3, 'lab': 3},
                {'code': 'BTZ203', 'name': 'Genetics & Genomics', 'theory': 3, 'lab': 4},
                {'code': 'DZG101', 'name': 'Dzongkha Communication', 'theory': 2, 'lab': 0},
            ]
        },
        'Year 3': {
            'Semester V': [
                {'code': 'BTS306', 'name': 'Plant Breeding & Horticulture', 'theory': 3, 'lab': 6},
                {'code': 'ZLS307', 'name': 'Freshwater Biology', 'theory': 3, 'lab': 6},
                {'code': 'BTS307', 'name': 'Economic Botany', 'theory': 3, 'lab': 6},
                {'code': 'ZLS308', 'name': 'Animal Physiology', 'theory': 3, 'lab': 6},
                {'code': 'BTS308', 'name': 'Plant Biotechnology & Tissue Culture', 'theory': 3, 'lab': 3},
            ],
            'Semester VI': [
                {'code': 'BTS309', 'name': 'Physiology & Ecophysiology of Plant', 'theory': 3, 'lab': 3},
                {'code': 'ZLS309', 'name': 'Animal Biotechnology', 'theory': 3, 'lab': 3},
                {'code': 'BTS310', 'name': 'Plant Ecology & Conservation', 'theory': 3, 'lab': 3},
                {'code': 'BTZ304', 'name': 'Environmental Biotechnology', 'theory': 3, 'lab': 4},
                {'code': 'ZLS310', 'name': 'Animal Behavior', 'theory': 3, 'lab': 3},
            ]
        },
        'Year 4': {
            'Semester VII': [
                {'code': 'BTS407', 'name': 'Ethnobotany and Phytochemistry', 'theory': 3, 'lab': 4},
                {'code': 'BTZ405', 'name': 'Biotechnology and Tissue Culture', 'theory': 3, 'lab': 4},
                {'code': 'BTZ406', 'name': 'Ecology and Biodiversity Conservation', 'theory': 3, 'lab': 3},
                {'code': 'ZLS406', 'name': 'Freshwater Biology', 'theory': 3, 'lab': 3},
                {'code': 'CRD403', 'name': 'Capstone Project I', 'theory': 2, 'lab': 4},
            ],
            'Semester VIII': [
                {'code': 'ZLS407', 'name': 'Animal Behaviour', 'theory': 3, 'lab': 3},
                {'code': 'BTZ407', 'name': 'Immunology and Forensic Biology', 'theory': 3, 'lab': 4},
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
if 'manual_programme' not in st.session_state:
    st.session_state.manual_programme = ""
if 'manual_curriculum' not in st.session_state:
    st.session_state.manual_curriculum = ""
if 'manual_year' not in st.session_state:
    st.session_state.manual_year = ""
if 'manual_semester' not in st.session_state:
    st.session_state.manual_semester = ""
if 'manual_module_code' not in st.session_state:
    st.session_state.manual_module_code = ""
if 'manual_module_name' not in st.session_state:
    st.session_state.manual_module_name = ""
if 'manual_module_type' not in st.session_state:
    st.session_state.manual_module_type = "Theory Only"
if 'manual_theory' not in st.session_state:
    st.session_state.manual_theory = 3
if 'manual_lab' not in st.session_state:
    st.session_state.manual_lab = 0
if 'manual_students' not in st.session_state:
    st.session_state.manual_students = 30
if 'manual_room' not in st.session_state:
    st.session_state.manual_room = ""

# ==========================================
# 7. STUDENT COUNTER FUNCTION
# ==========================================
def student_counter(label, key, min_val=20, max_val=70, default=30):
    """
    Create a student counter with +/- buttons.
    
    Args:
        label: Display label for the counter
        key: Unique session state key
        min_val: Minimum value (default: 20)
        max_val: Maximum value (default: 70)
        default: Default value (default: 30)
    
    Returns:
        int: Current counter value
    """
    
    # Initialize session state if not exists
    if key not in st.session_state:
        st.session_state[key] = default
    
    # Create layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Decrease button
    with col1:
        if st.button("−", key=f"{key}_dec", help="Decrease by 1", use_container_width=True):
            if st.session_state[key] > min_val:
                st.session_state[key] -= 1
    
    # Display current value
    with col2:
        st.markdown(f"""
        <div style="text-align:center; font-size:1.2rem; font-weight:700; color:#1a2a4a; padding:0.2rem 0;">
            {st.session_state[key]}
        </div>
        """, unsafe_allow_html=True)
    
    # Increase button
    with col3:
        if st.button("+", key=f"{key}_inc", help="Increase by 1", use_container_width=True):
            if st.session_state[key] < max_val:
                st.session_state[key] += 1
    
    # Show range
    st.caption(f"Students {min_val}-{max_val}")
    
    return st.session_state[key]
# ==========================================
# 8. ACADEMIC HEADER
# ==========================================
st.markdown(f"""
<div class="academic-header">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">
        <div>
            <h1>Workload & Roaster System</h1>
            <div class="subtitle">Department of Natural Sciences • Sherubtse College • Royal University of Bhutan</div>
            <div class="meta">
                <span class="badge">📅 {datetime.now().strftime('%B %d, %Y')}</span>
                <span class="badge" style="margin-left:0.5rem;">📚 Autumn 2026</span>
                <span class="badge" style="margin-left:0.5rem;">🏛️ Academic Year 2026-2027</span>
            </div>
        </div>
        <div style="text-align:right; font-size:0.9rem; color: #ffffff;">
            <div>Faculty Self-Service Portal</div>
            <div>Workload Allocation Module</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 9. SIDEBAR
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
    
    designation = st.selectbox(
        "Designation",
        ["Assistant Professor", "Senior Lecturer", "Lecturer", "Associate Lecturer", "Assistant Lecturer"]
    )
    
    st.divider()
    st.markdown("### Module Selection")
    
    # ===== PROGRAMME SELECTION WITH MANUAL ENTRY =====
    prog_option = st.radio("Select Programme", ["From List", "Enter Manually"], key="prog_radio", horizontal=True)
    
    if prog_option == "From List":
        prog = st.selectbox("Programme", ["Physics", "Chemistry", "Life Sciences"])
        st.session_state.manual_programme = ""
    else:
        prog = st.text_input("Enter Programme", value=st.session_state.manual_programme, placeholder="e.g., Environmental Science")
        if prog:
            st.session_state.manual_programme = prog
    
    # ===== CURRICULUM SELECTION WITH MANUAL ENTRY =====
    curr_option = st.radio("Select Curriculum", ["From List", "Enter Manually"], key="curr_radio", horizontal=True)
    
    if curr_option == "From List":
        curr = st.selectbox("Curriculum", ["Old (3-Year)", "New (4-Year)"])
        st.session_state.manual_curriculum = ""
    else:
        curr = st.text_input("Enter Curriculum", value=st.session_state.manual_curriculum, placeholder="e.g., New (4-Year)")
        if curr:
            st.session_state.manual_curriculum = curr
    
    # ===== YEAR SELECTION WITH MANUAL ENTRY =====
    year_option = st.radio("Select Year", ["From List", "Enter Manually"], key="year_radio", horizontal=True)
    
    if year_option == "From List":
        year = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
        st.session_state.manual_year = ""
    else:
        year = st.text_input("Enter Year", value=st.session_state.manual_year, placeholder="e.g., Year 1")
        if year:
            st.session_state.manual_year = year
    
    # ===== SEMESTER SELECTION WITH MANUAL ENTRY =====
    sem_option = st.radio("Select Semester", ["From List", "Enter Manually"], key="sem_radio", horizontal=True)
    
    if sem_option == "From List":
        sem = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI", "Semester VII", "Semester VIII"])
        st.session_state.manual_semester = ""
    else:
        sem = st.text_input("Enter Semester", value=st.session_state.manual_semester, placeholder="e.g., Semester I")
        if sem:
            st.session_state.manual_semester = sem
    
    # ===== GET MODULES =====
    modules = []
    try:
        prog_key = {"Physics":"Physics", "Chemistry":"Chemistry", "Life Sciences":"LifeSciences"}.get(prog, prog)
        curr_key = "Old" if curr == "Old (3-Year)" else "New" if curr == "New (4-Year)" else curr
        key = f"{prog_key}_{curr_key}"
        
        if key in MODULE_DATABASE and year in MODULE_DATABASE[key] and sem in MODULE_DATABASE[key][year]:
            modules = MODULE_DATABASE[key][year][sem]
        else:
            for p in ["Physics", "Chemistry", "LifeSciences"]:
                for c in ["Old", "New"]:
                    test_key = f"{p}_{c}"
                    if test_key in MODULE_DATABASE:
                        if year in MODULE_DATABASE[test_key] and sem in MODULE_DATABASE[test_key][year]:
                            modules = MODULE_DATABASE[test_key][year][sem]
                            break
                if modules:
                    break
    except:
        pass
    
    if modules:
        # ===== MODULE SELECTION WITH MANUAL ENTRY =====
        mod_option = st.radio("Select Module", ["From List", "Enter Manually"], key="mod_radio", horizontal=True)
        
        if mod_option == "From List":
            opts = [f"{m['code']} - {m['name']}" for m in modules]
            sel = st.selectbox("Select Module", ["-- Select --"] + opts)
            
            if sel != "-- Select --" and sel:
                code = sel.split(" - ")[0]
                mod = next(m for m in modules if m['code'] == code)
                
                # ===== MODULE TYPE SELECTION =====
                st.markdown("**Module Type**")
                mod_type = st.radio(
                    "Select Module Type",
                    ["Theory Only", "Lab Only", "Theory + Lab"],
                    index=0,
                    horizontal=True,
                    key="mod_type_from_list"
                )
                
                # Hours based on type selection
                col_t, col_l = st.columns(2)
                with col_t:
                    if mod_type in ["Theory Only", "Theory + Lab"]:
                        theory = st.number_input(
                            "Theory Hours", 
                            min_value=0, 
                            max_value=6, 
                            value=mod['theory'] if mod['theory'] > 0 else 3, 
                            step=1,
                            key="theory_from_list"
                        )
                    else:
                        theory = 0
                        st.info("Theory hours: 0 (Lab Only module)")
                
                with col_l:
                    if mod_type in ["Lab Only", "Theory + Lab"]:
                        lab = st.number_input(
                            "Lab Hours", 
                            min_value=0, 
                            max_value=6, 
                            value=mod['lab'] if mod['lab'] > 0 else 3, 
                            step=1,
                            key="lab_from_list"
                        )
                    else:
                        lab = 0
                        st.info("Lab hours: 0 (Theory Only module)")
                
                # ===== STUDENT COUNTER WITH +/- BUTTONS =====
                st.markdown("**Student Enrolment**")
                students = student_counter(
                    label="Students",
                    key="student_count_from_list",
                    min_val=25,
                    max_val=60,
                    default=30
                )
                
                room = st.text_input(
                    "Room / Laboratory",
                    value=st.session_state.rooms.get(code, ""),
                    placeholder="e.g., Science Hall 1, Lab 203"
                )
                
                # Show module summary
                st.markdown(f"""
                <div class="module-detail-box">
                    <strong>📋 Module Summary:</strong><br>
                    Type: {mod_type} • Theory: {theory}h • Lab: {lab}h • Total: {theory + lab}h • Students: {students}
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("Add Module", use_container_width=True):
                        if not any(m['code'] == code for m in st.session_state.modules):
                            custom_mod = {
                                'code': code,
                                'name': mod['name'],
                                'theory': theory,
                                'lab': lab
                            }
                            st.session_state.modules.append(custom_mod)
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
        
        else:
            # ===== MANUAL MODULE ENTRY WITH FULL OPTIONS =====
            st.markdown("### 📝 Enter Module Details")
            
            # Module Code and Name
            mod_code = st.text_input(
                "Module Code", 
                value=st.session_state.manual_module_code, 
                placeholder="e.g., ENV101"
            )
            mod_name = st.text_input(
                "Module Name", 
                value=st.session_state.manual_module_name, 
                placeholder="e.g., Environmental Science"
            )
            
            # Module Type Selection
            st.markdown("**Module Type**")
            mod_type = st.radio(
                "Select Module Type",
                ["Theory Only", "Lab Only", "Theory + Lab"],
                index=["Theory Only", "Lab Only", "Theory + Lab"].index(st.session_state.manual_module_type) 
                    if st.session_state.manual_module_type in ["Theory Only", "Lab Only", "Theory + Lab"] else 0,
                horizontal=True,
                key="mod_type_manual"
            )
            st.session_state.manual_module_type = mod_type
            
            # Hours based on type
            col_t, col_l = st.columns(2)
            with col_t:
                if mod_type in ["Theory Only", "Theory + Lab"]:
                    theory = st.number_input(
                        "Theory Hours", 
                        min_value=0, 
                        max_value=6, 
                        value=st.session_state.manual_theory if st.session_state.manual_theory > 0 else 3, 
                        step=1,
                        key="theory_manual"
                    )
                else:
                    theory = 0
                    st.info("Theory hours: 0 (Lab Only module)")
            
            with col_l:
                if mod_type in ["Lab Only", "Theory + Lab"]:
                    lab = st.number_input(
                        "Lab Hours", 
                        min_value=0, 
                        max_value=6, 
                        value=st.session_state.manual_lab if st.session_state.manual_lab > 0 else 3, 
                        step=1,
                        key="lab_manual"
                    )
                else:
                    lab = 0
                    st.info("Lab hours: 0 (Theory Only module)")
            
            # ===== STUDENT COUNTER WITH +/- BUTTONS =====
            st.markdown("**Student Enrolment**")
            students = student_counter(
                label="Students",
                key="student_count_manual",
                min_val=25,
                max_val=60,
                default=st.session_state.manual_students
            )
            st.session_state.manual_students = students
            
            # Room / Laboratory
            room = st.text_input(
                "Room / Laboratory", 
                value=st.session_state.manual_room,
                placeholder="e.g., Science Hall 1, Lab 203"
            )
            st.session_state.manual_room = room
            
            # Summary of module
            st.markdown(f"""
            <div class="module-detail-box">
                <strong>📋 Module Summary:</strong><br>
                Code: {mod_code if mod_code else '(Not Set)'} • Name: {mod_name if mod_name else '(Not Set)'}<br>
                Type: {mod_type} • Theory: {theory}h • Lab: {lab}h • Total: {theory + lab}h • Students: {students}<br>
                Room: {room if room else 'Not Assigned'}
            </div>
            """, unsafe_allow_html=True)
            
            # Save to session state
            if mod_code:
                st.session_state.manual_module_code = mod_code
            if mod_name:
                st.session_state.manual_module_name = mod_name
            st.session_state.manual_theory = theory
            st.session_state.manual_lab = lab
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("➕ Add Module", use_container_width=True):
                    if mod_code and mod_name:
                        if not any(m['code'] == mod_code for m in st.session_state.modules):
                            new_mod = {
                                'code': mod_code,
                                'name': mod_name,
                                'theory': theory,
                                'lab': lab
                            }
                            st.session_state.modules.append(new_mod)
                            st.session_state.counts[mod_code] = students
                            if room:
                                st.session_state.rooms[mod_code] = room
                            st.success(f"✅ Added: {mod_code}")
                            # Reset manual fields
                            st.session_state.manual_module_code = ""
                            st.session_state.manual_module_name = ""
                            st.session_state.manual_room = ""
                            st.rerun()
                        else:
                            st.warning("⚠️ Module already in list")
                    else:
                        st.error("Please enter Module Code and Name")
            
            with col_b:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.modules = []
                    st.session_state.counts = {}
                    st.session_state.rooms = {}
                    st.rerun()
    
    else:
        # ===== NO MODULES FOUND - ONLY MANUAL ENTRY =====
        st.info("No modules found for the selected parameters. Enter manually below.")
        
        st.markdown("### 📝 Enter Module Details")
        
        # Module Code and Name
        mod_code = st.text_input(
            "Module Code", 
            value=st.session_state.manual_module_code, 
            placeholder="e.g., ENV101"
        )
        mod_name = st.text_input(
            "Module Name", 
            value=st.session_state.manual_module_name, 
            placeholder="e.g., Environmental Science"
        )
        
        # Module Type Selection
        st.markdown("**Module Type**")
        mod_type = st.radio(
            "Select Module Type",
            ["Theory Only", "Lab Only", "Theory + Lab"],
            index=["Theory Only", "Lab Only", "Theory + Lab"].index(st.session_state.manual_module_type) 
                if st.session_state.manual_module_type in ["Theory Only", "Lab Only", "Theory + Lab"] else 0,
            horizontal=True,
            key="mod_type_no_modules"
        )
        st.session_state.manual_module_type = mod_type
        
        # Hours based on type
        col_t, col_l = st.columns(2)
        with col_t:
            if mod_type in ["Theory Only", "Theory + Lab"]:
                theory = st.number_input(
                    "Theory Hours", 
                    min_value=0, 
                    max_value=6, 
                    value=st.session_state.manual_theory if st.session_state.manual_theory > 0 else 3, 
                    step=1,
                    key="theory_no_modules"
                )
            else:
                theory = 0
                st.info("Theory hours: 0 (Lab Only module)")
        
        with col_l:
            if mod_type in ["Lab Only", "Theory + Lab"]:
                lab = st.number_input(
                    "Lab Hours", 
                    min_value=0, 
                    max_value=6, 
                    value=st.session_state.manual_lab if st.session_state.manual_lab > 0 else 3, 
                    step=1,
                    key="lab_no_modules"
                )
            else:
                lab = 0
                st.info("Lab hours: 0 (Theory Only module)")
        
        # ===== STUDENT COUNTER WITH +/- BUTTONS =====
        st.markdown("**Student Enrolment**")
        students = student_counter(
            label="Students",
            key="student_count_no_modules",
            min_val=25,
            max_val=60,
            default=st.session_state.manual_students
        )
        st.session_state.manual_students = students
        
        # Room / Laboratory
        room = st.text_input(
            "Room / Laboratory", 
            value=st.session_state.manual_room,
            placeholder="e.g., Science Hall 1, Lab 203"
        )
        st.session_state.manual_room = room
        
        # Summary of module
        st.markdown(f"""
        <div class="module-detail-box">
            <strong>📋 Module Summary:</strong><br>
            Code: {mod_code if mod_code else '(Not Set)'} • Name: {mod_name if mod_name else '(Not Set)'}<br>
            Type: {mod_type} • Theory: {theory}h • Lab: {lab}h • Total: {theory + lab}h • Students: {students}<br>
            Room: {room if room else 'Not Assigned'}
        </div>
        """, unsafe_allow_html=True)
        
        # Save to session state
        if mod_code:
            st.session_state.manual_module_code = mod_code
        if mod_name:
            st.session_state.manual_module_name = mod_name
        st.session_state.manual_theory = theory
        st.session_state.manual_lab = lab
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("➕ Add Module", use_container_width=True):
                if mod_code and mod_name:
                    if not any(m['code'] == mod_code for m in st.session_state.modules):
                        new_mod = {
                            'code': mod_code,
                            'name': mod_name,
                            'theory': theory,
                            'lab': lab
                        }
                        st.session_state.modules.append(new_mod)
                        st.session_state.counts[mod_code] = students
                        if room:
                            st.session_state.rooms[mod_code] = room
                        st.success(f"✅ Added: {mod_code}")
                        # Reset manual fields
                        st.session_state.manual_module_code = ""
                        st.session_state.manual_module_name = ""
                        st.session_state.manual_room = ""
                        st.rerun()
                    else:
                        st.warning("⚠️ Module already in list")
                else:
                    st.error("Please enter Module Code and Name")
        
        with col_b:
            if st.button("🗑️ Clear All", use_container_width=True):
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
# 10. MAIN CONTENT (SAME AS BEFORE)
# ==========================================
# [Rest of the code remains the same - main content, print section, tabs, admin section, footer]
# ...
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
# 11. PRINTABLE CONTENT
# ==========================================
st.markdown('<div class="print-content">', unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; padding:0.4rem 0; border-bottom:3px solid #1a2a4a; margin-bottom:0.5rem;">
    <h1 style="color:#1a2a4a; font-size:1.4rem; margin:0;">Workload & Roaster Report</h1>
    <p style="color:#495057; margin:0.1rem 0; font-size:0.75rem;">Department of Natural Sciences • Royal University of Bhutan</p>
    <p style="color:#7f8c8d; font-size:0.7rem; margin:0;">{datetime.now().strftime('%B %d, %Y')} • Autumn 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:0.3rem; margin-bottom:0.5rem; padding:0.4rem; background:#f8f9fa; border-radius:4px; font-size:0.7rem;">
    <div><strong>Faculty:</strong> {st.session_state.name}</div>
    <div><strong>Designation:</strong> {designation if 'designation' in locals() else 'Not Specified'}</div>
    <div><strong>Programme:</strong> {prog if 'prog' in locals() else 'Not Specified'}</div>
    <div><strong>Semester:</strong> Autumn 2026</div>
</div>
""", unsafe_allow_html=True)

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
            'Total': m['theory'] + m['lab'],
            'Students': students,
            'Room': room,
            'WAM': w
        })
    df_print = pd.DataFrame(data)
    
    st.table(df_print)
    
    st.markdown(f"""
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:0.2rem; margin-top:0.3rem; padding:0.4rem; background:#f8f9fa; border-radius:4px; text-align:center; font-size:0.7rem;">
        <div><strong>Modules</strong><br>{len(st.session_state.modules)}</div>
        <div><strong>Theory</strong><br>{df_print['Theory'].sum()}h</div>
        <div><strong>Lab</strong><br>{df_print['Lab'].sum()}h</div>
        <div><strong>Students</strong><br>{df_print['Students'].sum()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    wam_total = calculate_wam([
        {**m, 'students': st.session_state.counts.get(m['code'], 25)}
        for m in st.session_state.modules
    ])
    status, emoji, color, msg = get_status(wam_total)
    
    st.markdown(f"""
    <div style="background:#1a2a4a; color:white; padding:0.5rem; border-radius:4px; margin-top:0.5rem; text-align:center;">
        <div style="font-size:1.2rem; font-weight:700;">{wam_total}</div>
        <div style="font-size:0.65rem; opacity:0.8;">Workload Allocation Model Score</div>
        <div style="margin-top:0.2rem; background:{color}; display:inline-block; padding:0.1rem 0.8rem; border-radius:3px; color:white; font-weight:600; font-size:0.7rem;">{emoji} {status}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No modules selected")

st.markdown("""
<div style="text-align:center; margin-top:0.8rem; padding-top:0.4rem; border-top:2px solid #e8ecf0; color:#7f8c8d; font-size:0.6rem;">
    Generated by Workload & Roaster System • Royal University of Bhutan
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 12. DETAILED SECTIONS
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
                'Type': 'Theory + Lab' if m['lab'] > 0 and m['theory'] > 0 else 'Theory Only' if m['theory'] > 0 else 'Lab Only'
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
# 13. PRINT BUTTON
# ==========================================
st.divider()

st.markdown("""
<script>
function printReport() {
    window.print();
}
</script>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="no-print" style="text-align:center; padding:0.5rem 0;">
        <button onclick="printReport()" style="
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
            width: 100%;
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
