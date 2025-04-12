
import time
import threading
import multiprocessing
import glob, os
import tools.video_downloader as downloader
import tools.audio_extracter as audioExtract
import tools.text_extracter as textExtract
import tools.emotion_extracter as emotionExtract
import tools.text_translator as translator 
from logger import Logger

# Semaphore to limit the number of concurrent threads to 5
semaphore = threading.Semaphore(5)
multiprocessingSemaphore = multiprocessing.Semaphore(5)

# Logger instance to log download activities
logManager = Logger('emotion-analyzer/download_log.txt')


urls = []
videos = []
audios = []
texts = {}
translatedTexts = {}

#--------------------------LIST GETTERS--------------------------------
# Function to read URLs from a file and store them in the urls list
def getURLs():
    url_file = "emotion-anaylzer/video_urls.txt" 
    with open(url_file, 'r') as file:
        for line in file:
            url = line.strip()
            if(url):
                urls.append(url)

# Function to get a list of video files in the specified directory
def getVideos():
    videos.clear()
    videos.extend(glob.glob(os.path.join("emotion-analyzer/videos", '*.mp4')))

# Function to get a list of audio files in the specified directory
def getAudios():
    audios.clear()
    audios.extend(glob.glob(os.path.join("emotion-analyzer/audios", '*.wav')))

# Function to read text files and store their contents in the texts list
def getTexts():
    texts.clear()
    text_files = glob.glob(os.path.join("emotion-analyzer/audioTexts", '*.txt'))
    for text_file in text_files:
        # Extract the title from the file name (assuming the title is the file name without the extension)
        title = os.path.basename(text_file).replace(".txt", "")
        with open(text_file, 'r') as file:
            content = file.read()
            texts[title] = content


def getTranslatedTexts():
    translatedTexts.clear()
    text_files = glob.glob(os.path.join("emotion-analyzer/translatedTexts", '*.txt'))
    for text_file in text_files:
        # Extract the title from the file name (assuming the title is the file name without the extension)
        title = os.path.basename(text_file).replace(".txt", "")
        with open(text_file, 'r') as file:
            content = file.read()
            translatedTexts[title] = content


#--------------------------TOOL FUNCTIOONS--------------------------------
# Function to download a video with Threading from a URL with error handling and logging
def threadingDownloadVideo(url):
    with semaphore:
        try:
            downloader.downloadVideoURL(url)
            logManager.log(url,True)
        
        except Exception as e:
            logManager.log(url,False)
            print(f"Failed to download video from URL: {url}. Error: {e}")

        finally:
            semaphore.release()

# Function to download a video with Multi-processing from a URL with error handling and logging   
def multiprocessingDownloadVideo(url):
    with multiprocessingSemaphore:
        try:
            downloader.downloadVideoURL(url)
            logManager.log(url,True)
        
        except Exception as e:
            logManager.log(url,False)
            print(f"Failed to download video from URL: {url}. Error: {e}")

        finally:
            multiprocessingSemaphore.release()

# Function to download a video from a URL with error handling and logging
def downloadVideo(url):
    try:
        downloader.downloadVideoURL(url)
        logManager.log(url,True)
        
    except Exception as e:
        logManager.log(url,False)
        print(f"Failed to download video from URL: {url}. Error: {e}")

# Function to convert a video to an audio file
def videoToAudio(video):
    audioExtract.extractToAudioFile(video)
    
#Function to convert a audio to an text file
def audioToText(audio):
    textExtract.extractToTextFile(audio)

def translateText(text,title):
    translator.extractToSentiment(text,title)

# Function to convert a text to emotions
def textToEmotion(translatedText,title):
    emotionExtract.extractToEmotions(translatedText,title)
    
