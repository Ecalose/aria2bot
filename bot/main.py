

import telebot
#import config
import os
from modules.delete import file_del
from modules.new_download import the_download
from modules.resume import file_resume
from modules.pause import file_pause
import threading

Telegram_bot_api=os.environ.get('Telegram_bot_api')
Telegram_user_id=os.environ.get('Telegram_user_id')

bot = telebot.TeleBot(Telegram_bot_api)
BOT_name=bot.get_me().username
'''command = [BotCommand("status","查看所有种子状态"),
           BotCommand("down", "后接磁力链接，下载种子"),
           BotCommand("resume", "后接hash，继续种子任务"),
           BotCommand("pause", "后接hash，暂停种子任务"),
           BotCommand("del", "后接hash，删除种子")]
print(bot.set_my_commands(commands=command))'''


@bot.callback_query_handler(func=lambda call: "Pause" in call.data)
def add_pause(call):
    try:
        print(call)
        caption = str(call.message.text)
        print(caption)
        print(call.data)
        key_data=str(call.data).replace("Pause ","")
        print(key_data)
        text=file_pause(key_data)
        bot.answer_callback_query(callback_query_id=call.id,text=text,cache_time=3)
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: "Resume" in call.data)
def add_resume(call):
    try:
        print(call)
        caption = str(call.message.text)
        print(caption)
        print(call.data)
        key_data=str(call.data).replace("Resume ","")
        print(key_data)
        text=file_resume(key_data)
        bot.answer_callback_query(callback_query_id=call.id,text=text,cache_time=3)
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: "Remove" in call.data)
def add_del(call):
    try:
        print(call)
        caption = str(call.message.text)
        print(caption)
        print(call.data)
        key_data=str(call.data).replace("Remove ","")
        print(key_data)
        text=file_del(key_data)
        bot.answer_callback_query(callback_query_id=call.id,text=text,cache_time=3)
    except Exception as e:
        print(e)

@bot.message_handler(commands=['del'],func=lambda message:str(message.chat.id) == str(Telegram_user_id))
def start_del(message):

        keywords = str(message.text)
        if str(BOT_name) in keywords:
            keywords = keywords.replace(f"/del@{BOT_name} ", "")
            print(keywords)
            result_text=file_del(keywords)
            bot.send_message(chat_id=message.chat.id,text=result_text)

        else:
            keywords = keywords.replace(f"/del ", "")
            print(keywords)
            result_text=file_del(keywords)
            print(result_text)
            #bot.send_message(chat_id=message.chat.id,text=result_text)

@bot.message_handler(commands=['magnet'],func=lambda message:str(message.chat.id) == str(Telegram_user_id))
def start_download(message):
    try:
        keywords = str(message.text)
        if str(BOT_name) in keywords:
            keywords = keywords.replace(f"/magnet@{BOT_name} ", "")
            print(keywords)
            t1 = threading.Thread(target=the_download, args=(keywords,message))
            t1.start()
        else:
            keywords = keywords.replace(f"/magnet ", "")
            print(keywords)
            t1 = threading.Thread(target=the_download, args=(keywords,message))
            t1.start()

    except:
        print("down函数错误")

@bot.message_handler(commands=['status'],func=lambda message:message.chat.type == "private")
def start_status(message):
    try:
        keywords = str(message.text)
        if keywords==f"/status@{BOT_name}":
            print("全部种子")

        elif str(BOT_name) in keywords:
            # print(message.chat.type)
            keywords = keywords.replace(f"/status@{BOT_name} ", "")
            print("单个种子")

        elif keywords=="/status":
            print("全部种子")

        else:

            keywords = keywords.replace(f"/status ", "")
            print("单个种子")


    except:
        print("status函数报错")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(BOT_name)
    bot.send_message(chat_id=Telegram_user_id,text="bot已上线")
    bot.polling()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/