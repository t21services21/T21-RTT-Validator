with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Delete lines 2073-2936 (broken lab content in unit 6)
new_lines = lines[:2072] + [
    '        st.markdown("---")\n',
    '        st.markdown("## Labs for Unit 6")\n',
    '        st.markdown("**Lab content coming soon - focus on MLOps and monitoring**")\n',
    '\n'
] + lines[2936:]

with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Fixed pathway3 unit 6. Deleted lines 2073-2936 ({2936-2072} lines). New total: {len(new_lines)}')
