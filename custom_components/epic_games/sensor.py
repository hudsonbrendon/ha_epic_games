import logging
from typing import List

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from aiohttp import ClientSession
from homeassistant import config_entries, const, core
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.util.dt import utc_from_timestamp
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .const import (
    BASE_URL,
    CONF_COUNTRY,
    CONF_LOCALE,
    CONF_ALLOW_COUNTRIES,
    DEFAULT_POSTER,
    DOMAIN,
    ICON,
    SCAN_INTERVAL,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_LOCALE): cv.string,
        vol.Required(CONF_COUNTRY): cv.string,
        vol.Required(CONF_ALLOW_COUNTRIES): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    """Setup sensor platform."""
    config = hass.data[DOMAIN][config_entry.entry_id]

    session = async_get_clientsession(hass)
    sensors = [
        EpicGamesSensor(
            locale=config[CONF_LOCALE],
            country=config[CONF_COUNTRY],
            allow_countries=config[CONF_ALLOW_COUNTRIES],
            name="Epic Games",
            session=session,
        )
    ]
    async_add_entities(sensors, update_before_add=True)


class EpicGamesSensor(Entity):
    """epicgames.com Sensor class"""

    def __init__(
        self,
        locale: int,
        country: str,
        allow_countries: str,
        name: str,
        session: ClientSession,
    ) -> None:
        self._locale = locale
        self._country = country
        self._allow_countries = allow_countries
        self.session = session
        self._name = name
        self._games = [
            {
                "title_default": "$title",
                "line1_default": "$rating",
                "line2_default": "$release",
                "line3_default": "$runtime",
                "line4_default": "$studio",
                "icon": "mdi:arrow-down-bold",
            }
        ]
        self._last_updated = const.STATE_UNKNOWN

    @property
    def locale(self) -> str:
        return self._locale

    @property
    def country(self) -> str:
        return self._country

    @property
    def allow_countries(self) -> str:
        return self._allow_countries

    @property
    def url(self):
        return f"{BASE_URL}/freeGamesPromotions?locale={self.locale}&country={self.country}&allowCountries={self.allow_countries}"

    @property
    def name(self) -> str:
        """Name."""
        return "Epic Games"

    @property
    def state(self) -> str:
        """State."""
        return len(self.games)

    @property
    def last_updated(self):
        """Returns date when it was last updated."""
        if self._last_updated != "unknown":
            stamp = float(self._last_updated)
            return utc_from_timestamp(int(stamp))

    @property
    def games(self) -> List[dict]:
        """Games."""
        return self._games

    @property
    def icon(self) -> str:
        """Icon."""
        return ICON

    @property
    def extra_state_attributes(self) -> dict:
        """Attributes."""
        return {
            "data": self.games,
        }

    def update(self) -> None:
        """Update sensor."""
        _LOGGER.debug("%s - Running update", self.name)
        retry_strategy = Retry(
            total=3,
            status_forcelist=[400, 401, 500, 502, 503, 504],
            method_whitelist=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)

        games = http.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        parsed_games = games.json()["data"]["Catalog"]["searchStore"]["elements"]

        if games.ok:
            self._games.extend(
                [
                    dict(
                        title=game.get("title", "Não informado"),
                        poster=game["keyImages"][0]["url"]
                        if game["keyImages"]
                        else DEFAULT_POSTER,
                        synopsis=game.get("description", "Não informado"),
                        director=game.get("director", "Não informado"),
                        cast=game.get("cast", "Não informado"),
                        studio=game.get("distributor", "Não informado"),
                        genres=game.get("genres", "Não informado"),
                        runtime=game.get("duration", "Não informado"),
                        rating=game.get("contentRating", "Não informado"),
                        release="$date",
                        airdate=game["viewableDate"].split("T")[0],
                        city=game.get("city", "Não informado"),
                        ticket=game.get("siteURL", "Não informado"),
                    )
                    for game in parsed_games
                ]
            )
            _LOGGER.debug("Payload received: %s", games.json())
        else:
            _LOGGER.debug("Error received: %s", games.content)
