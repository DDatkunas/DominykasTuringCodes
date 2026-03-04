import pandas as pd
import numpy as np

# Merging datasets: Employee data and department budget data (merging on Department)
employees = pd.DataFrame({
    'EmployeeID': [101, 102, 103, 104],
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Department': ['Sales', 'IT', 'HR', 'Sales']
})

budgets = pd.DataFrame({
    'Department': ['Sales', 'IT', 'HR'],
    'Annual_Budget': [250000, 300000, 150000]
})

merged = pd.merge(employees, budgets, on='Department', how='left')
print("Merged employee and budget data:\n", merged)

# Select departments with high budget
employees["Department"] = employees["Department"].astype("category")
high_budget = merged.query("Annual_Budget > 200000")
print("\nDepartments with high budget:\n", high_budget)

# Concatenating datasets: Combining employee logs (Concatenate vertically)
jan_logs = pd.DataFrame({
    'EmployeeID': [101, 102],
    'LoginDate': ['2023-01-15', '2023-01-20'],
    'HoursWorked': [8, 7]
})

feb_logs = pd.DataFrame({
    'EmployeeID': [101, 103],
    'LoginDate': ['2023-02-12', '2023-02-18'],
    'HoursWorked': [9, 6]
})

logs = pd.concat([jan_logs, feb_logs], ignore_index=True)
logs['LoginDate'] = pd.to_datetime(logs['LoginDate'])
print("\nCombined login logs:\n", logs)

# Pivot table: Total hours worked by employee and month
logs['Month'] = logs['LoginDate'].dt.to_period('M')
pivot = logs.pivot_table(index='EmployeeID', columns='Month', values='HoursWorked', aggfunc='sum', fill_value=0)
print("\nPivot table of hours worked:\n", pivot)

# Time Series: Resample login data monthly
monthly_summary = logs.set_index('LoginDate').resample('ME')['HoursWorked'].sum()
print("\nMonthly total hours worked:\n", monthly_summary)