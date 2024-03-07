import asyncio
import json
import pandas as pd

from onvif import ONVIFCamera
from onvif.exceptions import ONVIFError

SERVICES = [
    "devicemgmt",
    "media",
    "ptz",
    "imaging",
    "deviceio",
    "events",
    "analytics",
    "recording",
    "search",
    "replay",
    "notification",
    "subscription",
    "receiver",
]
async def run():

    cam = ONVIFCamera(
        '172.18.212.18',
        80,
        'admin',
        'Supervisor',
        wsdl_dir=r'C:\Users\Viktoriia\PycharmProjects\OnvifTester\.venv\Lib\site-packages\onvif\wsdl',
    )
    await cam.update_xaddrs()
    device = await cam.create_devicemgmt_service()
    print(await device.GetHostname())
    services = await device.GetServices({'IncludeCapability': True})
    s = str(services).replace("<", "'<").replace(">", ">'")
    with open('output2.txt', 'w') as f:
        f.write(s)
    services_list = eval(s)
    for service in services_list:
        print(service)
    # with open('output2.json') as f:
    #     context = json.load(f)
    # print(type(context))
    # print(await device.GetServices({'IncludeCapability': True}))
    media = await cam.create_media_service()
    profiles = await media.GetProfiles()


    # result = []
    # for s in SERVICES:
    #     try:
    #         service = await cam.create_onvif_service(s)
    #         try:
    #             capabilities = await service.GetServiceCapabilities()
    #             result.append(f'{s}: {str(capabilities)}')
    #         except AttributeError:
    #             print(f'{s} has no operation "GetServiceCapabilities"')
    #     except ONVIFError:
    #         print(f"Camera doesn't support {s}")
    # print(result)
    # with open('output1.txt', 'w') as f:
    #     for s in result:
    #         f.write(f'{s}\n')



loop = asyncio.get_event_loop()
loop.run_until_complete(run())