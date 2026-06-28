import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Workload Calculator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DATA DEFINITIONS
# ==========================================
CURRICULUM_DATA = {
    'Old': {
        'Chemistry': {
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
                    {'code': 'FMT103', 'name': 'Foundations of Mathematics-II', 'theory': 3, 'lab': 0},
                ]
            },
            'Year 2': {
                'Semester III': [
                    {'code': 'ICH101', 'name': 'Inorganic Chemistry I', 'theory': 3, 'lab': 3},
                    {'code': 'PCH201', 'name': 'Physical Chemistry I', 'theory': 3, 'lab': 3},
                    {'code': 'FMT204', 'name': 'Foundations of Mathematics-III', 'theory': 3, 'lab': 0},
                    {'code': 'RSM301', 'name': 'Research Methods', 'theory': 3, 'lab': 0},
                ],
                'Semester IV': [
                    {'code': 'OCH201', 'name': 'Organic Chemistry I', 'theory': 3, 'lab': 3},
                    {'code': 'OCH202', 'name': 'Organic Chemistry II', 'theory': 3, 'lab': 3},
                    {'code': 'PCH202', 'name': 'Physical Chemistry II', 'theory': 3, 'lab': 3},
                    {'code': 'AMT202', 'name': 'Foundations of Statistics', 'theory': 3, 'lab': 0},
                    {'code': 'ACH201', 'name': 'Introduction to Analytical Chemistry', 'theory': 3, 'lab': 2},
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
        'Physics': {
            'Year 1': {
                'Semester I': [
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
        'Life Sciences': {
            'Year 1': {
                'Semester I': [
                    {'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4},
                    {'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2},
                    {'code': 'FMT101', 'name': 'Fundamentals of Mathematics', 'theory': 3, 'lab': 0},
                    {'code': 'ACS101', 'name': 'Academic Skills', 'theory': 2, 'lab': 0},
                ],
                'Semester II': [
                    {'code': 'BTS101', 'name': 'Plant Diversity', 'theory': 3, 'lab': 3},
                    {'code': 'PLS101', 'name': 'Fundamentals of Physics for Life Sciences', 'theory': 2, 'lab': 2},
                    {'code': 'CSP101', 'name': 'Foundations of Python Programming', 'theory': 2, 'lab': 3},
                ]
            },
            'Year 2': {
                'Semester III': [
                    {'code': 'BTS202', 'name': 'Plant Anatomy and Physiology', 'theory': 3, 'lab': 3},
                    {'code': 'BCH201', 'name': 'Biochemistry', 'theory': 3, 'lab': 4},
                    {'code': 'ZLS201', 'name': 'Invertebrate Biology and Parasitology', 'theory': 3, 'lab': 3},
                    {'code': 'DAT101', 'name': 'Statistical Computing I', 'theory': 2, 'lab': 3},
                ],
                'Semester IV': [
                    {'code': 'BTS203', 'name': 'Embryology of Angiosperms', 'theory': 3, 'lab': 6},
                    {'code': 'BTZ202', 'name': 'Genetics', 'theory': 3, 'lab': 4},
                    {'code': 'ZLS202', 'name': 'Cell and Molecular Biology', 'theory': 3, 'lab': 4},
                    {'code': 'ZLS203', 'name': 'Chordate Biology', 'theory': 3, 'lab': 3},
                ]
            },
            'Year 3': {
                'Semester V': [
                    {'code': 'BTS304', 'name': 'Fungi and Plant Pathology', 'theory': 3, 'lab': 3},
                    {'code': 'GRS301', 'name': 'GIS and Remote Sensing', 'theory': 2, 'lab': 3},
                    {'code': 'ZLS304', 'name': 'Anatomy and Physiology of Vertebrates', 'theory': 3, 'lab': 3},
                    {'code': 'ZLS305', 'name': 'Developmental Biology', 'theory': 3, 'lab': 3},
                ],
                'Semester VI': [
                    {'code': 'BTS305', 'name': 'Principles of Plant Systematics', 'theory': 3, 'lab': 3},
                    {'code': 'BTS306', 'name': 'Horticulture and Postharvest Management', 'theory': 3, 'lab': 3},
                    {'code': 'BTZ303', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
                    {'code': 'BTZ304', 'name': 'Bioinformatics', 'theory': 2, 'lab': 4},
                ]
            }
        }
    },
    'New': {
        'Physics': {
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
                    {'code': 'APH304', 'name': 'Applied Integrated Circuits and Logic Design', 'theory': 3, 'lab': 3},
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
        'Life Sciences': {
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
                    {'code': 'ZLS201', 'name': 'Invertebrate Biology and Parasitology', 'theory': 3, 'lab': 3},
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
                    {'code': 'ZLS304', 'name': 'Anatomy and Physiology of Vertebrates', 'theory': 3, 'lab': 3},
                    {'code': 'ZLS305', 'name': 'Developmental Biology', 'theory': 3, 'lab': 3},
                ],
                'Semester II': [
                    {'code': 'BTS305', 'name': 'Principles of Plant Systematics', 'theory': 3, 'lab': 3},
                    {'code': 'BTS306', 'name': 'Horticulture and Postharvest Management', 'theory': 3, 'lab': 3},
                    {'code': 'BTZ303', 'name': 'Microbiology', 'theory': 3, 'lab': 6},
                    {'code': 'BTZ304', 'name': 'Bioinformatics', 'theory': 2, 'lab': 4},
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
        }
    }
}

# ==========================================
# 3. WAM CALCULATION ENGINE
# ==========================================
def calculate_wam(selected_modules, student_counts):
    """Calculate WAM based on selected modules and student counts"""
    total_wam = 0
    assess_score = {'Low': 2, 'Medium': 4, 'High': 7}
    
    for module in selected_modules:
        # Get student count for this module
        students = student_counts.get(module['code'], 25)
        
        # Base load calculation
        base_load = (module['theory'] * 1.0) + module['lab'] + 0  # admin default 0
        
        # Assessment intensity (default Medium)
        intensity = assess_score['Medium']
        
        # Student loading
        student_loading = (students * intensity) * 0.04
        
        # Shadow factor (default No)
        shadow_factor = 1.0  # No shadow
        
        total_wam += base_load + student_loading
    
    return round(total_wam, 1)

def get_status(wam):
    """Get status based on WAM score"""
    if wam == 0:
        return 'No Load', '⚪'
    elif wam < 10:
        return 'Sharing', '🟡'
    elif wam <= 19:
        return 'Balanced', '🟢'
    else:
        return 'Review', '🔴'

# ==========================================
# 4. CUSTOM CSS FOR MOBILE RESPONSIVENESS
# ==========================================
st.markdown("""
<style>
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
        }
        .stSelectbox, .stNumberInput {
            margin-bottom: 10px;
        }
        .stMetric {
            text-align: center;
        }
    }
    /* Card-like styling */
    .module-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    .selected-module {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .wam-display {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. MAIN APP
# ==========================================
st.title("⚖️ Workload Allocation Model Calculator")
st.markdown("**Department of Natural Sciences**")
st.caption(f"📅 {datetime.now().strftime('%B %d, %Y')}")

# Initialize session state
if 'selected_modules' not in st.session_state:
    st.session_state.selected_modules = []
if 'student_counts' not in st.session_state:
    st.session_state.student_counts = {}

# ==========================================
# SIDEBAR - User Profile & Filters
# ==========================================
with st.sidebar:
    st.header("👤 Faculty Profile")
    
    faculty_name = st.text_input("Your Name", placeholder="e.g., Dr. Jas Raj Subba")
    faculty_designation = st.selectbox(
        "Designation",
        ["Professor", "Associate Professor", "Assistant Professor", "Senior Lecturer", "Lecturer"]
    )
    
    st.markdown("---")
    st.header("📚 Module Selection")
    
    # Program selection
    program = st.selectbox("Program", ["Physics", "Chemistry", "Life Sciences"])
    
    # Curriculum selection
    curriculum = st.selectbox("Curriculum", ["Old", "New"])
    
    # Year and Semester selection
    year = st.selectbox("Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
    semester = st.selectbox("Semester", ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI"])
    
    # Get available modules
    available_modules = []
    try:
        available_modules = CURRICULUM_DATA[curriculum][program][year][semester]
    except KeyError:
        st.warning("No modules available for this selection")
    
    # Module selector
    if available_modules:
        module_options = [f"{m['code']} - {m['name']}" for m in available_modules]
        selected_module_str = st.selectbox("Select Module", ["-- Select --"] + module_options)
        
        if selected_module_str != "-- Select --":
            module_code = selected_module_str.split(" - ")[0]
            selected_module = next(m for m in available_modules if m['code'] == module_code)
            
            # Student count slider
            students = st.slider(
                f"Student Count for {module_code}",
                min_value=25,
                max_value=40,
                value=30,
                step=1,
                key=f"students_{module_code}"
            )
            
            # Add module button
            if st.button("➕ Add Module", use_container_width=True):
                # Check if module already added
                if not any(m['code'] == module_code for m in st.session_state.selected_modules):
                    st.session_state.selected_modules.append(selected_module)
                    st.session_state.student_counts[module_code] = students
                    st.success(f"✅ Added {module_code}")
                    st.rerun()
                else:
                    st.warning(f"⚠️ {module_code} already added")
    
    st.markdown("---")
    
    # Quick Actions
    if st.button("🗑️ Clear All Modules", use_container_width=True):
        st.session_state.selected_modules = []
        st.session_state.student_counts = {}
        st.rerun()
    
    # Export functionality
    st.markdown("---")
    st.header("📥 Export Data")
    
    if st.session_state.selected_modules:
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
        
        # Create export data
        export_data = []
        for module in st.session_state.selected_modules:
            students = st.session_state.student_counts.get(module['code'], 25)
            wam = calculate_wam([module], {module['code']: students})
            export_data.append({
                'Module Code': module['code'],
                'Module Name': module['name'],
                'Theory Hours': module['theory'],
                'Lab Hours': module['lab'],
                'Students': students,
                'WAM Score': wam
            })
        
        df_export = pd.DataFrame(export_data)
        csv = convert_df(df_export)
        st.download_button(
            label="📊 Download My Workload",
            data=csv,
            file_name=f'workload_{faculty_name.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )

# ==========================================
# MAIN CONTENT
# ==========================================
# Split into columns for better layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("📋 Your Selected Modules")
    
    if not st.session_state.selected_modules:
        st.info("👆 Use the sidebar to select your modules. Add modules to calculate your WAM.")
    else:
        # Display selected modules
        total_theory = 0
        total_lab = 0
        total_students = 0
        
        for i, module in enumerate(st.session_state.selected_modules):
            students = st.session_state.student_counts.get(module['code'], 25)
            total_theory += module['theory']
            total_lab += module['lab']
            total_students += students
            
            # Module card
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 0.5])
            with col1:
                st.markdown(f"**{module['code']}**")
                st.caption(module['name'])
            with col2:
                st.metric("Theory", f"{module['theory']}h", delta=None)
            with col3:
                st.metric("Lab", f"{module['lab']}h", delta=None)
            with col4:
                st.metric("Students", f"{students}")
            with col5:
                if st.button("✖️", key=f"remove_{module['code']}"):
                    st.session_state.selected_modules.remove(module)
                    del st.session_state.student_counts[module['code']]
                    st.rerun()
            st.divider()
        
        # Summary stats
        st.subheader("📊 Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Modules", len(st.session_state.selected_modules))
        with col2:
            st.metric("Total Theory Hours", total_theory)
        with col3:
            st.metric("Total Lab Hours", total_lab)
        with col4:
            st.metric("Total Students", total_students)

with col_right:
    st.header("📊 WAM Score")
    
    if st.session_state.selected_modules:
        # Calculate WAM
        wam = calculate_wam(st.session_state.selected_modules, st.session_state.student_counts)
        status, emoji = get_status(wam)
        
        # Display WAM
        st.markdown(f"""
        <div class="wam-display">
            {wam}
        </div>
        """, unsafe_allow_html=True)
        
        # Status display
        status_color = {
            'No Load': '#6c757d',
            'Sharing': '#ffc107',
            'Balanced': '#28a745',
            'Review': '#dc3545'
        }
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <span class="status-badge" style="background-color: {status_color[status]}; color: white;">
                {emoji} {status}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Interpretation
        if status == 'Balanced':
            st.success("✅ Your workload is well-balanced!")
        elif status == 'Sharing':
            st.info("ℹ️ You have capacity for more modules")
        elif status == 'Review':
            st.warning("⚠️ Your workload is high - consider sharing modules")
        else:
            st.info("📝 No modules selected yet")
        
        # Progress bar
        st.markdown("### Workload Level")
        progress = min(wam / 25, 1.0)  # Cap at 25 WAM
        st.progress(progress)
        st.caption(f"0{' ' * 50}25+")
        
        # Breakdown chart
        st.markdown("### Module Contribution")
        if len(st.session_state.selected_modules) > 1:
            module_wams = []
            for module in st.session_state.selected_modules:
                temp_wam = calculate_wam([module], {module['code']: st.session_state.student_counts.get(module['code'], 25)})
                module_wams.append({
                    'Module': module['code'],
                    'WAM': temp_wam,
                    'Theory': module['theory'],
                    'Lab': module['lab']
                })
            
            df_wam = pd.DataFrame(module_wams)
            fig = px.bar(
                df_wam,
                x='Module',
                y='WAM',
                title="WAM per Module",
                color='Module',
                height=300
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 Select modules from the sidebar to calculate your WAM")

# ==========================================
# DETAILED BREAKDOWN SECTION
# ==========================================
if st.session_state.selected_modules:
    st.markdown("---")
    st.header("📊 Detailed Breakdown")
    
    # Create detailed table
    details = []
    for module in st.session_state.selected_modules:
        students = st.session_state.student_counts.get(module['code'], 25)
        # Calculate individual WAM
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
    
    # Display as table with formatting
    st.dataframe(
        df_details,
        use_container_width=True,
        hide_index=True,
        column_config={
            "WAM": st.column_config.NumberColumn("WAM Score", format="%.1f"),
            "Students": st.column_config.NumberColumn("Students", format="%d"),
        }
    )
    
    # Visual breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        # Theory vs Lab distribution
        total_theory = df_details['Theory'].sum()
        total_lab = df_details['Lab'].sum()
        fig_pie = px.pie(
            values=[total_theory, total_lab],
            names=['Theory Hours', 'Lab Hours'],
            title="Theory vs Lab Distribution",
            color_discrete_sequence=['#667eea', '#764ba2']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # WAM distribution
        fig_bar = px.bar(
            df_details,
            x='Code',
            y='WAM',
            title="WAM per Module",
            color='WAM',
            color_continuous_scale='Viridis',
            height=300
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Additional stats
    st.subheader("📈 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_wam = df_details['WAM'].mean()
        st.metric("Average WAM per Module", f"{avg_wam:.1f}")
    with col2:
        max_wam = df_details['WAM'].max()
        max_module = df_details[df_details['WAM'] == max_wam]['Code'].iloc[0]
        st.metric("Highest WAM Module", f"{max_module} ({max_wam:.1f})")
    with col3:
        total_students = df_details['Students'].sum()
        st.metric("Total Students", total_students)

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.caption("💡 **Tip:** Use the sidebar to add/remove modules. Adjust student counts using sliders.")
st.caption("📱 This dashboard is optimized for both desktop and mobile devices.")
st.caption("📧 For support, contact: support@natural-sciences.edu")
st.caption(f"🔄 Last updated: {datetime.now().strftime('%B %Y')}")
