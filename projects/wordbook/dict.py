import json
# import difflib 
from difflib import get_close_matches, SequenceMatcher

data = json.load(open("projects/wordbook/data.json"))


# input                         output
# if word                       data, status=success
# elif word                     date=null, status=similar_word, meta_data=[]
    # word, yes_or_no = yes     data=[], status=success
    # word, yes_or_no = no      data=null, status=error, message   
# else word                     data=null, status=error, message


 
def translate(word_lower):
    if word_lower == None:
        return None, "no_data", None
    word_lower = word_lower.lower()
    similar_words = get_close_matches(word_lower, data.keys())
    if word_lower in data:
        return data[word_lower], "success", None
    elif len(similar_words)>0:
        return None, "similar_word", similar_words 
 
    else: 
        return None, "unsuccessful", "Please double check the word"
        
        
# match_ratio = SequenceMatcher(None, "sagar", "sagrrr").ratio()
# print(match_ratio)      


# word = input("Enter a word: ")
# output =translate()
# if type(output) == list:
#     for i in output:
#         print(i)
# else:
#     print("enter valid word")
