import os
import PySimpleGUI as sg
from translations import translations

def create_window():
    progress_bar = sg.ProgressBar(100, orientation='h', size=(20, 20), key='progress_bar')

    def get_default_dir():
        # You can modify this default directory as per your requirements
        return os.path.join(os.getcwd(), "YT_Downloads")

    destination_dir = get_default_dir()

    layout = [
        [sg.Text('Video URL'), sg.InputText(key='video_url')],
        [sg.Text('Destination Folder'), sg.InputText(key='destination_folder', default_text=destination_dir), sg.FolderBrowse(button_text="Browse")],
        [sg.Button('Download'), sg.Button('Open Destination Folder'), sg.Button('Cancel')],
        [sg.Multiline(size=(40, 6), key='output', disabled=True, autoscroll=True)],
        [progress_bar]
    ]

    window = sg.Window('YouTube Downloader', layout)
    return window
