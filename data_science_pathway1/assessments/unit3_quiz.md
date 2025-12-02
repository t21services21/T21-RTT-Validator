# Pathway 1 – Unit 3 Quiz
## Working with Data using Pandas & NumPy

Total questions: **15**  
Suggested pass mark: **12 / 15 (80%)**

---

## Section A – Multiple Choice (10 questions)

**Q1.** In Pandas, which object type is used to represent a table of data
with rows and columns?

A. `Series`  
B. `DataFrame`  
C. `Panel`  
D. `Array`

**Correct answer:** B

---

**Q2.** Which method shows the **first few rows** of a DataFrame?

A. `df.tail()`  
B. `df.head()`  
C. `df.sample()`  
D. `df.info()`

**Correct answer:** B

---

**Q3.** Which method shows the **column types** and non-null counts?

A. `df.describe()`  
B. `df.dtypes`  
C. `df.info()`  
D. `df.columns`

**Correct answer:** C

---

**Q4.** Which code selects the `sales_amount` column from a DataFrame `df`?

A. `df.sales_amount`  
B. `df["sales_amount"]`  
C. Both A and B  
D. Neither A nor B

**Correct answer:** C

---

**Q5.** What does this code do?

```python
df["revenue_per_tx"] = df["sales_amount"] / df["transactions"]
```

A. Deletes the `sales_amount` column.  
B. Creates a new column with a ratio of sales to transactions.  
C. Sorts the DataFrame.  
D. Filters rows with missing values.

**Correct answer:** B

---

**Q6.** Which code removes rows with **any missing values**?

A. `df.dropna()`  
B. `df.fillna(0)`  
C. `df.isna()`  
D. `df.drop_duplicates()`

**Correct answer:** A

---

**Q7.** What does the following code compute?

```python
df.groupby("region")["sales_amount"].sum()
```

A. Total sales per region.  
B. Average sales per region.  
C. Number of rows per region.  
D. Maximum sales per region.

**Correct answer:** A

---

**Q8.** Which Pandas function is typically used to **join** two tables on a
key column?

A. `pd.concat()`  
B. `pd.merge()`  
C. `df.join()` only  
D. `df.groupby()`

**Correct answer:** B (or `df.join`, but here we emphasise `pd.merge`).

---

**Q9.** What is the main advantage of using **vectorised operations** in
Pandas/NumPy instead of Python `for` loops over rows?

A. They always use less memory.  
B. They are usually faster and the code is shorter and clearer.  
C. They make debugging much easier.  
D. They automatically prevent all errors.

**Correct answer:** B

---

**Q10.** Which code converts a column `date` to a proper datetime type?

A. `df["date"] = pd.to_datetime(df["date"])`  
B. `df["date"] = df["date"].astype(int)`  
C. `df["date"] = df["date"].astype(str)`  
D. `df["date"] = df["date"].to_date()`

**Correct answer:** A

---

## Section B – Short Answer (5 questions)

**Q11.** Why is it important to check for **duplicates** and **missing
values** before doing analysis?

**Model answer (guide):**  
Duplicates can lead to double-counting and inflated metrics. Missing values
can distort averages and other statistics if not handled properly, leading to
incorrect conclusions.

---

**Q12.** Describe, in steps, how you would calculate **total sales by
product category** in a UK retail dataset using Pandas.

**Model answer (guide):**  
Load the CSV into a DataFrame, check column names, then use
`groupby("product_category")["sales_amount"].sum()` and reset the index or
convert to a new DataFrame for reporting.

---

**Q13.** Give one example of a new feature you could create from existing
columns in a retail dataset and why it might be useful.

**Model answer (guide):**  
Create `average_sale_per_transaction` by dividing sales by transactions to
compare store performance more fairly.

---

**Q14.** Explain what is meant by the **grain** of a table.

**Model answer (guide):**  
The grain describes what one row represents (e.g. one order, one line item,
one day per store). Understanding it helps avoid double-counting when
joining or aggregating.

---

**Q15.** Describe one real-world UK or US use case where good data cleaning
with Pandas is essential before reporting results.

**Model answer (guide):**  
For example, cleaning hospital appointment records before reporting waiting
times, or cleaning e-commerce order data before calculating conversion and
revenue by marketing channel.
