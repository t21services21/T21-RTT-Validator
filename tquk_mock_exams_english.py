"""
TQUK Functional Skills English - Mock Exams
Complete practice papers with answer keys and marking guidance
"""

import streamlit as st
from datetime import datetime
import random

# Mock Exam Papers
MOCK_EXAMS = {
    "Level 1": {
        "Paper 1": {
            "reading": {
                "title": "Reading Assessment - Mock Paper 1",
                "duration": 60,
                "total_marks": 20,
                "documents": [
                    {
                        "title": "Document 1: Email from Manager",
                        "text": """
From: sarah.jones@company.co.uk
To: all.staff@company.co.uk
Subject: New Office Hours

Dear Team,

From Monday 1st November, our office hours will change. We will now open at 8:30am instead of 9:00am. 
The office will still close at 5:30pm.

This change will help us serve our customers better as many have requested earlier opening times.

Please make sure you arrive on time. If you have any concerns about the new hours, please speak to your line manager.

Best regards,
Sarah Jones
Office Manager
                        """
                    },
                    {
                        "title": "Document 2: Notice",
                        "text": """
COMMUNITY CENTRE - WEEKLY CLASSES

Monday: Yoga (6pm-7pm) - £5 per session
Tuesday: Art Class (7pm-9pm) - £8 per session  
Wednesday: Cooking (6:30pm-8:30pm) - £10 per session
Thursday: Dance (6pm-7:30pm) - £6 per session
Friday: Photography (7pm-9pm) - £12 per session

All classes are suitable for beginners. 
Book online at www.communitycentre.co.uk or call 0151 123 4567.

First session FREE for new members!
                        """
                    }
                ],
                "questions": [
                    {
                        "id": 1,
                        "question": "What time will the office open from 1st November?",
                        "marks": 1,
                        "answer": "8:30am",
                        "guidance": "Award 1 mark for correct time. Accept '8:30' or '8.30' or 'half past eight'."
                    },
                    {
                        "id": 2,
                        "question": "Why is the office changing its opening hours?",
                        "marks": 1,
                        "answer": "To serve customers better / Customers requested earlier opening",
                        "guidance": "Award 1 mark for any answer showing understanding that it's for customer benefit."
                    },
                    {
                        "id": 3,
                        "question": "What should staff do if they have concerns about the new hours?",
                        "marks": 1,
                        "answer": "Speak to their line manager",
                        "guidance": "Award 1 mark for mentioning line manager or manager."
                    },
                    {
                        "id": 4,
                        "question": "Which class at the community centre is the most expensive?",
                        "marks": 1,
                        "answer": "Photography (£12)",
                        "guidance": "Award 1 mark for Photography. Accept with or without price."
                    },
                    {
                        "id": 5,
                        "question": "How long does the cooking class last?",
                        "marks": 1,
                        "answer": "2 hours / 120 minutes",
                        "guidance": "Award 1 mark for 2 hours or 120 minutes. Must show understanding of duration."
                    },
                    {
                        "id": 6,
                        "question": "What day is the yoga class?",
                        "marks": 1,
                        "answer": "Monday",
                        "guidance": "Award 1 mark for Monday only."
                    },
                    {
                        "id": 7,
                        "question": "How can you book a class? Give two ways.",
                        "marks": 2,
                        "answer": "1. Online at www.communitycentre.co.uk 2. Call 0151 123 4567",
                        "guidance": "Award 1 mark for each correct method. Must give TWO methods for full marks."
                    },
                    {
                        "id": 8,
                        "question": "What is the purpose of the email from Sarah Jones?",
                        "marks": 2,
                        "answer": "To inform staff about new office hours / To tell staff about the change in opening time",
                        "guidance": "Award 2 marks for clear statement about informing/telling staff about hours change. 1 mark for partial answer."
                    },
                    {
                        "id": 9,
                        "question": "Who is the email intended for?",
                        "marks": 1,
                        "answer": "All staff / The team / Employees",
                        "guidance": "Award 1 mark for any answer showing it's for all staff members."
                    },
                    {
                        "id": 10,
                        "question": "The community centre notice says 'All classes are suitable for beginners'. What does this tell you?",
                        "marks": 2,
                        "answer": "You don't need experience / Anyone can join / No previous skills needed",
                        "guidance": "Award 2 marks for clear explanation. 1 mark for partial understanding."
                    },
                    {
                        "id": 11,
                        "question": "What special offer is available for new members?",
                        "marks": 1,
                        "answer": "First session free",
                        "guidance": "Award 1 mark for mentioning first session is free."
                    },
                    {
                        "id": 12,
                        "question": "If you wanted to attend the dance class, what time would you need to arrive?",
                        "marks": 1,
                        "answer": "6pm / 6 o'clock",
                        "guidance": "Award 1 mark for 6pm or equivalent."
                    },
                    {
                        "id": 13,
                        "question": "Compare the cost of the art class and the yoga class. Which is cheaper and by how much?",
                        "marks": 3,
                        "answer": "Yoga is cheaper by £3 (Yoga £5, Art £8, difference £3)",
                        "guidance": "Award 3 marks for complete answer with calculation. 2 marks for identifying cheaper class with prices. 1 mark for identifying cheaper class only."
                    },
                    {
                        "id": 14,
                        "question": "The email uses formal language. Give one example of formal language from the email.",
                        "marks": 2,
                        "answer": "Examples: 'Dear Team', 'Best regards', 'Please make sure', 'line manager'",
                        "guidance": "Award 2 marks for appropriate example with explanation. 1 mark for example only."
                    },
                    {
                        "id": 15,
                        "question": "Why might someone prefer to book online rather than by phone?",
                        "marks": 2,
                        "answer": "More convenient / Can do it anytime / Don't have to speak to someone / Quicker",
                        "guidance": "Award 2 marks for clear, sensible reason. 1 mark for basic answer."
                    }
                ]
            },
            "writing": {
                "title": "Writing Assessment - Mock Paper 1",
                "duration": 60,
                "total_marks": 27,
                "tasks": [
                    {
                        "id": 1,
                        "title": "Task 1: Email (Informal)",
                        "prompt": """
You are planning a birthday party for your friend. Write an email to another friend inviting them to the party.

In your email you should:
• Say when and where the party is
• Explain what activities you have planned
• Ask them to let you know if they can come

Write at least 150 words.

Your friend's email address is: alex.brown@email.com
                        """,
                        "word_count": 150,
                        "marks": 13,
                        "format": "Email (informal)",
                        "marking_criteria": {
                            "content": 4,
                            "organisation": 3,
                            "language": 3,
                            "spag": 3
                        }
                    },
                    {
                        "id": 2,
                        "title": "Task 2: Letter (Formal)",
                        "prompt": """
You recently bought a mobile phone from an online shop but it arrived damaged. Write a letter to the shop complaining about the problem.

In your letter you should:
• Explain what you ordered and when
• Describe the problem with the phone
• Say what you would like the shop to do

Write at least 150 words.
                        """,
                        "word_count": 150,
                        "marks": 14,
                        "format": "Letter (formal)",
                        "marking_criteria": {
                            "content": 4,
                            "organisation": 3,
                            "language": 4,
                            "spag": 3
                        }
                    }
                ]
            },
            "slc": {
                "title": "Speaking, Listening and Communicating - Mock Assessment",
                "duration": 25,
                "activities": [
                    {
                        "id": 1,
                        "title": "Activity 1: Discussion",
                        "prompt": """
**Topic: Healthy Eating**

You will take part in a discussion about healthy eating with your assessor and possibly other learners.

You should:
• Share your views on healthy eating
• Listen to others' opinions
• Respond to what others say
• Ask relevant questions

Duration: 10-15 minutes
                        """,
                        "assessment_criteria": [
                            "Makes relevant contributions",
                            "Listens and responds to others",
                            "Uses appropriate language",
                            "Asks relevant questions"
                        ]
                    },
                    {
                        "id": 2,
                        "title": "Activity 2: Presentation",
                        "prompt": """
**Topic: A Place You Would Like to Visit**

Prepare and deliver a short presentation about a place you would like to visit.

You should include:
• Where the place is
• Why you want to visit it
• What you would do there
• When you might go

Duration: 3-5 minutes
Preparation time: 10 minutes
                        """,
                        "assessment_criteria": [
                            "Presents information clearly",
                            "Uses appropriate language",
                            "Speaks clearly and at appropriate pace",
                            "Engages the audience"
                        ]
                    }
                ]
            }
        }
    },
    "Level 2": {
        "Paper 1": {
            "reading": {
                "title": "Reading Assessment - Mock Paper 1",
                "duration": 60,
                "total_marks": 30,
                "documents": [
                    {
                        "title": "Document 1: Article",
                        "text": """
THE BENEFITS OF REGULAR EXERCISE

Regular physical activity is one of the most important things you can do for your health. According to recent studies, adults who engage in regular exercise reduce their risk of developing serious health conditions by up to 50%.

Exercise doesn't just benefit your physical health. Research has shown that people who exercise regularly report better mental health, including reduced symptoms of depression and anxiety. Physical activity releases endorphins, often called 'feel-good' hormones, which can improve mood and reduce stress.

The NHS recommends that adults should aim for at least 150 minutes of moderate-intensity activity per week. This could include brisk walking, cycling, or swimming. Alternatively, 75 minutes of vigorous-intensity activity, such as running or playing sports, can provide similar benefits.

Many people believe they don't have time for exercise, but experts suggest that even short bursts of activity can be beneficial. Taking the stairs instead of the lift, walking during your lunch break, or doing household chores all count towards your weekly activity target.

Starting an exercise routine can seem daunting, but the key is to find activities you enjoy. Whether it's dancing, gardening, or playing with your children, any movement is better than none. The important thing is to make physical activity a regular part of your daily routine.
                        """
                    },
                    {
                        "title": "Document 2: Workplace Policy",
                        "text": """
FLEXIBLE WORKING POLICY

1. Introduction
This policy outlines the company's approach to flexible working arrangements. We recognise that employees may need flexibility to balance work and personal commitments.

2. Eligibility
All employees who have completed 26 weeks of continuous service are eligible to request flexible working.

3. Types of Flexible Working
• Part-time working
• Flexitime (choosing start and finish times)
• Job sharing
• Working from home
• Compressed hours (working full-time hours in fewer days)

4. How to Apply
Requests must be made in writing to your line manager at least 8 weeks before the proposed start date. Your request should include:
• The type of flexible working you are requesting
• The proposed start date
• How you think it will affect your work and colleagues
• How any potential problems could be addressed

5. Decision Process
Your manager will arrange a meeting within 28 days to discuss your request. A decision will be made within 14 days of this meeting. If approved, a trial period of 3 months will be implemented before the arrangement becomes permanent.

6. Grounds for Refusal
Requests may be refused on business grounds, including:
• Additional costs that would harm the business
• Inability to reorganise work among existing staff
• Negative impact on quality or performance
• Insufficient work during the proposed working times
                        """
                    },
                    {
                        "title": "Document 3: Advertisement",
                        "text": """
SUMMER MUSIC FESTIVAL 2025
15-17 AUGUST | RIVERSIDE PARK

Join us for three days of incredible live music!

FRIDAY: Rock & Indie
Headliner: The Electric Storm (9:30pm)
Support: Rising Phoenix, The Echoes

SATURDAY: Pop & Dance
Headliner: Luna Sky (9:45pm)
Support: Neon Dreams, Crystal Beats

SUNDAY: Folk & Acoustic
Headliner: The Wanderers (9:00pm)
Support: Meadow Lane, Sunset Strings

TICKET PRICES:
Day Ticket: £45 (advance) / £55 (on the door)
Weekend Pass: £110 (advance only)
VIP Weekend Pass: £250 (includes backstage access, premium viewing area, and complimentary drinks)

FACILITIES:
• Food court with 20+ vendors
• Camping area (additional £30 per tent)
• Free parking
• Cash machines on site
• First aid stations

Children under 12 go FREE with a paying adult (max 2 children per adult).

Book now at www.summermusicfest.co.uk
Early bird discount: 10% off all tickets booked before 1st June!
                        """
                    }
                ],
                "questions": [
                    {
                        "id": 1,
                        "question": "According to the article, by how much can regular exercise reduce the risk of serious health conditions?",
                        "marks": 1,
                        "answer": "Up to 50% / 50%",
                        "guidance": "Award 1 mark for 50% or up to 50%."
                    },
                    {
                        "id": 2,
                        "question": "What are endorphins and what effect do they have?",
                        "marks": 2,
                        "answer": "Endorphins are 'feel-good' hormones that improve mood and reduce stress",
                        "guidance": "Award 2 marks for both parts (what they are AND their effect). 1 mark for one part only."
                    },
                    {
                        "id": 3,
                        "question": "How many minutes of moderate-intensity activity does the NHS recommend per week?",
                        "marks": 1,
                        "answer": "150 minutes",
                        "guidance": "Award 1 mark for 150 minutes."
                    },
                    {
                        "id": 4,
                        "question": "Give three examples of moderate-intensity activity mentioned in the article.",
                        "marks": 3,
                        "answer": "Brisk walking, cycling, swimming",
                        "guidance": "Award 1 mark for each correct example (max 3 marks)."
                    },
                    {
                        "id": 5,
                        "question": "The article suggests ways to fit exercise into a busy schedule. Identify two of these suggestions.",
                        "marks": 2,
                        "answer": "Taking stairs instead of lift, walking during lunch break, doing household chores",
                        "guidance": "Award 1 mark for each correct suggestion (max 2 marks)."
                    },
                    {
                        "id": 6,
                        "question": "According to the Flexible Working Policy, how long must an employee have worked for the company before they can request flexible working?",
                        "marks": 1,
                        "answer": "26 weeks",
                        "guidance": "Award 1 mark for 26 weeks or 6 months."
                    },
                    {
                        "id": 7,
                        "question": "List three types of flexible working mentioned in the policy.",
                        "marks": 3,
                        "answer": "Part-time working, Flexitime, Job sharing, Working from home, Compressed hours",
                        "guidance": "Award 1 mark for each correct type (max 3 marks). Accept any 3 from the list."
                    },
                    {
                        "id": 8,
                        "question": "How much notice must employees give when requesting flexible working?",
                        "marks": 1,
                        "answer": "At least 8 weeks / 8 weeks",
                        "guidance": "Award 1 mark for 8 weeks."
                    },
                    {
                        "id": 9,
                        "question": "What happens if a flexible working request is approved?",
                        "marks": 2,
                        "answer": "A trial period of 3 months is implemented before it becomes permanent",
                        "guidance": "Award 2 marks for mentioning both trial period AND that it becomes permanent. 1 mark for one part only."
                    },
                    {
                        "id": 10,
                        "question": "Compare the cost of a day ticket bought in advance with one bought on the door. How much do you save by buying in advance?",
                        "marks": 2,
                        "answer": "£10 (£55 - £45 = £10)",
                        "guidance": "Award 2 marks for correct calculation with answer. 1 mark for identifying prices without calculation."
                    },
                    {
                        "id": 11,
                        "question": "What is the latest time a headliner will perform across the weekend?",
                        "marks": 1,
                        "answer": "9:45pm (Saturday)",
                        "guidance": "Award 1 mark for 9:45pm. Accept with or without day."
                    },
                    {
                        "id": 12,
                        "question": "A family of 2 adults and 3 children (aged 8, 10, and 14) want weekend passes. How much will it cost them?",
                        "marks": 3,
                        "answer": "£330 (3 adults × £110 = £330. Two children under 12 go free, one child aged 14 needs ticket)",
                        "guidance": "Award 3 marks for correct answer with working. 2 marks for correct method with minor error. 1 mark for some understanding."
                    },
                    {
                        "id": 13,
                        "question": "What is the purpose of the exercise article? Support your answer with evidence from the text.",
                        "marks": 3,
                        "answer": "To inform/persuade readers about the benefits of exercise. Evidence: provides facts about health benefits, NHS recommendations, practical suggestions",
                        "guidance": "Award 3 marks for clear purpose with relevant evidence. 2 marks for purpose with limited evidence. 1 mark for purpose only."
                    },
                    {
                        "id": 14,
                        "question": "The festival advertisement uses persuasive language. Identify one example and explain how it persuades.",
                        "marks": 3,
                        "answer": "Examples: 'incredible live music', 'Early bird discount', 'FREE'. Explanation should show how it encourages people to attend/book.",
                        "guidance": "Award 3 marks for example with clear explanation. 2 marks for example with basic explanation. 1 mark for example only."
                    },
                    {
                        "id": 15,
                        "question": "Compare the tone and style of the workplace policy with the festival advertisement. How are they different and why?",
                        "marks": 4,
                        "answer": "Policy is formal, factual, uses official language (for employees, legal document). Advertisement is informal, exciting, persuasive (to attract customers, sell tickets).",
                        "guidance": "Award 4 marks for clear comparison with reasons. 3 marks for comparison with limited reasons. 2 marks for basic comparison. 1 mark for identifying difference only."
                    }
                ]
            },
            "writing": {
                "title": "Writing Assessment - Mock Paper 1",
                "duration": 60,
                "total_marks": 27,
                "tasks": [
                    {
                        "id": 1,
                        "title": "Task 1: Article (Informal)",
                        "prompt": """
Your local community magazine has asked readers to write about their favorite local business. Write an article recommending a local business you like.

In your article you should:
• Describe the business and what it offers
• Explain why you recommend it
• Encourage others to visit

Write at least 250 words.
                        """,
                        "word_count": 250,
                        "marks": 13,
                        "format": "Article (informal)",
                        "marking_criteria": {
                            "content": 4,
                            "organisation": 3,
                            "language": 3,
                            "spag": 3
                        }
                    },
                    {
                        "id": 2,
                        "title": "Task 2: Report (Formal)",
                        "prompt": """
You work for a company that is considering introducing flexible working hours. Your manager has asked you to write a report on the advantages and disadvantages of flexible working.

In your report you should:
• Explain what flexible working means
• Discuss the advantages for employees and the company
• Discuss any potential disadvantages
• Make a recommendation

Write at least 250 words.
                        """,
                        "word_count": 250,
                        "marks": 14,
                        "format": "Report (formal)",
                        "marking_criteria": {
                            "content": 4,
                            "organisation": 4,
                            "language": 3,
                            "spag": 3
                        }
                    }
                ]
            }
        }
    }
}

