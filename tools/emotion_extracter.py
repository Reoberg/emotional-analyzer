import spacy,nltk
from nrclex import NRCLex
import os

def extractToEmotions(text, title):
    nlp = spacy.load('en_core_web_sm')
    nltk.download('punkt')
    results_path = "assesment/emotionResults"

    # Process the text with spaCy to split it into sentences
    doc = nlp(text) 
    # Join the sentences back into a full text
    full_text = ' '.join([sent.text for sent in doc.sents])
    # Use NRCLex to analyze the emotions in the text
    emotion = NRCLex(full_text)

    # Ensure the results directory exists, create if it doesn't
    try:
        os.makedirs(results_path, exist_ok=True)
    except FileExistsError:
        pass  # Directory already exists
    
    output_file = os.path.join(results_path, f"{title}_results.txt")

    # Write the original text and detected emotions to the output file
    with open(output_file, 'w') as file:
        file.write(text + "\n")
        file.write("Detected Emotions and Frequencies:\n")
        for emotion, frequency in emotion.affect_frequencies.items():
            file.write(f"{emotion}: {frequency}\n")
    
    print(f"Emotion frequencies written to {output_file}")
