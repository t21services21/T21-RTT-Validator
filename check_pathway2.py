with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway2_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== PATHWAY 2 CONTENT AUDIT ===\n')
print(f'Total lines: {len(lines):,}\n')

# Check for unit functions
print('Unit Functions:')
units = {
    1: 'Feature Engineering & Data Pipelines',
    2: 'Supervised Learning: Regression',
    3: 'Supervised Learning: Classification',
    4: 'Model Evaluation & Validation',
    5: 'Unsupervised Learning & Segmentation',
    6: 'Deploying & Operationalising Models',
    7: 'Pathway 2 Capstone Project'
}

for num, name in units.items():
    func_name = f'def _render_unit{num}_learning_materials'
    has_func = any(func_name in line for line in lines)
    status = '✅' if has_func else '❌'
    print(f'  Unit {num}: {name[:35]:35} - {status}')

# Check for labs
print('\nLab Functions:')
for num in range(1, 8):
    func_name = f'def _render_unit{num}_labs'
    has_func = any(func_name in line for line in lines)
    status = '✅' if has_func else '❌'
    print(f'  Unit {num} Labs: {status}')

# Check for quizzes
print('\nQuiz Functions:')
for num in range(1, 8):
    func_name = f'def _render_unit{num}_quiz'
    has_func = any(func_name in line for line in lines)
    status = '✅' if has_func else '❌'
    print(f'  Unit {num} Quiz: {status}')

# Count content
lab_count = sum(1 for line in lines if 'Lab 1:' in line or 'Lab 2:' in line or 'Lab 3:' in line)
quiz_count = sum(1 for line in lines if 'Quick-check quiz' in line)

print(f'\nTotal Lab sections: {lab_count}')
print(f'Total Quiz sections: {quiz_count}')
