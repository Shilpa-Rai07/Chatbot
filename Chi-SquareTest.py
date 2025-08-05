import pandas as pd
from scipy.stats import chi2_contingency, chi2

df = pd.read_csv('student_results.csv')

print("=== Raw Data ===")
print(df)

contingency_table = pd.crosstab(df['Attendance'], df['Result'])

print("\n=== Contingency Table ===")
print(contingency_table)

chi2_stat, p_val, dof, expected = chi2_contingency(contingency_table)

print("\n=== Test Results ===")
print("Chi-Square Statistic:", chi2_stat)
print("Degrees of Freedom:", dof)
print("P-Value:", p_val)

expected_df = pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)
print("\n=== Expected Frequencies ===")
print(expected_df)

alpha = 0.05
critical_value = chi2.ppf(1 - alpha, dof)
print("\nCritical Value at α = 0.05:", critical_value)

print("\n=== Conclusion ===")
if chi2_stat > critical_value:
    print("Reject the null hypothesis.")
    print("There is a significant relationship between Attendance and Result.")
else:
    print("Fail to reject the null hypothesis.")
    print("There is no significant relationship between Attendance and Result.")
