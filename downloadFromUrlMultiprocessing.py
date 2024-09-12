from chat_downloader import ChatDownloader
import json
import multiprocessing

def load_from_links(streamer_name):
    # load links from json
    with open(streamer_name + "_stream_links.json", "r") as openfile:
        links_dict = json.load(openfile)
    # get chat for every link in dict, copy essential items, save to new dict
    chat_dict = {}
    downloader = ChatDownloader()
    for dict_key in links_dict:
        url = links_dict[dict_key]
        try:
            chat = downloader.get_chat(url, message_groups=["messages"])
        except:
            continue
        message_list = [] # contains seconds and text of each message
        prev_commenter_names = []
        prev_seconds = -1
        for message in chat:
            # use try b/c sometimes messages don't have seconds/text/name and will raise error
            try:
                seconds = message["time_in_seconds"]
                text = message["message"]
                commenter_name = message["author"]["name"]
            except:
                pass
            else:
                if prev_seconds == seconds:
                    if commenter_name not in prev_commenter_names:
                        message_list.append((seconds, text))
                        prev_commenter_names.append(commenter_name)
                else:
                    prev_seconds = seconds
                    prev_commenter_names = []
                    message_list.append((seconds, text))
        # copy trimmed down chat
        chat_dict[dict_key] = message_list
        print(dict_key + " saved")

    return chat_dict

def download_json(streamer_name):
    chat_dict = load_from_links(streamer_name)
    json_object = json.dumps(chat_dict,indent=4)
    with open(streamer_name + "_stream_chats.json", "w") as outfile:
        outfile.write(json_object)
    print(streamer_name + "_stream_chats.json saved")
    return

if __name__ == '__main__':
    streamer_names = ["ninja","clix","jynxzi","stableronaldo"]

    process_dict = {}
    for i in range(len(streamer_names)):
        process_dict[str(i)] = multiprocessing.Process(target=download_json, args=(streamer_names[i],))
    for dict_key in process_dict:
        process_dict[dict_key].start()
    for dict_key in process_dict:
        process_dict[dict_key].join()

# TODO: use multiprocessing to speed up for one streamer