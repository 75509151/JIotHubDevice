import pytest
import time

from jdevice.device import Device

from .config import *

@pytest.yield_fixture(scope="class")
def device():
    d = Device(PRODUCT_NAME, DEVICE_NAME, SECRET)
    # d.connect(MQTT_BORKER_URL, MQTT_BORKER_PORT)
    d.start()
    time.sleep(0.5)
    yield d
    d.stop()


