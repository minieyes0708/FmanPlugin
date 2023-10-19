import os, traceback
import fman.fs as fs
from fman.url import as_human_readable, as_url
from fman import DirectoryPaneCommand, QuicksearchItem, show_quicksearch
from fman import show_alert, show_prompt, show_status_message, load_json, save_json

SETTING_FILE = "Bookmarks.json"

def fuzzy_search(target, query, offset = 0):
    i, j = 0, 0
    result = []

    def eatup(i, j):
        while i+offset < len(target) and j < len(query) and target[i+offset] == query[j]:
            result.append(i+offset)
            i += 1
            j += 1
        return i, j
    def skip(i, j):
        while j < len(query) and query[j] == ' ': j += 1
        while i+offset < len(target) and j < len(query) and target[i+offset] != query[j]:
            i += 1
        return i, j
    
    while True:
        if j == len(query): return result
        if i+offset == len(target): return []
        if target[i+offset] == query[j]:
            i, j = eatup(i, j)
        elif i == 0 or query[j] == ' ':
            i, j = skip(i, j)
        else:
            return fuzzy_search(target, query, result[0]+1)

class BookmarkEditSettings(DirectoryPaneCommand):
    def __call__(self):
        filepath = load_json(SETTING_FILE)['bookmark list file path']
        os.system(f'code {filepath}')

class BookmarksList(DirectoryPaneCommand):
    def __call__(self):
        self.bookmarks = [v.strip() for v in open(load_json(SETTING_FILE)['bookmark list file path'], encoding='utf8').readlines()]
        result = show_quicksearch(self._listing)
        if result:
            self.pane.set_path(as_url(result[1]))
    def _listing(self, query):
        if query.strip():
            for item in self.bookmarks:
                index = fuzzy_search(item, query)
                if index:
                    yield QuicksearchItem(item, highlight=index)
        else:
            for item in self.bookmarks:
                yield QuicksearchItem(item)

class BookmarkAdd(DirectoryPaneCommand):
    def __call__(self):
        filepath = load_json(SETTING_FILE)['bookmark list file path']
        bookmarks = [v.strip() for v in open(load_json(SETTING_FILE)['bookmark list file path'], encoding='utf8').readlines()]
        current_folder = as_human_readable(self.pane.get_path()).replace('\\', '/')
        if current_folder not in bookmarks:
            bookmarks.append(current_folder)
            show_alert(current_folder + ' added to bookmarks')
        bookmarks.sort()
        open(filepath, 'w', encoding='utf8').write('\n'.join(bookmarks))

class BookmarkDelete(DirectoryPaneCommand):
    def __call__(self):
        filepath = load_json(SETTING_FILE)['bookmark list file path']
        self.bookmarks = [v.strip() for v in open(load_json(SETTING_FILE)['bookmark list file path'], encoding='utf8').readlines()]
        result = show_quicksearch(self._listing)
        if result:
            if result[1] in self.bookmarks:
                self.bookmarks.remove(result[1])
                open(filepath, 'w', encoding='utf8').write('\n'.join(self.bookmarks))
    def _listing(self, query):
        if query.strip():
            for item in self.bookmarks:
                index = fuzzy_search(item, query)
                if index:
                    yield QuicksearchItem(item, highlight=index)
        else:
            for item in self.bookmarks:
                yield QuicksearchItem(item, highlight=index)