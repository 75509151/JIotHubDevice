import shortuuid 
import paho.mqtt.client as mqtt


class Device(mqtt.Client):

    def __init__(self, product_name, device_name, secret, client_id=None, host="127.0.0.1", port=1883):
        self.product_name = product_name
        self.device_name = device_name
        self._jclient_id = client_id if client_id else "{}/{}".format(product_name, device_name)
        print(self._jclient_id)
        self._secret = secret
        self._jhost = host
        self._jport = port
        self._jkeepalive = 60

        super(Device, self).__init__(self._jclient_id, clean_session=False, protocol=mqtt.MQTTv311)
        self._setup()

    def _on_device_connect(self, client, userdata, flags, rc):
        print("connect")

    def _setup(self):
        self.username_pw_set(self._jclient_id, self._secret)
        self.on_connect = self._on_device_connect

    def _teardown(self):
        pass

    def start(self):
        self.connect(self._jhost, self._jport, keepalive=self._jkeepalive)
        self.loop_start()

    def stop(self):
        self._teardown()
        self.loop_stop()

    def publish(self, topic, payload, qos=1):
        return super(Device, self).publish(topic, payload, qos=qos)

    def upload_data(self, data, _type="default"):
        topic = "upload_data/{product_name}/{device_name}/{type}/{uuid}".format(product_name=self.product_name,
                                                                                device_name=self.device_name,
                                                                                type=_type,
                                                                                uuid=shortuuid.uuid())
        self.publish(topic, data)

    def update_status(self, stats):
        pass

    def _check_request_duplication(self):
        pass

    def set_tags(self):
        pass

    def send_to_device(self, data):
        pass

    def report_shadow(self):
        pass
