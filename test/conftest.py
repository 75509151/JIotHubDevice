import pytest
import time

from jdevice.device import Device

from .config import *


MQTT_BORKER_URL = "127.0.0.1"                                                                                                                                                                                      
MQTT_BORKER_PORT = 1883


PRODUCT_NAME = "r1s"
DEVICE_NAME = "a01"
SECRET = "howcute121"

@pytest.yield_fixture(scope="class")
def device():
    d = Device(PRODUCT_NAME, DEVICE_NAME, SECRET, 
            host=MQTT_BORKER_URL, port=MQTT_BORKER_PORT)

    d.start()
    time.sleep(0.5)
    yield d
    d.stop()




