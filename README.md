# Goodwe SEMS integration for Home Assistant

## Installation

Copy this folder to `<config_dir>/custom_components/goodwe_sems/`.

Add the following to your configuration.yaml file:
```
# Example configuration.yaml entry
sensor:
  - platform: goodwe_sems
```

## Dev

```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```