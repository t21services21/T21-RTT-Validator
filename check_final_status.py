import os

files = {
    'Pathway 1': r'd:\CascadeProjects\T21-RTT-Validator\data_science_foundations_module.py',
    'Pathway 2': r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway2_module.py',
    'Pathway 3': r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py'
}

print('='*70)
print('FINAL PATHWAY 3 COMPLETION STATUS')
print('='*70)
print()

pathway3_lines = 0
grand_total = 0

for name, path in files.items():
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            count = len(f.readlines())
        grand_total += count
        if 'Pathway 3' in name:
            pathway3_lines = count
        print(f'{name}: {count:,} lines')

print()
print('='*70)
print(f'PATHWAY 3 TARGET: 11,000 lines')
print(f'PATHWAY 3 ACTUAL: {pathway3_lines:,} lines')
print()

if pathway3_lines >= 11000:
    diff = pathway3_lines - 11000
    print('TARGET REACHED!')
    print(f'EXCEEDED BY: {diff:,} lines!')
else:
    remaining = 11000 - pathway3_lines
    progress = pathway3_lines / 11000 * 100
    print(f'Progress: {progress:.1f}%')
    print(f'Need: {remaining:,} more lines')

print()
print('='*70)
print(f'GRAND TOTAL: {grand_total:,} LINES!')
print('='*70)
print()
print('Status:', 'COMPLETE' if pathway3_lines >= 10000 else 'IN PROGRESS')
