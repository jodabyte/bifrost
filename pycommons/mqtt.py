import json
import logging
from typing import Any, List

import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage, SubscribeOptions
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import PacketTypes, ReasonCodes


class MqttClient:
    def __init__(
        self,
        id: str,
        protocol: int = mqtt.MQTTv5,
        enable_logging: bool = False,
    ) -> None:
        self.logger = logging.getLogger(id)
        self._client = mqtt.Client(client_id=id, protocol=protocol)
        if enable_logging:
            self._client.enable_logger()
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_subscribe = self._on_subscribe
        self._client.on_unsubscribe = self._on_unsubscribe
        self._client.on_message = self._on_message
        self._client.on_publish = self._on_publish

    def connect(self, host: str, port: int = 1883, properties: Properties = None):
        rc: int = self._client.connect(
            host=host, port=port, clean_start=True, properties=properties
        )
        self.logger.debug(
            f"Sending CONNECT host='{host}' port='{port}' properties='{properties}' rc='{mqtt.error_string(rc)}'"
        )

    def disconnect(self, reasoncode: ReasonCodes = None, properties: Properties = None):
        rc: int = self._client.disconnect(reasoncode=reasoncode, properties=properties)
        self.logger.debug(
            f"Sending DISCONNECT reasoncode='{reasoncode}' properties='{properties}' rc='{ReasonCodes(PacketTypes.DISCONNECT, identifier=rc)}'"
        )

    def subscribe(
        self,
        topic: str,
        qos: int = 0,
        options: SubscribeOptions = None,
        properties: Properties = None,
    ) -> None:
        rc, mid = self._client.subscribe(
            topic=topic, qos=qos, options=options, properties=properties
        )
        self.logger.debug(
            f"Sending SUBSCRIBE topic='{topic}' with qos='{qos}' options='{options}' properties='{properties}' mid='{mid}' rc='{mqtt.error_string(rc)}'"
        )

    def unsubscribe(self, topic: str, properties: Properties = None) -> None:
        rc, mid = self._client.unsubscribe(topic, properties=properties)
        self.logger.debug(
            f"Sending UNSUBSCRIBE topic='{topic}' properties='{properties}' mid='{mid}' rc='{mqtt.error_string(rc)}'"
        )

    def publish(
        self,
        topic: str,
        payload: dict,
        qos: int = 0,
        retain: bool = False,
        properties: Properties = None,
    ) -> None:
        info: mqtt.MQTTMessageInfo = self._client.publish(
            topic=topic,
            payload=json.dumps(payload),
            qos=qos,
            retain=retain,
            properties=properties,
        )
        self.logger.debug(
            f"Sending PUBLICH topic='{topic}' payload='{payload}' with qos='{qos}' retain='{retain}' properties='{properties}' mid='{info.mid}' rc='{mqtt.error_string(info.rc)}'"
        )

    def loop_start(self) -> None:
        self._client.loop_start()

    def loop_stop(self) -> None:
        self._client.loop_stop()

    def loop_forever(self) -> None:
        self._client.loop_forever()

    def _on_message(
        self, client: mqtt.Client, userdata: Any, message: MQTTMessage
    ) -> None:
        self.logger.info(
            f"Received ON_MESSAGE client_id='{client._client_id.decode('utf-8')}' userdata='{userdata}' topic='{message.topic}' payload='{message.payload}' qos='{message.qos}' retain='{message.retain}' mid='{message.info.mid}' rc='{mqtt.error_string(message.info.rc)}'"
        )

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: dict,
        rc: ReasonCodes,
        properties: mqtt.Properties,
    ) -> None:
        self.logger.info(
            f"Received ON_CONNECT client_id='{client._client_id.decode('utf-8')}' rc='{mqtt.connack_string(rc)}' userdata='{userdata}' flags='{flags}' properties='{properties}'"
        )

    def _on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        rc: int,
    ) -> None:
        self.logger.info(
            f"Received ON_DISCONNECT client_id='{client._client_id.decode('utf-8')}' rc='{ReasonCodes(PacketTypes.DISCONNECT, identifier=rc)}' userdata='{userdata}'"
        )

    def _on_subscribe(
        self,
        client: mqtt.Client,
        userdata: Any,
        mid: int,
        rc: List[ReasonCodes],
        properties: List[Properties],
    ) -> None:
        self.logger.info(
            f"Received ON_SUBSCRIBE client_id='{client._client_id.decode('utf-8')}' mid='{mid}' qos='{[qos.getName() for qos in rc]}' userdata='{userdata}' properties='{properties}'"
        )

    def _on_unsubscribe(
        self,
        client: mqtt.Client,
        userdata: Any,
        mid: int,
        properties: List[Properties],
        rc: List[ReasonCodes],
    ) -> None:
        self.logger.info(
            f"Received ON_UNSUBSCRIBE client_id='{client._client_id.decode('utf-8')}' mid='{mid}' rc='{[qos.getName() for qos in rc]}' userdata='{userdata}' properties='{properties}'"
        )

    def _on_publish(self, client: mqtt.Client, userdata: Any, mid: int) -> None:
        self.logger.info(
            f"Received ON_PUBLICH client_id='{client._client_id.decode('utf-8')}' mid='{mid}' userdata='{userdata}'"
        )
