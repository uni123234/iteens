import json

def load_words_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_test_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
