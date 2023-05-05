import cleantext

def normalize_text(text):
    return ' '.join(cleantext.clean_words(text,
                                 clean_all= False, # Execute all cleaning operations
                                 extra_spaces=True ,  # Remove extra white spaces 
                                 stemming=False , # Stem the words
                                 stopwords=False ,# Remove stop words
                                 lowercase=True ,# Convert to lowercase
                                 numbers=True ,# Remove all digits 
                                 punct=True ,# Remove all punctuations
                                 reg='<regex>', # Remove parts of text based on regex
                                 reg_replace='<replace_value>', # String to replace the regex used in reg
                                 stp_lang='english'  # Language for stop words
                                 ))
