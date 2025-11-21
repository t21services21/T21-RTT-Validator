# Pathway 1 – Unit 2 Quiz
## Python Programming for Data

Total questions: **15**  
Suggested pass mark: **12 / 15 (80%)**

---

## Section A – Multiple Choice (10 questions)

**Q1.** Which of the following is a valid Python variable name?

A. `1variable`  
B. `total_sales`  
C. `monthly-revenue`  
D. `class`

**Correct answer:** B

---

**Q2.** What is the type of the value `True` in Python?

A. `int`  
B. `str`  
C. `bool`  
D. `list`

**Correct answer:** C

---

**Q3.** Which data structure is best suited to store **an ordered collection** of monthly revenue values?

A. `dict`  
B. `list`  
C. `set`  
D. `tuple`

**Correct answer:** B

---

**Q4.** Given the list `values = [10, 20, 30]`, which expression returns the
**second** item?

A. `values[0]`  
B. `values[1]`  
C. `values[2]`  
D. `values[-1]`

**Correct answer:** B

---

**Q5.** What does the following code print?

```python
x = 5
if x > 10:
    print("A")
else:
    print("B")
```

A. `A`  
B. `B`  
C. `AB`  
D. Nothing, it errors

**Correct answer:** B

---

**Q6.** Which keyword is used to define a **function** in Python?

A. `func`  
B. `define`  
C. `fn`  
D. `def`

**Correct answer:** D

---

**Q7.** What does the `return` statement do inside a function?

A. It stops the program completely.  
B. It prints a value and then exits the function.  
C. It sends a value back to the caller and exits the function.  
D. It automatically saves data to a file.

**Correct answer:** C

---

**Q8.** Which line correctly opens a file called `data.csv` for reading?

A. `open("data.csv")`  
B. `open("data.csv", "r")`  
C. Both A and B  
D. Neither A nor B

**Correct answer:** C

---

**Q9.** Which data type is best for representing **key–value pairs**, such as
customer ID -> country?

A. `list`  
B. `tuple`  
C. `dict`  
D. `set`

**Correct answer:** C

---

**Q10.** What is the result of the following code?

```python
values = [1, 2, 3]
values.append(4)
print(values)
```

A. `[1, 2, 3]`  
B. `[1, 2, 3, 4]`  
C. `[4, 1, 2, 3]`  
D. Error

**Correct answer:** B

---

## Section B – Short Answer (5 questions)

**Q11.** In your own words, explain the difference between a **list** and a
**dictionary** in Python.

**Model answer (guide):**  
A list is an ordered collection of values accessed by position (index). A
dictionary stores key–value pairs and is accessed by key, which is useful for
labelled data like `customer_id -> country`.

---

**Q12.** Write a small function called `percentage_change(old, new)` that
returns the percentage change from `old` to `new`.

**Model answer (guide):**

```python
def percentage_change(old, new):
    return (new - old) / old * 100
```

---

**Q13.** Give one reason why using **functions** makes your code more
professional and easier to maintain.

**Model answer (guide):**  
Functions group related logic into reusable blocks, so you only need to write
and fix the code once, and the main script becomes easier to read.

---

**Q14.** Describe a small task in a UK or US data job that could be solved
with a simple Python script.

**Model answer (guide):**  
For example, a script that reads daily sales CSV files from a folder,
combines them into one file and calculates total revenue per day.

---

**Q15.** Why is it important to use **meaningful variable names** instead of
names like `x` or `data1` in production code?

**Model answer (guide):**  
Meaningful names make the code easier to understand for you and your
colleagues, reduce mistakes, and help during code reviews and interviews.
