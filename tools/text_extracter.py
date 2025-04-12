import speech_recognition as sr
import os 

def extractToTextFile(audioPath):
  
    recognizer = sr.Recognizer()

    # Load the audio file using the speech recognizer
    with sr.AudioFile(audioPath) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    print(text)
    
    # Generate the output text file name by replacing the '.wav' extension with '.txt'
    text_file_name = os.path.basename(audioPath).replace(".wav", ".txt")
    # Define the path to save the output text file
    textPath = os.path.join('assesment/audioTexts', text_file_name)
    # Ensure the directory exists; create it if it doesn't
    os.makedirs(os.path.dirname(textPath), exist_ok=True)

    # Write the recognized text to the output text file
    with open(textPath, 'w') as file:
        file.write(text)

    print(f'Text has been written to {textPath}')
