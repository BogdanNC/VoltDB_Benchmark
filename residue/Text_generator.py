import random

def generate_random_text():
    words = [
        "apple", "banana", "car", "dog", "elephant", "flower", "guitar", 
        "house", "ice", "jungle", "kite", "lemon", "moon", "notebook", 
        "orange", "piano", "queen", "river", "sun", "tree", "umbrella", 
        "violet", "whale", "xylophone", "yellow", "zebra","i","you","love",
        "always", "when", "if", "now"
    ]
    sentence = " ".join(random.choices(words, k=random.randint(5, 10)))
    return sentence

def generate_lines(num_lines=20000):
    lines = []
    for i in range(1, num_lines + 1):
        text = generate_random_text()
        lines.append(f"{i},{text}")
    return lines

def save_to_file(filename="mydataset.txt", num_lines=20000):
    lines = generate_lines(num_lines)
    with open(filename, "w") as file:
        file.write("\n".join(lines))

if __name__ == "__main__":
    save_to_file("mydataset.txt", 20000)
    print("File 'mydataset.txt' generated with 2000 lines of random text.")
