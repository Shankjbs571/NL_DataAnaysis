import re
from nltk import word_tokenize
from nltk.corpus import cmudict

#@title p_n_scores, polarity_score,subjectivity_score functions
def p_n_scores(filtered_content,positive_words,negative_words):
  filtered_content_words = filtered_content.split()
  positive_score = 0
  negative_score = 0
  for word in filtered_content_words:
    if word in positive_words:
      positive_score+=1
    elif word in negative_words:
      negative_score+=1
  return positive_score,negative_score

def polarity_score(p,n):
  diff = p-n
  sum = p+n
  sum+=0.000001
  pol_score = diff/sum
  return pol_score

def subjectivity_score(p,n,total_words):
  sum = p+n
  total_words+=0.000001
  return sum/total_words


#@title Lets Find How many Complex words are there



def count_syllables(word, pronunciations):
    # Lookup the pronunciation of the word
    word_pronunciations = pronunciations.get(word.lower(), [])
    # word_pronunciations = pronunciations[word.lower()]
    max_syllables = 0

    # Iterate over each pronunciation
    for pron in word_pronunciations:
        syllable_count = 0
        # Iterate over each syllable in the pronunciation
        for syl in pron:
            # Check if the syllable ends with a digit
            if syl[-1].isdigit():
                syllable_count += 1
        # Update the maximum syllable count
        if syllable_count > max_syllables:
            max_syllables = syllable_count

    return max_syllables

   
def is_complex(word, pronunciations):
    return count_syllables(word, pronunciations) > 2

# Load the CMU Pronouncing Dictionary
pronunciations = cmudict.dict()


def complex_words_percentage(filtered_content,pronunciations):
  # Tokenize the text into words
  raw_words = word_tokenize(filtered_content)
  words = [word for word in raw_words if re.match('^[a-zA-Z]+$', word)]

  # Count the total number of words and complex words
  total_words = len(words)
  complex_words = sum([1 for word in words if is_complex(word, pronunciations)])

  # Calculate the percentage of complex words
  percentage_complex_words = (complex_words / total_words)*100
  return total_words,complex_words,percentage_complex_words


#@title Analysis of Readibility

from nltk import sent_tokenize


def fog_index(content,pronunciations):
  # Tokenize the text into sentences
  sentences = sent_tokenize(content)

  # Count the number of sentences
  num_sentences = len(sentences)
  # total_words,complex_words,complex_words_p = complex_words_percentage(content,pronunciations)
  total_words,complex_words,percentage_complex_words = complex_words_percentage(content,pronunciations)
  avg_sent_len = total_words / num_sentences
  # Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
  fog_i = 0.4 * (avg_sent_len + percentage_complex_words)
  return fog_i , avg_sent_len,num_sentences 


#@title Syllable Count Per Word
# Tokenize the text into words

def syllable_count_per_word(article,pronunciations):
  words = word_tokenize(article)

  # Calculate the total number of syllables and words
  total_syllables = sum(count_syllables(word,pronunciations) for word in words)
  total_words = len(words)

  # Calculate the syllable count per word
  if total_words > 0:
      syllables_per_word = total_syllables / total_words
  else:
      syllables_per_word = 0

  return total_syllables,total_words,syllables_per_word


#@title Count Personal Pronouns

def count_personal_pronouns(text):
    # Define the regex pattern to match the personal pronouns
    pattern = r"\b(?:I|we|my|ours|us)\b"

    # Use findall to get all matches of the pattern in the text
    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    # Filter out 'US' as a country name
    filtered_matches = [match for match in matches if match.lower() != 'us']

    # Return the count of personal pronouns
    return len(filtered_matches)


#@title Average Word Length

def average_word_length(text):
    # Tokenize the text into words
    words = text.split()

    # Calculate the total number of characters in all words
    total_characters = sum(len(word) for word in words)

    # Calculate the total number of words
    total_words = len(words)

    # Calculate the average word length
    if total_words > 0:
        average_length = total_characters / total_words
    else:
        average_length = 0

    return average_length


#@title Get the stopwords removed

def remove_stop_words(article_content,stop_words):
  # Tokenize the article content
  words = article_content.split()

  # Remove stop words
  filtered_words = [word for word in words if word.lower() not in stop_words]

  # Join the filtered words back into a string
  filtered_content = ' '.join(filtered_words)

  return filtered_words,filtered_content
