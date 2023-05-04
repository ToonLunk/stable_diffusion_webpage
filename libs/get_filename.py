from libs.requirements import *

def getFilename(prompt):
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        print("INFO: Downloading 'en_core_web_sm'...")
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(prompt)
    
    # get only the nouns and verbs and combine them into a string like this: "noun_verb_noun_verb", etc.
    filename = ""
    remove = ["PUNCT", "DET", "ADP", "CCONJ", "PRON", "AUX", "NUM", "PART", "INTJ", "SPACE"]
    for token in doc:
        if token.pos_ not in remove:
            filename += token.text + "_" # add an underscore to separate the words
    filename = filename[:-1] # remove the last underscore
    # make sure filename isn't too long and if it is, use only the 6 most important words
    if len(filename) > 40:
        filename = "_".join(filename.split("_")[:6])
    print("filename: ", filename)
    # check if the filename exists already
    if os.path.exists(f"./static/img/output/{filename}.png"):
        # if it does, add a number to the end of the filename
        i = 1
        while os.path.exists(f"./static/img/output/{filename}_{i}.png"):
            i += 1
        filename = f"{filename}_{i}"
    return filename.lower()