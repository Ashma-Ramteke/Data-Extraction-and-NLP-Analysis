# -*- coding: utf-8 -*-
"""NLP Assessment

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15eAECXwH_QIhnQNN6SSWRx2_yTlUnAe_
"""

# Step 1 Import Necessary Libraries
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from collections import Counter
import zipfile

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

#  Step 2 Load Input.xlsx
input_file = "Input.xlsx"
data = pd.read_excel(input_file)

# Create output directory for articles
output_dir = "extracted_articles"
os.makedirs(output_dir, exist_ok=True)

#Step 3 Define Function to extract article text from a URL

def extract_title_and_article_text(soup, url):
    try:
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else ""
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        article_text = "\n".join(paragraphs)

        return title, article_text
    except Exception as e:
        print(f"Error extracting URL {url}: {e}")
        return "", ""

# Step 4  Define extract_article_text function
def extract_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else ""
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        article_text = "\n".join(paragraphs)
        return title, article_text
    except Exception as e:
        print(f"Error extracting URL {url}: {e}")
        return "", ""

# Load data and process URLs
extracted_data = []
for index, row in data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    # Call the defined extract_article_text function
    title, article_text = extract_article_text(url)

    if article_text:
        # Save extracted text to a file
        with open(os.path.join(output_dir, f"{url_id}.txt"), 'w', encoding='utf-8') as file:
            file.write(title + "\n" + article_text)

        extracted_data.append((url_id, url, title, article_text))

# Define the directory containing stopwords
stopwords_dir = "/content/stopwords"  # Update this path to your stopwords directory

stop_words = set()
for root, dirs, files in os.walk(stopwords_dir):
    for file in files:
        file_path = os.path.join(root, file)
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            stop_words.update(word.strip() for word in f)

!pip install chardet

import chardet

def detect_encoding(file_path):
    with open("/content/StopWords-20241223T054355Z-001.zip", 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

stop_words = set()
for root, dirs, files in os.walk(stopwords_dir):
    for file in files:
        file_path = os.path.join(root, file)
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            stop_words.update(word.strip() for word in f)

#Step 5: Load Stop Words and Master Dictionary
# Skip Invalid Lines
stop_words = set()
for root, dirs, files in os.walk(stopwords_dir):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            stop_words.update(word.strip() for word in f)

import os
import zipfile

# Path to the ZIP file
zip_file_path = "/content/MasterDictionary-20241223T054355Z-001.zip"
extract_to_dir = "/content/MasterDictionary"  # Directory to extract files

# Extract the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_dir)

# Define the directory containing the extracted files
master_dict_dir = extract_to_dir

# List all files in the extracted MasterDictionary directory
master_dict_files = os.listdir(master_dict_dir)
print("Files in MasterDictionary directory:", master_dict_files)

import zipfile

with zipfile.ZipFile("/content/MasterDictionary-20241223T054355Z-001.zip", 'r') as zip_ref:
    zip_ref.extractall(master_dict_dir)

# Check again after extraction
master_dict_files = os.listdir(master_dict_dir)
print("Files in MasterDictionary directory after extraction:", master_dict_files)

# Example if files are in a subdirectory
sub_dir = "some_subdirectory"
positive_file_path = os.path.join(master_dict_dir, sub_dir, "positive-words.txt")
negative_file_path = os.path.join(master_dict_dir, sub_dir, "negative-words.txt")

# Search for positive-words.txt
for root, dirs, files in os.walk(master_dict_dir):
    for file in files:
        if "positive" in file.lower() and file.endswith(".txt"):
            print("Found positive words file:", os.path.join(root, file))
        if "negative" in file.lower() and file.endswith(".txt"):
            print("Found negative words file:", os.path.join(root, file))

# Update paths if needed
positive_file_path = os.path.join(master_dict_dir, "positive-words.txt")  # Adjust if file is in a subdirectory
negative_file_path = os.path.join(master_dict_dir, "negative-words.txt")  # Adjust if file is in a subdirectory

# Load the positive and negative words
positive_words = set()
negative_words = set()

with open("/content/MasterDictionary/MasterDictionary/positive-words.txt", 'r', encoding='ISO-8859-1') as f:
    positive_words.update(word.strip() for word in f if word.strip())

with open("/content/MasterDictionary/MasterDictionary/negative-words.txt", 'r', encoding='ISO-8859-1') as f:
    negative_words.update(word.strip() for word in f if word.strip())

#Step 7 Perform Analysis
#Perform the analysis and compute the variables.
import nltk
nltk.download('punkt_tab')
output_data = []

for url_id, url, title, article_text in extracted_data:
    cleaned_tokens = clean_text(article_text)
    sentences = sent_tokenize(article_text)

    pos_score = compute_positive_score(cleaned_tokens)
    neg_score = compute_negative_score(cleaned_tokens)
    polarity_score = compute_polarity_score(pos_score, neg_score)
    subjectivity_score = compute_subjectivity_score(pos_score, neg_score, len(cleaned_tokens))
    avg_sentence_length = compute_avg_sentence_length(sentences)
    perc_complex_words = compute_percentage_complex_words(cleaned_tokens)
    fog_index = compute_fog_index(avg_sentence_length, perc_complex_words)
    word_count = len(cleaned_tokens)
    personal_pronouns = compute_personal_pronouns(article_text)
    avg_word_length = compute_avg_word_length(cleaned_tokens)

    output_data.append([
        url_id, url, pos_score, neg_score, polarity_score, subjectivity_score,
        avg_sentence_length, perc_complex_words, fog_index, word_count,
        personal_pronouns, avg_word_length
    ])

#Step 7 Perform Analysis
#Perform the analysis and compute the variables.
def clean_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text)  # Remove non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)  # Tokenize the text
    return [word for word in tokens if word not in stop_words]

