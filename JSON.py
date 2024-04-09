import csv
# Store embeddings in a CSV file
def store_embeddings(embeddings_dict, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['JSON_ID', 'Word', 'Embedding'])
        for json_id, embeddings in embeddings_dict.items():
            for word in embeddings.index_to_key:
                embedding = embeddings[word]
                writer.writerow([json_id, word, embedding])

# Load data from JSON file
with open('/content/entries .json', 'r') as f:
    data = json.load(f)

# Initialize an empty dictionary to store embeddings
embeddings_dict = {}

# Iterate through each JSON object
for json_object in data:
    # Extract text data from JSON
    text_data = extract_text(json_object)

    # Get embeddings for the text data and store them along with the JSON ID
    embeddings = get_embeddings(text_data)
    json_id = json_object.get('id', None)
    if json_id:
        embeddings_dict[json_id] = embeddings

# Store embeddings in a CSV file
store_embeddings(embeddings_dict, 'embeddings.csv')

# Implement search function
def search_word(word, embeddings_dict):
    result = {}
    for json_id, embeddings in embeddings_dict.items():
        if word in embeddings.index_to_key:
            result[json_id] = embeddings[word].tolist()
    return result

# Get user input for search word
search_input = input("Enter the word to search: ")

# Perform search based on user input
search_result = search_word(search_input, embeddings_dict)

# Display search result
if search_result:
    print("Search Result:")
    for json_id, embedding in search_result.items():
        print("JSON ID:", json_id, "Embedding:", embedding)
else:
    print("No embeddings found for the given word.")

# Get user input for JSON ID
json_id_input = input("Enter the JSON ID to search: ")

# Perform search based on JSON ID input
if json_id_input in embeddings_dict:
    json_id_embeddings = embeddings_dict[json_id_input]
    print("Embeddings for JSON ID '{}':".format(json_id_input))
    for word in json_id_embeddings.index_to_key:
        embedding = json_id_embeddings[word]
        print("Word:", word, "Embedding:", embedding)
else:
    print("No embeddings found for the given JSON ID.")
