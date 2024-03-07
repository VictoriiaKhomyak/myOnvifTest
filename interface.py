import asyncio
import tkinter as tk
from tkinter import ttk
from onvif import ONVIFCamera
from pprint import pprint

# Глобальные переменные для управления камерой и интерфейсом
camera = None
root = None
profiles = []

async def get_camera_profiles(ip, port, user, password):
    global camera, profiles
    camera = ONVIFCamera(ip, port, user, password, r'C:\Users\Gigabyte-PC\PycharmProjects\OnvifTester\.venv\Lib\site-packages\onvif\wsdl')
    await camera.update_xaddrs()
    media_service = await camera.create_media_service()
    profiles = await media_service.GetProfiles()
    result = []
    print(profiles)
    return
    for profile in profiles:
        now = {}
        for key in profile:
            if key == 'Name':
                name = key
                now['profile'] = {'profile_name': getattr(profile, key)}
            else:
                dct = getattr(profile, key)
                if dct:
                    subdct = {}
                    for k in dct:
                        if k == 'Name':
                            subdct_name = getattr(dct, k)
                            now['profile'][subdct_name] = {}
                        else:
                            now['profile'][subdct_name][k] = getattr(dct, k)
                break
        print(now)
        print('\n\n\n\n')
        # result.append(now)
    # pprint(result)
    update_profile_listbox()

def update_profile_listbox():
    global profiles_listbox, profiles
    profiles_listbox.delete(0, tk.END)
    for profile in profiles:
        profiles_listbox.insert(tk.END, profile.Name)


def parse_profiles():
    parsed_profiles = []
    for profile in profiles:
        # Словарь для хранения информации о текущем профиле
        profile_info = {
            'Name': profile.Name,
            'Token': profile.token
        }

        # Извлечение информации о видеоконфигурации, если она есть
        if hasattr(profile, 'VideoEncoderConfiguration'):
            vec = profile.VideoEncoderConfiguration
            profile_info['VideoEncoder'] = {
                'Encoding': vec.Encoding,
                'Resolution': f"{vec.Resolution.Width}x{vec.Resolution.Height}",
                'FrameRateLimit': vec.RateControl.FrameRateLimit,
                'EncodingInterval': vec.RateControl.EncodingInterval,
                'BitrateLimit': vec.RateControl.BitrateLimit,
            }

        # Добавление информации о профиле в список
        parsed_profiles.append(profile_info)

    return parsed_profiles
def on_profile_select(event):
    # Здесь можно добавить вывод информации о выбранном профиле
    pass

def connect_to_camera():
    ip = '172.18.212.18'# ip_entry.get()
    port = 80 #int(port_entry.get())
    user = 'admin' # user_entry.get()
    password = 'Supervisor' #password_entry.get()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_camera_profiles(ip, port, user, password))

ip = '172.18.212.18'# ip_entry.get()
port = 80 #int(port_entry.get())
user = 'admin' # user_entry.get()
password = 'Supervisor' #password_entry.get()
loop = asyncio.get_event_loop()
loop.run_until_complete(get_camera_profiles(ip, port, user, password))

# # Создание графического интерфейса
# root = tk.Tk()
# root.title("ONVIF Camera Interface")
#
# connection_frame = ttk.Frame(root)
# connection_frame.pack(padx=10, pady=10, fill='x', expand=True)
#
# tk.Label(connection_frame, text="IP Address:").pack(side=tk.LEFT)
# ip_entry = ttk.Entry(connection_frame)
# ip_entry.pack(side=tk.LEFT, expand=True, padx=2)
#
# tk.Label(connection_frame, text="Port:").pack(side=tk.LEFT)
# port_entry = ttk.Entry(connection_frame)
# port_entry.pack(side=tk.LEFT, expand=True, padx=2)
#
# tk.Label(connection_frame, text="Username:").pack(side=tk.LEFT)
# user_entry = ttk.Entry(connection_frame)
# user_entry.pack(side=tk.LEFT, expand=True, padx=2)
#
# tk.Label(connection_frame, text="Password:").pack(side=tk.LEFT)
# password_entry = ttk.Entry(connection_frame, show="*")
# password_entry.pack(side=tk.LEFT, expand=True, padx=2)
#
# connect_button = ttk.Button(connection_frame, text="Connect", command=connect_to_camera)
# connect_button.pack(side=tk.LEFT, padx=5)
#
# profiles_frame = ttk.Frame(root)
# profiles_frame.pack(padx=10, pady=10, fill='both', expand=True)
#
# profiles_listbox = tk.Listbox(profiles_frame)
# profiles_listbox.pack(side=tk.LEFT, fill='both', expand=True)
# profiles_listbox.bind('<<ListboxSelect>>', on_profile_select)
#
# root.mainloop()