import logging
import re
import shortuuid
import paho.mqtt.client as mqtt

log = logging.getLogger(__name__)


class Device(mqtt.Client):

    def __init__(self, product_name, device_name, secret, client_id=None, host="127.0.0.1", port=1883, subscribe=True):
        self._msg_route = {}
        self._task_route = {}
        self.product_name = product_name
        self.device_name = device_name
        self._jclient_id = client_id if client_id else "{}/{}".format(product_name, device_name)
        self._secret = secret
        self._jhost = host
        self._jport = port
        self._jkeepalive = 60
        self._jsubscribe = subscribe

        super(Device, self).__init__(self._jclient_id, clean_session=False, protocol=mqtt.MQTTv311)
        self._setup()

    def _on_device_connect(self, client, userdata, flags, rc):
        log.debug("connect")

        def _subscribe():
            #TODO:
            topics = [("rpc/{product_name}/{device_name}/+/+/+/#", 1),
            ("cmd/{product_name}/{device_name}/+/+/+/#", 1),
            ("tags/{product_name}/tag/+/+/+/#",1),
           ("m2m/{product_name}/{device_name}/+/+".format(product_name=self.product_name), 1)]
            self.subscribe(topics)
            return 

        if self._jsubscribe:
            _subscribe()


    def _on_device_msg(self, client, userdata, message):
        log.debug("on_msg: %s" % message)
        topic = message.topic
        func = None
        match = None
        for rule, f in self._msg_route.items():
            # TODO: re.compile
            match = re.match(rule, topic)
            if match:
                func = f
                break

        if func:
            func(message, *match.groups())

        else:
            self.default_handler(message)

    def msg_route(self, rule, **options):
        def register(fn):
            return self._add_msg_route(rule, fn)
        return register

    def task(self, _type="rpc"):
        assert _type in ("rpc", "cmd", "tag", "m2m")

        def register(fn):
            tasks_map = self._task_route.get(_type, {})
            tasks_map[fn.__name__] = fn
            self._task_route[_type] = tasks_map
            return fn
        return register

    def _setup_inner_route(self):
        cmd_rule = "cmd/{product_name}/{device_name}/(?P<cmd>.*?)/(?P<encoding>.*?)/(?P<msg_id>.*?)/(?P<expires_at>.*?)".format(product_name=self.product_name,
                                                                               device_name=self.device_name)
        rpc_rule = "rpc/{product_name}/{device_name}/(?P<cmd>.*?)/(?P<encoding>.*?)/(?P<msg_id>.*?)/(?P<expires_at>.*?)".format(product_name=self.product_name,
                                                                               device_name=self.device_name)
        tag_topic_rule = "tags/{product_name}/tag/(?P<cmd>.*?)/(?P<encoding>.*?)/(?P<msg_id>.*?)/(?P<expires_at>.*?)".format(product_name=self.product_name)
        m2m_topic_rule = "m2m/{product_name}/{device_name}/(?P<sender>.*?)/(?P<msg_id>.*?)".format(product_name=self.product_name,
                                                                                                   device_name=self.device_name)
        self._add_msg_route(rpc_rule, self.rpc_handler)
        self._add_msg_route(cmd_rule, self.cmd_handler)
        self._add_msg_route(tag_topic_rule, self.tag_handler)
        self._add_msg_route(m2m_topic_rule, self.m2m_handler)

    def rpc_handler(self, msg, cmd, encodeing, msg_id, expires_at=None):
        log.debug("cmd:%s, encodeing: %s, msg_id: %s, expires_at:%s" % (
            cmd,
            encodeing, msg_id,
            expires_at))
        func = self._task_route.get("rpc", {}).get(cmd, None)
        if func:
            func(msg, cmd, encodeing, msg_id, expires_at)

    def cmd_handler(self, msg, cmd, encodeing, msg_id, expires_at=None):
        log.debug("cmd:%s, encodeing: %s, msg_id: %s, expires_at:%s" % (
            cmd,
            encodeing, msg_id,
            expires_at))
        func = self._task_route.get("cmd", {}).get(cmd, None)
        if func:
            func(msg, cmd, encodeing, msg_id, expires_at)

    def tag_handler(self, msg, sender, msg_id):
        log.debug("sender: %s, msg_id: %s" % (sender, msg_id))

    def m2m_handler(self, msg, product_name, device_name, sender, msg_id):
        log.debug("product_name: %s,  device_name:%s, sender: %s, msg_id: %s" % (product_name,
                                                                                 device_name,
                                                                                 sender, msg_id))

    def default_handler(self, msg):
        log.debug("topic: %s, payload: %s" % (msg.topic, msg.payload))

    def _add_msg_route(self, route, f):
        self._msg_route[route] = f

    def _setup(self):
        self.username_pw_set(self._jclient_id, self._secret)
        self.on_connect = self._on_device_connect
        self.on_message = self._on_device_msg

        self._setup_inner_route()

    def _teardown(self):
        pass

    def start(self, block=False):
        self.connect(self._jhost, self._jport, keepalive=self._jkeepalive)
        if block:
            self.loop_forever()
        else:
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
