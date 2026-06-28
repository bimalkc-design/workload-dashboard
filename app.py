import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Workload Dashboard", page_icon="📊", layout="wide")

# ==========================================
# 2. DATA LOADERS & WAM ENGINE
# ==========================================
@st.cache_data
def load_data():
    # Core Faculty Data (from your provided dataset)
    faculty_data = [
        {'id': 'F1', 'name': 'Dr. Jas Raj Subba', 'program': 'Chemistry', 'designation': 'Professor', 'core': True},
        {'id': 'F2', 'name': 'Mr. Sangay Wangchuk', 'program': 'Chemistry', 'designation': 'Lecturer', 'core': True},
        {'id': 'F3', 'name': 'Mrs. Punam Mafchan', 'program': 'Chemistry', 'designation': 'Lecturer', 'core': True},
        {'id': 'F4', 'name': 'Ms. Kuenzang Choki', 'program': 'Chemistry', 'designation': 'Lecturer', 'core': True},
        {'id': 'F5', 'name': 'Ms. Sangay Yuden', 'program': 'Chemistry', 'designation': 'Lecturer', 'core': True},
        {'id': 'F6', 'name': 'Mr. Tashi Dendup', 'program': 'Chemistry', 'designation': 'Lecturer', 'core': True},
        {'id': 'F7', 'name': 'Shacha Thinley', 'program': 'Physics', 'designation': 'Lecturer', 'core': True},
        {'id': 'F8', 'name': 'Nachiketa Homchaudhuri', 'program': 'Physics', 'designation': 'Assistant Professor', 'core': True},
        {'id': 'F9', 'name': 'Mon Bahadur Ghalley', 'program': 'Physics', 'designation': 'Lecturer', 'core': True},
        {'id': 'F10', 'name': 'Dr. Karma Tenzin', 'program': 'Physics', 'designation': 'Professor', 'core': True},
        {'id': 'F11', 'name': 'Rit Wik Sharma', 'program': 'Physics', 'designation': 'Lecturer', 'core': True},
        {'id': 'F12', 'name': 'Ugyen Dorji Tamang', 'program': 'Life Sciences', 'designation': 'Lecturer', 'core': True},
        {'id': 'F13', 'name': 'Karma Wangchuck', 'program': 'Life Sciences', 'designation': 'Assistant Professor', 'core': True},
        {'id': 'F14', 'name': 'Mohan Singh Rana', 'program': 'Life Sciences', 'designation': 'Lecturer', 'core': True},
        {'id': 'F15', 'name': 'Tshering Dekar', 'program': 'Life Sciences', 'designation': 'Lecturer', 'core': True},
        {'id': 'F16', 'name': 'Bimal Kumar Chetri', 'program': 'Life Sciences', 'designation': 'Lecturer', 'core': True},
        {'id': 'F17', 'name': 'Sonam Tobgay', 'program': 'Life Sciences', 'designation': 'Lecturer', 'core': True},
        {'id': 'F18', 'name': 'Dechen Lhendup', 'program': 'Service', 'designation': 'Lecturer', 'core': False},
        {'id': 'F19', 'name': 'S. Chitra', 'program': 'Service', 'designation': 'Lecturer', 'core': False},
        {'id': 'F20', 'name': 'DS-Y', 'program': 'Service', 'designation': 'Lecturer', 'core': False},
        {'id': 'F21', 'name': 'Paul Raj', 'program': 'Service', 'designation': 'Lecturer', 'core': False}
    ]

    # Workload assignments for Autumn 2026 Transition
    workload_data = [
        # Chemistry
        {'faculty': 'Dr. Jas Raj Subba', 'program': 'Chemistry', 'code': 'OCH201', 'name': 'Organic Chemistry I', 'theory': 3, 'lab': 3, 'students': 30, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'No', 'admin': 2},
        {'faculty': 'Dr. Jas Raj Subba', 'program': 'Chemistry', 'code': 'FCH101', 'name': 'Fundamentals of Chemistry', 'theory': 3, 'lab': 2, 'students': 37, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'No', 'admin': 1},
        {'faculty': 'Mr. Sangay Wangchuk', 'program': 'Chemistry', 'code': 'PCH303', 'name': 'Physical Chemistry III', 'theory': 3, 'lab': 3, 'students': 32, 'prep': 1.2, 'assess': 'High', 'shadow': 'No', 'admin': 3},
        {'faculty': 'Mr. Sangay Wangchuk', 'program': 'Chemistry', 'code': 'RSM301', 'name': 'Research Methods', 'theory': 4, 'lab': 0, 'students': 30, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'No', 'admin': 0},
        {'faculty': 'Mrs. Punam Mafchan', 'program': 'Chemistry', 'code': 'OCH304', 'name': 'Spectroscopic Methods', 'theory': 4, 'lab': 0, 'students': 32, 'prep': 1.2, 'assess': 'Medium', 'shadow': 'No', 'admin': 0},
        {'faculty': 'Mrs. Punam Mafchan', 'program': 'Chemistry', 'code': 'PCH201', 'name': 'Physical Chemistry I', 'theory': 3, 'lab': 3, 'students': 30, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'No', 'admin': 0},
        
        # Physics
        {'faculty': 'Shacha Thinley', 'program': 'Physics', 'code': 'MPH303', 'name': 'Atomic Physics', 'theory': 3, 'lab': 3, 'students': 35, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'No', 'admin': 2},
        {'faculty': 'Shacha Thinley', 'program': 'Physics', 'code': 'PHY101', 'name': 'Fundamentals of Physics', 'theory': 2, 'lab': 3, 'students': 36, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'No', 'admin': 1},
        {'faculty': 'Nachiketa Homchaudhuri', 'program': 'Physics', 'code': 'TPH302', 'name': 'Statistical Mechanics', 'theory': 4, 'lab': 0, 'students': 33, 'prep': 1.2, 'assess': 'High', 'shadow': 'No', 'admin': 4},
        {'faculty': 'Nachiketa Homchaudhuri', 'program': 'Physics', 'code': 'MEC204', 'name': 'Mechanics II', 'theory': 3, 'lab': 3, 'students': 28, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'No', 'admin': 2},
        {'faculty': 'Dr. Karma Tenzin', 'program': 'Physics', 'code': 'MMP302', 'name': 'Computational Physics', 'theory': 3, 'lab': 3, 'students': 33, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'No', 'admin': 2},
        
        # Life Sciences
        {'faculty': 'Ugyen Dorji Tamang', 'program': 'Life Sciences', 'code': 'BTZ101', 'name': 'Fundamentals of Life Science', 'theory': 3, 'lab': 4, 'students': 42, 'prep': 1.0, 'assess': 'Medium', 'shadow': 'Yes', 'admin': 2},
        {'faculty': 'Ugyen Dorji Tamang', 'program': 'Life Sciences', 'code': 'BTZ202', 'name': 'Microbiology', 'theory': 3, 'lab': 6, 'students': 33, 'prep': 1.0, 'assess': 'High', 'shadow': 'Yes', 'admin': 2},
        {'faculty': 'Karma Wangchuck', 'program': 'Life Sciences', 'code': 'BTS204', 'name': 'Embryology of Angiosperms', 'theory': 3, 'lab': 6, 'students': 33, 'prep': 1.0, 'assess': 'High', 'shadow': 'Yes', 'admin': 2},
        {'faculty': 'Karma Wangchuck', 'program': 'Life Sciences', 'code': 'BTS307', 'name': 'Economic Botany', 'theory': 3, 'lab': 6, 'students': 22, 'prep': 1.2, 'assess': 'High', 'shadow': 'No', 'admin': 2}
    ]
    return faculty_data, workload_data

