import json
import matplotlib.pyplot as plt
import math
from chat_downloader import ChatDownloader
import webbrowser
import keyboard
import time

def get_keyword_frequency(comment_list, find_funny_comments):
    frequency_list = []
    num_comments = 0
    prev_offset_seconds = -1
    for index in range(len(comment_list)):
        offset_seconds = comment_list[index][0]
        message_body = comment_list[index][1]
        message_body_lowercase = comment_list[index][1].lower()

        if find_funny_comments:
            contains_keyword = ("omE" in message_body or "lmao" in message_body_lowercase or "lol" in message_body_lowercase or "omega" in message_body_lowercase or "lmfao" in message_body_lowercase or "haha" in message_body_lowercase or "kekw" in message_body_lowercase) and "gifted" not in message_body_lowercase
        else:
            contains_keyword = "?" in message_body_lowercase or "yo" in message_body_lowercase or "huh" in message_body_lowercase and "gifted" not in message_body_lowercase

        if prev_offset_seconds == offset_seconds and contains_keyword:
            num_comments+=1
        elif prev_offset_seconds != offset_seconds:
            frequency_list.append([offset_seconds,num_comments])
            prev_offset_seconds = offset_seconds
            if contains_keyword:
                num_comments = 1
            else:
                num_comments = 0
    return frequency_list

def plot_comment_list(comment_list):
    x_values = []
    y_values = []
    for i in range(0,len(comment_list)):
        x_values.append(comment_list[i][0])
        y_values.append(comment_list[i][1])
    plt.plot(x_values,y_values)
    plt.show()

def get_top_frequency_times(num_to_show, frequency_dict):
    top_times = []
    num_top_times = 0
    while num_top_times < num_to_show:
        top_frequency = 0
        top_seconds = -1
        top_stream_name = ""
        for stream_name in frequency_dict:
            current_stream_comment_list = frequency_dict[stream_name]
            for comment_num in range(len(frequency_dict[stream_name])):
                seconds = current_stream_comment_list[comment_num][0]
                frequency = current_stream_comment_list[comment_num][1]
                if frequency > top_frequency:
                    top_seconds = seconds
                    top_frequency = frequency
                    top_stream_name = stream_name
        if top_seconds != -1:
            top_times.append([top_stream_name, top_seconds, top_frequency])
            index = frequency_dict[top_stream_name].index([top_seconds, top_frequency])
            del frequency_dict[top_stream_name][index]
            # remove next/prev 10 seconds worth of frequencies
            for i in range(10):
                if len(frequency_dict[top_stream_name]) > index:
                    del frequency_dict[top_stream_name][index]
            for i in range(10):
                if len(frequency_dict[top_stream_name]) > index and (index - i - 1) > 0:
                    del frequency_dict[top_stream_name][index - i - 1]
        num_top_times+=1
    return top_times

def seconds_to_time(total_seconds):
    hours = math.trunc(total_seconds / (60*60))
    minutes = math.trunc(((total_seconds / (60*60)) - hours) * 60)   # remainder (in hours) * 60 to convert to minutes
    seconds = math.trunc((((total_seconds / (60*60)) - hours) * 60 - minutes) * 60) # min remainder * 60
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)

def open_top_streams(top_moments, links_dict):
    for i in range(len(top_moments)):
        dict_key = top_moments[i][0]
        url = links_dict[dict_key]
        seconds = top_moments[i][1]
        frequency = top_moments[i][2]
        print("-------------------------")
        print("time: " + seconds_to_time(seconds) + "    frequency: " + str(frequency))
        webbrowser.open(url)
        time.sleep(2)
        while not keyboard.is_pressed("w"):
            time.sleep(0.2)

    return

# loads chat and links
def load(streamer_name):
    # load links from json
    with open(streamer_name + "_stream_links.json", "r") as openfile:
        links_dict = json.load(openfile)
    # load chat from json
    with open(streamer_name + "_stream_chats.json", "r") as openfile:
        chat_dict = json.load(openfile)
    return chat_dict, links_dict

streamer_name = "jynxzi"
num_moments_to_show = 50
find_funny_comments = True

chat_dict, links_dict = load(streamer_name)
print("chats from all " + str(len(chat_dict)) + " streams have been loaded")
frequency_dict = {}
for dict_key in chat_dict:
    frequency = get_keyword_frequency(chat_dict[dict_key], find_funny_comments)
    frequency_dict[dict_key] = frequency
print("frequencies have been found... now finding top times")
top_moments = get_top_frequency_times(num_moments_to_show, frequency_dict)
print("press ctrl + w to get new clip")
open_top_streams(top_moments, links_dict)