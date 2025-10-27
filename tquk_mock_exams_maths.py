"""
TQUK Functional Skills Maths - Mock Exams
Complete practice papers with answer keys
"""

import streamlit as st

# Mock exam data structure
MOCK_EXAMS_MATHS = {
    "Level 1": {
        "Paper 1": {
            "section_a": {
                "title": "Section A: Non-Calculator",
                "duration": 30,
                "marks": 15,
                "questions": [
                    {"q": "Calculate: 45 + 37", "answer": "82", "marks": 1},
                    {"q": "What is 10% of £60?", "answer": "£6", "marks": 1},
                    {"q": "Round 47 to the nearest 10", "answer": "50", "marks": 1},
                    {"q": "Calculate: 8 × 7", "answer": "56", "marks": 1},
                    {"q": "What is 1/2 of 24?", "answer": "12", "marks": 1},
                    {"q": "Order these: 45, 54, 40, 50", "answer": "40, 45, 50, 54", "marks": 2},
                    {"q": "Calculate: 100 - 37", "answer": "63", "marks": 1},
                    {"q": "What is 5²?", "answer": "25", "marks": 1},
                    {"q": "Convert 2.5 hours to minutes", "answer": "150 minutes", "marks": 2},
                    {"q": "Calculate: 72 ÷ 9", "answer": "8", "marks": 1},
                    {"q": "What is 25% of 80?", "answer": "20", "marks": 2},
                    {"q": "Write 3/4 as a decimal", "answer": "0.75", "marks": 1}
                ]
            },
            "section_b": {
                "title": "Section B: Calculator Allowed",
                "duration": 90,
                "marks": 45,
                "questions": [
                    {"q": "A shop sells pens at £2.50 each. How much for 6 pens?", "answer": "£15.00", "marks": 2},
                    {"q": "Calculate the area of a rectangle 12cm × 8cm", "answer": "96 cm²", "marks": 2},
                    {"q": "You travel 120 miles in 3 hours. What is your average speed?", "answer": "40 mph", "marks": 3},
                    {"q": "A jacket costs £80. There is 20% off. What is the sale price?", "answer": "£64", "marks": 3},
                    {"q": "Find the mean of: 5, 8, 12, 15", "answer": "10", "marks": 2},
                    {"q": "Convert 3.5 kg to grams", "answer": "3500 g", "marks": 2},
                    {"q": "Calculate the perimeter of a square with sides of 9cm", "answer": "36 cm", "marks": 2},
                    {"q": "You work 35 hours at £9.50/hour. What do you earn?", "answer": "£332.50", "marks": 3},
                    {"q": "What is the probability of rolling a 3 on a dice?", "answer": "1/6", "marks": 2},
                    {"q": "A recipe needs 250g flour for 12 cakes. How much for 18 cakes?", "answer": "375 g", "marks": 3},
                    {"q": "Calculate: 15% of £240", "answer": "£36", "marks": 2},
                    {"q": "Find the range of: 12, 18, 9, 25, 14", "answer": "16", "marks": 2},
                    {"q": "Share £100 in ratio 2:3", "answer": "£40 and £60", "marks": 3},
                    {"q": "Calculate the volume of a cube with sides of 4cm", "answer": "64 cm³", "marks": 3},
                    {"q": "You buy 3 items at £4.50 each. Pay with £20. How much change?", "answer": "£6.50", "marks": 3},
                    {"q": "Convert 2.5 km to metres", "answer": "2500 m", "marks": 2},
                    {"q": "Calculate: 3/5 of 45", "answer": "27", "marks": 2},
                    {"q": "A car travels 45 miles per gallon. How many gallons for 180 miles?", "answer": "4 gallons", "marks": 3},
                    {"q": "Find 20% of £150 then add it to £150", "answer": "£180", "marks": 3}
                ]
            }
        }
    },
    "Level 2": {
        "Paper 1": {
            "section_a": {
                "title": "Section A: Non-Calculator",
                "duration": 30,
                "marks": 15,
                "questions": [
                    {"q": "Calculate: 456 + 789", "answer": "1245", "marks": 1},
                    {"q": "What is 15% of £80?", "answer": "£12", "marks": 2},
                    {"q": "Calculate: 12²", "answer": "144", "marks": 1},
                    {"q": "Simplify ratio 12:18", "answer": "2:3", "marks": 2},
                    {"q": "Calculate: 3/4 + 1/4", "answer": "1 or 4/4", "marks": 1},
                    {"q": "Order: -5, 3, -2, 0, 7", "answer": "-5, -2, 0, 3, 7", "marks": 2},
                    {"q": "Calculate: 7 × 8 × 2", "answer": "112", "marks": 1},
                    {"q": "Convert 0.75 to a fraction", "answer": "3/4", "marks": 2},
                    {"q": "Calculate: 200 - 87", "answer": "113", "marks": 1},
                    {"q": "What is 2/3 of 90?", "answer": "60", "marks": 2}
                ]
            },
            "section_b": {
                "title": "Section B: Calculator Allowed",
                "duration": 90,
                "marks": 45,
                "questions": [
                    {"q": "Calculate compound interest: £500 at 4% for 2 years", "answer": "£540.80", "marks": 4},
                    {"q": "Find area of circle with radius 7cm (π = 3.14)", "answer": "153.86 cm²", "marks": 3},
                    {"q": "A laptop costs £400 + 20% VAT. Then 10% discount. Final price?", "answer": "£432", "marks": 4},
                    {"q": "Calculate volume of cylinder: radius 5cm, height 12cm", "answer": "942 cm³", "marks": 4},
                    {"q": "Share £450 in ratio 2:3:5", "answer": "£90, £135, £225", "marks": 3},
                    {"q": "Find mean of grouped data: 0-10(5), 11-20(8), 21-30(6)", "answer": "~15.8", "marks": 4},
                    {"q": "Convert 10 miles to km (1 mile = 1.6km)", "answer": "16 km", "marks": 2},
                    {"q": "Calculate: 35% of £450", "answer": "£157.50", "marks": 2},
                    {"q": "Find median of: 12, 18, 9, 25, 14, 20, 16", "answer": "16", "marks": 2},
                    {"q": "A car depreciates 20% per year. Worth after 2 years if bought for £15,000?", "answer": "£9,600", "marks": 4},
                    {"q": "Calculate area of triangle: base 12cm, height 8cm", "answer": "48 cm²", "marks": 2},
                    {"q": "Express 45 out of 180 as a percentage", "answer": "25%", "marks": 2},
                    {"q": "Calculate: 4.56 × 3.2", "answer": "14.592", "marks": 2},
                    {"q": "Find range and mode of: 5, 7, 5, 9, 5, 11, 7", "answer": "Range=6, Mode=5", "marks": 3},
                    {"q": "£144 is after 20% increase. Find original amount", "answer": "£120", "marks": 3}
                ]
            }
        }
    }
}

