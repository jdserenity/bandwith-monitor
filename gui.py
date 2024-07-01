import PySimpleGUI as sg; from bandwith_monitor import BandwithMonitor; import threading; 

class GUI():
    def __init__(self):
        with open('database.txt', mode='r') as f:
            data = f.readlines()
            highest_numbers = data[1].split(',')

        self.highest_ever = {'upload':float(highest_numbers[0]), 'download':float(highest_numbers[1])}

        self.layout = [
            # row 1 # pad = left, right, top, bottom
            [sg.ProgressBar(max_value=self.highest_ever['upload'], orientation='v', size=(10, 30), pad=((17, 0), (10, 0)), bar_color=('green', 'white'), key='-UPLOAD_BAR-'), 
            sg.ProgressBar(max_value=self.highest_ever['download'], orientation='v', size=(10, 30), pad=((17, 0), (10, 0)), bar_color=('red', 'white'), key='-DOWNLOAD_BAR-')], 

            # row 2
            [sg.Text('Upload: ', font=('Helvetica', 16)),
            sg.Text('', key='-UPLOAD-', font=('Helvetica', 16)), # display upload speed
            sg.Text('Download: ', font=('Helvetica', 16)), 
            sg.Text('', key='-DOWNLOAD-', font=('Helvetica', 16))], # display download speed
            
            # row 3
            [sg.Button('Start', button_color=('white', 'green'),size=(4, 1), font=('Helvetica', 16)),
            sg.Button('Stop', button_color=('white', 'red'), size=(4, 1),font=('Helvetica', 16))],

            # row 4
            [sg.Button('Keep on top of all windows')]
        ]

        self.keep_on_top = False

        self.window = sg.Window('Lightweight Bandwith Monitor', self.layout, size=(400, 200), keep_on_top=self.keep_on_top)

        self.bm = BandwithMonitor(self.window)

    def run(self):
        while True:
            event, values = self.window.read(timeout=1000)
            
            if event == sg.WIN_CLOSED:
                self.bm.stop_monitoring()
                break


            if event == "Keep on top of all windows":
                self.keep_on_top = not self.keep_on_top
                self.window.TKroot.attributes("-topmost", self.keep_on_top)


            if event == "Start":
                threading.Thread(target=self.bm.monitor, daemon=True).start()


            if event == "Stop":
                self.bm.stop_monitoring()

                self.window['-UPLOAD-'].update('')
                self.window['-UPLOAD_BAR-'].update(current_count=0)

                self.window['-DOWNLOAD-'].update('')
                self.window['-DOWNLOAD_BAR-'].update(current_count=0)


            if event == '-UPDATE-':
                upload_speed, download_speed = values['-UPDATE-']
                if upload_speed < 1024:
                    self.window['-UPLOAD-'].update(f'{upload_speed} KB/s')
                else:
                    self.window['-UPLOAD-'].update(f'{upload_speed/1024:.2f} MB/s')
                self.window['-UPLOAD_BAR-'].update(current_count=upload_speed)

                if upload_speed < 1024:
                    self.window['-DOWNLOAD-'].update(f'{download_speed} KB/s')
                else:
                    self.window['-DOWNLOAD-'].update(f'{upload_speed/1024:.2f} MB/s')
                self.window['-DOWNLOAD_BAR-'].update(current_count=download_speed)

                if upload_speed > self.highest_ever['upload']:
                    self.highest_ever['upload'] = upload_speed
                    self.window['-UPLOAD_BAR-'].update(max_value=upload_speed)
                    with open('database.txt', mode='w') as f:
                        f.write(f'highest upload ever reached,highest download ever reached\n{self.highest_ever['upload']},{self.highest_ever['download']}')
                
                if download_speed > self.highest_ever['download']:
                    self.highest_ever['download'] = download_speed
                    self.window['-DOWNLOAD_BAR-'].update(max_value=download_speed)
                    with open('database.txt', mode='w') as f:
                        f.write(f'highest upload ever reached,highest download ever reached\n{self.highest_ever['upload']},{self.highest_ever['download']}')


        self.window.close()