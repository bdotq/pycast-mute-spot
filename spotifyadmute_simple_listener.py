"""
simple Chromecast event listener that will mute Spotify during ads
"""

import argparse
import logging
import sys
import time
import pychromecast
import zeroconf

# Change to the friendly name of your cast device
CAST_NAME = "My Google Home"


class StatusListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_cast_status(self, status):
        print("[", time.ctime(), " - ", self.name, "] status chromecast change:")
        print(status)


class StatusMediaListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_media_status(self, status):
        print("[", time.ctime(), " - ", self.name, "] status media change:")
        #print(status)
        print("\nCurrent Title:", status.title)
        if status.title == "Advertising" or status.title == "Advertisement" or status.title == "Spotify":
            chromecast.set_volume_muted(True)
            print("Cast device is muted")
        else:
            chromecast.set_volume_muted(False)
            print("Cast device is unmuted")

        #print("\nMUTED:", chromecast.status.volume_muted)


parser = argparse.ArgumentParser(
    description="Example on how to create a simple Chromecast event listener."
)
parser.add_argument("--show-debug", help="Enable debug log", action="store_true")
parser.add_argument("--show-zeroconf-debug", help="Enable zeroconf debug log", action="store_true")
parser.add_argument(
    "--cast", help='Name of cast device (default: "%(default)s")', default=CAST_NAME
)
args = parser.parse_args()

if args.show_debug:
    logging.basicConfig(level=logging.DEBUG)
if args.show_zeroconf_debug:
    print("Zeroconf version: " + zeroconf.__version__)
    logging.getLogger("zeroconf").setLevel(logging.DEBUG)

chromecasts, browser  = pychromecast.get_listed_chromecasts(friendly_names=[args.cast])
if not chromecasts:
    print('No chromecast with name "{}" discovered'.format(args.cast))
    sys.exit(1)

chromecast = chromecasts[0]
# Start socket client's worker thread and wait for initial status update
chromecast.wait()

listenerMedia = StatusMediaListener(chromecast.name, chromecast)
chromecast.media_controller.register_status_listener(listenerMedia)

print("Mute Spotify on Ads\n")
input("Listening for cast events...\n\n")

# Shut down discovery
pychromecast.discovery.stop_discovery(browser)
