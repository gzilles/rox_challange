# External libraries
import pandas as pd

# Count how many bytes per column 
df = pd.read_csv('csv_files/Production.Product.csv', sep=';')

for i in df.columns:
    max = 0
    for value in df[i]:
        if len(str(value)) >= max:
            max = len(str(value))
    print(f'{i} ({max}),')