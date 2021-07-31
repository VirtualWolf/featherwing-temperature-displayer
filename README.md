# featherwing-temperature-displayer
A CircuitPython script used to pull temperature and humidity data from an HTTP endpoint and update a [2.9" greyscale e-ink FeatherWing](https://www.adafruit.com/product/4777) that's attached to a [FeatherS2](https://www.adafruit.com/product/4769).

## Usage
Update the `WIFI_NETWORK`, `WIFI_NETWORK_PASSWORD`, and `API_ENDPOINT` values at the top of the script as appropriate. The endpoint should return data in the following format:

```
{
    "outdoor": {
        "temperature": "17.8",
        "humidity": "35"
    },
    "indoor": {
        "temperature": "20.2",
        "humidity": "50"
    }
}
```

Copy `code.py` and the `fonts` and `lib` directories to the `CIRCUITPY` volume when the FeatherS2 is attached to the computer.

The display will update every three minutes.

## Credits
The font [Pixellium](https://www.fontspace.com/pixellium-font-f30306) used in this project is licensed as Creative Commons (by-nd) Attribution No Derivatives.
