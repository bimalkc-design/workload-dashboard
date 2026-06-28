import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Workload Self-Service Portal",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. STYLING - Professional & Appealing
# ==========================================
st.markdown("""
<style>
    /* Main gradient header */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* WAM Display Card */
    .wam-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        margin: 1rem 0;
        transition: transform 0.3s;
    }
    .wam-card:hover {
        transform: translateY(-5px);
    }
    .wam-number {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
    }
    .wam-label {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 2rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        margin: 0.5rem 0;
        letter-spacing: 0.5px;
    }
    
    /* Module Cards */
    .module-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s;
    }
    .module-card:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        transform: translateX(5px);
    }
    .module-code {
        font-weight: 700;
        color: #667eea;
        font-size: 1.1rem;
    }
    .module-name {
        font-size: 0.95rem;
        color: #333;
    }
    .module-details {
        font-size: 0.85rem;
        color: #666;
    }
    
    /* Stats Container */
    .stats-container {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
        .wam-number { font-size: 3rem; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. COMPLETE MODULE DATABASE - ALL PROGRAMS
# ==========================================
MODULE_DATABASE = {
    # ========================================
    # OLD CURRICULUM - 3 YEAR PROGRAMS
    # ========================================
    
    # ----- OLD CHEMISTRY (3 Year) -----
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
    
    # ----- OLD PHYSICS (3 Year) -----
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
    
    # ----- OLD LIFE SCIENCES (3 Year) -----
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
    
    # ========================================
    # NEW CURRICULUM - 4 YEAR PROGRAMS
    # ========================================
    
    # ----- NEW PHYSICS (4 Year) -----
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
    
    # ----- NEW LIFE SCIENCES (4 Year) -----
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
    
    # ----- NEW CHEMISTRY (4 Year) -----
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
# 4. FACULTY DATABASE
# ==========================================
FACULTY_LIST = [
    "Dr. Jas Raj Subba",
    "Mr. Sangay Wangchuk",
    "Mrs. Punam Mafchan",
    "Ms. Kuenzang Choki",
    "Ms. Sangay Yuden",
    "Mr. Tashi Dendup",
    "Shacha Thinley",
    "Nachiketa Homchaudhuri",
    "Mon Bahadur Ghalley",
    "Dr. Karma Tenzin",
    "Rit Wik Sharma",
    "Ugyen Dorji Tamang",
    "Karma Wangchuck",
    "Mohan Singh Rana",
    "Tshering Dekar",
    "Bimal Kumar Chetri",
    "Sonam Tobgay",
    "Dechen Lhendup",
    "S. Chitra",
    "DS-Y",
    "Paul Raj"
]

# ==========================================
# 5. WAM ENGINE & LOGGING
# ==========================================
def calculate_wam(selected_modules, student_counts):
    """Calculate WAM based on selected modules"""
    total_wam = 0
    assess_score = {'Low': 2, 'Medium': 4, 'High': 7}
    
    for module in selected_modules:
        students = student_counts.get(module['code'], 25)
        base_load = (module['theory'] * 1.0) + module['lab']
        intensity = assess_score['Medium']
        student_loading = (students * intensity) * 0.04
        total_wam += base_load + student_loading
    
    return round(total_wam, 1)

def get_status(wam):
    """Get status based on WAM score"""
    if wam == 0:
        return 'No Load', '⚪', '#6c757d', 'You haven\'t selected any modules yet'
    elif wam < 10:
        return 'Light Load', '🟡', '#ffc107', 'You have capacity for more modules'
    elif wam <= 19:
        return 'Optimal', '🟢', '#28a745', 'Your workload is well-balanced!'
    else:
        return 'Heavy Load', '🔴', '#dc3545', 'Consider sharing modules with colleagues'

def log_activity(faculty_name, modules, wam, status):
    """Log faculty activity to JSON file"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'faculty': faculty_name,
        'modules': modules,
        'wam': wam,
        'status': status
    }
    
    # Load existing logs
    log_file = 'workload_logs.json'
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(log_entry)
    
    # Save logs
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

