import pandas as pd

def find_avg(input_file, column_name):

    df = pd.read_csv(input_file)
    sum = df[column_name].sum()
    return sum

out = find_avg('Sample.csv','abc') 
print(out)