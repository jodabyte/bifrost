import time

from pycommons.mqtt import MqttClient

try:
    client = MqttClient("NLU-RASA", "broker.hivemq.com")
    client.loop_start()
    time.sleep(2)
except Exception as e:
    print(e)
