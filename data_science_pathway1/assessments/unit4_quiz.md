# Pathway 1 – Unit 4 Quiz
## SQL & Relational Databases for Analysis

Total questions: **15**  
Suggested pass mark: **12 / 15 (80%)**

---

## Section A – Multiple Choice (10 questions)

**Q1.** In a relational database, what is a **primary key**?

A. A column that allows nulls and duplicates.  
B. A column (or set of columns) that uniquely identifies each row.  
C. Any numeric column.  
D. A column that stores foreign currency values.

**Correct answer:** B

---

**Q2.** Which SQL keyword is used to **filter rows** returned by a query?

A. `SELECT`  
B. `FROM`  
C. `WHERE`  
D. `GROUP BY`

**Correct answer:** C

---

**Q3.** Which SQL clause is used to **sort** the results of a query?

A. `ORDER BY`  
B. `SORT BY`  
C. `GROUP BY`  
D. `HAVING`

**Correct answer:** A

---

**Q4.** Which type of JOIN keeps **all rows from the left table**, and only
matching rows from the right table?

A. INNER JOIN  
B. LEFT JOIN  
C. RIGHT JOIN  
D. FULL OUTER JOIN

**Correct answer:** B

---

**Q5.** What does this query compute?

```sql
SELECT country, COUNT(*) AS num_customers
FROM customers
GROUP BY country;
```

A. Total number of orders per country.  
B. Total number of customers per country.  
C. Total revenue per country.  
D. Average age per country.

**Correct answer:** B

---

**Q6.** Which aggregate function would you use to calculate **average
order value**?

A. `SUM()`  
B. `COUNT()`  
C. `AVG()`  
D. `MAX()`

**Correct answer:** C

---

**Q7.** What is wrong with this query?

```sql
SELECT country, order_value
FROM orders
GROUP BY country;
```

A. `GROUP BY` cannot be used with `country`.  
B. `order_value` is not aggregated, so the query is invalid in many SQL
   engines.  
C. The table name is incorrect.  
D. Nothing is wrong.

**Correct answer:** B

---

**Q8.** Which clause allows you to filter **after** aggregation (e.g. only
show countries with total revenue > 10000)?

A. `WHERE`  
B. `GROUP BY`  
C. `HAVING`  
D. `ORDER BY`

**Correct answer:** C

---

**Q9.** What is a **foreign key**?

A. A key used only for international customers.  
B. A column that references a primary key in another table.  
C. A key used for encryption.  
D. A key that must always be numeric.

**Correct answer:** B

---

**Q10.** Which query correctly returns the **total revenue per customer
segment** by joining `orders` and `customers`?

A.
```sql
SELECT segment, SUM(order_value) AS total_revenue
FROM orders
GROUP BY segment;
```

B.
```sql
SELECT c.segment, SUM(o.order_value) AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.segment;
```

C.
```sql
SELECT country, SUM(order_value)
FROM customers
GROUP BY country;
```

D.
```sql
SELECT * FROM orders, customers;
```

**Correct answer:** B

---

## Section B – Short Answer (5 questions)

**Q11.** Explain the difference between an **INNER JOIN** and a **LEFT
JOIN**.

**Model answer (guide):**  
An INNER JOIN keeps only rows that have matching keys in both tables. A LEFT
JOIN keeps all rows from the left table and brings in matching data from the
right, with nulls where there is no match.

---

**Q12.** Describe a real-world question in a UK or US business that could be
answered using SQL on the `orders` and `customers` tables.

**Model answer (guide):**  
For example, "What is the total revenue by customer segment and country in
the last 30 days?" using a join between orders and customers, grouped by
segment and country with a date filter.

---

**Q13.** Why is it important to understand the **grain** of a table before
writing aggregation queries?

**Model answer (guide):**  
If you do not know whether one row is an order, order line, or daily summary,
you can easily double-count or misinterpret totals when grouping or
joining.

---

**Q14.** What problem can happen if you join tables in a way that creates a
**many-to-many** relationship without realising it?

**Model answer (guide):**  
The number of rows can explode and metrics like revenue or customer counts
can be multiplied, giving misleading results.

---

**Q15.** In your own words, explain why SQL is still important for data
professionals even when they mainly work in Python.

**Model answer (guide):**  
Most organisational data lives in relational databases. SQL is the most
common way to query and prepare this data before loading it into tools like
Pandas, and many analyst/scientist roles include SQL tests in interviews.
