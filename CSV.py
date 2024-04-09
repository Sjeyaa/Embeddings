import pandas as pd
from gensim.models import Word2Vec

# Load your dataset
df = pd.read_csv('d3.csv')

# Assuming your text data is in column 2 (index 1), column 3 (index 2), and column 4 (index 3)
text_data = df.iloc[:, 1:4].values.flatten().tolist()

# Tokenize your text data (you can use any tokenizer suitable for your dataset)
tokenized_data = [text.split() for text in text_data]

# Train Word2Vec model
model = Word2Vec(sentences=tokenized_data, vector_size=5, window=5, min_count=1, workers=4)

# Function to get embeddings for a given text
def get_embeddings(text):
    words = text.split()
    embeddings = [model.wv[word] for word in words if word in model.wv]
    if embeddings:
        return sum(embeddings) / len(embeddings)  # Average of word embeddings
    else:
        return [0] * model.vector_size  # return zero vector if no embeddings found

# Apply the function to each row of the dataframe
df['embeddings'] = df.apply(lambda row: get_embeddings(row[1] + ' ' + row[2] + ' ' + row[3]), axis=1)

# Display the dataframe with the original columns and embeddings
print(df[['Column2', 'Column3', 'Column4', 'embeddings']])

# Save the dataframe to a new CSV file
df.to_csv('embedded_data.csv', index=False)


import pandas as pd

def get_csv_column_info(file_path, search_value):
    try:
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        result = []

        # Iterate over each row
        for index, row in df.iterrows():
            # Check if the search value is present in the row
            if search_value in row.values:
                # If found, store the row data along with column names
                row_data = {}
                for col in df.columns:
                    row_data[col] = row[col]
                result.append(row_data)

        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
file_path = "embedded_data.csv"  # Replace with your CSV file path
search_value = input("Enter the search value: ")  # Prompt the user to enter the search value
column_info = get_csv_column_info(file_path, search_value)
if column_info:
    for row in column_info:
        print(row)
