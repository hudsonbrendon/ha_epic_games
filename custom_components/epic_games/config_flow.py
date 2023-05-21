import voluptuous as vol
from homeassistant import config_entries

from . import get_games
from .const import CONF_LOCALE, CONF_COUNTRY, CONF_ALLOW_COUNTRIES, DOMAIN, VALID_LOCALES, VALID_COUNTRIES


DATA_SCHEMA: vol.Schema = vol.Schema(
    {
        vol.Optional(CONF_LOCALE): vol.In(VALID_LOCALES),
        vol.Optional(CONF_COUNTRY): vol.In(VALID_COUNTRIES),
        vol.Optional(CONF_ALLOW_COUNTRIES): vol.In(VALID_COUNTRIES),
    }
)


class EpicGamesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Epic Games config flow."""

    def __init__(self) -> None:
        """Initialize Epic Games config flow."""
        self.locale: str
        self.country: str
        self.allow_contries: str

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            if await get_games(
                hass=self.hass,
                locale=user_input.get(CONF_LOCALE),
                country=user_input.get(CONF_COUNTRY),
                allow_countries=user_input.get(CONF_ALLOW_COUNTRIES),
            ):
                self.locale = user_input.get(CONF_LOCALE)
                self.country = user_input.get(CONF_COUNTRY)
                self.allow_contries = user_input.get(CONF_ALLOW_COUNTRIES)

                return self.async_create_entry(
                    title=f"Epic Games {self.country}",
                    data={
                        CONF_LOCALE: self.locale,
                        CONF_COUNTRY: self.country,
                        CONF_ALLOW_COUNTRIES: self.allow_contries,
                    },
                )

            errors[CONF_LOCALE] = "locale_error"
            errors[CONF_COUNTRY] = "country_error"
            errors[CONF_ALLOW_COUNTRIES] = "allow_countries_error"

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                DATA_SCHEMA,
                user_input,
            ),
            errors=errors,
        )