def compute_positive_score(tokens):
    return sum(1 for word in tokens if word in positive_words)

def compute_negative_score(tokens):
    return sum(1 for word in tokens if word in negative_words)

def compute_polarity_score(pos_score, neg_score):
    return (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)

def compute_subjectivity_score(pos_score, neg_score, total_words):
    return (pos_score + neg_score) / (total_words + 0.000001)

def compute_avg_sentence_length(sentences):
    return sum(len(sentence.split()) for sentence in sentences) / len(sentences) if sentences else 0

def syllable_count(word):
    vowels = "aeiouy"
    word = word.lower()
    syllables = 0
    prev_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                syllables += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False
    if word.endswith('e'):
        syllables = max(1, syllables - 1)
    return syllables

def compute_percentage_complex_words(tokens):
    return len([word for word in tokens if syllable_count(word) > 2]) / len(tokens) * 100

def compute_fog_index(avg_sent_length, perc_complex_words):
    return 0.4 * (avg_sent_length + perc_complex_words)

def compute_avg_words_per_sentence(sentences):
    return sum(len(sentence.split()) for sentence in sentences) / len(sentences) if sentences else 0

def compute_complex_word_count(tokens):
    return len([word for word in tokens if syllable_count(word) > 2])

def compute_syllables_per_word(tokens):
    total_syllables = sum(syllable_count(word) for word in tokens)
    return total_syllables / len(tokens) if tokens else 0

def compute_personal_pronouns(text):
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, flags=re.IGNORECASE)
    return len(pronouns)

def compute_avg_word_length(tokens):
    return sum(len(word) for word in tokens) / len(tokens)

# Process each URL
extracted_data = []
for index, row in data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    title, article_text = extract_article_text(url)
    if article_text:
        with open(os.path.join(output_dir, f"{url_id}.txt"), 'w', encoding='utf-8') as file:
            file.write(title + "\n" + article_text)
        sentences = sent_tokenize(article_text)
        tokens = clean_text(article_text)
        pos_score = compute_positive_score(tokens)
        neg_score = compute_negative_score(tokens)
        polarity_score = compute_polarity_score(pos_score, neg_score)
        subjectivity_score = compute_subjectivity_score(pos_score, neg_score, len(tokens))
        avg_sentence_length = compute_avg_sentence_length(sentences)
        perc_complex_words = compute_percentage_complex_words(tokens)
        fog_index = compute_fog_index(avg_sentence_length, perc_complex_words)
        avg_words_per_sentence = compute_avg_words_per_sentence(sentences)
        complex_word_count = compute_complex_word_count(tokens)
        word_count = len(tokens)
        syllables_per_word = compute_syllables_per_word(tokens)
        personal_pronouns = compute_personal_pronouns(article_text)
        avg_word_length = compute_avg_word_length(tokens)
        extracted_data.append([
            url_id, url, pos_score, neg_score, polarity_score, subjectivity_score,
            avg_sentence_length, perc_complex_words, fog_index, avg_words_per_sentence,
            complex_word_count, word_count, syllables_per_word, personal_pronouns, avg_word_length
        ])

#Step 8: Save Results to Excel
output_columns = [
    'URL_ID', 'URL', 'Positive Score', 'Negative Score', 'Polarity Score', 'Subjectivity Score',
    'Avg Sentence Length', 'Percentage Complex Words', 'Fog Index', 'Avg Number of Words per Sentence',
    'Complex Word Count', 'Word Count', 'Syllable Per Word', 'Personal Pronouns', 'Avg Word Length'
]
output_df = pd.DataFrame(extracted_data, columns=output_columns)
output_file = "Output.xlsx"
output_df.to_excel(output_file, index=False)

print(f"Analysis completed. Results saved to {output_file}")