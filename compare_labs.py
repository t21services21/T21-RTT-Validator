with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway2_module.py', 'r', encoding='utf-8') as f:
    p2_lines = f.readlines()

with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'r', encoding='utf-8') as f:
    p3_lines = f.readlines()

print('=== LAB CONTENT COMPARISON ===\n')
print(f'Pathway 2: {len(p2_lines):,} total lines')
print(f'Pathway 3: {len(p3_lines):,} total lines\n')

for i in range(1, 7):
    p2_func = f'def _render_unit{i}_labs'
    p3_func = f'def _render_unit{i}_labs'
    
    p2_start = next((idx for idx, line in enumerate(p2_lines) if p2_func in line), None)
    p3_start = next((idx for idx, line in enumerate(p3_lines) if p3_func in line), None)
    
    if p2_start and p3_start:
        # Find next function
        p2_end = next((idx for idx in range(p2_start+1, len(p2_lines)) 
                      if 'def ' in p2_lines[idx] and '_render' in p2_lines[idx]), len(p2_lines))
        p3_end = next((idx for idx in range(p3_start+1, len(p3_lines)) 
                      if 'def ' in p3_lines[idx] and '_render' in p3_lines[idx]), len(p3_lines))
        
        p2_size = p2_end - p2_start
        p3_size = p3_end - p3_start
        
        ratio = (p3_size / p2_size * 100) if p2_size > 0 else 0
        status = "✅" if ratio >= 50 else "⚠️" if ratio >= 30 else "❌"
        
        print(f'Unit {i} Labs: P2={p2_size:3} lines | P3={p3_size:3} lines | {ratio:3.0f}% {status}')
    elif p2_start:
        print(f'Unit {i} Labs: P2 exists | P3 MISSING ❌')
    elif p3_start:
        print(f'Unit {i} Labs: P2 MISSING | P3 exists ✅')
