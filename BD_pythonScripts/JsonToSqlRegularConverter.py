import json
import uuid
import csv
import os

genders = ["male" , "female"]
file_path = '../DataSets/test.json'  # Path to your JSON file containing entrys

class GeoHMap:
    def __init__(self):
        self.map = {}
        self.counter = 10

    def get_or_allocate(self, pair):
        # Convert the list to a tuple to use as a dictionary key
        key = tuple(pair)
        
        if key in self.map:
            # If the pair already exists, return the associated number
            return self.map[key]
        else:
            # If the pair does not exist, allocate the next number
            self.map[key] = self.counter
            self.counter += 1
            return self.map[key]

class AuthorHMap:
    def __init__(self):
        self.map = {}

    def get_or_allocate(self, number, touple):

        key = number
        
        if key in self.map:
            # If the pair already exists, return the associated touple
            return self.map[key]
        else:
            # If the pair does not exist, allocate the next touple
            self.map[key] = touple
            return -1

class WordsHmap:
    def __init__(self):
        self.map = {}
        self.counter = 1000000

    def get_or_allocate(self, word):
        key = word
        
        if key in self.map:
            # If the pair already exists, return the associated number
            return self.map[key]
        else:
            # If the pair does not exist, allocate the next number
            self.map[key] = self.counter
            self.counter += 1
            return self.map[key]

geomap = GeoHMap()
words = WordsHmap()
authorsmap = AuthorHMap()

def read_json_entries(file_path):

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Parse each line as a JSON object
                entry = json.loads(line.strip())
                
                # Process the entry (write to CSV in this example)
                check_genders(entry)
                print_entry(entry)

                
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def write_genders_to_csv():
    with open('output_csv/genders.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "type"
        ])
        writer.writerow([
            1,
            "male"
        ])
        writer.writerow([
            2,
            "female"
        ])

def write_geolocations_to_csv():
    with open('output_csv/geo_location.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "X",
            "Y"
        ])
        for key, value in geomap.map.items():
            X = key[0]
            Y = key[1]
            writer.writerow([
            value,
            X,
            Y
            ])

def write_words_to_csv():
     with open('output_csv/words.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "word"
        ])
        for key, value in words.map.items():
            writer.writerow([
            value,
            key
            ])

def write_authors_to_csv():
     with open('output_csv/authors.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id_gender",
            "id",
            "firstname",
            "lastname",
            "age"
        ])
        for key, value in authorsmap.map.items():
            [id_gender, age] = value
            writer.writerow([
            id_gender,
            key,
            "",
            "",
            age
            ])

def check_genders(entry):
    if entry.get('gender') == "male" :
        return
    if entry.get('gender') == "female" :
        return
    print("we have a 3'd gender ")


def print_entry(entry):
    # documents CSV:
    geoID = geomap.get_or_allocate(entry.get('geoLocation'))
    date = entry.get('date')
    id_data = entry.get('_id')

    datetime = date['$date']
    formatted_datetime = datetime.replace('T', ' ').replace('Z', '')

    with open('output_csv/documents.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                int(id_data['$numberLong']),
                geoID,
                entry.get('rawText'),
                entry.get('lemmaText'),
                entry.get('cleanText'),
                formatted_datetime
            ])

    # documents_authors CSV:

    author_data = entry.get('author')
    author_id = -1
    if isinstance(author_data, dict) and '$numberLong' in author_data:
        # Extract the number from the dictionary
        author_id = int(author_data['$numberLong'])
    else:
        # Assume it's already an integer
        author_id = int(author_data)

    age = int(entry.get('age'))
    if entry.get('gender') == "male" :
        id_gender = 1
    else : 
        id_gender = 2
    
    # Add the next element in the hashmap if i don't already have the author
    if authorsmap.get_or_allocate(author_id, [id_gender, age]) == -1 : 
        with open('output_csv/documents_authors.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                author_id,
                int(id_data['$numberLong'])
            ])
    else :
        with open('output_csv/documents_authors.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                author_id,
                int(id_data['$numberLong'])
            ])
    

    # words and vocabulary CSV:

    word_list = entry.get('words')
    for word in word_list :
        words.get_or_allocate(word['word'])
        with open('output_csv/vocabulary.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                int(id_data['$numberLong']),
                words.get_or_allocate(word['word']),
                word['count'],
                word['tf']
            ])
 
os.makedirs('output_csv', exist_ok=True)
with open('output_csv/documents.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "id_geo_loc",
            "raw_text",
            "lemmaText",
            "cleanText",
            "document_date"
        ])
with open('output_csv/vocabulary.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "id_document",
                "id_word",
                "count",
                "tf"
            ])
with open('output_csv/documents_authors.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "id_author",
                "id_document"
            ])
write_genders_to_csv()

read_json_entries(file_path)
write_geolocations_to_csv()
write_words_to_csv()
write_authors_to_csv()