def render_mock_exam_tab(level):
    """Render mock exam interface"""
    st.subheader("🎯 Mock Examinations")
    
    st.info(f"""
    **Complete Practice Exams for {level}**
    
    These mock exams match the format and difficulty of real TQUK assessments.
    Use them to prepare for your actual exam.
    """)
    
    # Select paper
    available_papers = list(MOCK_EXAMS[level].keys())
    selected_paper = st.selectbox(
        "Select Mock Paper:",
        available_papers,
        key=f"mock_paper_{level}"
    )
    
    # Select component
    component = st.radio(
        "Select Component:",
        ["📖 Reading", "✍️ Writing", "🗣️ Speaking, Listening & Communicating"],
        horizontal=True,
        key=f"mock_component_{level}"
    )
    
    st.markdown("---")
    
    paper = MOCK_EXAMS[level][selected_paper]
    
    if component == "📖 Reading":
        render_reading_mock(level, selected_paper, paper["reading"])
    elif component == "✍️ Writing":
        render_writing_mock(level, selected_paper, paper["writing"])
    else:
        render_slc_mock(level, selected_paper, paper["slc"])

def render_reading_mock(level, paper_name, reading_data):
    """Render reading mock exam"""
    st.markdown(f"## {reading_data['title']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Duration", f"{reading_data['duration']} minutes")
    with col2:
        st.metric("Total Marks", reading_data['total_marks'])
    with col3:
        st.metric("Questions", len(reading_data['questions']))
    
    st.markdown("---")
    
    # Display documents
    st.markdown("### 📄 Reading Documents")
    
    for doc in reading_data['documents']:
        with st.expander(f"📄 {doc['title']}", expanded=True):
            st.markdown(doc['text'])
    
    st.markdown("---")
    
    # Display questions
    st.markdown("### ❓ Questions")
    
    # Option to show/hide answers
    show_answers = st.checkbox("Show Answer Key & Marking Guidance", key=f"show_answers_{level}_{paper_name}_reading")
    
    for q in reading_data['questions']:
        st.markdown(f"**Question {q['id']}** ({q['marks']} mark{'s' if q['marks'] > 1 else ''})")
        st.markdown(q['question'])
        
        if show_answers:
            st.success(f"**Answer:** {q['answer']}")
            st.info(f"**Marking Guidance:** {q['guidance']}")
        else:
            st.text_area(
                "Your answer:",
                key=f"answer_{level}_{paper_name}_q{q['id']}",
                height=100,
                placeholder="Write your answer here..."
            )
        
        st.markdown("---")
    
    # Download options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download Question Paper (PDF)", key=f"download_q_{level}_{paper_name}"):
            st.info("PDF generation coming soon! For now, you can print this page.")
    with col2:
        if st.button("📥 Download Answer Key (PDF)", key=f"download_a_{level}_{paper_name}"):
            st.info("PDF generation coming soon! For now, use 'Show Answer Key' above.")

