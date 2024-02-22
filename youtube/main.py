import PySimpleGUI as sgui
from functions import set_working_directory, get_default_dir, open_folder, is_valid_youtube_url, check_if_dir_exists, download_thread
from ui import create_window
from translations import translations

set_working_directory()
destination_dir = get_default_dir()

window = create_window()

while True:
    event, values = window.read()

    if event in (sgui.WINDOW_CLOSED, 'Cancel'):
        break

    video_url = values['video_url']
    destination_folder = values['destination_folder']

    if event == 'Open Destination Folder':
        window["output"].print(translations['opening_destination_folder'])
        open_folder(window, destination_folder)

    if event == 'Download':
        console_output = ''

        if not video_url:
            console_output += translations['error_video_url_empty']
        elif not destination_folder:
            console_output += translations['error_destination_folder_empty']
        elif not is_valid_youtube_url(video_url):
            console_output += translations['error_invalid_youtube_url']
        else:
            window['progress_bar'].update_bar(0)
            download_thread(window, video_url, destination_folder)

        window['output'].update(console_output)

window.close()
