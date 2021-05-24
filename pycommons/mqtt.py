import logging
from typing import Any, List, Tuple

import paho.mqtt.client as mqtt
from paho.mqtt.reasoncodes import PacketTypes, ReasonCodes

import pycommons.config.config


class MqttClient:
    def __init__(
        self,
        id: str,
        host: str,
        port: int = 1883,
        protocol: int = mqtt.MQTTv5,
        enable_logging: bool = True,
    ) -> None:
        self.logger = logging.getLogger(id)
        self._client = mqtt.Client(client_id=id, protocol=protocol)
        if enable_logging:
            self._client.enable_logger()
        self._client.on_connect = self._on_connect
        self._client.on_subscribe = self._on_subscribe
        self._client.on_message = self._on_message
        self._client.on_publish = self._on_publish
        self._client.on_unsubscribe = self._on_unsubscribe
        self._client.on_disconnect = self._on_disconnect
        error_code: int = self._client.connect(host=host, port=port, clean_start=True)
        self.logger.debug(
            f"Connected to broker with code='{mqtt.error_string(error_code)}'"
        )

    def subscribe(self, topics: List[Tuple[str, int]]) -> None:
        pass

    def publish(
        self, topic: str, payload: dict, qos: int = 0, retain: bool = False
    ) -> None:
        pass
        # info: mqtt.MQTTMessageInfo = self._client.publish(
        #     topic=topic, payload=payload, qos=qos, retain=retain
        # )

    def loop_start(self) -> None:
        self._client.loop_start()

    def loop_stop(self) -> None:
        self._client.loop_stop()

    def loop_forever(self) -> None:
        self._client.loop_forever()

    def _on_message(self, client, userdata, message) -> None:
        pass

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: dict,
        rc: ReasonCodes,
        properties: mqtt.Properties,
    ) -> None:
        self.logger.info(
            f"Received callback=on_connect client_id='{client._client_id.decode('utf-8')}' rc='{mqtt.connack_string(rc)}' userdata='{userdata}' flags='{flags}' properties='{properties}'"
        )

    def _on_subscribe(self, client, userdata, mid, rc, properties) -> None:
        pass

    def _on_publish(self, client, userdata, mid) -> None:
        pass

    def _on_unsubscribe(self, client, userdata, mid, properties, rc) -> None:
        pass

    def _on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        rc: int,
    ) -> None:
        self.logger.info(
            f"Received callback=on_disconnect client_id='{client._client_id.decode('utf-8')}' rc='{ReasonCodes(PacketTypes.DISCONNECT, identifier=rc)}' userdata='{userdata}'"
        )

    def _on_log(self) -> None:
        pass
