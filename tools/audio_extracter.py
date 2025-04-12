import os
import moviepy.editor as mp


def extractToAudioFile(videoPath):
    # Load the video file from the given path
    video = mp.VideoFileClip(videoPath)

    # Refering the folder we want to upload audio files
    audio_output_folder = "assesment/audios"

    # Create the output folder if it doesn't exist 
    try:
        os.makedirs(audio_output_folder, exist_ok=True)
    except FileExistsError:
        pass  # Directory already exists

    # Create the audio filename by replacing the video file extension with .wav
    audio_filename = os.path.basename(videoPath).replace(".mp4", ".wav")
    audioPath = os.path.join(audio_output_folder, audio_filename)

    # Extract the audio from the video and save it to the audio file
    video.audio.write_audiofile(audioPath)

    # Define the path for the log file
    output_log = "assesment/audio_log"

    # Define the path for the log file
    if not os.path.exists(output_log):
        os.makedirs(output_log)
    output_filename = os.path.join(output_log, "audioFile.txt")

     # Append a log entry to the log file indicating the extraction of audio
    with open(output_filename, 'a') as file:
        file.write(f"Extracted audio from {videoPath} to {audioPath}\n")