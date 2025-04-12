from pytube import YouTube

def downloadVideoURL(url):
    # Create a YouTube object for the given URL
    yt = YouTube(url)
    
    # Get the highest resolution stream available for the video
    stream = yt.streams.get_highest_resolution()

    # Log the download process
    print(f"Downloading video: {yt.title}")

    # Download the selected stream to the specified output path
    stream.download(output_path="assesment/videos")
    print(f"Download completed: {yt.title}")