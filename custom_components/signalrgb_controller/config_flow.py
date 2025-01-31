import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD

class VirtualLightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Virtual Light."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user configuration step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Virtual Light", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT, default=8080): int,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
