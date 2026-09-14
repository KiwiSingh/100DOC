import pandas as pd
df = pd.read_csv('salaries_by_college_major.csv')
clean_df = df.dropna()
median = clean_df['Mid-Career Median Salary'].max()
tenth = clean_df['Mid-Career 10th Percentile Salary'].max() 
ninety = clean_df['Mid-Career 90th Percentile Salary'].max()
highest_mid_career_salary=int(max(median, tenth, ninety))
print(f"The highest mid-career salary is ${highest_mid_career_salary}")
major_with_highest_mid_career_salary=clean_df[clean_df["Mid-Career 90th Percentile Salary"] == highest_mid_career_salary]["Undergraduate Major"].iloc[0]
print(f"The major with the highest mid-career salary is {major_with_highest_mid_career_salary}")
lowest_starting_salary_idx = clean_df['Starting Median Salary'].idxmin()
major_with_lowest_starting_salary = clean_df['Undergraduate Major'][lowest_starting_salary_idx]
print(f"The major with the lowest starting salary is {major_with_lowest_starting_salary}")
median_low=clean_df['Mid-Career Median Salary'].min()
tenth_low = clean_df['Mid-Career 10th Percentile Salary'].min()
ninety_low = clean_df['Mid-Career 90th Percentile Salary'].min()
lowest_mid_career_salary=int(min(median_low, tenth_low, ninety_low))
major_with_lowest_mid_career_salary=clean_df[clean_df["Mid-Career 10th Percentile Salary"] == lowest_mid_career_salary]["Undergraduate Major"].iloc[0]
print(f"The major with the lowest mid-career salary is {major_with_lowest_mid_career_salary}")
print(f"The lowest mid-career salary is ${lowest_mid_career_salary}")
highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
spread_col = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
clean_df.insert(1, 'Spread', spread_col)
print("The top 5 undergraduate majors with the highest earning potential are as follows:\n")
print(highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head())
highest_spread = clean_df.sort_values('Spread', ascending=False)
print("The top 5 undergraduate majors with the highest salary spread are as follows:\n")
print(highest_spread[['Undergraduate Major', 'Spread']].head())
