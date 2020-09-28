import logging
import json

import attr
import beacontools
import click
import paho.mqtt.client


LOG = logging.getLogger()
MQTT_LOG = logging.getLogger("mqtt")


@click.command(
    context_settings=dict(
        auto_envvar_prefix="IBEACON_MQTT", help_option_names=["-h", "--help"]
    )
)
@click.option(
    "--host",
    "-h",
    default="127.0.0.1",
    help="Hostname of MQTT broker",
    show_envvar=True,
    show_default=True,
)
@click.option(
    "--port",
    "-p",
    default=1883,
    type=int,
    help="Port of MQTT broker",
    show_envvar=True,
    show_default=True,
)
@click.option(
    "--user",
    "-u",
    help="Username for optional MQTT broker authentication",
    show_envvar=True,
)
@click.option(
    "--password",
    "-P",
    help="Password for optional MQTT broker authentication",
    show_envvar=True,
)
def main(host, port, user, password):
    logging.basicConfig(level=logging.DEBUG)

    mqtt_client = paho.mqtt.client.Client()
    mqtt_client.enable_logger(logger=MQTT_LOG)

    if user:
        LOG.info("Configuring MQTT client with username %s", user)
        mqtt_client.username_pw_set(user, password=password)

    LOG.info("Connecting to MQTT broker at %s:%d", host, port)
    mqtt_client.connect(host, port=port)
    mqtt_client.loop_start()

    ibeacon_publisher = IBeaconPublisher(mqtt_client)
    ibeacon_scanner = beacontools.BeaconScanner(
        ibeacon_publisher.publish_beacon, packet_filter=beacontools.IBeaconAdvertisement
    )
    ibeacon_scanner.start()
    LOG.info("Started scanning for iBeacons")


@attr.s
class IBeaconPublisher:

    mqtt_client = attr.ib()

    def publish_beacon(self, bt_addr, rssi, packet, additional_info):
        LOG.debug(
            "Received iBeacon: <%s, %d> %s %s", bt_addr, rssi, packet, additional_info
        )
        try:
            topic = f"ibeacon/{packet.uuid}"
            payload = json.dumps({"major": packet.major, "minor": packet.minor})
            self.mqtt_client.publish(topic, payload)
        except Exception:
            LOG.exception("Failed to publish iBeacon data to MQTT")


if __name__ == "__main__":
    main()