def render_writing_mock(level, paper_name, writing_data):
    """Render writing mock exam"""
    st.markdown(f"## {writing_data['title']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Duration", f"{writing_data['duration']} minutes")
    with col2:
        st.metric("Total Marks", writing_data['total_marks'])
    
    st.markdown("---")
    
    for task in writing_data['tasks']:
        st.markdown(f"### {task['title']}")
        st.markdown(f"**Marks:** {task['marks']} | **Format:** {task['format']} | **Minimum Words:** {task['word_count']}")
        
        st.markdown(task['prompt'])
        
        st.text_area(
            "Your response:",
            key=f"writing_{level}_{paper_name}_task{task['id']}",
            height=300,
            placeholder=f"Write at least {task['word_count']} words..."
        )
        
        # Show marking criteria
        with st.expander("📊 Marking Criteria"):
            st.markdown("**This task is marked on:**")
            for criterion, marks in task['marking_criteria'].items():
                st.markdown(f"- **{criterion.title()}:** {marks} marks")
            
            st.markdown("""
            **Marking Guidance:**
            - **Content:** Addresses all bullet points, appropriate detail
            - **Organisation:** Logical structure, clear paragraphs
            - **Language:** Appropriate for audience and purpose
            - **SPaG:** Spelling, Punctuation and Grammar accuracy
            """)
        
        st.markdown("---")
    
    if st.button("📥 Download Writing Paper (PDF)", key=f"download_writing_{level}_{paper_name}"):
        st.info("PDF generation coming soon! For now, you can print this page.")

def render_slc_mock(level, paper_name, slc_data):
    """Render SLC mock assessment"""
    st.markdown(f"## {slc_data['title']}")
    
    st.metric("Total Duration", f"~{slc_data['duration']} minutes")
    
    st.warning("""
    **Note:** Speaking, Listening and Communicating must be assessed by your tutor in person.
    
    These activities show you what to expect, but you'll need to complete them with an assessor.
    """)
    
    st.markdown("---")
    
    for activity in slc_data['activities']:
        st.markdown(f"### {activity['title']}")
        st.markdown(activity['prompt'])
        
        with st.expander("✅ Assessment Criteria"):
            st.markdown("**You will be assessed on:**")
            for criterion in activity['assessment_criteria']:
                st.markdown(f"- {criterion}")
        
        st.markdown("---")
    
    st.info("""
    **How to Prepare:**
    1. Read the activities carefully
    2. Make notes on what you want to say
    3. Practice with a friend or family member
    4. Book your assessment with your tutor when ready
    """)

if __name__ == "__main__":
    st.title("🎯 Mock Examinations")
    level = st.radio("Select Level:", ["Level 1", "Level 2"], horizontal=True)
    render_mock_exam_tab(level)
