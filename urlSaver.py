import pyautogui
import keyboard
import win32clipboard
import json
import time

# hover over twitch vod you want to get the url of, then press "`"
# repeat until you got all the links you wanted. Press "s" to save to .json


# TODO: make it so I can keep going for different streamers. Don't need to restart for each streamer
def clear_clipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    return

def get_link_from_clipboard():
    win32clipboard.OpenClipboard()
    link = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return link

links = {}
streamer_name = "ninja"
link_num = 0
print("listening...")
while True:
    # get link
    if keyboard.is_pressed("`"):
        clear_clipboard()
        # open link in new tab
        pyautogui.keyDown("ctrl")
        pyautogui.click()
        pyautogui.keyUp("ctrl")
        # go to tab
        pyautogui.hotkey("ctrl", "tab")
        time.sleep(0.1)
        # copy link
        pyautogui.hotkey("ctrl", "l")
        pyautogui.hotkey("ctrl", "c")
        # close tab
        pyautogui.hotkey("ctrl", "w")
        # save link
        try:
            link = get_link_from_clipboard()
        except:
            pass
        else:
            links[streamer_name + str(link_num)] = link
            link_num+=1

            print("link " + str(link_num) + " obtained")
            time.sleep(0.3) # prevents accidentally getting/saving multiple times
    # save links
    if keyboard.is_pressed("s"):
        if streamer_name != "":
            # TODO: could maybe make sure every stream link is unique

            json_object = json.dumps(links,indent=4)
            with open(streamer_name + "_stream_links.json", "w") as outfile:
                outfile.write(json_object)
            print(streamer_name + "_stream_links.json saved")
            exit()