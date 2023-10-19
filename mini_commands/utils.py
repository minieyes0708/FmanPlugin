import os
import fman.fs as fs
from fman.url import as_url

class EnterPath:
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(self.path)
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.cwd)

def edit_with_code(original_input):
    tmpfilename = 'tmp'
    open(tmpfilename, 'w').write(original_input)
    os.system(f'code --wait {tmpfilename}')
    result = open(tmpfilename, 'r').read()
    fs.delete(as_url(os.path.join(os.getcwd(), tmpfilename)))
    return result

def fuzzy_search(target, query, offset = 0):
    i, j = 0, 0
    result = []

    def eatup(i, j):
        while i < len(target) and j < len(query) and target[i] == query[j]:
            result.append(i + offset)
            i += 1
            j += 1
        return i, j
    def skip(i, j):
        while j < len(query) and query[j] == ' ': j += 1
        while i < len(target) and j < len(query) and target[i] != query[j]:
            i += 1
        return i, j
    
    while True:
        if j == len(query): return result
        if i == len(target): return []
        if target[i] == query[j]:
            i, j = eatup(i, j)
        elif i == 0 or query[j] == ' ':
            i, j = skip(i, j)
        else:
            return fuzzy_search(target[result[0]+1:], query, result[0]+1)