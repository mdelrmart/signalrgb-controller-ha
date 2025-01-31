DOMAIN = "virtual_light"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Lista de efectos y sus parámetros configurables
EFFECTS = {
    "Solid Color": ["color"],  # Un solo color en formato HEX
    "Rainbow Rise": ["reverse", "scale", "speed", "xPos", "yPos"],
    "Color Cycle": [],
    "Fireworks": ["intensity", "speed"],
    "Strobe": ["speed", "color"],
}
