import PySimpleGUI as sg
from pytube import YouTube
import os
import re
import threading
import sys

def set_working_directory():
    # Change the working directory to the directory where the executable file lies
    executable_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(executable_dir)

def get_default_dir():
    set_working_directory()  # Set the working directory first
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(parent_directory, "YT_Downloads")

def open_folder(folder_path):
    if os.path.exists(folder_path):
        os.system(f'explorer "{folder_path}"')
    else:
        window["output"].print(f'The folder does not exist: {folder_path}')

def is_valid_youtube_url(url):
    # Patterns for common YouTube URL formats
    youtube_url_patterns = [
        r'^https?://www\.youtube\.com/watch\?v=.*',
        r'^https?://youtu\.be/.*'
    ]

    for pattern in youtube_url_patterns:
        if re.match(pattern, url):
            return True
    return False

def check_if_dir_exists(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            window["output"].print(f"Path created: {path}")
        except OSError as e:
            window["output"].print(f"Error creating path '{path}': {e}")
    return path

def get_only_audio_stream(youtube_link: str):
    return youtube_link.streams.get_audio_only()

def download_mp3_from_ytlink(only_audio_stream, destination_path):
    return only_audio_stream.download(output_path=destination_path)

def convert_to_mp3_and_remove_double_data(file_path: str) -> None:
    base, _ = os.path.splitext(file_path)
    new_file = base + '.mp3'
    if os.path.exists(new_file):
        window["output"].print('File already exists in the destination folder!')
    else:
        os.rename(file_path,new_file)

def start_download(video_url, destination_folder):
    try:
        youtube_link = YouTube(video_url)
        destination_folder = check_if_dir_exists(destination_folder)
        window["output"].print(f'Downloading: {youtube_link.title} as mp3')
        window['progress_bar'].update_bar(20) 
        only_audio_stream = get_only_audio_stream(youtube_link)
        window['progress_bar'].update_bar(30) 
        out_file = download_mp3_from_ytlink(only_audio_stream, destination_folder)
        window['progress_bar'].update_bar(60) 
        convert_to_mp3_and_remove_double_data(out_file)
        window['progress_bar'].update_bar(70) 
        window["output"].print("Download completed!")
        window["output"].print(f"Destination folder: {destination_folder}")
        window['progress_bar'].update_bar(100) 
    except:
        window["output"].print("Download failed!")

def download_thread(video_url, destination_folder):
    threading.Thread(target=start_download, args=(video_url, destination_folder)).start()

progress_bar = sg.ProgressBar(100, orientation='h', size=(20, 20), key='progress_bar')
set_working_directory()
destination_dir = get_default_dir()

layout = [
    [sg.Text('Video URL'), sg.InputText(key='video_url')],
    [sg.Text('Destination Folder'), sg.InputText(key='destination_folder', default_text=destination_dir), sg.FolderBrowse(button_text="Browse")],
    [sg.Button('Download'), sg.Button('Open Destination Folder'), sg.Button('Cancel')],
    [sg.Multiline(size=(40, 6), key='output', disabled=True, autoscroll=True)],
    [progress_bar]
]

window = sg.Window('YouTube Downloader', layout)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Cancel'):
        break

    video_url = values['video_url']
    destination_folder = values['destination_folder']

    if event == 'Open Destination Folder':
        window["output"].print("Opening Destination Folder")
        open_folder(destination_folder)

    if event == 'Download':
        console_output = ''

        if not video_url:
            console_output += "Error: Video URL cannot be empty.\n"
        elif not destination_folder:
            console_output += "Error: Destination folder cannot be empty.\n"
        elif not is_valid_youtube_url(video_url):
            console_output += "Error: Invalid YouTube video URL.\n"
        else:
            window['progress_bar'].update_bar(0)
            download_thread(video_url, destination_folder)

        window['output'].update(console_output)

window.close()