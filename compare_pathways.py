import os

files = {
    'Pathway 1 (Foundations)': r'd:\CascadeProjects\T21-RTT-Validator\data_science_foundations_module.py',
    'Pathway 2 (Intermediate)': r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway2_module.py',
    'Pathway 3 (Advanced)': r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py'
}

print('=== DATA SCIENCE PATHWAYS COMPARISON ===\n')

for name, filepath in files.items():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Count content
        total_lines = len(lines)
        unit_funcs = sum(1 for line in lines if 'def _render_unit' in line and '_learning_materials' in line)
        lab_funcs = sum(1 for line in lines if 'def _render_unit' in line and '_labs' in line)
        quiz_funcs = sum(1 for line in lines if 'def _render_unit' in line and '_quiz' in line)
        lab_sections = sum(1 for line in lines if 'Lab 1:' in line or 'Lab 2:' in line or 'Lab 3:' in line)
        
        print(f'{name}:')
        print(f'  Total lines: {total_lines:,}')
        print(f'  Unit functions: {unit_funcs}')
        print(f'  Lab functions: {lab_funcs}')
        print(f'  Quiz functions: {quiz_funcs}')
        print(f'  Lab sections: {lab_sections}')
        print()
    else:
        print(f'{name}: FILE NOT FOUND\n')
