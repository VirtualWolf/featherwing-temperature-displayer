import time
import wifi
import adafruit_requests
import socketpool
import busio
import board
import displayio
import adafruit_il0373
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

WIFI_NETWORK = 'Network name'
WIFI_NETWORK_PASSWORD = 'Network password'
API_ENDPOINT = 'http://example.com'

try:
    wifi.radio.connect(WIFI_NETWORK, WIFI_NETWORK_PASSWORD)

    print(wifi.radio.ipv4_address)

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool)

    displayio.release_displays()

    spi = busio.SPI(board.SCK, board.MOSI)

    # These two values may need to be changed depending on your board. See the pinout
    # diagram at https://learn.adafruit.com/adafruit-eink-display-breakouts/pinouts-2.
    # These are for a FeatherS2: https://www.adafruit.com/product/4769
    epd_cs = board.IO1
    epd_dc = board.IO3

    display_bus = displayio.FourWire(
        spi,
        command=epd_dc,
        chip_select=epd_cs,
        baudrate=1000000
    )
    time.sleep(1)

    DISPLAY_WIDTH=296
    DISPLAY_HEIGHT=128

    display = adafruit_il0373.IL0373(
        display_bus,
        width=DISPLAY_WIDTH,
        height=DISPLAY_HEIGHT,
        rotation=270,
        black_bits_inverted=True,
        color_bits_inverted=True,
        grayscale=True,
        refresh_time=1,
    )

    display_group = displayio.Group()

    large_font = bitmap_font.load_font('/fonts/pixellium-96.bdf', displayio.Bitmap)
    small_font = bitmap_font.load_font('/fonts/pixellium-80.bdf', displayio.Bitmap)

    outdoor_temperature = label.Label(large_font, text='     ')
    outdoor_temperature.anchor_point = (0.0, 1.0)
    outdoor_temperature.anchored_position = (4, (DISPLAY_HEIGHT / 2) - 6)

    outdoor_humidity = label.Label(small_font, text='   ')
    outdoor_humidity.anchor_point = (1.0, 1.0)
    outdoor_humidity.anchored_position = (DISPLAY_WIDTH - 4, (DISPLAY_HEIGHT / 2) - 6)

    indoor_temperature = label.Label(large_font, text='     ')
    indoor_temperature.anchor_point = (0.0, 1.0)
    indoor_temperature.anchored_position = (4, DISPLAY_HEIGHT - 4)

    indoor_humidity = label.Label(small_font, text='   ')
    indoor_humidity.anchor_point = (1.0, 1.0)
    indoor_humidity.anchored_position = (DISPLAY_WIDTH - 4, DISPLAY_HEIGHT - 4)

    display_group.append(outdoor_temperature)
    display_group.append(outdoor_humidity)
    display_group.append(indoor_temperature)
    display_group.append(indoor_humidity)
    display.show(display_group)

    while True:
        print('Getting data...')

        try:
            response = requests.get(API_ENDPOINT)
            data = response.json()
            response.close()

            outdoor_temperature.text = data['outdoor']['temperature'] + chr(176)
            outdoor_humidity.text = data['outdoor']['humidity']  + '%'
            indoor_temperature.text = data['indoor']['temperature']  + chr(176)
            indoor_humidity.text = data['indoor']['humidity'] + '%'

            display.refresh()
        except Exception as e:
            print(e)

        time.sleep(180)

except Exception as e:
    print(e)
