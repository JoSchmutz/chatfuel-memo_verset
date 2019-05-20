############# Made by Willy Konguem ##############
from nltk import word_tokenize
import ast
import random
# import scriptures
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


#print(Dbt.find_verse("DBY", "1Tim", 2, 1))

#print(Dbt.find_chapter("DBY", "1Tim", 2).get_verses())

#message = "Je voudrais lire 1Tim 12 verset 2"

message = "mathieu 10:15"

read_words = ["lire", "écouter", "lis moi", "lis"]

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

            search_verse = re.search(pattern_verse, v)
            if search_verse is not None:
                if search_verse.group("book_number") is None:
                    bk = search_verse.group("book_name")
                else:
                    bk = search_verse.group("book_number")+search_verse.group("book_name")
                verse = Dbt.find_verse("DBY", bk , search_verse.group("chapter_number"), search_verse.group("verse_number"))
                print('--------> '+verse.text)
                return [verse]
            else:
                print('------------> ')
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


# verse = str(Dbt.find_verse("DBY", "Jean", 3, 16))
# str_verse = verse[1:-1]
# new_vers = complexify_verse(2,str_verse)
# print(new_vers)
# # print(Dbt.find_verse("DBY", "Jean", 3, 16))
# verses = get_verse(message, read_words)
# print(verses)
# for verse in verses:
#    print("{} {} - verset {} : {}".format(verse.chapter.book.name, verse.chapter.chapter_number, verse.verse_number, verse.text))

# print(Dbt.get_random_verse("DBY"))
