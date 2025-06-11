import runpy
from script import *

def test_script():
    runpy.run_path("script.py")

def test_process_name():
    rawName = json.loads('{"use": "official", "family": "Dickens475", "given": ["Aaron697"], "prefix": ["Mr."]}')
    assert process_name(rawName) == "Mr. Aaron697 Dickens475"