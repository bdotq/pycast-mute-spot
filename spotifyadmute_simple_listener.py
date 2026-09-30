"""
simple Chromecast event listener that will mute Spotify during ads and skip some News briefing ads
"""

import argparse
import logging
import sys
import time
import pychromecast
import zeroconf
import threading


# Change to the friendly name of your cast device
CAST_NAME = "Google Home"


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
        self.command_lock = threading.Lock()


    def new_media_status(self, status):
        # Ignore this callback if another command is already running
        if not self.command_lock.acquire(blocking=False):
            return

        print("[", time.ctime(), " - ", self.name, "] status media change:")
        #print(status)
        print("Current title:", status.title or "",
            ", Artist:", status.artist or "",
            ", Album:", status.album_name or ""
        )
        threading.Thread(
            target=self.handle_media,
            args=(status,),
            daemon=True,
        ).start()
        #time.sleep(0.5)


    def handle_media(self, status):
        #time.sleep(1)
        is_title = False
        is_current_time = False
        is_duration = False
        is_pubilsher = False
        is_content_id = False
        isCidSpotifyAd = False
        try:
            if status.title:
                is_title = True
        #except pychromecast.error.RequestTimeout as error:
        except Exception as error: pass #print(error) #missing variable title
        try:
            if status.current_time:
                is_current_time = True
        except Exception as error: pass #print(error) #missing variable current_time
        try:
            if status.duration:
                is_duration = True
        except Exception as error: pass #print(error) #missing variable duration
        try:
            if status.media_custom_data["publisher"]:
                is_pubilsher = True
        except Exception as error: pass #print(error) #missing variable duration
        try:
            if status.content_id:
                is_content_id = True
        except Exception as error: pass #print(error) #missing variable duration


        try:
            if is_title and is_duration and is_current_time:
                #print("Time: " + str(int(status.current_time//60))+":"+str(int(status.current_time%60)) + "/" + str(int(status.duration//60))+":"+str(int(status.duration%60)) )
                if status.title == "CNBC":
                    if status.current_time < 15.0:
                        chromecast.media_controller.seek(15.0)
                        print("SKIP AD 15s start\n")
                    if status.current_time > (status.duration - 23.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 22s end\n")
                elif status.title == "CNBC Tech Check":
                    if status.current_time < 7.0:
                        chromecast.media_controller.seek(8.0)
                        print("SKIP AD 8s start\n")
                    if status.current_time > (status.duration - 21.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 21s end\n")

            if is_pubilsher and is_duration and is_current_time:
                print("Publisher: " + status.media_custom_data["publisher"] + " - Time: " + str(int(status.current_time//60))+":"+str(int(status.current_time%60)) + "/" + str(int(status.duration//60))+":"+str(int(status.duration%60)) )
                cbc = "CBC News: The World at Six"
                if status.media_custom_data["publisher"] == "The World in Brief from The Economist":
                    if status.current_time < 40.0:
                        chromecast.media_controller.seek(40.0)
                        print("SKIP AD 40s start\n")
                    if status.current_time > (status.duration - 48.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 48s end\n")
                elif status.media_custom_data["publisher"] == "WSJ Tech News Briefing":
                    if status.current_time < 30.0:
                        chromecast.media_controller.seek(25.0)
                        print("SKIP AD 25s start\n")
                    if status.current_time > (status.duration - 33.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 33s end\n")
                elif status.media_custom_data["publisher"] == "Engadget":
                    if status.current_time < 32.0:
                        chromecast.media_controller.seek(32.0)
                        print("SKIP AD 32s start\n")
                    if status.current_time > (status.duration - 30.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 30s end\n")
                elif status.media_custom_data["publisher"] == "TechCrunch Startups - Spoken Edition":
                    if status.current_time < 41.0:
                        chromecast.media_controller.seek(41.0)
                        print("SKIP AD 41s start\n")
                    if status.current_time > (status.duration - 7.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 7s end\n")
                elif status.media_custom_data["publisher"] == "Bloomberg News Now":
                    if status.current_time < 30.0:
                        chromecast.media_controller.seek(30.0)
                        print("SKIP AD 30s start\n")
                    if status.current_time > (status.duration - 62.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 62s end\n")
                elif status.media_custom_data["publisher"] == cbc:
                    if status.current_time < 30.0:
                        chromecast.media_controller.seek(30.0)
                        print("SKIP AD 30s start\n")
                elif status.media_custom_data["publisher"] == "TechCrunch":
                    if status.current_time < 60.0:
                        chromecast.media_controller.seek(60.0)
                        print("SKIP AD 60s start\n")
                elif status.media_custom_data["publisher"] == "The Exchange":
                    if status.current_time < 45.0:
                        chromecast.media_controller.seek(45.0)
                        print("SKIP AD 45s start\n")
                    if status.current_time > (status.duration - 15.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 15s end\n")
                elif status.media_custom_data["publisher"] == "Reuters TV (U.S.)":

                    if status.current_time > (status.duration - 60.0):
                        chromecast.media_controller.seek(status.duration - 1)
                        print("SKIP AD 60s end\n")



            if is_content_id:
                isCidSpotifyAd = status.content_id.startswith("spotify:ad")
            if is_title or isCidSpotifyAd:
                #print("contentid:", status.content_id)
                if isCidSpotifyAd or status.title == "Advertising" or status.title == "Advertisement" or status.title == "Spotify":
                    chromecast.set_volume_muted(True)
                    print("Cast device is muted")
                else:
                    chromecast.set_volume_muted(False)
                    print("Cast device is unmuted")
                #print("\nMUTED:", chromecast.status.volume_muted)
        except Exception as error:
            print(error)
        finally:
            self.command_lock.release()


print("Mute Google Cast on Ads\n")

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

print("Searching for " + args.cast + "...")
chromecasts, browser  = pychromecast.get_listed_chromecasts(friendly_names=[args.cast],discovery_timeout=30)
if not chromecasts:
    print('No chromecast with name "{}" discovered...\n'.format(args.cast))
    devices, browser = pychromecast.get_chromecasts(timeout=30)
    if devices:
        print("Other devices found: (and connecting to the first one)")
        chromecast = devices[0]
    else:
        pychromecast.discovery.stop_discovery(browser)
        sys.exit(1)

    for cast in devices:
        print(
            f"{cast.cast_info.friendly_name} "
            f"({cast.cast_info.model_name}) — "
            f"{cast.cast_info.host}:{cast.cast_info.port}"
    )


else:
    chromecast = chromecasts[0]
# Start socket client's worker thread and wait for initial status update
chromecast.wait()

listenerMedia = StatusMediaListener(chromecast.name, chromecast)
chromecast.media_controller.register_status_listener(listenerMedia)


input("Connected. Listening for cast events...\n\n")

# Shut down discovery
pychromecast.discovery.stop_discovery(browser)
