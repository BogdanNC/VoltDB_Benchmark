import json
import uuid
import csv
import os

file_path = '../DataSets/test.json'  # Path to your JSON file containing entrys

class TimeHMap:
    def __init__(self):
        self.map = {}
        self.counter = 10000

    def get_or_allocate(self, date):
        
        # Convert the list to a tuple to use as a dictionary key
        key = date['$date']
        
        if key in self.map:
            # If the pair already exists, return the associated number
            return self.map[key]
        else:
            # If the pair does not exist, allocate the next number
            self.map[key] = self.counter
            self.counter += 1
            return self.map[key]

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
            return self.map[key]

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
timemap = TimeHMap()

def read_json_entries(file_path):

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Parse each line as a JSON object
                entry = json.loads(line.strip())
                
                # Process the entry (write to CSV in this example)
                print_entry(entry)

                
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def write_geolocations_to_csv():
    with open('output_csv_star/location_dimension.csv', mode='w', newline='') as file:
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
     with open('output_csv_star/word_dimension.csv', mode='w', newline='') as file:
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
     with open('output_csv_star/author_dimension.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "firstname",
            "lastname",
            "gender",
            "age"
        ])
        for key, value in authorsmap.map.items():
            [gender, age] = value
            writer.writerow([
            key,
            "",
            "",
            gender,
            age
            ])

def write_date_to_csv():
     with open('output_csv_star/time_dimension.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "minute",
            "hour",
            "day",
            "month",
            "year",
            "full_date"
        ])
        for key, value in timemap.map.items():
            id = value
            formatted_key = key.replace('T', ' ').replace('Z', '')
            writer.writerow([
            id,
            "",
            "",
            "",
            "",
            "",
            formatted_key
            ])

def print_entry(entry):
    #location_dimension.csv:
    id_location = geomap.get_or_allocate(entry.get('geoLocation'))


    #author_dimension.csv:
    author_data = entry.get('author')
    author_id = -1
    if isinstance(author_data, dict) and '$numberLong' in author_data:
        # Extract the number from the dictionary
        author_id = int(author_data['$numberLong'])
    else:
        # Assume it's already an integer
        author_id = int(author_data)

    age = int(entry.get('age'))
    gender = entry.get('gender')

    #add the next author in the Hmap
    authorsmap.get_or_allocate(author_id, [gender, age])

    #time_dimension:(to do)
        
    id_date = timemap.get_or_allocate(entry.get('date'))

    #document_dimension

    id_document = entry.get('_id')

    with open('output_csv_star/document_dimension.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                int(id_document['$numberLong']),
                entry.get('rawText'),
                entry.get('cleanText'),
                entry.get('lemmaText')
            ])

    #word_dimension and document_fact
    word_list = entry.get('words')
    for word in word_list :
        id_word = words.get_or_allocate(word['word'])
        with open('output_csv_star/document_fact.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                int(id_document['$numberLong']),
                author_id,
                id_date,
                id_location,
                id_word,
                word['count'],
                word['tf']
            ])

 
#the proper execution

os.makedirs('output_csv_star', exist_ok=True)

with open('output_csv_star/document_fact.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id_document",
            "id_author",
            "id_time",
            "id_location",
            "id_word",
            "count",
            "tf"
        ])

with open('output_csv_star/document_dimension.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "raw_text",
            "clean_text",
            "lemma_text"
        ])

read_json_entries(file_path)

write_authors_to_csv()
write_geolocations_to_csv()

write_words_to_csv()
write_authors_to_csv()
write_date_to_csv()
