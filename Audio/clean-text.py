import spacy
from word2number import w2n
import contractions
import re
import sys

def CleanText(FileName):
    
    nlp = spacy.load('en_core_web_sm')

    DeselectedStopWords = ['no', 'not']

    for i in DeselectedStopWords:
        nlp.vocab[i].is_stop = False
    
    FileText = open("ChunkData/" + FileName + "/Text.txt", "r")

    TextRaw = FileText.readlines()
    Text = []

    for i in range(1, len(TextRaw), 2):
        Text.append(TextRaw[i].strip())
    
    CleanedText = []


def remove_whitespace(text):
    """remove extra whitespaces from text"""
    text = text.strip()
    return " ".join(text.split())

def remove_symbols(text):
    return re.sub(r'[^\w]', ' ', text)

def expand_contractions(text):
    """expand shortened words, e.g. don't to do not"""
    text = contractions.fix(text)
    return text


def text_preprocessing(text, accented_chars=True, contractions=True, 
                       convert_num=True, extra_whitespace=True, 
                       lemmatization=True, lowercase=True, punctuations=True,
                       remove_html=True, remove_num=True, special_chars=True, 
                       stop_words=True):
    """preprocess text with default option set to true for all steps"""
    if extra_whitespace == True: #remove extra whitespaces
        text = remove_whitespace(text)
    if contractions == True: #expand contractions
        text = expand_contractions(text)
    if lowercase == True: #convert all characters to lowercase
        text = text.lower()

    doc = nlp(text) #tokenise text

    clean_text = []
    
    for token in doc:
        flag = True
        edit = token.text
        # remove stop words
        if stop_words == True and token.is_stop and token.pos_ != 'NUM': 
            flag = False
        # remove punctuations
        if punctuations == True and token.pos_ == 'PUNCT' and flag == True: 
            flag = False
        # remove special characters
        if special_chars == True and token.pos_ == 'SYM' and flag == True: 
            flag = False
        # remove numbers
        if remove_num == True and (token.pos_ == 'NUM' or token.text.isnumeric()) \
        and flag == True:
            flag = False
        # convert number words to numeric numbers
        if convert_num == True and token.pos_ == 'NUM' and flag == True:
            edit = w2n.word_to_num(token.text)
        # convert tokens to base form
        elif lemmatization == True and token.lemma_ != "-PRON-" and flag == True:
            edit = token.lemma_
        # append tokens edited and not removed to list 
        if edit != "" and flag == True:
            clean_text.append(edit)        
    return clean_text

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]

    CleanText(FileName)