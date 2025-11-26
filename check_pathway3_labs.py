with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== PATHWAY 3 LABS AUDIT ===\n')

# Check for lab functions
for i in range(1, 8):
    func_name = f'def _render_unit{i}_labs'
    has_func = any(func_name in line for line in lines)
    status = '✅' if has_func else '❌'
    print(f'Unit {i} Labs Function: {status}')

# Check where labs are called in the main render
print('\nLabs Tab Content:')
in_labs_tab = False
for i, line in enumerate(lines):
    if 'Labs & Mini Projects' in line and 'st.subheader' in line:
        in_labs_tab = True
        print(f'Found Labs tab at line {i+1}')
    if in_labs_tab and 'with tabs[' in line and 'Labs' not in lines[i-5:i+5]:
        break
    if in_labs_tab and ('_render_unit' in line or 'st.info' in line or 'st.markdown' in line):
        print(f'  Line {i+1}: {line.strip()[:80]}')
