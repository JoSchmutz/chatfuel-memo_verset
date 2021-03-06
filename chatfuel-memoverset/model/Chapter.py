############# Made by Willy Konguem ##############
from model.Verse import Verse
import util

class Chapter:
    def __init__(self, book, chapter_number):
        self.chapter_number = chapter_number
        self.book = book

    def get_verses(self):
        list_verses = []
        url = util.Dbt.Dbt.get_api_url("/text/verse", {
            "dam_id": self.book.testament.damn_id,
            "book_id": self.book.code,
            "chapter_id": self.chapter_number
        })
        verses = util.Dbt.Dbt.get_request(url)
        for verse in verses:
            list_verses.append(Verse(self, verse['verse_id'], verse['verse_text']))
        return list_verses
