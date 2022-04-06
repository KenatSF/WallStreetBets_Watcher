import os
import pandas as pd
import re
from nltk.tokenize import TweetTokenizer, RegexpTokenizer
from nltk import regexp_tokenize
from dotenv import load_dotenv
import os
load_dotenv()

def main():
    # Set up tokenizers
    tknzr_a = TweetTokenizer()
    tknzr_b = RegexpTokenizer('\w+')
    pattern = r'''(?x)                 # set flag to allow verbose regexps
                  (?:[A-Z]\.)+         # abbreviations, e.g. U.S.A.
                  | \w+(?:-\w+)*       # words with optional internal hyphens
                  | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
                  | \.\.\.             # ellipsis
                  | [][.,;"'?():-_`]   # these are separate tokens; includes ], [
    '''

    # Call data base
    os.chdir(os.getenv("DATA_PATH"))
    file_name = "reddit_data.csv"
    df = pd.read_csv(file_name)

    # Check-out body column
    index_to_check = [2, 38]
    body_index = df.loc[df.loc[:, "body"].notnull(), :].index
    text1 = str(df.loc[8, ["body"]].values.any())

    # Check-out differnt patterns
    case_1 = re.split(r' ', text1)
    case_2 = re.split(r'[ \t\n]+', text1)
    case_3 = re.split(r'[ \W\t\n]+', text1)
    case_4 = tknzr_a.tokenize(text1)
    case_5 = tknzr_b.tokenize(text1)
    case_6 = regexp_tokenize(text1, pattern)

    # Save patterns
    text_list = [case_1, case_2, case_3, case_4, case_5, case_6]

    # d5
    print("CASO 1:  " + str(len(
        case_1)))  # Deja palabras con los signos tipo (, ?, etc., deja espacios y cuando hay [] o () deja ese contenido unido.            ## Sí lee emojis (burdos)
    print(case_1)

    # d5
    print("CASO 2:  " + str(len(
        case_2)))  # Deja palabras con los signos tipo (, ?, etc., NO deja espacios y cuando hay [] o () deja ese contenido unido.         ## Sí lee emojis (burdos)
    print(case_2)

    # t8
    print("CASO 3:  " + str(len(
        case_3)))  # Separa absolutamente stodo y omite los símbolos ortográficos.                                                         ## No lee emojis
    print(case_3)

    # *
    print("CASO 4:  " + str(len(
        case_4)))  # Separa absolutamente stodo y NO omite los símbolo ortográficos                                                        ## Sí lee emojis (abrevia)
    print(case_4)

    # a6
    print("CASO 5:  " + str(len(
        case_5)))  # Separa absolutamente stodo y omite los símbolos ortográficos                                                          ## No lee emojis
    print(case_5)

    # a6
    print("CASO 6:  " + str(len(
        case_6)))  # Separa absolutamente stodo y NO omite los símbolos ortográficos.                                                      ## No lee emojis
    print(case_6)


if __name__ == '__main__':
    main()



