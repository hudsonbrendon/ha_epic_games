from datetime import timedelta

BASE_URL = "https://store-site-backend-static.ak.epicgames.com/"

ICON = "mdi:controller-classic"
CONF_LOCALE = "locale"
CONF_COUNTRY = "country"
CONF_ALLOW_COUNTRIES = "allow_countries"
SCAN_INTERVAL = timedelta(minutes=120)
DOMAIN = "epic_games"
DEFAULT_POSTER = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/1200px-Epic_Games_logo.svg.png"

VALID_LOCALES = [
    'en-US', 'en-GB', 'en-CA', 'en-AU', 'en-NZ',
    'es-ES', 'es-MX', 'es-AR', 'es-CL', 'es-CO', 'es-PE',
    'fr-FR', 'fr-CA',
    'de-DE', 'de-AT', 'de-CH',
    'it-IT',
    'pt-BR',
    'ru-RU',
    'pl-PL',
    'ko-KR',
    'ja-JP',
    'zh-CN', 'zh-TW',
]

VALID_COUNTRIES = [
    'US', 'CA', 'GB', 'AU', 'NZ',
    'ES', 'MX', 'AR', 'CL', 'CO', 'PE',
    'FR', 'CA',
    'DE', 'AT', 'CH',
    'IT',
    'BR',
    'RU',
    'PL',
    'KR',
    'JP',
    'CN', 'TW',
]
