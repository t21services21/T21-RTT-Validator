with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Delete ALL broken lab content from line 2076 to 8236
new_lines = lines[:2075] + [
    '\n',
    '\n'
] + lines[8236:]

with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Fixed pathway3 completely. Deleted lines 2076-8236 ({8236-2075} lines). New total: {len(new_lines)}')