def get_faculty_history(faculty_name):
    """Get historical logs for a faculty member"""
    log_file = 'workload_logs.json'
    if not os.path.exists(log_file):
        return []
    
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
        return [log for log in logs if log['faculty'] == faculty_name]
    except:
        return []

# ==========================================
# 6. SESSION STATE
# ==========================================
if 'selected_modules' not in st.session_state:
    st.session_state.selected_modules = []
if 'student_counts' not in st.session_state:
    st.session_state.student_counts = {}
if 'faculty_name' not in st.session_state:
    st.session_state.faculty_name = ""
if 'history_view' not in st.session_state:
    st.session_state.history_view = False

# ==========================================
# 7. HEADER
# ==========================================
st.markdown("""
<div class="main-header">
    <h1>⚖️ Workload Self-Service Portal</h1>
    <p>Department of Natural Sciences • Autumn 2026 Transition</p>
    <p style="font-size:0.9rem; opacity:0.7; margin-top:0.5rem;">
        📅 {} • Select your modules and calculate your WAM instantly
    </p>
</div>
""".format(datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)

# ==========================================
# 8. SIDEBAR - Faculty Profile & Module Selection
# ==========================================
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    
    # Faculty Name - Select or Enter
    name_option = st.radio(
        "Choose your name",
        ["Select from list", "Enter manually"],
        index=0
    )
    
    if name_option == "Select from list":
        faculty_name = st.selectbox(
            "Select your name",
            [""] + sorted(FACULTY_LIST),
            help="Choose your name from the list"
        )
    else:
        faculty_name = st.text_input(
            "Enter your name",
            value=st.session_state.faculty_name,
            placeholder="e.g., Dr. Jas Raj Subba"
        )
    
    if faculty_name:
        st.session_state.faculty_name = faculty_name
        st.success(f"Welcome, {faculty_name}!")
    
    designation = st.selectbox(
        "Designation",
        ["Professor", "Associate Professor", "Assistant Professor", "Senior Lecturer", "Lecturer"]
    )
    
    st.markdown("---")
    st.markdown("### 📚 Module Selection")
    
    # Selection filters
    program = st.selectbox("Program", ["Physics", "Chemistry", "Life Sciences"])
    curriculum = st.selectbox("Curriculum", ["Old", "New"])
    
    # Map selections
    prog_map = {"Physics": "Physics", "Chemistry": "Chemistry", "Life Sciences": "LifeSciences"}
    full_key = f"{prog_map[program]}_{curriculum}"
    
    year = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
    semester = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI"])
    
    # Get available modules
    available_modules = []
    try:
        available_modules = MODULE_DATABASE[full_key][year][semester]
    except KeyError:
        st.warning("No modules available for this selection")
    
    if available_modules:
        module_options = [f"{m['code']} - {m['name']} ({m['theory']}T + {m['lab']}L)" for m in available_modules]
        selected_module_str = st.selectbox("Select Module", ["-- Select --"] + module_options)
        
        if selected_module_str != "-- Select --":
            module_code = selected_module_str.split(" - ")[0]
            selected_module = next(m for m in available_modules if m['code'] == module_code)
            
            students = st.slider(
                f"Student Count",
                min_value=25,
                max_value=40,
                value=30,
                step=1,
                key=f"slider_{module_code}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Add", use_container_width=True):
                    if not any(m['code'] == module_code for m in st.session_state.selected_modules):
                        st.session_state.selected_modules.append(selected_module)
                        st.session_state.student_counts[module_code] = students
                        st.success(f"✅ Added {module_code}")
                        st.rerun()
                    else:
                        st.warning(f"⚠️ Already added")
            with col2:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.selected_modules = []
                    st.session_state.student_counts = {}
                    st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Your Session")
    if st.session_state.selected_modules:
        st.metric("Modules Selected", len(st.session_state.selected_modules))
        total_students = sum(st.session_state.student_counts.values())
        st.metric("Total Students", total_students)

# ==========================================
# 9. MAIN CONTENT
# ==========================================
# Check if faculty name is provided
if not st.session_state.faculty_name:
    st.info("👈 Please select or enter your name in the sidebar to get started")
    st.stop()

# Main layout - Two columns
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📋 Your Selected Modules")
    
    if not st.session_state.selected_modules:
        st.info("👈 Use the sidebar to select your modules")
    else:
        # Display modules in a clean card layout
        total_theory = 0
        total_lab = 0
        
        for module in st.session_state.selected_modules:
            students = st.session_state.student_counts.get(module['code'], 25)
            total_theory += module['theory']
            total_lab += module['lab']
            
            st.markdown(f"""
            <div class="module-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="module-code">{module['code']}</span>
                        <span class="module-name"> - {module['name']}</span>
                        <br>
                        <span class="module-details">📖 {module['theory']}h Theory • 🧪 {module['lab']}h Lab • 👨‍🎓 {students} Students</span>
                    </div>
                    <div>
                        <span style="background: #667eea; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">
                            {module['theory'] + module['lab']}h
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Remove button
            if st.button(f"✖️ Remove {module['code']}", key=f"remove_{module['code']}"):
                st.session_state.selected_modules.remove(module)
                del st.session_state.student_counts[module['code']]
                st.rerun()
        
        # Summary stats
        st.markdown("""
        <div class="stats-container">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; text-align: center;">
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #667eea;">{}</div>
                    <div style="font-size: 0.85rem; color: #666;">Total Modules</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #667eea;">{}h</div>
                    <div style="font-size: 0.85rem; color: #666;">Theory Hours</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #667eea;">{}h</div>
                    <div style="font-size: 0.85rem; color: #666;">Lab Hours</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #667eea;">{}</div>
                    <div style="font-size: 0.85rem; color: #666;">Total Students</div>
                </div>
            </div>
        </div>
        """.format(
            len(st.session_state.selected_modules),
            total_theory,
            total_lab,
            sum(st.session_state.student_counts.values())
        ), unsafe_allow_html=True)

with col_right:
    st.markdown("### 📊 Your WAM Score")
    
    if st.session_state.selected_modules:
        wam = calculate_wam(st.session_state.selected_modules, st.session_state.student_counts)
        status, emoji, color, message = get_status(wam)
        
        # Log the activity
        if st.session_state.faculty_name:
            log_activity(
                st.session_state.faculty_name,
                [{'code': m['code'], 'name': m['name'], 'students': st.session_state.student_counts.get(m['code'], 25)} 
                 for m in st.session_state.selected_modules],
                wam,
                status
            )
        
        # WAM Display Card
        st.markdown(f"""
        <div class="wam-card">
            <div class="wam-number">{wam}</div>
            <div class="wam-label">Workload Allocation Model Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Status Badge
        st.markdown(f"""
        <div style="text-align: center;">
            <span class="status-badge" style="background-color: {color}; color: white;">
                {emoji} {status}
            </span>
            <p style="margin-top: 0.5rem; color: #666; font-size: 0.95rem;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress Bar
        st.markdown("### Workload Level")
        progress = min(wam / 25, 1.0)
        st.progress(progress)
        st.caption("0" + " " * 50 + "25+")
        
        # Status indicators
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Theory Load", f"{total_theory}h")
        with col2:
            st.metric("Lab Load", f"{total_lab}h")
        with col3:
            st.metric("Total Hours", f"{total_theory + total_lab}h")
        
        # Module Contribution Chart
        if len(st.session_state.selected_modules) > 1:
            st.markdown("### Module Contribution")
            module_wams = []
            for module in st.session_state.selected_modules:
                temp_wam = calculate_wam([module], {module['code']: st.session_state.student_counts.get(module['code'], 25)})
                module_wams.append({'Module': module['code'], 'WAM': temp_wam})
            
            df_wam = pd.DataFrame(module_wams)
            fig = px.bar(
                df_wam,
                x='Module',
                y='WAM',
                title="WAM per Module",
                color='WAM',
                color_continuous_scale='Viridis',
                height=250
            )
            fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 Select modules to calculate your WAM")

# ==========================================
# 10. DETAILED BREAKDOWN & HISTORY
# ==========================================
if st.session_state.selected_modules:
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Detailed Breakdown", "📈 Charts", "📜 Your History"])
    
    with tab1:
        details = []
        for module in st.session_state.selected_modules:
            students = st.session_state.student_counts.get(module['code'], 25)
            wam = calculate_wam([module], {module['code']: students})
            details.append({
                'Code': module['code'],
                'Module': module['name'],
                'Theory': module['theory'],
                'Lab': module['lab'],
                'Students': students,
                'WAM': wam,
                'Type': 'Theory + Lab' if module['lab'] > 0 else 'Theory Only'
            })
        
        df_details = pd.DataFrame(details)
        st.dataframe(
            df_details,
            use_container_width=True,
            hide_index=True,
            column_config={
                "WAM": st.column_config.NumberColumn("WAM Score", format="%.1f"),
                "Students": st.column_config.NumberColumn("Students", format="%d"),
            }
        )
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            csv = df_details.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Report (CSV)",
                data=csv,
                file_name=f"workload_{st.session_state.faculty_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv',
                use_container_width=True
            )
        with col2:
            json_data = json.dumps(df_details.to_dict('records'), indent=2)
            st.download_button(
                label="📥 Download Report (JSON)",
                data=json_data,
                file_name=f"workload_{st.session_state.faculty_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime='application/json',
                use_container_width=True
            )
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Theory vs Lab
            fig_pie = px.pie(
                values=[df_details['Theory'].sum(), df_details['Lab'].sum()],
                names=['Theory Hours', 'Lab Hours'],
                title="Theory vs Lab Distribution",
                color_discrete_sequence=['#667eea', '#764ba2']
            )
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # WAM Distribution
            fig_bar = px.bar(
                df_details,
                x='Code',
                y='WAM',
                title="WAM Distribution by Module",
                color='WAM',
                color_continuous_scale='Viridis',
                height=350
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Additional stats
        st.subheader("📊 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Average WAM", f"{df_details['WAM'].mean():.1f}")
        with col2:
            st.metric("Max WAM", f"{df_details['WAM'].max():.1f}")
        with col3:
            st.metric("Min WAM", f"{df_details['WAM'].min():.1f}")
        with col4:
            st.metric("Total Students", df_details['Students'].sum())
    
    with tab3:
        st.subheader("📜 Your Workload History")
        
        history = get_faculty_history(st.session_state.faculty_name)
        
        if history:
            # Convert to DataFrame
            history_df = pd.DataFrame(history)
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            history_df = history_df.sort_values('timestamp', ascending=False)
            
            st.dataframe(
                history_df[['timestamp', 'wam', 'status', 'modules']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn("Date & Time"),
                    "wam": st.column_config.NumberColumn("WAM Score", format="%.1f"),
                    "status": st.column_config.Column("Status"),
                    "modules": st.column_config.Column("Modules Selected")
                }
            )
            
            # Download history
            csv_history = history_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Complete History",
                data=csv_history,
                file_name=f"history_{st.session_state.faculty_name.replace(' ', '_')}.csv",
                mime='text/csv'
            )
        else:
            st.info("No history found for this faculty member")

# ==========================================
# 11. FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💡 Select your modules from the sidebar to calculate your WAM in real-time</p>
    <p style="font-size: 0.85rem; margin-top: 0.5rem;">
        📱 Optimized for desktop and mobile • All activities are logged for reference
    </p>
</div>
""", unsafe_allow_html=True)
