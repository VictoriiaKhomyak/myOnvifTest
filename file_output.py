import asyncio

from onvif import ONVIFCamera
import pandas as pd

# Асинхронная функция для подключения к камере и получения возможностей
async def get_camera_capabilities(ip, port, user, password):
    # Создание экземпляра камеры
    mycam = ONVIFCamera(ip, port, user, password, r'C:\Users\Gigabyte-PC\PycharmProjects\OnvifTester\.venv\Lib\site-packages\onvif\wsdl')
    # Получение сервисов и возможностей
    await mycam.update_xaddrs()
    device = await mycam.create_devicemgmt_service()
    capabilities = await device.GetCapabilities({'Category': 'All'})
    print(capabilities)

    # Словарь для хранения возможностей
    capabilities_dict = {}

    # Заполнение словаря
    if capabilities.Media:
        capabilities_dict['Media'] = True
        if capabilities.Media.XAddr:
            capabilities_dict['Media_XAddr'] = capabilities.Media.XAddr
    if capabilities.Imaging:
        capabilities_dict['Imaging'] = True
        if capabilities.Imaging.XAddr:
            capabilities_dict['Imaging_XAddr'] = capabilities.Imaging.XAddr
    if capabilities.Device:
        capabilities_dict['Device'] = True
        if capabilities.Device.XAddr:
            capabilities_dict['Device_XAddr'] = capabilities.Device.XAddr

    # Перевод словаря в DataFrame
    df = pd.DataFrame([capabilities_dict])

    # Сохранение в Excel файл
    df.to_excel('camera_capabilities.xlsx', index=False)

# Замените '192.168.1.1', 80, 'admin', 'admin' на IP-адрес, порт, имя пользователя и пароль вашей камеры
ip_address = '172.18.212.18'
port = 80
username = 'admin'
password = 'Supervisor'

# Запуск асинхронной задачи
loop = asyncio.get_event_loop()
loop.run_until_complete(get_camera_capabilities(ip_address, port, username, password))