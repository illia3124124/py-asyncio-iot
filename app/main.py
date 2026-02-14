import time
import asyncio

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    gathered_devices = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )
    hue_light_id = gathered_devices[0]
    speaker_id = gathered_devices[1] 
    toilet_id = gathered_devices[2]
    await asyncio.gather(
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_ON),
                Message(speaker_id, MessageType.SWITCH_ON),
                Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
            ]
        ),
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_OFF),
                Message(speaker_id, MessageType.SWITCH_OFF),
                Message(toilet_id, MessageType.FLUSH),
                Message(toilet_id, MessageType.CLEAN)
            ]
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
