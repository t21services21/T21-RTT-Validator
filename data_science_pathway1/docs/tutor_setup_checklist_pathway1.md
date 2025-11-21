# Tutor Setup Checklist – Data Science Foundations (Pathway 1)

This checklist is for tutors, trainers and admins to get Pathway 1 ready for teaching and assessment.

## 1. Enrol learners on the pathway

- Ensure the course ID used by the LMS is:
  - `data_science_foundations_pathway_1`
- Use your normal course/enrolment tools to:
  - Create or confirm the course exists.
  - Enrol each learner so that progress and evidence tracking work.

## 2. Create the SQL training database (foundations.db)

This step is required **once per environment**.

1. Open PowerShell in the project root:
   - `D:\CascadeProjects\T21-RTT-Validator`
2. Run the database creation script:
   - `python .\data_science_pathway1\datasets\create_foundations_db.py`
3. Confirm that `foundations.db` now exists in `data_science_pathway1\datasets`.

Learners can then use this database in the SQL unit and notebooks.

## 3. Know where learning assets live

- **Datasets** (CSV files used in labs and projects):
  - `data_science_pathway1/datasets/`
- **SQL database script and file**:
  - Script: `data_science_pathway1/datasets/create_foundations_db.py`
  - DB file (after running script): `data_science_pathway1/datasets/foundations.db`
- **Jupyter notebooks (labs for Units 1–7)**:
  - `data_science_pathway1/notebooks/`
- **Supporting documents** (study plan, unit checklists, portfolio guide):
  - `data_science_pathway1/docs/`
- **Quiz and exam authoring files**:
  - `data_science_pathway1/assessments/`

## 4. Use in-app automation for learners

Most learner-facing actions are already automated inside the app:

- **Learning Materials tab**
  - Full reading content for Units 1–7.
  - Optional "Download theory summary as PDF" button per unit.
- **Labs & Mini Projects tab**
  - Per-unit lab ideas plus a standard lab workflow learners can follow.
- **Assessments tab**
  - Evidence submission form per unit (uses the central evidence system).
  - "Quick-check" multiple-choice quizzes for Units 1–7 with auto-marking.
- **Documents & Downloads tab**
  - One-click PDF generation for:
    - 8-week study plan.
    - Unit checklists.
    - Portfolio guide.
- **My Progress & Certificate tabs**
  - Show progress (if enrolment and tracking are configured in the LMS).
  - Explain completion requirements and certificate issuing.

## 5. Optional: upload PDFs and link resources in the main LMS

To align with your organisation’s standards you may also:

- Generate the PDFs from the app (study plan, checklists, portfolio guide) and
  upload them into your central document library.
- Attach key datasets and notebooks to the course using the LMS course/lesson
  manager so they appear in your usual learning materials interface.

## 6. Testing before going live

- Log in as a test learner and:
  - Open each tab in Pathway 1.
  - Complete at least one quick-check quiz.
  - Upload a sample evidence file.
- Confirm that progress and evidence submissions appear correctly in your
  tutor/admin views.

Once these steps are complete, Pathway 1 is ready for delivery.
