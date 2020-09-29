import inspect
import os
import re
import time
import pytest
from freezegun import freeze_time
from datetime import datetime
import session9 as s9
from unittest import TestCase
from decimal import Decimal


README_CONTENT_CHECK_FOR = ["odd_sec_run","log_func","authenticate","time_it","privilege","htmlize"]


def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 400, "Make your README.md file interesting! Add atleast 400 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r")
    content = f.read()
    f.close()
    assert content.count("#") >= 6

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(s9)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines" 

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(s9, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"


def test_docstring():
    functions = inspect.getmembers(s9, inspect.isfunction)

    for func in functions:
        assert not func.__doc__ is None, f"docstring not included in {func}"


def test_odd_sec_run():
    time = datetime.utcnow()

    @s9.odd_sec_run(time)
    def add(a,b):
        return a+b
    
    if time.second %2 == 0:
        assert add(1,3) == "it is odd time"+str(time)
    else:
        assert add(1,3) == 4

class TestLog(TestCase):
    def test_log(self):
        @s9.log_func
        def add(x):
            return x+2
        self.assertEqual(add(4),6)

log = TestLog()
log.test_log()

def test_authenticate():

    userpass = "Bond@007"
    @s9.authenticate(userpass)
    def plant_bomb():
        return "Authenticated"
    assert plant_bomb() == "Authenticated"
    userpass = "dont have access"

    with pytest.raises(ValueError):
        @s9.authenticate(userpass)
        def plant_bomb():
            return "Authenticated"


def test_time_it():
    @s9.time_it(5)
    def mul(a,b):
        return a*b
    assert mul(1,3) == 3, "Multiplication is working"