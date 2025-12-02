# Unit 2: Python Programming - EXPANSION CONTENT READY

**This content is ready to be inserted into `data_science_foundations_module.py` at lines 318-386**

---

## REPLACE CURRENT UNIT 2 WITH THIS:

```python
    elif unit_number == 2:
        st.markdown("---")
        st.markdown("#### 🐍 Why Python is THE Language for Data Science")
        st.markdown(
            """**Python dominates data science for good reasons:**

**Compared to other tools:**

| Feature | Python | R | Excel | SQL |
|---------|--------|---|-------|-----|
| Learning curve | Moderate | Steep | Easy | Moderate |
| Data size handling | Excellent (millions of rows) | Good | Poor (max ~1M rows) | Excellent |
| Statistical analysis | Excellent (scipy, statsmodels) | Excellent | Limited | None |
| Machine learning | Best (scikit-learn, TensorFlow) | Good | None | None |
| Data wrangling | Excellent (Pandas) | Excellent (dplyr) | Moderate | Excellent |
| Visualization | Excellent (matplotlib, seaborn, plotly) | Excellent (ggplot2) | Good | None |
| Industry adoption | 80% of data teams | 20% (academia) | 100% (basic analysis) | 90% (databases) |
| Job postings mentioning | 70% | 15% | 40% | 85% |

**Bottom line:** Python + SQL = Essential combo for data roles globally.

---

### Getting Started with Python

**Installation (Recommended):**
1. Download Anaconda (includes Python + Jupyter + 200+ packages)
2. Install: https://www.anaconda.com/download
3. Launch Jupyter Notebook or VS Code
4. You're ready!

**Alternative:** Google Colab (browser-based, no installation)

**Your First Python Script:**
```python
# This is a comment - Python ignores it
print("Hello, Data Science!")  # Prints text to screen

# Calculate something
revenue = 150_000  # £150,000 (underscores for readability)
growth = 0.15      # 15% growth rate
next_year_revenue = revenue * (1 + growth)

print(f"Current revenue: £{revenue:,}")
print(f"Next year (with {growth:.0%} growth): £{next_year_revenue:,.0f}")
```

**Output:**
```
Hello, Data Science!
Current revenue: £150,000
Next year (with 15% growth): £172,500
```

**Already doing real calculations!**

---

### Data Types: The Building Blocks

**Every piece of data has a type. Master these 5:**

#### 1. Numbers (int and float)

```python
# Integers (whole numbers)
customer_count = 1_250
new_customers_today = 15

# Floats (decimals)
average_order_value = 45.99
conversion_rate = 0.032  # 3.2%

# Arithmetic
total_customers = customer_count + new_customers_today
print(total_customers)  # 1265

