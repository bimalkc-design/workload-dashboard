import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import hashlib

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="DNS Workload Command Center",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. COMPLETE MODULE DATABASE
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
            ]
        },
        'Year 2': {
            'Semester I': [
                {'code': 'APH201', 'name': 'Physics of Space and Satellites', 'theory': 3, 'lab': 2},
                {'code': 'EMT201', 'name': 'Electricity and Magnetism', 'theory': 3, 'lab': 3},
                {'code': 'MMP201', 'name': 'Essential Mathematics for Physics', 'theory': 3, 'lab': 0},
                {'code': 'APH202', 'name': 'Introduction to Electronic Systems', 'theory': 2, 'lab': 3},
            ],
            'Semester II': [
                {'code': 'MMP202', 'name': 'Mathematical Methods in Physics', 'theory': 3, 'lab': 0},
                {'code': 'FMP201', 'name': 'Modern Physics', 'theory': 3, 'lab': 2},
                {'code': 'PHW202', 'name': 'Optics', 'theory': 3, 'lab': 3},
                {'code': 'TPH201', 'name': 'Thermal Physics', 'theory': 3, 'lab': 2},
            ]
        },
        'Year 3': {
            'Semester I': [
                {'code': 'APH303', 'name': 'Computational Physics', 'theory': 3, 'lab': 3},
                {'code': 'APH304', 'name': 'Applied Integrated Circuits', 'theory': 3, 'lab': 3},
                {'code': 'EPH301', 'name': 'Atmospheric Physics', 'theory': 3, 'lab': 2},
                {'code': 'QME301', 'name': 'Quantum Mechanics', 'theory': 4, 'lab': 0},
            ],
            'Semester II': [
                {'code': 'ANP301', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3},
                {'code': 'ANP302', 'name': 'Nuclear Physics', 'theory': 3, 'lab': 2},
                {'code': 'SSP301', 'name': 'Condensed Matter Physics', 'theory': 3, 'lab': 3},
                {'code': 'APH305', 'name': 'Machine Learning for Physics', 'theory': 3, 'lab': 3},
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
            ]
        },
        'Year 2': {
            'Semester I': [
                {'code': 'BTS202', 'name': 'Plant Anatomy and Physiology', 'theory': 3, 'lab': 3},
                {'code': 'BCH201', 'name': 'Biochemistry', 'theory': 3, 'lab': 4},
                {'code': 'ZLS201', 'name': 'Invertebrate Biology', 'theory': 3, 'lab': 3},
                {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
            ],
            'Semester II': [
                {'code': 'BTS203', 'name': 'Embryology of Angiosperms', 'theory': 3, 'lab': 6},
                {'code': 'BTZ202', 'name': 'Genetics', 'theory': 3, 'lab': 4},
                {'code': 'ZLS202', 'name': 'Cell and Molecular Biology', 'theory': 3, 'lab': 4},
                {'code': 'ZLS203', 'name': 'Chordate Biology', 'theory': 3, 'lab': 3},
            ]
        },
        'Year 3': {
            'Semester I': [
                {'code': 'BTS304', 'name': 'Fungi and Plant Pathology', 'theory': 3, 'lab': 3},
                {'code': 'GRS301', 'name': 'GIS and Remote Sensing', 'theory': 2, 'lab': 3},
                {'code': 'ZLS304', 'name': 'Anatomy and Physiology', 'theory': 3, 'lab': 3},
                {'code': 'ZLS305', 'name': 'Developmental Biology', 'theory': 3, 'lab': 3},
            ],
            'Semester II': [
                {'code': 'BTS305', 'name': 'Principles of Plant Systematics', 'theory': 3, 'lab': 3},
                {'code': 'BTS306', 'name': 'Horticulture Management', 'theory': 3, 'lab': 3},
                {'code': 'BTZ303', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
                {'code': 'BTZ304', 'name': 'Bioinformatics', 'theory': 2, 'lab': 4},
            ]
        },
        'Year 4': {
            'Semester I': [
                {'code': 'BTS407', 'name': 'Ethnobotany and Phytochemistry', 'theory': 3, 'lab': 4},
                {'code': 'BTZ405', 'name': 'Biotechnology and Tissue Culture', 'theory': 3, 'lab': 4},
                {'code': 'BTZ406', 'name': 'Ecology and Conservation', 'theory': 3, 'lab': 3},
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
# 3. FACULTY DATABASE
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
# 4. CORE FUNCTIONS
# ==========================================
def calculate_wam(modules):
    """Calculate WAM based on selected modules"""
    total_wam = 0
    for module in modules:
        theory = module.get('theory', 0)
        lab = module.get('lab', 0)
        students = module.get('students', 25)
        base_load = (theory * 1.0) + lab
        student_loading = (students * 4) * 0.04
        total_wam += base_load + student_loading
    return round(total_wam, 1)

def get_status(wam):
    """Get status based on WAM score"""
    if wam == 0:
        return 'No Load', '⚪', '#6c757d', 'No modules selected'
    elif wam < 12:
        return 'Light Load', '🟡', '#ffc107', 'You have capacity for more modules'
    elif wam <= 16:
        return 'Balanced', '🟢', '#28a745', 'Your workload is well-balanced!'
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
    log_file = 'workload_logs.json'
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    logs.append(log_entry)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

# ==========================================
# 5. ADVANCED STYLING
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header .subtitle {
        font-size: 1.1rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    .main-header .badge {
        background: rgba(255,215,0,0.2);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        border: 1px solid rgba(255,215,0,0.3);
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .wam-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
        margin: 1rem 0;
        transition: all 0.3s;
    }
    .wam-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5);
    }
    .wam-number {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
    }
    .wam-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.5rem 2rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1rem;
        margin: 0.5rem 0;
        letter-spacing: 0.5px;
    }
    
    .module-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s;
    }
    .module-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
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
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin: 1rem 0;
    }
    .stat-item {
        text-align: center;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .admin-zone {
        background: #1a1a2e;
        color: #daa520;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        margin-bottom: 2rem;
        border: 1px solid #daa520;
    }
    
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem 0 1rem 0;
        font-size: 0.85rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 2rem;
    }
    
    .threshold-guide {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .threshold-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .threshold-dot {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        display: inline-block;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
        .wam-number { font-size: 3rem; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .threshold-guide { flex-direction: column; align-items: center; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 6. SESSION STATE
# ==========================================
if 'selected_modules' not in st.session_state:
    st.session_state.selected_modules = []
if 'student_counts' not in st.session_state:
    st.session_state.student_counts = {}
if 'faculty_name' not in st.session_state:
    st.session_state.faculty_name = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# ==========================================
# 7. HEADER
# ==========================================
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
        <div>
            <div style="font-size: 0.8rem; letter-spacing: 3px; color: #daa520; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem;">
                Royal University of Bhutan
            </div>
            <h1>⚖️ DNS Workload Command Center</h1>
            <div class="subtitle">Department of Natural Sciences • Academic Resource & Workload Portal</div>
            <div class="badge">📅 {} • Autumn 2026 Transition</div>
        </div>
        <div style="text-align: right; font-size: 0.9rem; opacity: 0.7;">
            <div>🎓 Faculty Self-Service</div>
            <div>📊 Real-time WAM Calculator</div>
        </div>
    </div>
</div>
""".format(datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)

# ==========================================
# 8. SIDEBAR - User Profile & Module Selection
# ==========================================
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    
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
        st.success(f"✅ Welcome, {faculty_name}!")
    
    designation = st.selectbox(
        "Designation",
        ["Professor", "Associate Professor", "Assistant Professor", "Senior Lecturer", "Lecturer"]
    )
    
    st.divider()
    st.markdown("### 📚 Module Selection")
    
    program = st.selectbox("Program", ["Physics", "Chemistry", "Life Sciences"])
    curriculum = st.selectbox("Curriculum", ["Old", "New"])
    
    prog_map = {"Physics": "Physics", "Chemistry": "Chemistry", "Life Sciences": "LifeSciences"}
    full_key = f"{prog_map[program]}_{curriculum}"
    
    year = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
    semester = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI"])
    
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
                "Student Count",
                min_value=25,
                max_value=40,
                value=30,
                step=1,
                key=f"slider_{module_code}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Add Module", use_container_width=True):
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
    
    st.divider()
    st.markdown("### 📊 Your Session")
    if st.session_state.selected_modules:
        st.metric("Modules Selected", len(st.session_state.selected_modules))
        total_students = sum(st.session_state.student_counts.values())
        st.metric("Total Students", total_students)
    
    st.divider()
    st.markdown("### 🔒 Admin Access")
    admin_pass = st.text_input("Admin PIN", type="password")
    if admin_pass == "DNS777":
        st.session_state.is_admin = True
        st.success("🔓 Admin mode activated")
    elif admin_pass:
        st.error("❌ Invalid PIN")

# ==========================================
# 9. MAIN CONTENT
# ==========================================
if not st.session_state.faculty_name:
    st.info("👈 Please select or enter your name in the sidebar to get started")
    st.stop()

# Main layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📋 Your Selected Modules")
    
    if not st.session_state.selected_modules:
        st.info("👈 Use the sidebar to select your modules")
    else:
        total_theory = 0
        total_lab = 0
        
        for module in st.session_state.selected_modules:
            students = st.session_state.student_counts.get(module['code'], 25)
            total_theory += module['theory']
            total_lab += module['lab']
            
            st.markdown(f"""
            <div class="module-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <span class="module-code">{module['code']}</span>
                        <span class="module-name"> - {module['name']}</span>
                        <br>
                        <span class="module-details">📖 {module['theory']}h Theory • 🧪 {module['lab']}h Lab • 👨‍🎓 {students} Students</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="background: #667eea; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">
                            {module['theory'] + module['lab']}h
                        </span>
                        <button onclick="removeModule('{module['code']}')" style="background: none; border: none; color: #dc3545; font-size: 1.2rem; cursor: pointer;">✖️</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"✖️ Remove {module['code']}", key=f"remove_{module['code']}"):
                st.session_state.selected_modules.remove(module)
                del st.session_state.student_counts[module['code']]
                st.rerun()
        
        # Summary stats
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{len(st.session_state.selected_modules)}</div>
                <div class="stat-label">Total Modules</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{total_theory}h</div>
                <div class="stat-label">Theory Hours</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{total_lab}h</div>
                <div class="stat-label">Lab Hours</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{sum(st.session_state.student_counts.values())}</div>
                <div class="stat-label">Total Students</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 📊 Your WAM Score")
    
    if st.session_state.selected_modules:
        wam = calculate_wam([
            {**m, 'students': st.session_state.student_counts.get(m['code'], 25)}
            for m in st.session_state.selected_modules
        ])
        status, emoji, color, message = get_status(wam)
        
        # Log activity
        log_activity(
            st.session_state.faculty_name,
            [{'code': m['code'], 'name': m['name'], 'students': st.session_state.student_counts.get(m['code'], 25)} 
             for m in st.session_state.selected_modules],
            wam,
            status
        )
        
        # WAM Display
        st.markdown(f"""
        <div class="wam-card">
            <div class="wam-number">{wam}</div>
            <div class="wam-label">Workload Allocation Model Score</div>
        </div>
        """, unsafe_allow_html=True)
        
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
        progress = min(wam / 16, 1.0)
        st.progress(progress)
        st.caption("0" + " " * 50 + "16+")
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Theory", f"{total_theory}h")
        with col2:
            st.metric("Lab", f"{total_lab}h")
        with col3:
            st.metric("Total", f"{total_theory + total_lab}h")
        
        # Module Contribution Chart
        if len(st.session_state.selected_modules) > 1:
            st.markdown("### Module Contribution")
            module_wams = []
            for module in st.session_state.selected_modules:
                temp_wam = calculate_wam([{**module, 'students': st.session_state.student_counts.get(module['code'], 25)}])
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
# 10. WAM THRESHOLD GUIDE
# ==========================================
st.markdown("""
<div class="threshold-guide">
    <div class="threshold-item">
        <span class="threshold-dot" style="background: #ffc107;"></span>
        <span><strong>Light Load</strong> (WAM &lt; 12)</span>
    </div>
    <div class="threshold-item">
        <span class="threshold-dot" style="background: #28a745;"></span>
        <span><strong>Balanced</strong> (WAM 12 - 16)</span>
    </div>
    <div class="threshold-item">
        <span class="threshold-dot" style="background: #dc3545;"></span>
        <span><strong>Heavy Load</strong> (WAM &gt; 16)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 11. DETAILED BREAKDOWN
# ==========================================
if st.session_state.selected_modules:
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Detailed Breakdown", "📈 Analytics", "📜 Your History"])
    
    with tab1:
        details = []
        for module in st.session_state.selected_modules:
            students = st.session_state.student_counts.get(module['code'], 25)
            wam = calculate_wam([{**module, 'students': students}])
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
            fig_pie = px.pie(
                values=[df_details['Theory'].sum(), df_details['Lab'].sum()],
                names=['Theory Hours', 'Lab Hours'],
                title="Theory vs Lab Distribution",
                color_discrete_sequence=['#667eea', '#764ba2']
            )
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
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
        log_file = 'workload_logs.json'
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    all_logs = json.load(f)
                my_logs = [log for log in all_logs if log['faculty'] == st.session_state.faculty_name]
                
                if my_logs:
                    history_df = pd.DataFrame(my_logs)
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
                    
                    csv_history = history_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Complete History",
                        data=csv_history,
                        file_name=f"history_{st.session_state.faculty_name.replace(' ', '_')}.csv",
                        mime='text/csv'
                    )
                else:
                    st.info("No history found for this faculty member")
            except:
                st.info("No history found")
        else:
            st.info("No history found")

# ==========================================
# 12. ADMIN DASHBOARD
# ==========================================
if st.session_state.is_admin:
    st.markdown("---")
    st.markdown("""
    <div class="admin-zone">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="font-size: 1.5rem; font-weight: 700;">🔐 ADMIN COMMAND CENTER</span>
                <span style="margin-left: 1rem; font-size: 0.9rem; opacity: 0.7;">Master Workload Records</span>
            </div>
            <div style="font-size: 0.8rem; color: #666;">
                🔒 Secure Access • Department of Natural Sciences
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    log_file = 'workload_logs.json'
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                all_logs = json.load(f)
            
            if all_logs:
                admin_df = pd.DataFrame(all_logs)
                admin_df['timestamp'] = pd.to_datetime(admin_df['timestamp'])
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Submissions", len(admin_df))
                col2.metric("Unique Faculty", admin_df['faculty'].nunique())
                col3.metric("Avg WAM", round(admin_df['wam'].mean(), 2))
                col4.metric("Heavy Load Cases", len(admin_df[admin_df['status'] == 'Heavy Load']))
                
                st.dataframe(
                    admin_df.sort_values('timestamp', ascending=False),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "timestamp": st.column_config.DatetimeColumn("Date & Time"),
                        "wam": st.column_config.NumberColumn("WAM Score", format="%.1f"),
                    }
                )
                
                # Export all data
                csv_all = admin_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Complete Departmental Report",
                    data=csv_all,
                    file_name=f"DNS_Complete_Report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime='text/csv'
                )
                
                if st.button("🗑️ Purge Database (Caution!)", use_container_width=True):
                    os.remove(log_file)
                    st.success("Database purged successfully!")
                    st.rerun()
            else:
                st.info("No records found in the database")
        except:
            st.info("No records found")
    else:
        st.info("No records found in the database")

# ==========================================
# 13. FOOTER
# ==========================================
st.markdown("""
<div class="footer">
    <p>🏛️ Department of Natural Sciences • Royal University of Bhutan</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        💡 Select your modules from the sidebar to calculate your WAM in real-time
    </p>
    <p style="font-size: 0.7rem; opacity: 0.5; margin-top: 0.5rem;">
        📱 Optimized for desktop and mobile • All activities are logged for reference
    </p>
</div>
""", unsafe_allow_html=True)
