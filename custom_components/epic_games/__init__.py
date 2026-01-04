import logging
from typing import Optional, Union

import requests
from homeassistant import config_entries, core
from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryAuthFailed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .const import (
    BASE_URL,
    DOMAIN,
    CONF_LOCALE,
    CONF_COUNTRY,
    CONF_ALLOW_COUNTRIES,
)

PLATFORMS = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up Epic Games from a config entry."""

    data = await get_games(
        hass=hass,
        locale=entry.data.get(CONF_LOCALE),
        country=entry.data.get(CONF_COUNTRY),
        allow_countries=entry.data.get(CONF_ALLOW_COUNTRIES),
    )

    if not data:
        raise ConfigEntryAuthFailed("Invalid credentials or API error")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # API NUEVA (Home Assistant moderno)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_migrate_entry(
    hass: core.HomeAssistant, config_entry: config_entries.ConfigEntry
) -> bool:
    """Migrate old config entries."""

    hass.config_entries.async_update_entry(
        config_entry,
        data={
            CONF_LOCALE: config_entry.data.get(CONF_LOCALE),
            CONF_COUNTRY: config_entry.data.get(CONF_COUNTRY),
            CONF_ALLOW_COUNTRIES: config_entry.data.get(CONF_ALLOW_COUNTRIES),
        },
    )

    return True


async def get_games(
    hass, locale: str, country: str, allow_countries: str
) -> Union[dict, Optional[None]]:
    """Fetch free games from Epic Games API."""

    def get():
        url = (
            f"{BASE_URL}/freeGamesPromotions"
            f"?locale={locale}&country={country}&allowCountries={allow_countries}"
        )

        retry_strategy = Retry(
            total=3,
            status_forcelist=[400, 401, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)

        return session.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20,
        )

    response = await hass.async_add_executor_job(get)
    _LOGGER.debug("Epic Games API response: %s", response.text)

    if response.ok:
        return response.json()

    _LOGGER.error(
        "Epic Games API error %s: %s",
        response.status_code,
        response.text,
    )
    return None