def calculate_wam(faculty_name, workload_data):
    """Calculates your specific Workload Allocation Model score"""
    total_wam = 0
    assess_score = {'Low': 2, 'Medium': 4, 'High': 7}
    assignments = [w for w in workload_data if w['faculty'] == faculty_name]
    
    for work in assignments:
        base_load = (work['theory'] * work['prep']) + work['lab'] + work['admin']
        intensity = assess_score.get(work.get('assess', 'Medium'), 4)
        student_loading = (work['students'] * intensity) * 0.04
        
        if work.get('shadow') == 'Yes':
            student_loading = student_loading * 0.5
            
        total_wam += base_load + student_loading
    return round(total_wam, 1)

def get_status(wam):
    """Assigns status based on target WAM thresholds"""
    if wam == 0: return 'Empty'
    if wam < 10: return 'Sharing'
    if wam <= 19: return 'Balanced'
    return 'Review'

# Load Data
faculty_data, workload_data = load_data()

# Pre-calculate WAM for all faculty
for f in faculty_data:
    f['WAM'] = calculate_wam(f['name'], workload_data)
    f['Status'] = get_status(f['WAM'])
    f['Modules'] = len([w for w in workload_data if w['faculty'] == f['name']])

df_faculty = pd.DataFrame(faculty_data)
df_workload = pd.DataFrame(workload_data)

# ==========================================
# 3. DASHBOARD UI
# ==========================================
st.title("🏛️ Department of Natural Sciences")
st.subheader("Workload Management Dashboard - Autumn 2026 Transition")
st.markdown("---")

# Top Level KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Core Faculty", len(df_faculty[df_faculty['core'] == True]))
col2.metric("Total Modules Running", len(df_workload))
col3.metric("Avg WAM (Active Faculty)", round(df_faculty[df_faculty['WAM'] > 0]['WAM'].mean(), 1))
col4.metric("Faculty Overloaded (Review)", len(df_faculty[df_faculty['Status'] == 'Review']))

st.markdown("---")

# TABS
tab1, tab2, tab3 = st.tabs(["📊 WAM Visualizer", "🗂️ Faculty Roster", "📚 Module Assignments"])

# TAB 1: WAM Visualizer
with tab1:
    st.header("Faculty Workload Distribution")
    
    # Program Filter
    program_filter = st.selectbox("Filter by Program", ["All", "Chemistry", "Physics", "Life Sciences"])
    
    plot_df = df_faculty if program_filter == "All" else df_faculty[df_faculty['program'] == program_filter]
    
    # Plotly Bar Chart
    fig = px.bar(
        plot_df[plot_df['WAM'] > 0].sort_values('WAM', ascending=True), 
        x='WAM', 
        y='name', 
        color='Status',
        color_discrete_map={'Balanced': '#28a745', 'Sharing': '#ffc107', 'Review': '#dc3545', 'Empty': '#6c757d'},
        orientation='h',
        title=f"WAM Scores ({program_filter})",
        hover_data=['designation', 'Modules']
    )
    
    # Add vertical line for "Optimal Load" threshold (19 based on your logic)
    fig.add_vline(x=19, line_dash="dash", line_color="red", annotation_text="Max Optimal Load (19)")
    
    st.plotly_chart(fig, width="stretch")

# TAB 2: Faculty Roster
with tab2:
    st.header("Faculty Data Table")
    st.dataframe(
        df_faculty[['name', 'program', 'designation', 'Modules', 'WAM', 'Status']].sort_values(by="WAM", ascending=False),
        width="stretch",
        hide_index=True
    )

# TAB 3: Module Assignments
with tab3:
    st.header("Autumn 2026 Module Assignments")
    st.markdown("This reflects the concurrent running of New Year 1 programs and Old Year 2/3 programs.")
    st.dataframe(df_workload, width="stretch", hide_index=True)
