# Save this as edit_app.py
import re

# Read current app.py
with open('app.py', 'r') as f:
    content = f.read()

# Example: Add a new feature
# Find where to add code and insert it
new_feature = '''
# ==========================================
# NEW FEATURE: Additional Statistics
# ==========================================
with st.expander("📊 Additional Statistics"):
    st.write("Your new feature here")
'''

# Insert after a specific section
if "st.title" in content:
    content = content.replace(
        'st.title("⚖️ Workload Allocation Model Calculator")',
        f'st.title("⚖️ Workload Allocation Model Calculator")\n{new_feature}'
    )

# Save the modified file
with open('app.py', 'w') as f:
    f.write(content)

print("✅ app.py updated successfully!")