#--------------------------Serial Processing--------------------------------
def serialRunner():
    # Start the timer to measure the total execution time
    start = time.perf_counter()

    # Get URLs from the file and store them in the urls list
    getURLs()
    
    # Loop through each URL and download the corresponding video
    for url in urls:
        downloadVideo(url)

    # Measure and print the time taken to download all videos
    finishDownload = time.perf_counter()
    print(f'Download Time: {finishDownload - start} second(s)')

    # Get the list of downloaded videos
    getVideos()
    
    # Loop through each video and convert it to audio
    for video in videos:
        videoToAudio(video)

    # Get the list of converted audio files
    getAudios()
    
    # Loop through each audio file and convert it to text
    for audio in audios:
        audioToText(audio)

    # Get the list of text files and store their contents in the texts dictionary
    getTexts()
    
    # Loop through each text in the dictionary and translate it
    for title, text in texts.items():
        translateText(text, title)

    # Get the list of translated texts and store their contents in the texts dictionary
    getTexts()
    
    # Loop through each translated text and analyze it for emotions
    for title, text in texts.items():
        textToEmotion(text, title)
    
    # Measure and print the total time taken for the entire process
    end = time.perf_counter()
    print(f'Serial: {end - start} second(s)')

#--------------------------Threading--------------------------------
def threadingRunner():
    start = time.perf_counter()

    getURLs()
    # Creating a threads for parallel downloading
    download_threads = [] 
    for url in urls:  
        thread = threading.Thread(target=threadingDownloadVideo, args=(url,))
        download_threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in download_threads:
        thread.join()
    
    finishDownload= time.perf_counter()
    print(f'Download Time: {finishDownload-start} second(s)')
    
    getVideos()
    # Creating threads for parallel covertion
    convert_audio_threads = []
    for video in videos:
        thread = threading.Thread(target=videoToAudio, args=(video,))
        convert_audio_threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in convert_audio_threads:
        thread.join()
 
    getAudios()
    # Creating threads for parallel covertion
    convert_text_threads = []
    for audio in audios:
        thread = threading.Thread(target=audioToText, args=(audio,))
        convert_text_threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in convert_text_threads:
        thread.join()

    getTexts()
    # Creating threads for parallel covertion
    translate_threads = []
    for title, text in texts.items():
        thread = threading.Thread(target=translateText, args=(text,title,))
        translate_threads.append(thread)
        thread.start()
    
    for thread in translate_threads:
        thread.join()

    # getTranslatedTexts()
    # Creating threads for parallel covertion
    convert_emotion_threads = []
    for title, text in texts.items():
        thread = threading.Thread(target=textToEmotion, args=(text,title,))
        convert_emotion_threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in convert_emotion_threads:
        thread.join()
   
    end=time.perf_counter()
    print(f'Threading: {end-start} second(s)') 
    print("All analyse operations completed.")

#-----------------------Multi-Processing-------------------------------
def multiprocessRunner():

    start = time.perf_counter()

    getURLs()
    
    # Use multiprocessing to download videos in parallel
    with multiprocessing.Pool() as pool:
        pool.map(multiprocessingDownloadVideo, urls)

    finishDownload = time.perf_counter()
    print(f'Download Time: {finishDownload - start} second(s)')

    getVideos()
    
    # Use multiprocessing to convert videos to audio in parallel
    with multiprocessing.Pool() as pool:
        pool.map(videoToAudio, videos)
    print("All videos converted to audio.")

    getAudios()
    # Use multiprocessing to convert audios to text in parallel
    with multiprocessing.Pool() as pool:
        pool.map(audioToText, audios)
    print("All audios converted to text.")

    getTexts()
    # Prepare tasks for translating texts, each task is a tuple of (text, title)
    translate_tasks = [(text, title) for title, text in texts.items()]
    
    # Use multiprocessing to translate texts in parallel
    with multiprocessing.Pool() as pool:
        pool.starmap(translateText, translate_tasks)
    print("All texts translated.")

    # Prepare tasks for emotion analysis, each task is a tuple of (text, title)
    emotion_tasks = [(text, title) for title, text in texts.items()]
    
    # Use multiprocessing to analyze emotions in translated texts in parallel
    with multiprocessing.Pool() as pool:
        pool.starmap(textToEmotion, emotion_tasks)
    print("All translated texts analyzed for emotions.")

    # Measure and print the total time taken for the entire process
    end = time.perf_counter()
    print(f'Multiprocessing: {end - start} second(s)')
    print("All analysis operations completed.")

# Main Function where we call analyse processes.
if __name__ == '__main__':
   #serialRunner() 
   #threadingRunner() 
   multiprocessRunner() 