def render_maths_mock_exam(level):
    """Render maths mock exam"""
    st.subheader("🎯 Mock Examinations - Maths")
    
    st.info(f"""
    **{level} Mock Exam**
    
    Complete both sections in one sitting (2 hours total).
    Section A: No calculator | Section B: Calculator allowed
    """)
    
    paper = MOCK_EXAMS_MATHS[level]["Paper 1"]
    
    # Section selector
    section = st.radio(
        "Select Section:",
        ["Section A: Non-Calculator", "Section B: Calculator"],
        horizontal=True
    )
    
    section_key = "section_a" if "Non-Calculator" in section else "section_b"
    section_data = paper[section_key]
    
    st.markdown("---")
    st.markdown(f"## {section_data['title']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Duration", f"{section_data['duration']} minutes")
    with col2:
        st.metric("Total Marks", section_data['marks'])
    
    st.markdown("---")
    
    # Show/hide answers
    show_answers = st.checkbox("Show Answer Key", key=f"show_maths_answers_{level}_{section_key}")
    
    # Display questions
    for i, q_data in enumerate(section_data['questions'], 1):
        st.markdown(f"**Question {i}** ({q_data['marks']} mark{'s' if q_data['marks'] > 1 else ''})")
        st.markdown(q_data['q'])
        
        if show_answers:
            st.success(f"**Answer:** {q_data['answer']}")
        else:
            st.text_input(
                "Your answer:",
                key=f"maths_answer_{level}_{section_key}_q{i}",
                placeholder="Enter your answer..."
            )
        
        st.markdown("---")
    
    # Download button
    if st.button("📥 Download Mock Exam (PDF)", key=f"download_maths_{level}_{section_key}"):
        st.info("PDF generation coming soon! For now, you can print this page.")

if __name__ == "__main__":
    st.title("🔢 Maths Mock Exams")
    level = st.radio("Select Level:", ["Level 1", "Level 2"], horizontal=True)
    render_maths_mock_exam(level)
