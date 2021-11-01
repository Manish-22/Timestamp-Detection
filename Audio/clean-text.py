import spacy
from word2number import w2n
import contractions
import sys

nlp = spacy.load('en_core_web_sm')

DeselectedStopWords = ['no', 'not']

for i in DeselectedStopWords:
    nlp.vocab[i].is_stop = False

def CleanText(FileName):
    
    FileText = open("ChunkData/" + FileName + "/Text.txt", "r")
    TextRaw = FileText.readlines()
    FileText.close()

    Text = []

    for i in range(1, len(TextRaw), 2):
        Text.append(TextRaw[i].strip())
    
    CleanedText = []

    for i in Text:
        CleanedText.append(TextPreprocessing(i))

    FileCleanedText = open("ChunkData/" + FileName + "/CleanedText.txt", "w")

    for i in range(0, len(CleanedText)):
        Temp = ""
        for j in list(set(CleanedText[i])):
            Temp = Temp + j + ', '
        Temp = Temp[:-2]
        if(i == len(CleanedText) - 1):
            FileCleanedText.write(Temp)
        else:
            FileCleanedText.write(Temp + "\n")
    
    FileCleanedText.close()


def TextPreprocessing(Text):
    
    Text = Text.strip()
    Text = " ".join(Text.split())
        
    Text = contractions.fix(Text)
    
    Text = Text.lower()

    Temp = nlp(Text)

    CleanText = []
    
    for Token in Temp:
        Flag = True
        edit = Token.text
        
        if Token.is_stop and Token.pos_ != 'NUM': 
            Flag = False
        
        if Token.pos_ == 'PUNCT' and Flag == True: 
            Flag = False
        
        if Token.pos_ == 'SYM' and Flag == True: 
            Flag = False
        
        if (Token.pos_ == 'NUM' or Token.text.isnumeric()) and Flag == True:
            Flag = False
        
        if Token.pos_ == 'NUM' and Flag == True:
            edit = w2n.word_to_num(Token.text)
        elif Token.lemma_ != "-PRON-" and Flag == True:
            edit = Token.lemma_
         
        if edit != "" and Flag == True:
            CleanText.append(edit)

    return CleanText

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]

    CleanText(FileName)