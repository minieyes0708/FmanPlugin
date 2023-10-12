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