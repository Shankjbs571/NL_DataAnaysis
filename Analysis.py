import nltk
import pandas as pd
import os
nltk.download('cmudict')
nltk.download('punkt')
from utils import *

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Paths to Stop word files
STOPWORD1 = os.getenv('STOPWORD1')
STOPWORD2 = os.getenv('STOPWORD2')
STOPWORD3 = os.getenv('STOPWORD3')
STOPWORD4 = os.getenv('STOPWORD4')
STOPWORD5 = os.getenv('STOPWORD5')
STOPWORD6 = os.getenv('STOPWORD6')
STOPWORD7 = os.getenv('STOPWORD7')

# Paths to Positive and Negative word files
POSITIVE_FILE_PATH = os.getenv('POSITIVE_FILE_PATH')
NEGATIVE_FILE_PATH = os.getenv('NEGATIVE_FILE_PATH')

# Path to output Excel file
OUTPUT_XLSX_FILE = os.getenv('OUTPUT_XLSX_FILE')

# Path to article text file directory
ARTICLE_DIR = os.getenv('ARTICLE_DIR')

#Custom Stop words for the analysis
# Initialize a set to store stop words
stop_words = set()

# Read each stop word file and add words to the set
stopword1 = STOPWORD1
stopword2 = STOPWORD2 
stopword3 = STOPWORD3 
stopword4 = STOPWORD4 
stopword5 = STOPWORD5 
stopword6 = STOPWORD6 
stopword7 = STOPWORD7 


stopword_files = [stopword1, stopword2,stopword3,stopword4,stopword5,stopword6,stopword7 ]
for stopword_file in stopword_files:
  try:
    with open(stopword_file, 'r',encoding='utf-8') as file:
        stop_words.update(file.read().splitlines())
  except UnicodeDecodeError:
    with open(stopword_file, 'r', encoding='latin1') as file:
        stop_words.update(file.read().splitlines())


#@title Set of Negative and Positive words  from MASTER Dictionary
# Load positive and negative words into sets
pw = POSITIVE_FILE_PATH
nw = NEGATIVE_FILE_PATH
positive_words = set(open(pw).read().splitlines())
try:
  negative_words = set(open(nw,encoding="utf-8").read().splitlines())
except UnicodeDecodeError:
  negative_words = set(open(nw,encoding='latin1').read().splitlines())

# print(len(positive_words))
# print(len(negative_words))


#@title Lets Write Data Back to excel sheet

# Load the Excel file
df = pd.read_excel(OUTPUT_XLSX_FILE)
path_to_txt = ARTICLE_DIR
# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    file_name = row['URL_ID']
    text_path = os.path.join(path_to_txt, file_name + '.txt')  # Adjust the path as needed
    # with open(text_path, 'r') as file:
    #   lines = file.readlines()
    #   # Join lines starting from the second line
    #   article_con = ''.join(lines[1:])
    try:
        with open(text_path, 'r', encoding='cp1252') as file:
            lines = file.readlines()
            article_con = ''.join(lines[1:])
    except UnicodeDecodeError:
        # If decoding fails, try using a different encoding (e.g., 'utf-8')
        with open(text_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            article_con = ''.join(lines[1:])



    

    #get the filtered content
    filtered_wor,filtered_con = remove_stop_words(article_con,stop_words)

    # Perform the analysis
    positive_score,negative_score = p_n_scores(filtered_con,positive_words,negative_words)

    pol_score = polarity_score(positive_score,negative_score)

    sub_score = subjectivity_score(positive_score,negative_score,len(filtered_wor))

    fg_index,avg_s_len,num_sentences = fog_index(filtered_con,pronunciations)

    total_words,complex_words,percentage_complex_words = complex_words_percentage(filtered_con,pronunciations)

    avg_num_words_per_sen = total_words/num_sentences

    avg_length_word = average_word_length(filtered_con)

    total_syllables,total_words,syllables_per_word = syllable_count_per_word(filtered_con,pronunciations)
    
    pronoun_count = count_personal_pronouns(article_con)

    avg_length = average_word_length(filtered_con)



    # Now Updating the df with the analysis results
    df.at[index, 'POSITIVE SCORE'] = positive_score
    df.at[index, 'NEGATIVE SCORE'] = negative_score
    df.at[index, 'POLARITY SCORE'] = pol_score
    df.at[index, 'SUBJECTIVITY SCORE'] = sub_score
    df.at[index, 'AVG SENTENCE LENGTH'] = avg_s_len
    df.at[index, 'PERCENTAGE OF COMPLEX WORDS'] = percentage_complex_words
    df.at[index, 'FOG INDEX'] = fg_index
    df.at[index, 'AVG NUMBER OF WORDS PER SENTENCE'] = avg_num_words_per_sen
    df.at[index, 'COMPLEX WORD COUNT'] = complex_words
    df.at[index, 'WORD COUNT'] =  total_words
    df.at[index, 'SYLLABLE PER WORD'] = syllables_per_word
    df.at[index, 'PERSONAL PRONOUNS'] = pronoun_count
    df.at[index, 'AVG WORD LENGTH'] = avg_length
    

# Write the updated DataFrame back to the Excel file
df.to_excel(OUTPUT_XLSX_FILE, index=False)
print("Successfull computed the values")
