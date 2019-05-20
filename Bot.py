############# Made by Willy Konguem ##############
from nltk import word_tokenize
import ast
import random
import scriptures
import sys
import time
import urllib

from urllib.request import urlopen
from flask import Flask, request, session
import requests
import sys
import os
import json

from util.Dbt import Dbt
import re

import discord
from util.Dbt import Dbt
import re
import time
TOKEN = 'NTQ1MzYyNzMxODA1NDQyMDk4.D0YleA.v1od-EncHrNwpD0yRaWuy224qg0'

client = discord.Client()

read_verse_words = ["lire", "écouter", "lis moi", "lis"]

read_random_word = ["hasard", "aléatoire"]

def get_chapter_verses(message, read_words, query):
    pattern_chapter = "(?P<book_number>\d)*(\s)*(?P<book_name>\w+)(\s)+(?P<chapter_number>\d)+"
    search_chapter = re.search(pattern_chapter, query)
    if search_chapter is not None:
        if search_chapter.group("book_number") is None:
            bk = search_chapter.group("book_name")
        else:
            bk = search_chapter.group("book_number") + search_chapter.group("book_name")
        verses = Dbt.find_chapter("DBY", bk, search_chapter.group("chapter_number")).get_verses()
        return verses
    else:
        return []

def get_verse(message, read_words):
    for rwrod in read_words:
        if rwrod in message:
            v = message.split(rwrod,1)[1]
            v = v.strip()

            pattern_verse = "(?P<book_number>\d)*(\s)*(?P<book_name>\w+)(\s)+(?P<chapter_number>\d)+(\s)*([-|verset|v|\.|,])+(\s)*(?P<verse_number>\d)+"
            pattern_chapter = "(?P<book_number>\d)*(\s)*(?P<book_name>\w+)(\s)+(?P<chapter_number>\d)+"
            search_verse = re.search(pattern_verse, v)
            if search_verse is not None:
                if search_verse.group("book_number") is None:
                    bk = search_verse.group("book_name")
                else:
                    bk = search_verse.group("book_number")+search_verse.group("book_name")
                verse = Dbt.find_verse("DBY", bk , search_verse.group("chapter_number"), search_verse.group("verse_number"))
                return [verse]
            else:
                return get_chapter_verses(message, read_words, v)

def complexify_verse(complexity, verse_final):

    tuple_complexity = (0, 1, 2, 3, 4, 5)
    if complexity in tuple_complexity:
        verse_list = verse_final.split()
        if complexity == 1:
            part = 0.2 * len(verse_list)
            part = int(part)
        elif complexity == 2:
            part = 0.4 * len(verse_list)
            part = int(part)
        elif complexity == 3:
            part = 0.6 * len(verse_list)
            part = int(part)
        elif complexity == 4:
            part = 0.8 * len(verse_list)
            part = int(part)
        elif complexity == 5:
            part = 1.0 * len(verse_list)
            part = int(part)
        elif complexity == 0:
            part = 0
        list_index = random.sample(range(len(verse_final.split())), part)

        for index in list_index:
            length = len(verse_list[index])
            verse_list[index] = "_"*length

        complexified_verse = ' '.join(verse_list)

        # complexified_verse = complexified_verse+"_complexity_"+str(complexity)
        return complexified_verse
        #return str(resp)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.lower().startswith('bonjour'):
        msg = 'Bonjour {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    elif any(ext in message.content.lower() for ext in read_random_word):
        verse = Dbt.get_random_verse("DBY")
        await client.send_message(message.channel, "{} {} - verset {} : {}".format(verse.chapter.book.name, verse.chapter.chapter_number,
                                                                  verse.verse_number, verse.text))

    elif any(ext in message.content.lower() for ext in read_verse_words):
        verses = get_verse(message.content.lower(), read_verse_words)
        # verses_complexified = verses.split()
        # list_index = random.sample(range(len(verses.split())), part)
        # for index in list_index:
        #     length = len(verse_list[index])
        #     verse_list[index] = "_"*length

        # verse_final = ' '.join(verse_list)
        # print()
        # print(verses_complexified)
        # for verse in verses:
        #     await client.send_message(message.channel, "{} {} - verset {} : {}".format(verse.chapter.book.name, verse.chapter.chapter_number, verse.verse_number, verse.text))

        for i in range(3):
            time.sleep(10)
            for verse in verses:
                str_verse = str(verse)[1:-2]
                complex_verse = complexify_verse(3,str_verse)
                await client.send_message(message.channel, complex_verse)
                # await client.send_message(message.channel, "{} {} - verset {} : {}".format(verse.chapter.book.name, verse.chapter.chapter_number, verse.verse_number, verse.text))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
