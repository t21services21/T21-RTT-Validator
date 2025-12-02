with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Delete lines 2070-2356 (broken lab content in unit 5)
new_lines = lines[:2069] + [
    '        st.markdown("---")\n',
    '        st.markdown("## Labs for Unit 5")\n',
    '        st.markdown("**Lab content coming soon - focus on environments, packaging, and CI/CD**")\n',
    '\n'
] + lines[2356:]

with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Fixed pathway3 unit 5. Deleted lines 2070-2356 ({2356-2069} lines). New total: {len(new_lines)}')