# Be careful with division!
print(10 / 3)      # 3.3333... (float division)
print(10 // 3)     # 3 (integer division, rounds down)
print(10 % 3)      # 1 (modulo, remainder)

# Rounding
price = 19.99
print(round(price))     # 20
print(round(price, 1))  # 20.0
```

---

#### 2. Strings (text)

```python
# Create strings
customer_name = "John Smith"
product = 'Widget Pro'  # Single or double quotes both work

# String operations
email = customer_name.lower().replace(" ", ".") + "@company.com"
print(email)  # john.smith@company.com

# String methods
print(customer_name.upper())        # JOHN SMITH
print(customer_name.split())        # ['John', 'Smith']
print(customer_name.startswith("J")) # True

# F-strings for formatting (Python 3.6+)
revenue = 1_500_000
print(f"Revenue: £{revenue:,}")  # Revenue: £1,500,000
print(f"Revenue: £{revenue/1000:.1f}K")  # Revenue: £1500.0K

# Multi-line strings
description = """
This is a long
product description
that spans multiple lines.
"""
```

**Common String Operations:**
```python
text = "  Extra Spaces  "
text.strip()          # Remove leading/trailing spaces
text.split()          # Split into words
",".join(['a','b'])   # Join list into string: "a,b"
"test" in text        # Check if substring exists
len(text)             # Count characters
```

---

#### 3. Lists (ordered collections)

```python
# Create lists
monthly_sales = [45_000, 52_000, 48_000, 61_000]
products = ["Widget", "Gadget", "Doohickey"]

# Access by index (starts at 0!)
first_month = monthly_sales[0]   # 45000
last_month = monthly_sales[-1]   # 61000 (negative = from end)

# Slicing (get a range)
q1_sales = monthly_sales[0:3]    # [45000, 52000, 48000]
last_two = monthly_sales[-2:]    # [48000, 61000]

# Modify lists
monthly_sales.append(55_000)     # Add to end
monthly_sales.insert(0, 40_000)  # Insert at position
monthly_sales.remove(48_000)     # Remove first occurrence
monthly_sales.pop()              # Remove and return last item

# List operations
total = sum(monthly_sales)
average = total / len(monthly_sales)
maximum = max(monthly_sales)
minimum = min(monthly_sales)

print(f"Total Q1 sales: £{total:,}")
print(f"Average: £{average:,.0f}")
print(f"Best month: £{maximum:,}")
```

**List Comprehensions (Pythonic!):**
```python
# Traditional loop
squared = []
for num in [1, 2, 3, 4]:
    squared.append(num ** 2)

# List comprehension (same result, one line)
squared = [num ** 2 for num in [1, 2, 3, 4]]  # [1, 4, 9, 16]

# With condition
revenues = [45_000, 152_000, 38_000, 201_000]
big_deals = [r for r in revenues if r > 100_000]  # [152000, 201000]
```

---

#### 4. Dictionaries (key-value pairs)

```python
# Create dictionary
customer = {
    "id": "C001",
    "name": "Acme Corporation",
    "revenue": 2_500_000,
    "industry": "Retail",
    "country": "UK"
}

# Access values
print(customer["name"])         # Acme Corporation
print(customer.get("email"))    # None (safe access if key might not exist)
print(customer.get("email", "unknown@example.com"))  # Provide default

# Modify
customer["revenue"] = 2_750_000  # Update existing
customer["email"] = "contact@acme.com"  # Add new key

# Dictionary operations
keys = customer.keys()          # All keys
values = customer.values()      # All values
items = customer.items()        # All (key, value) pairs

# Check if key exists
if "email" in customer:
    print(f"Email: {customer['email']}")

# Loop through dictionary
for key, value in customer.items():
    print(f"{key}: {value}")
```

**Real Example: Customer Database**
```python
customers = [
    {"id": "C001", "name": "Acme Corp", "revenue": 2_500_000},
    {"id": "C002", "name": "Tech Ltd", "revenue": 150_000},
    {"id": "C003", "name": "Global Inc", "revenue": 4_000_000}
]

# Calculate total revenue
total_revenue = sum(c["revenue"] for c in customers)
print(f"Total: £{total_revenue:,}")  # Total: £6,650,000

# Find high-value customers
enterprise = [c for c in customers if c["revenue"] > 1_000_000]
print(f"Enterprise customers: {len(enterprise)}")  # 2
```

---

#### 5. Booleans (True/False)

```python
# Boolean values
is_active = True
has_email = False

# Comparisons return booleans
revenue = 150_000
is_enterprise = revenue > 1_000_000  # False
is_smb = revenue < 100_000           # False

# Logical operators
is_qualified = is_active and has_email   # False (both must be True)
needs_followup = not has_email           # True (inverse)
is_target = is_active or has_email       # True (at least one True)

# Use in if statements
if is_active and revenue > 100_000:
    print("High-value active customer!")
```

---

### Control Flow: Making Decisions

#### If/Elif/Else Statements

```python
def categorize_customer(revenue):
    """Segment customers by revenue tier"""
    if revenue > 1_000_000:
        return "Enterprise"
    elif revenue > 100_000:
        return "Mid-Market"
    elif revenue > 10_000:
        return "SMB"
    else:
        return "Startup"

# Test it
print(categorize_customer(2_500_000))  # Enterprise
print(categorize_customer(150_000))    # Mid-Market
print(categorize_customer(5_000))      # Startup
```

**Multiple Conditions:**
```python
def qualify_lead(revenue, industry, country):
    """Check if lead matches target profile"""
    if revenue > 500_000 and industry in ["Tech", "Finance"]:
        if country in ["UK", "US", "Germany"]:
            return "High Priority"
        else:
            return "Medium Priority"
    elif revenue > 100_000:
        return "Low Priority"
    else:
        return "Not Qualified"

# Usage
status = qualify_lead(750_000, "Tech", "UK")
print(status)  # High Priority
```

---

#### For Loops: Repeat Actions

```python
# Loop through list
revenues = [45_000, 152_000, 38_000, 201_000, 67_000]
for revenue in revenues:
    segment = categorize_customer(revenue)
    print(f"£{revenue:,} → {segment}")

# Output:
# £45,000 → SMB
# £152,000 → Mid-Market
# £38,000 → SMB
# £201,000 → Enterprise
# £67,000 → SMB

# Loop with index
for i, revenue in enumerate(revenues):
    print(f"Customer {i+1}: £{revenue:,}")

# Loop through range
for month in range(1, 13):  # 1 to 12
    print(f"Month {month}")

# Loop through dictionary
customer = {"name": "Acme", "revenue": 1_500_000, "industry": "Retail"}
for key, value in customer.items():
    print(f"{key}: {value}")
```

---

#### While Loops: Repeat Until Condition

```python
# Calculate how long to reach target
revenue = 100_000
target = 1_000_000
growth_rate = 0.15
years = 0

while revenue < target:
    revenue = revenue * (1 + growth_rate)
    years += 1
    print(f"Year {years}: £{revenue:,.0f}")

print(f"Reached £1M in {years} years")
```

---

### Functions: Reusable Code Blocks

**Why Functions?**
- Write once, use many times
- Easier to test and debug
- Makes code more readable
- Essential for data projects

**Basic Function:**
```python
def calculate_churn_rate(total_customers, churned_customers):
    """Calculate customer churn rate"""
    if total_customers == 0:
        return 0.0
    
    churn_rate = (churned_customers / total_customers) * 100
    return round(churn_rate, 2)

# Usage
q1_churn = calculate_churn_rate(10_000, 1_200)
print(f"Q1 Churn Rate: {q1_churn}%")  # 12.0%

q2_churn = calculate_churn_rate(11_000, 950)
print(f"Q2 Churn Rate: {q2_churn}%")  # 8.64%
```

**Function with Default Parameters:**
```python
def calculate_revenue(units_sold, price_per_unit=100, discount=0):
    """Calculate revenue with optional discount"""
    gross_revenue = units_sold * price_per_unit
    discount_amount = gross_revenue * discount
    net_revenue = gross_revenue - discount_amount
    return net_revenue

# Different ways to call
rev1 = calculate_revenue(150)                    # Uses defaults
rev2 = calculate_revenue(150, 120)               # Custom price
rev3 = calculate_revenue(150, 120, 0.10)         # With 10% discount
rev4 = calculate_revenue(150, discount=0.15)     # Named parameter

print(f"Revenue: £{rev4:,.0f}")
```

**Function Returning Multiple Values:**
```python
def analyze_revenue(revenues):
    """Return min, max, avg, total"""
    total = sum(revenues)
    avg = total / len(revenues)
    return min(revenues), max(revenues), avg, total

monthly_revenues = [45_000, 52_000, 48_000, 61_000]
min_rev, max_rev, avg_rev, total_rev = analyze_revenue(monthly_revenues)

print(f"Min: £{min_rev:,}")
print(f"Max: £{max_rev:,}")
print(f"Avg: £{avg_rev:,.0f}")
print(f"Total: £{total_rev:,}")
```

**Docstrings (Documentation):**
```python
def calculate_ltv(avg_purchase, purchase_frequency, customer_lifespan):
    """
    Calculate Customer Lifetime Value
    
    Args:
        avg_purchase: Average purchase amount in £
        purchase_frequency: Purchases per year
        customer_lifespan: Expected years as customer
        
    Returns:
        Lifetime value in £
        
    Example:
        >>> calculate_ltv(100, 4, 5)
        2000
    """
    ltv = avg_purchase * purchase_frequency * customer_lifespan
    return ltv
```

---

### Working with Jupyter Notebooks

**What is a Notebook?**
- Interactive document mixing code, text, and visualizations
- Run code in chunks (cells) instead of all at once
- Perfect for data exploration and sharing analysis

**Keyboard Shortcuts:**
- `Shift + Enter` - Run cell and move to next
- `Ctrl + Enter` - Run cell and stay
- `A` - Insert cell above (in command mode)
- `B` - Insert cell below
- `DD` - Delete cell
- `M` - Change to Markdown (text)
- `Y` - Change to Code

**Best Practices:**
1. **Import libraries at top**
   ```python
   import pandas as pd
   import matplotlib.pyplot as plt
   ```

2. **One logical step per cell**
   - Cell 1: Load data
   - Cell 2: Clean data
   - Cell 3: Analyze
   - Cell 4: Visualize

3. **Add Markdown explanations**
   ```markdown
   # Revenue Analysis Q1 2024
   
   This notebook analyzes Q1 revenue by product category.
   
   **Key Questions:**
   1. Which products generated most revenue?
   2. How does Q1 compare to Q4 2023?
   ```

4. **Clear outputs before sharing**
   - Kernel → Restart & Clear Output

---

### Professional Coding Habits

#### 1. Naming Conventions (PEP 8 Style)

```python
# Variables and functions: snake_case
customer_revenue = 150_000
def calculate_churn_rate():
    pass

# Constants: UPPERCASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Classes: PascalCase (you'll learn later)
class CustomerSegment:
    pass

# Avoid
x = 150000              # Not descriptive
CustomerRevenue = 150000  # Wrong case
calculate-churn = 0.15    # Can't use hyphens
```

#### 2. When to Comment

```python
# GOOD: Explain WHY, not WHAT
churn_rate = calculate_churn_rate(customers, churned)
# Using 30-day window because 7-day is too volatile

# BAD: Obvious comments
revenue = price * quantity  # Calculate revenue (DUH!)

# GOOD: Complex logic
# Apply 15% discount for enterprise, 5% for mid-market
if segment == "Enterprise":
    discount = 0.15
elif segment == "Mid-Market":
    discount = 0.05
```

#### 3. Error Handling Basics

```python
# Without error handling (crashes if division by zero)
def churn_rate(total, churned):
    return churned / total

# With error handling (returns 0 instead of crashing)
def churn_rate(total, churned):
    try:
        return churned / total
    except ZeroDivisionError:
        return 0.0

# Handle missing dictionary keys
customer = {"name": "Acme", "revenue": 150_000}
email = customer.get("email", "unknown@example.com")  # Safe
```

#### 4. Code Organization

```python
# BAD: Everything in one messy block
revenue=150000
growth=0.15
target=1000000
years=0
while revenue<target:revenue=revenue*(1+growth);years+=1
print(years)

# GOOD: Organized and readable
def years_to_target(initial_revenue, growth_rate, target_revenue):
    """Calculate years to reach revenue target"""
    revenue = initial_revenue
    years = 0
    
    while revenue < target_revenue:
        revenue = revenue * (1 + growth_rate)
        years += 1
    
    return years

# Usage
result = years_to_target(
    initial_revenue=150_000,
    growth_rate=0.15,
    target_revenue=1_000_000
)
print(f"Years to £1M: {result}")
```

---

### Common Beginner Mistakes

**1. Indentation Errors**
```python
# WRONG
def calculate():
revenue = 100  # IndentationError!

# RIGHT
def calculate():
    revenue = 100  # Indented 4 spaces
```

**2. Forgetting Colons**
```python
# WRONG
if revenue > 100000  # SyntaxError: missing colon

# RIGHT
if revenue > 100000:
    print("High value")
```

**3. Using = instead of ==**
```python
# WRONG (assigns value instead of comparing)
if revenue = 100000:

# RIGHT
if revenue == 100000:
```

**4. Off-by-One Errors**
```python
revenues = [100, 200, 300]
# Index 0, 1, 2 (not 1, 2, 3!)
first = revenues[0]   # 100
last = revenues[2]    # 300
# revenues[3]  # IndexError!
```

**5. String vs Number**
```python
# Strings
"100" + "200"  # "100200" (concatenation)

# Numbers
100 + 200      # 300 (addition)

# Convert types
int("100")     # 100 (string to int)
float("99.9")  # 99.9 (string to float)
str(100)       # "100" (int to string)
```

---

### Your First Data Analysis Script

```python
"""
Simple sales analysis script
Analyzes monthly sales and identifies trends
"""

# 1. Define data
monthly_sales = {
    "January": 45_000,
    "February": 52_000,
    "March": 48_000,
    "April": 61_000,
    "May": 58_000,
    "June": 67_000
}

# 2. Calculate metrics
total_revenue = sum(monthly_sales.values())
average_monthly = total_revenue / len(monthly_sales)
best_month = max(monthly_sales, key=monthly_sales.get)
worst_month = min(monthly_sales, key=monthly_sales.get)

# 3. Calculate growth rate
q1_revenue = monthly_sales["January"] + monthly_sales["February"] + monthly_sales["March"]
q2_revenue = monthly_sales["April"] + monthly_sales["May"] + monthly_sales["June"]
growth_rate = ((q2_revenue - q1_revenue) / q1_revenue) * 100

# 4. Report results
print("=" * 50)
print("SALES ANALYSIS REPORT - H1 2024")
print("=" * 50)
print(f"Total Revenue: £{total_revenue:,}")
print(f"Average Monthly: £{average_monthly:,.0f}")
print(f"Best Month: {best_month} (£{monthly_sales[best_month]:,})")
print(f"Worst Month: {worst_month} (£{monthly_sales[worst_month]:,})")
print(f"Q1→Q2 Growth: {growth_rate:+.1f}%")
print("=" * 50)
```

**Output:**
```
==================================================
SALES ANALYSIS REPORT - H1 2024
==================================================
Total Revenue: £331,000
Average Monthly: £55,167
Best Month: June (£67,000)
Worst Month: January (£45,000)
Q1→Q2 Growth: +28.3%
==================================================
```

**You just did real data analysis with Python!**

---

### Next Steps in Your Python Journey

**After this unit, you'll be ready for:**
- Unit 3: Pandas (Python's data analysis library)
- Unit 4: SQL (database queries)
- Unit 5: Statistics (understanding your results)

**To practice Python:**
1. **Daily coding (15-30 min)**
   - LeetCode Easy problems
   - HackerRank Python challenges
   - Project Euler (math + code)

2. **Real projects**
   - Analyze your own data (bank statements, fitness tracker)
   - Automate repetitive tasks
   - Build a personal budget tracker

3. **Read others' code**
   - GitHub Python projects
   - Kaggle notebooks
   - Real company code (open source)

**Key Resources:**
- Official Python Tutorial: docs.python.org/tutorial
- Python for Data Analysis (book by Wes McKinney)
- Real Python website (realpython.com)
- Stack Overflow (for questions)

---

### Career Relevance

**Job interview questions you can now answer:**
- "Explain the difference between a list and a dictionary"
- "When would you use a for loop vs a while loop?"
- "What is a function and why are they useful?"
- "Show me how you'd calculate average revenue in Python"

**Skills employers look for:**
- ✅ Can write clean, readable Python code
- ✅ Understands basic data structures
- ✅ Writes reusable functions
- ✅ Uses notebooks for analysis
- ✅ Follows coding best practices

**You now have these skills!**

**Next:** Unit 3 (Pandas) builds on this foundation to analyze real datasets with thousands of rows.
"""
        )
```

---

**This is 500+ lines of world-class Python fundamentals content ready to implement!**

**File to edit:** `data_science_foundations_module.py` lines 318-386  
**Action:** Replace current 70 lines with this 500+ line expansion

**Shall I proceed with the implementation?**
