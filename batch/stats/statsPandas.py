import pandas as pd

df = pd.DataFrame({
    '몸무게': [70, 80, 90, 82, 91],
    '키': [170, 181, 185, 168, 180]})

total_age = df['몸무게'].sum()
print(total_age)

mean_age = df['키'].mean()
print(mean_age)
print(df.describe())

corr = df.corr()

print(corr)