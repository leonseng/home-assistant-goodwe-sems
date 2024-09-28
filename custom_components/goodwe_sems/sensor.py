from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import base64
from datetime import datetime
import json
import sys

import requests


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    add_entities([GeneratedPowerSensor()])


class GeneratedPowerSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Power Generated"
    _attr_native_unit_of_measurement = "W"
    _attr_device_class = "power"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, hass: HomeAssistant, username: str, password: str, power_station_id: str
    ) -> None:
        self.username = username
        self.password = password
        self.power_station_id = power_station_id

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        BASE_URL = "https://au.semsportal.com/api/v2"

        def encode_dict_as_token(token_dict):
            return base64.b64encode(json.dumps(token_dict).encode("utf-8")).decode(
                "ascii"
            )

        LOGIN_TOKEN = {
            "uid": "",
            "timestamp": 0,
            "token": "",
            "client": "web",
            "version": "",
            "language": "en",
        }

        req_data = {
            "account": self.username,
            "pwd": self.password,
            "agreement_agreement": 0,
            "is_local": False,
        }

        resp = requests.post(
            f"{BASE_URL}/common/crosslogin",
            headers={
                "Content-Type": "application/json",
                "token": encode_dict_as_token(LOGIN_TOKEN),
            },
            data=json.dumps(req_data),
        )

        data = resp.json().get("data", None)
        if data is None:
            print("Data not found in response")
            sys.exit(1)

        req_data = {
            "id": self.power_station_id,
            "date": datetime.now().strftime(
                "%Y-%m-%d"
            ),  # today's date in YYYY-MM-DD format
            "full_script": False,
        }

        resp = requests.post(
            f"{BASE_URL}/Charts/GetPlantPowerChart",
            headers={
                "Content-Type": "application/json",
                "token": encode_dict_as_token(data),
            },
            data=json.dumps(req_data),
        )

        data = resp.json().get("data", None)
        if data is None:
            print("Data not found in response")
            sys.exit(1)

        last_data_point = data["lines"][0]["xy"][-1]

        self._attr_native_value = last_data_point["y"]
