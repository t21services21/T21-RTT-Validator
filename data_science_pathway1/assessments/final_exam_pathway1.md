# Data Science Foundations (Pathway 1)
## Final Exam – Theory & Application

Total suggested questions: **35**  
Recommended pass mark: **26 / 35 (≈75%)**

This exam is designed to be taken **after all 7 units** and capstone work are
complete. It mixes auto-marked questions with open-ended ones.

---

## Section A – Multiple Choice & Short Numeric (20 questions)

These can be auto-marked.

### Q1–Q3: Concepts from Unit 1 (Intro & Roles)

1. Which CRISP-DM phase focuses on defining the problem and success
   criteria?
2. Which role is most responsible for building data pipelines and ETL
   processes?
3. Which statement about bias in data is most accurate?

*(See Unit 1 quiz for detailed options – reuse or adapt as needed.)*

---

### Q4–Q7: Python & Pandas Basics (Units 2–3)

4. In Python, what is the output type of `{"a": 1, "b": 2}.keys()`?  
5. Which Pandas method shows column types and non-null counts?  
6. What does the following code compute?

   ```python
   df.groupby("country")["revenue"].sum()
   ```

7. If a DataFrame has shape `(1000, 10)`, what do these numbers represent?

---

### Q8–Q11: SQL Basics (Unit 4)

8. Which SQL keyword is used to **combine rows from two tables** based on a
   related column?
9. Write the missing keyword:

   ```sql
   SELECT country, SUM(order_value) AS total_value
   FROM orders
   ______ country
   ```

10. In a `LEFT JOIN`, which table’s rows are always preserved: the left or
    the right?
11. Which constraint uniquely identifies a row within a table?

---

### Q12–Q15: Statistics & A/B Testing (Unit 5)

12. Which metric measures **spread** of a distribution: mean, median or
    standard deviation?
13. A control group has 1000 users and 80 conversions. What is the
    conversion rate (as a decimal to 2 dp)?
14. A variant group has a conversion rate of 0.10 and control is 0.08.
    What is the **absolute lift**? What is the **relative lift**?
15. In plain terms, what does a **p-value** represent in hypothesis testing?

---

### Q16–Q20: Visualisation & Ethics (Units 1, 6)

16. Which chart is best for showing a **trend over time**?  
17. Which chart is best for comparing **categories**?  
18. Name one problem with using 3D charts in dashboards.  
19. Why should axes normally start at zero for bar charts?  
20. Give one example where using a model without considering ethics could
    harm people.

---

## Section B – Applied Scenario (10 questions)

These questions use a **small integrated scenario**. Tutors can partially
auto-mark numeric parts and manually mark explanations.

### Scenario

You work as a junior data professional for a UK/US online retailer. You are
given two training datasets:

- `uk_retail_sales_clean.csv` – daily sales by store, region, category.  
- `web_ab_test_results.csv` – users in control or variant groups with a
  `converted` flag.

Answer the questions below.

21. Write a short description (2–3 sentences) of what one row represents in
    each dataset.

22. Using SQL or Pandas groupby logic, describe how you would calculate
    **total revenue per region** in the retail dataset.

23. The marketing team asks: *“Which product category is performing best in
    terms of total revenue?”*  
    - Describe the steps you would take to answer this.  
    - State which chart you would use to present the result and why.

24. In the A/B test dataset, explain how you would calculate conversion
    rates for control and variant.  
    - What numbers would you divide?  
    - Which Pandas functions could you use?

25. Suppose the variant conversion rate is slightly higher, but the sample
    size is small. Write 3–4 sentences explaining whether you would
    recommend rolling out the variant immediately.

26. You discover that some rows in the retail dataset have negative revenue.
    Give two possible reasons this might happen and how you would handle
    these rows.

27. You build a bar chart showing total revenue by region, but the axis is
    cut so that small differences look very large. Explain why this can be
    misleading to managers.

28. Write a short paragraph (4–6 sentences) summarising the key insights you
    might present to leadership from this combined analysis (retail + A/B
    test).

29. Identify one **ethical** consideration in using these datasets (for
    example, around privacy or fairness) and explain how you would address
    it.

30. Describe one way you could turn this work into a **portfolio project**
    to show employers (what files you would include and how you would
    publish them).

---

## Section C – Capstone Reflection (5 questions)

Learners should refer to their own Unit 7 capstone project.

31. In 3–5 sentences, describe the **problem** your capstone project tried
    to solve.

32. What were the **main data sources** you used, and what did one row
    represent in your final dataset?

33. List at least three **techniques** you used (e.g. grouping, joins,
    visualisation, simple modelling) and explain briefly why you chose
    them.

34. What was one **limitation** of your capstone project, and how would you
    improve it if you had more time or data?

35. In 3–5 sentences, explain how this project shows you are ready for an
    entry-level data role in your preferred country and sector.
