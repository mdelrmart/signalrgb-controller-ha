import logging
import requests
from homeassistant.components.light import (
    ATTR_EFFECT,
    LightEntity,
    SUPPORT_EFFECT
)
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, EFFECTS

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Configura la plataforma de luces virtuales."""
    light = VirtualLight(config)
    async_add_entities([light])

    # Guardamos la entidad en hass.data para que el servicio pueda acceder a ella
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["light_virtual"] = light


class VirtualLight(LightEntity):
    """Representación de la luz virtual con efectos."""

    def __init__(self, config):
        """Inicializar la luz virtual."""
        self._host = config[CONF_HOST]
        self._port = config[CONF_PORT]
        self._username = config[CONF_USERNAME]
        self._password = config[CONF_PASSWORD]
        self._state = False
        self._effect = "Solid Color"
        self._effect_params = {}

    @property
    def name(self):
        return "Virtual Light"

    @property
    def is_on(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORT_EFFECT

    @property
    def effect_list(self):
        """Lista de efectos disponibles."""
        return list(EFFECTS.keys())

    @property
    def effect(self):
        """Efecto actual."""
        return self._effect

    def turn_on(self, **kwargs):
        """Encender la luz y aplicar un efecto."""
        if ATTR_EFFECT in kwargs:
            self._effect = kwargs[ATTR_EFFECT]

        url = f"http://{self._host}:{self._port}/effect/apply/{self._effect.replace(' ', '%20')}"
        
        # Agregar los parámetros del efecto
        params = {"username": self._username, "password": self._password}
        for param in EFFECTS.get(self._effect, []):
            if param in kwargs:
                params[param] = kwargs[param]

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                self._state = True
            else:
                _LOGGER.error(f"Error al activar efecto {self._effect}. Código: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Error al activar efecto {self._effect}: {e}")

    def turn_off(self, **kwargs):
        """Apagar la luz (configurar color negro para que parezca apagada)."""
        url = f"http://{self._host}:{self._port}/effect/apply/Solid%20Color"
        params = {
            "color": "000000",
            "username": self._username,
            "password": self._password
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                self._state = False
            else:
                _LOGGER.error(f"Error al apagar la luz. Código: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Error al apagar la luz: {e}")

async def async_setup_entry(hass, entry):
    """Configurar la integración desde la UI."""

    async def handle_set_effect(call):
        """Manejar el servicio para cambiar efectos."""
        effect = call.data.get("effect")
        params = call.data.get("params", {})

        entity = hass.data[DOMAIN].get("light_virtual")
        if entity:
            entity.turn_on(effect=effect, **params)

    hass.services.async_register(DOMAIN, "set_effect", handle_set_effect)

    return True
