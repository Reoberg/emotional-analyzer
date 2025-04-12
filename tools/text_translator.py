from textblob import TextBlob
from googletrans import Translator
import os, datetime
def extractToSentiment(text, title):
    output_dir = "assesment/translatedTexts"

    # Ensure the output directory exists; create it if it doesn't
    try:
        os.makedirs(output_dir, exist_ok=True)
    except FileExistsError:
        pass  # Directory already exists

    # Analyze the sentiment of the input text using TextBlob
    blob = TextBlob(text)
    print(blob.sentiment)
    print(blob.sentiment.polarity)
    print(blob.sentiment.subjectivity)
    
    
    translator = Translator()

    # Translate the text from English to Spanish
    try:
        blob_translated = translator.translate(text, src='en', dest='es').text
    except Exception as e:
        print(f"Translation failed for {title}: {e}")
        return

    print(blob_translated)


    output_file = os.path.join(output_dir, f"{title}_translated.txt")
    
    # Write the translated text to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(blob_translated))
    
    print(f"Translated text written to {output_file}")