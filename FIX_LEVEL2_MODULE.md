# FIXING LEVEL 2 MODULE TO MATCH LEVEL 3

## WHAT NEEDS TO BE ADDED:

### 1. File References for All Units ✅ (In Progress)
- Mandatory units 1-5: DONE
- Optional units 6-7: DONE
- Optional units 8-18: NEED TO ADD

### 2. Load Markdown Function
```python
def load_markdown_file(filename):
    """Load markdown content from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file: {str(e)}\n\nPlease ensure the file '{filename}' exists in the project folder."
```

### 3. PDF Download Functionality
- Use existing `create_unit_pdf` from `tquk_pdf_converter`
- Add download button for each unit

### 4. Materials Tab Enhancement
- Load actual markdown content
- Display in expander
- Add PDF download button
- Show activities count
- Show learning outcomes count

## FILES THAT EXIST:
✅ tquk_materials/UNIT_01_ADMIN_SERVICES_COMPLETE.md
✅ tquk_materials/UNIT_02_DOCUMENT_PRODUCTION_COMPLETE.md
✅ tquk_materials/UNIT_03_EMPLOYER_ORGANISATIONS_COMPLETE.md
✅ tquk_materials/UNIT_04_COMMUNICATION_COMPLETE.md
✅ tquk_materials/UNIT_05_WORKING_RELATIONSHIPS_COMPLETE.md
✅ tquk_materials/UNITS_08_TO_18_COMPLETE.md (contains all optional units)

## QUICK FIX NEEDED:
1. Add file references to units 8-18
2. Add load_markdown_file function
3. Update materials display to load and show content
4. Add PDF download buttons

## ESTIMATED TIME: 10 minutes
