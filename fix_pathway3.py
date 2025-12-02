with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Delete lines 1550-1743 and replace with simple content
new_lines = lines[:1549] + [
    '        st.markdown("## Lab 3: Demand Forecasting Mini-Project (90 min)")\n',
    '        st.markdown("**Objective:** Production-ready demand forecast")\n',
    '        st.code("""# Placeholder for Lab 3 content""", language="python")\n',
    '\n'
] + lines[1743:]

with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Fixed pathway3. Deleted lines 1550-1743 ({1743-1549} lines). New total: {len(new_lines)}')
