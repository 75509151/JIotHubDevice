import logging

from jdevice import Device

from config import * 

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

jclient = Device(PRODUCT_NAME, DEVICE_NAME, SECRET, 
    host=MQTT_BORKER_URL, port=MQTT_BORKER_PORT)


class MyDevice():
    def __init__(self):
        self.client = jclient

    
    @jclient.task("rpc")
    def open_door(self, *args):
        log.debug("open door: %s" % args)
        log.info("open door: %s" % args)
        
    @jclient.task("cmd")
    def open_door2(self, *args):
        log.info("open door: %s" % args)
        log.debug("open door: %s" % args)

my_device = MyDevice()
jclient.start(block=True)

