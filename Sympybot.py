#!/usr/bin/env python3
import sys
import telebot
import time
from LaTeX2IMG import LaTeX2IMG
from time import sleep
from threading import current_thread
from sympy import *

TOKEN = ''


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            if text.startswith("/symbolic "):
                text = text.split("/symbolic ")[-1]
                command = "symbolic"
            elif text.startswith("/numeric "):
                text = text.split("/numeric ")[-1]
                command = "numeric"
            elif text.startswith("/plot "):
                text = text.split("/plot ")[-1]
                command = "plot"
            else:
                break

            tb.send_chat_action(chatid,'upload_document')

            filename = 'resultado' + current_thread().name

            ###########
            # Calculus or plot
            if command == "plot":
                try:
                    functions = text.split(" ")
                    p = plot(*functions,show=False,title=text,ylabel="")
                except SyntaxError:
                    tb.reply_to(m,"Sintaxis inválida")
                except:
                    tb.reply_to(m,"Error desconocido " + str(sys.exc_info()))
                else:
                    p.save(filename + '.png')
                    image = open(filename + '.png','rb')
                    tb.send_photo(chatid,image)
            else:
                try:
                    if command == "numeric":
                        output = latex(sympify(text).evalf())
                    else:
                        output = latex(sympify(text))
                except ValueError:
                    tb.reply_to(m,"No has escrito bien la expresión")
                except:
                    tb.reply_to(m,"Error desconocido " + str(sys.exc_info()))
                else:
                    LaTeX2IMG.main(['LaTeX2IMG',output,filename,'webp'])
                    result = open(filename + '.webp','rb')
                    tb.send_sticker(chatid, result)

with open("token.txt","r") as file:
    TOKEN = file.readline().strip()
# Init sympy session
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
##########
tb = telebot.TeleBot(TOKEN)
tb.set_update_listener(listener) #register listener
tb.polling(True)

while True: # Don't let the main Thread end.
    sleep(5)
