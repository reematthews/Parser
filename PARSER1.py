import nltk
from nltk.corpus import brown
import csv


class SimpleParser: #parsing of sentences 
    def __init__(self):  #define a simple grammar, NP: Noun Phrase, VP: Verb Phrase
        #determiners (DT), adjectives (JJ), singular noun, proper nouns , plural nouns (NN, NNP, NNPS), and verbs (VB)
        self.grammar = {
            "NP": ["DT", "JJ", "NN"], # a noun phrase can be a determiner followed by adjectives followed by a noun
            "VP": ["VB", "NP"], # a verb phrase can be a verb followed by a noun phrase
        }
        
    def tokenize(self, sentence): #method to tokenize the sentence into individual words.
        print("Tokenize:\n", nltk.word_tokenize(sentence))
        return nltk.word_tokenize(sentence) #returns the list of tokens
    
    def pos_tag(self, tokens): # use nltk's POS tagger. Labels each word as a noun, verb, etc.
        print("POS tagger:\n", nltk.pos_tag(tokens)) #prints tagged tokens
        return nltk.pos_tag(tokens)
    
    def parse(self, sentence): #parse the sentence based on predefined grammer 
        tokens = self.tokenize(sentence) #tokenize the sentence 
        tagged_tokens = self.pos_tag(tokens) #labels each word with its role in the sentence
        phrases = [] #empty list to store
        current_phrase_type = None
        current_phrase = [] #keeps track of the current pharse being constructed
        for word, tag in tagged_tokens: #goes through each tagged token in the sentence
            matched = False
            for phrase_type, components in self.grammar.items():
                if tag.startswith(tuple(components)): #checks if the words tagged matches any part of the components
                    if current_phrase_type == phrase_type: #add it if part of the phrase is currently being worked on 
                        current_phrase.append((word, tag))
                    else:
                        if current_phrase:  # save previous phrase if there was one
                            phrases.append((current_phrase_type, current_phrase))
                        current_phrase = [(word, tag)] #starts on a new phrase
                        current_phrase_type = phrase_type
                    matched = True
                    break
            if not matched and current_phrase: #saves it if the word didnt fit anywhere, unfinished phrase.
                phrases.append((current_phrase_type, current_phrase))
                current_phrase = []
                current_phrase_type = None
        if current_phrase: # adds the last phrase if there is one
            phrases.append((current_phrase_type, current_phrase))
        return phrases

def write_phrases_to_csv(sentences, filename="parser.csv"):
    parser = SimpleParser()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Document', 'Phrase Type', 'Phrase'])  # CSV header

        for sentence in sentences:
            phrases = parser.parse(sentence)
            for phrase_type, phrase in phrases:
                phrase_str = ' '.join([word for word, tag in phrase])  # Convert phrase to string
                writer.writerow([sentence, phrase_type, phrase_str])  # Write to CSV

def main():
    print("Parser:")
    parser = SimpleParser()  # Instantiate the SimpleParser

    while True:
        print("\nMenu:")
        print("1. Enter a sentence")
        print("2. Parse sentences from a text file")
        print("3. Parse sentences from a CSV file")
        print("4. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                try:
                    num_sentences = int(input("Enter the number of sentences: "))
                    if num_sentences <= 0:
                        raise ValueError("Number of sentences must be a positive integer.")
                    sentences = []
                    for _ in range(num_sentences):
                        sentence = input("Enter a sentence: ")
                        sentences.append(sentence)
                    write_phrases_to_csv(sentences)  
                    print("Sentences saved to parser.csv.")
                    break  
                except ValueError as error:
                    print(f"Error! Number of sentences must be a positive integer.")

        elif choice == "2":
            while True:
                try:
                    filename = input("Enter the path to the text file: ")
                    with open(filename, "r") as file:
                        sentences = file.readlines()
                    for sentence in sentences:
                        phrases = parser.parse(sentence)  # Parse each sentence from the file
                        for phrase_type, phrase in phrases:
                            phrase_str = ' '.join([word for word, _ in phrase])  # Extract phrase string
                            print(f"Phrase Type: {phrase_type}, Phrase: {phrase_str}")  # Print phrase type and phrase
                            
                            with open("parser.csv", mode='a', newline='', encoding='utf-8') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([sentence.strip(), phrase_type, phrase_str])
                    print("Parsing completed. Results saved to parser.")
                    break  
                except FileNotFoundError:
                    print("File not found. Please enter a valid file path.")
                except Exception as e:
                    print(f"An error occurred: {e}")

        elif choice == "3":
            try:
                filename = input("Enter the path to the CSV file: ")
                with open(filename, "r") as file, open("parser.csv", mode='w', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(file)
                    writer = csv.writer(csvfile)
                    writer.writerow(['Original Sentence', 'Phrase Type', 'Phrase'])  # Write header
                    next(reader, None)  # Skip header if present
                    for row in reader:
                        sentence = row[0]
                        phrases = parser.parse(sentence)
                        for phrase_type, phrase in phrases:
                            phrase_str = ' '.join([word for word, _ in phrase])
                            writer.writerow([sentence, phrase_type, phrase_str])
                print("Parsing completed. Results saved to parser.csv.")
            except FileNotFoundError:
                print("File not found. Please enter a valid file path.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif choice == "4":
            print("Exiting!")
            return
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
