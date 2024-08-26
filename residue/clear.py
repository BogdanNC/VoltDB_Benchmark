from pathlib import Path

def delete_file(file_path):
    file = Path(file_path)
    try:
        file.unlink()
        print(f"File {file_path} deleted successfully.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except PermissionError:
        print(f"Permission denied: {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

# Example usage
delete_file("./output_csv/words.csv")
delete_file("./output_csv/geo_location.csv")
delete_file("./output_csv/genders.csv")
delete_file("./output_csv/vocabulary.csv")
delete_file("./output_csv/documents.csv")
delete_file("./output_csv/authors.csv")
delete_file("./output_csv/documents_authors.csv")