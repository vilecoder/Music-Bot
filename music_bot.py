import telebot
import os
import yt_dlp as youtube_dl
import re


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]','_',filename)

API_TOKEN ='7817382079:AAEbs1E5DmLfcGrc8Le5d_mOz5LegRDuffo'
bot = telebot.TeleBot(API_TOKEN)# bot is a object /instance of Telebot class using API token here which allows us to send/recieve message through tg bot

download_dirc=r"C:\Users\Harsh Vardhan\Desktop\Music bot\downloads"

if not os.path.exists(download_dirc):
    os.makedirs("downloads")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Welcome to the Music Bot ! send me name of the song and i will download it for you.")

@bot.message_handler(func=lambda message:True)
def search_song(message):
    search_query = message.text
    bot.reply_to(message,f"Searching for {search_query}...")

    ydl_options={
        "format":"bestaudio/best",
        "postprocessors":[{
            "key":"FFmpegExtractAudio",
            "preferredcodec":"mp3",
            "preferredquality":"128",
            }],
        "outtmpl":f"{download_dirc}/%(title)s.%(ext)s",
        "noplaylist":True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info_dict=ydl.extract_info(f"ytsearch:{search_query}",download = True)
            video_title = info_dict["entries"][0]["title"]
            sanitized_title=sanitize_filename(video_title)
            file_name= f"{download_dirc}/{sanitized_title}.mp3"

    
        with open(file_name,"rb") as audio:
            bot.send_audio(message.chat.id,audio,timeout=60)

        os.remove(file_name)

    except Exception as e:
        bot.send_message(message.chat.id,f"an error occured {e}")
        if os.patg.exists(file_name):
            os.remove(file_name)


bot.polling()
