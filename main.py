import PySimpleGUI as sg
import function
import validators


YOUTUBE = 1
TIKTOK = 2
sg.theme('DarkAmber')   # Add a touch of color

theme_dict = {'BACKGROUND': '#2B475D',
              'TEXT': '#FFFFFF',
              'INPUT': '#F2EFE8',
              'TEXT_INPUT': '#000000',
              'SCROLL': '#F2EFE8',
              'BUTTON': ('#000000', '#C2D4D8'),
              'PROGRESS': ('#FFFFFF', '#C7D5E0'),
              'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}
# sg.theme_add_new('Dashboard', theme_dict)     # if using 4.20.0.1+
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')
# sg.theme('DarkAmber')   # Add a touch of color

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20, 20), (20, 10))
BPAD_LEFT = ((20, 10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((20, 20), (20, 20))

top_banner = [[sg.Text('Video Downloader' + ' '*64, font='Any 20', background_color=DARK_HEADER_COLOR),
               sg.Text('YouTube - Facebook - Tiktok', font='Any 20', background_color=DARK_HEADER_COLOR)]]

top = [[sg.Text('The Weather Will Go Here', size=(50, 1), justification='c', pad=BPAD_TOP, font='Any 20')],
       [sg.T(f'{i*25}-{i*34}') for i in range(7)],]

block_3 = [[sg.Text('Block 3', font='Any 20')],
           [sg.Input(), sg.Text('Some Text')],
           [sg.Button('Go'), sg.Button('Exit')]]


block_2 = [[sg.Text('Block 2', font='Any 20')],
           [sg.T('This is some random text')],
           [sg.Image(data=sg.DEFAULT_BASE64_ICON)]]

block_4 = [[sg.Text('Support youtube and tiktok link (without warter mark). Please input valid link to text bellow !', font=("Helvetica", 13), size=(80, 2))],
           [sg.Text('Enter youtube link ...',  font=("Helvetica", 16)),
            sg.InputText(font=("Helvetica", 16), size=(50, 3))],
           [sg.Text('Download format *', size=(20, 1),
                    text_color="#ffffff", font=("Helvertica", 13))],
           [sg.Radio('MP3', "download_type", default=True, size=(15, 2), font=("Helvetica", 15), k=1),
            sg.Radio('Mp4', "download_type", default=False, size=(15, 2), font=("Helvetica", 15),  k=2)],
           [sg.Button('DOWNLOAD', size=(15, 2), button_color='white on green'),
            sg.Button('CLOSE',  size=(15, 2))],]

layout = [[sg.Column(top_banner, size=(960, 60), pad=(0, 0), background_color=DARK_HEADER_COLOR)],
          [sg.Column(top, size=(920, 90), pad=BPAD_TOP)],
          #   [sg.Column([[sg.Column(block_2, size=(450, 150), pad=BPAD_LEFT_INSIDE)],
          #               [sg.Column(block_3, size=(450, 150),  pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT, background_color=BORDER_COLOR),
          [sg.Column(block_4, size=(920, 320), pad=BPAD_RIGHT)]]

window = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0, 0),
                   background_color=BORDER_COLOR, no_titlebar=True, grab_anywhere=True)


# layout = [[sg.Text('Mp3/Mp4 downloader', size=(60, 2), justification='center', font=(
#     "Helvetica", 20), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]

# layout += [[sg.Text('Support youtube and tiktok link (without warter mark). Please input valid link to text bellow !', font=("Helvetica", 13), size=(80, 2))],
#            [sg.Text('Enter youtube link ...',  font=("Helvetica", 16)),
#             sg.InputText(font=("Helvetica", 16), size=(50, 3))],
#            [sg.Text('Download format *', size=(20, 1),
#                     text_color="#ffffff", font=("Helvertica", 13))],
#            [sg.Radio('MP3', "download_type", default=True, size=(15, 2), font=("Helvetica", 15), k=1),
#             sg.Radio('Mp4', "download_type", default=False, size=(15, 2), font=("Helvetica", 15),  k=2)],
#            [sg.Button('DOWNLOAD', size=(15, 2), button_color='white on green'),
#             sg.Button('CLOSE',  size=(15, 2))],]
# #    [sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF,
# #              enable_events=True, key='-GIF-IMAGE-')]]
# window = sg.Window("Youtube-Tiktok video mp3 downloader", layout)
# window['-GIF-IMAGE-'].update_animation(
#     sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)

# function


def getLinkType(link):
    if (validators.url(link)):
        if (link.find('youtube.com/watch?') != -1):
            return YOUTUBE
        elif (link.find('tiktok.com/') != -1):
            return TIKTOK
        else:
            return False
    return False


# Create an event loop
while True:
    event, values = window.read()
    if event == "DOWNLOAD":
        # print(values)
        link = values[0]
        # check link isvalid
        check = getLinkType(link)
        if (check == YOUTUBE):
            youtube_link = values[0]
            is_playlist = youtube_link.find('&list=')
            # print(is_playlist)
            # true: mp3 ,false mp3
            download_type = 'mp4'
            if (values[1]):
                download_type = 'mp3'

            if (is_playlist == -1):
                function.download_single(youtube_link, download_type, 'max')
            else:
                list_txt = youtube_link[9-is_playlist:]
                playlist_txt_arr = list_txt.split('&')
                playlist_txt = playlist_txt_arr[0]
                # print(list_txt)
                function.download_multiple(playlist_txt, download_type, 'max')
        elif (check == TIKTOK):
            output_name = function.tiktokDownload(link)
        else:
            print('wrong')
            # sg.popup('Wrong')
            # continue

    if event == "CLOSE" or event == sg.WIN_CLOSED:
        break

window.close()


# https://www.tiktok.com/@hungbavuatiente/video/7195768642385005851
# https://www.tiktok.com/@baihoccuocsonghay/video/7193922445978373402?_r=1&_t=8ZehY0anHX7
# https://www.youtube.com/watch?v=5SkAm_jbfvY
# https://www.youtube.com/watch?v=Wl9VQCIayRM&list=PLxmMJgy-buNM_l7ZhgxHsbd5HCrTw0fys
