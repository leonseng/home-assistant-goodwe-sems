from homeassistant import config_entries
from .const import DOMAIN
import voluptuous as vol

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): str,
        vol.Required("power_station_id"): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, info):
        if info is not None:
            pass  # TODO: process info

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
