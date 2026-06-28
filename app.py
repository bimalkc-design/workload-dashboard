import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# ==========================================
# 1. CORE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Workload Intel | Natural Sciences",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Design System CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #4f46e5;
        --primary-hover: #4338ca;
        --bg-main: #f8fafc;
        --border: #e2e8f0;
        --text-slate: #1e293b;
        --text-muted: #64748b;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-slate);
    }

    .app-header {
        background: white;
        padding: 1.5rem 2rem;
        border-bottom: 1px solid var(--border);
        margin: -4rem -4rem 2rem -4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        color: var(--text-muted);
        letter-spacing: 0.025em;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-slate);
        margin-top: 0.25rem;
    }

    .module-row {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--primary);
        margin-bottom: 0.75rem;
        border-top: 1px solid var(--border);
        border-right: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
    }

    .pill {
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .pill-balanced { background: #dcfce7; color: #166534; }
    .pill-heavy { background: #fee2e2; color: #991b1b; }
    .pill-light { background: #fef9c3; color: #854d0e; }

    div.stButton > button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. COMPLETE DATA INTEGRATION
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

FACULTY_LIST = [
    "Dr. Jas Raj Subba", "Mr. Sangay Wangchuk", "Mrs. Punam Mafchan", "Ms. Kuenzang Choki", 
    "Ms. Sangay Yuden", "Mr. Tashi Dendup", "Shacha Thinley", "Nachiketa Homchaudhuri", 
    "Mon Bahadur Ghalley", "Dr. Karma Tenzin", "Rit Wik Sharma", "Ugyen Dorji Tamang", 
    "Karma Wangchuck", "Mohan Singh Rana", "Tshering Dekar", "Bimal Kumar Chetri", 
    "Sonam Tobgay", "Dechen Lhendup", "S. Chitra", "DS-Y", "Paul Raj"
]

# ==========================================
# 3. CORE LOGIC & CALCULATION
# ==========================================
def calculate_wam(basket):
    total = 0
    for m in basket:
        # Professional Scaler: Theory (1.1x) + Lab (0.8x) + Student Volume (0.045 per student)
        base = (m['theory'] * 1.1) + (m['lab'] * 0.8)
        volume = (m['students'] * 0.045)
        total += base + volume
    return round(total, 2)

def get_capacity_metadata(wam):
    if wam == 0: return "Pending", "pill-light", "Assign modules to begin."
    if wam < 12: return "Under Capacity", "pill-light", "Available for further assignment."
    if wam <= 16: return "Optimal", "pill-balanced", "Target workload achieved."
    return "Overloaded", "pill-heavy", "Consider redistributing modules."

# ==========================================
# 4. APP INTERFACE
# ==========================================
st.markdown(f"""
<div class="app-header">
    <div>
        <span style="color: var(--primary); font-weight: 800; font-size: 1.2rem;">DNS</span>
        <span style="font-weight: 700; font-size: 1.2rem; margin-left: 0.5rem; color: var(--text-slate);">Workload Intelligence</span>
        <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted);">Autumn 2026 Academic Planning Cycle</p>
    </div>
    <div style="text-align: right">
        <div style="font-size: 0.7rem; font-weight: 700; color: var(--text-muted);">SYSTEM STATUS</div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #166534;">● ONLINE / LOGS ACTIVE</div>
    </div>
</div>
""", unsafe_allow_html=True)

if 'basket' not in st.session_state: st.session_state.basket = []

with st.sidebar:
    st.markdown("### Faculty Identity")
    user_name = st.selectbox("Select Profile", [""] + sorted(FACULTY_LIST))
    designation = st.selectbox("Rank", ["Assistant Professor", "Senior Lecturer", "Lecturer", "Associate Lecturer", "Assistant Lecturer"])
    
    st.divider()
    
    if st.session_state.basket:
        total_wam = calculate_wam(st.session_state.basket)
        status, pill_class, note = get_capacity_metadata(total_wam)
        
        st.markdown(f"**Session Summary**")
        st.metric("Total WAM", total_wam)
        st.markdown(f'<span class="pill {pill_class}">{status}</span>', unsafe_allow_html=True)
        st.caption(note)
        
        st.divider()
        if st.button("Reset Planning Canvas"):
            st.session_state.basket = []
            st.rerun()

# --- MAIN CONTENT ---
if not user_name:
    st.info("👋 Select your faculty profile in the sidebar to begin drafting your workload.")
    st.stop()

tab_plan, tab_analytics, tab_review = st.tabs(["🎯 Drafting Plan", "📊 Analysis", "📜 Submission"])

with tab_plan:
    col_input, col_canvas = st.columns([1, 1.8])
    
    with col_input:
        st.markdown("#### Configure Assignment")
        with st.container(border=True):
            # Program Mapping
            prog_label = st.selectbox("Program", ["Physics", "Chemistry", "Life Sciences"])
            curr_choice = st.selectbox("Curriculum", ["Old", "New"])
            
            # Map labels to internal database keys
            prog_map = {"Physics": "Physics", "Chemistry": "Chemistry", "Life Sciences": "LifeSciences"}
            data_key = f"{prog_map[prog_label]}_{curr_choice}"
            
            if data_key in MODULE_DATABASE:
                year = st.selectbox("Year", list(MODULE_DATABASE[data_key].keys()))
                sem = st.selectbox("Semester", list(MODULE_DATABASE[data_key][year].keys()))
                
                avail_mods = MODULE_DATABASE[data_key][year][sem]
                mod_options = [f"{m['code']} - {m['name']}" for m in avail_mods]
                selected_mod_str = st.selectbox("Search Modules", mod_options)
                
                students = st.slider("Est. Enrollment", 10, 60, 30)
                
                if st.button("Add to Draft"):
                    code = selected_mod_str.split(" - ")[0]
                    mod_data = next(m for m in avail_mods if m['code'] == code).copy()
                    mod_data['students'] = students
                    
                    if not any(x['code'] == code for x in st.session_state.basket):
                        st.session_state.basket.append(mod_data)
                        st.toast(f"Assigned {code}")
                    else:
                        st.warning("Module already in draft.")
            else:
                st.warning(f"No data found for {data_key}")

    with col_canvas:
        st.markdown("#### Assignment Canvas")
        if not st.session_state.basket:
            st.markdown("<div style='border: 2px dashed #e2e8f0; border-radius: 12px; padding: 4rem; text-align: center; color: #94a3b8;'>Canvas is empty. Add modules to begin.</div>", unsafe_allow_html=True)
        else:
            for i, m in enumerate(st.session_state.basket):
                mod_wam = calculate_wam([m])
                st.markdown(f"""
                <div class="module-row">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-weight: 700; color: var(--primary);">{m['code']}</span>
                            <span style="margin-left: 0.5rem; font-weight: 600;">{m['name']}</span>
                            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 2px;">
                                {m['theory']}H Theory • {m['lab']}H Lab • {m['students']} Students
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.1rem; font-weight: 700;">{mod_wam}</div>
                            <div style="font-size: 0.6rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">WAM Weight</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Remove {m['code']}", key=f"btn_{i}"):
                    st.session_state.basket.pop(i)
                    st.rerun()

with tab_analytics:
    if not st.session_state.basket:
        st.info("Assign modules to view capacity analytics.")
    else:
        # Row 1: KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        total_h = sum(x['theory'] + x['lab'] for x in st.session_state.basket)
        total_s = sum(x['students'] for x in st.session_state.basket)
        
        with k1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Total WAM</div><div class="metric-value">{calculate_wam(st.session_state.basket)}</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Weekly Contact</div><div class="metric-value">{total_h}h</div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Total Students</div><div class="metric-value">{total_s}</div></div>', unsafe_allow_html=True)
        with k4:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Module Count</div><div class="metric-value">{len(st.session_state.basket)}</div></div>', unsafe_allow_html=True)

        st.divider()
        
        # Charts
        c1, c2 = st.columns([1.5, 1])
        df = pd.DataFrame(st.session_state.basket)
        df['WAM Weight'] = df.apply(lambda x: calculate_wam([x]), axis=1)

        with c1:
            fig = px.bar(df, x='code', y='WAM Weight', color='code',
                         title="Workload Distribution per Module", template="plotly_white",
                         color_discrete_sequence=px.colors.qualitative.Prism)
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            current_wam = calculate_wam(st.session_state.basket)
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = current_wam,
                title = {'text': "Capacity Utilization", 'font': {'size': 14}},
                gauge = {
                    'axis': {'range': [None, 24], 'tickwidth': 1},
                    'bar': {'color': "#4f46e5"},
                    'steps': [
                        {'range': [0, 12], 'color': "#f1f5f9"},
                        {'range': [12, 16], 'color': "#dcfce7"},
                        {'range': [16, 24], 'color': "#fee2e2"}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'value': 16}
                }
            ))
            fig_gauge.update_layout(height=400, margin=dict(t=80, b=0))
            st.plotly_chart(fig_gauge, use_container_width=True)

with tab_review:
    if st.session_state.basket:
        st.markdown("#### Allocation Summary")
        review_df = pd.DataFrame(st.session_state.basket)
        review_df['WAM'] = review_df.apply(lambda x: calculate_wam([x]), axis=1)
        
        st.dataframe(review_df[['code', 'name', 'theory', 'lab', 'students', 'WAM']], 
                     use_container_width=True, hide_index=True)
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            csv = review_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Report (CSV)", csv, f"Workload_{user_name}.csv", "text/csv", use_container_width=True)
        with col_ex2:
            if st.button("🚀 Finalize & Submit to HOD"):
                st.balloons()
                st.success("Allocation submitted to Departmental Records.")
    else:
        st.warning("Nothing to review. Add modules in the drafting tab.")

# FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: var(--text-muted); font-size: 0.8rem; padding: 1rem;">
    Department of Natural Sciences Internal Resource Planning Tool<br>
    v4.0.0-PRO • Cycle: Autumn 2026 • © 2026 Academic Affairs
</div>
""", unsafe_allow_html=True)
