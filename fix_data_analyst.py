with open(r'd:\CascadeProjects\T21-RTT-Validator\data_analyst_pathway_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the broken section - starts around line 7449, ends before render function at 21300
# Delete lines 7448-21299 (all broken lab content)
new_lines = lines[:7447] + [
    '\n',
    '        st.markdown("---")\n',
    '        st.markdown("## 🧪 Labs & Mini-Projects")\n',
    '        st.markdown("**Hands-on exercises for Unit 5 - Python for Data Analysis**")\n',
    '        st.code("""# Example: Load and analyze data with pandas\n',
    'import pandas as pd\n',
    '\n',
    'df = pd.read_csv("data.csv")\n',
    'print(df.head())\n',
    'print(df.describe())\n',
    '""", language="python")\n',
    '\n',
    '\n'
] + lines[21299:]

with open(r'd:\CascadeProjects\T21-RTT-Validator\data_analyst_pathway_module.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Fixed Data Analyst pathway. Deleted lines 7448-21299 ({21299-7447} lines). New total: {len(new_lines)}')
