import pandas as pd

def extract_unique_values(input_file, column_name, output_file):

    df = pd.read_csv(input_file)
    unique_values = df[column_name].unique()
    pd.DataFrame (unique_values, columns=[column_name]).to_csv(output_file, index=False)

extract_unique_values('Sample.csv','abc','out.csv')




    