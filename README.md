![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg) [![BuyMeCoffee][buymecoffeebedge]][buymecoffee] [![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

# Epic Games Custom Integration Home Assistant

Custom integration for the Home Assistant to obtain information present in [epicgames.com](https://www.epicgames.com/).

## Install

### Installation via HACS

Have HACS installed, this will allow you to update easily.

Adding Epic Games to HACS can be using this button:

[![image](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=hudsonbrendon&repository=ha_epic_games&category=integration)

If the button above doesn't work, add `https://github.com/hudsonbrendon/ha_epic_games` as a custom repository of type Integration in HACS.

- Click Install on the `Epic Games` integration.
- Restart the Home Assistant.

### Manual installation

- Copy `epic_games` folder from [latest release](https://github.com/hudsonbrendon/ha_epic_games/releases/latest) to your `<config dir>/custom_components/` directory.
- Restart the Home Assistant.

## Configuration

Adding Epic Games to your Home Assistant instance can be done via the UI using this button:

[![image](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=epic_games)

### Manual Configuration

If the button above doesn't work, you can also perform the following steps manually:

- Navigate to your Home Assistant instance.
- In the sidebar, click Settings.
- From the Setup menu, select: Devices & Services.
- In the lower right corner, click the Add integration button.
- In the list, search and select `Epic Games`.
- Follow the on-screen instructions to complete the setup.

## Debugging

To enable debug for Epic Games integration, add following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.epic_games: debug
```

## Make a card

To view Epic Games information, follow an example of a card. Remember to install the [upcoming-media-card](https://github.com/NemesisRE/upcoming-media-card)

```yaml
type: custom:upcoming-media-card
entity: sensor.epic_games
title: Epic Games
max: 10
image_style: fanart
date: ddmm
line1_text: "Metacritic: $rating"
```

After setup, the card above will look like this:

![image](https://github.com/hudsonbrendon/ha_epic_games/assets/5201888/8aef226f-bae3-48f4-82b1-2d09b1990e2d)

[buymecoffee]: https://www.buymeacoffee.com/hudsonbrendon
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
