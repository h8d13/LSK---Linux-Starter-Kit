Make sure python is installed on the system

> In VS code create a new file called hello.py
> In the bottom right you should now see python being detected 
> You can click it it should open the explorer window (useful to launch other programs) 
> Also make sure to naviguate to extensions and find the official python by microsoft extension

You can now create your first venv (virtual environment)

There should be a "+' Create Virtual Environment
This is also where you can chose other python versions if you have them. 

It will be created in what we call "cwd" current working directory. 
Meaning a folder! So just make sure you created one with a descriptive name for what you're trying to achieve. 

---

You can now start coding in a more secure way than interacting with operating system directly!

For good practice you want to make sure to track the versions of what you are using for example: 
```
requests==2.28.1
pandas>=1.5.0,<2.0.0
numpy~=1.23.0 
````

This is useful because you can use the same code in 3 or even 30 years. 

----

Project structures:

Here is a bit of a gray area, depending especially on the scale fo what you're attempting. 

For a small project you might not need more than:
```
/project_folder/
├── script.py
├── config.json
└── requirements.txt
```

While for a slightly larger code base: 

```
/project_folder/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   └── test_main.py
```

Python introduced another concept that makes it possible to create larger codebases without even have to do __init__ files (while useful) I really like to code without them sometimes.

```
/project_folder/
├── src/
│   └── myapp/
│       ├── api/
│       │   ├── routes.py
│       │   ├── auth.py
│       │   └── validators.py
│       │
│       ├── core/
│       │   ├── models.py
│       │   ├── services.py
│       │   └── database.py
│       │
│       ├── utils/
│       │   ├── helpers.py
│       │   └── logging.py
│       │
│       └── main.py
```

Basically init files are way to do what is above implicitely:

``` 
mypackage/__init__.py
from .user import User  # Chose what to expose
from .utils import helper_function
``` 

Then you can call it from your main script.

Why the above is important is because:

from mypackage.subpackage.module.file import function
is not as clean as from mypackage import function

---

But if you do decide to go without init files well you will have to be careful when importing other scripts.

I've made an imports folder that show this with a simple example. 

The main difference is that without init files your imports will look longer (and are not loaded until needed? I think): 

from calc.operations import add, substract
WHERE > FOLDER.SCRIPT > function

What I like to do is go without init files until there is a feature that is repeatable for example:

````
/project_folder/
├── filters/
│   ├── __init__.py
│   ├── basic/
│   │   ├── blur.py
│   │   ├── sharpen.py
│   │   ├── contrast.py
│   │   └── brightness.py
│   └── artistic/
│       ├── sepia.py
│       ├── vintage.py
│       ├── noir.py
│       └── vignette.py
├── utils/
│   └── image_loader.py
├── main.py
└── requirements.txt
````

Now this WILL simplify your life.

from .basic.blur import GaussianBlur
from .basic.sharpen import Sharpen
from .artistic.sepia import Sepia
from .artistic.vintage import Vintage

instead of 

from filters.basic.blur import GaussianBlur
from filters.basic.sharpen import Sharpen
from filters.artistic.sepia import Sepia
from filters.artistic.vintage import Vintage

Now that imports hopefully make a little more sense to you:

**For imports from pip packages be careful to read their docs to see usages of specific features**

You can also from X import * but it's never recommended. Better to import in the right places the right component for optimization reasons.

----

### Properly naming:

FOR FOLDERS
```
My-Package     # No hyphens
MyPackage      # No PascalCase
my.package     # No dots

my_package
mypackage
company_project
```

FOR MODULES
```
utils.py
database_connector.py
auth_helper.py

# Bad
Utils.py       # Don't use capitals
database-connector.py
```

FOR CLASSES
``` 
**Good**
class UserProfile:
class DatabaseConnection:
class APIClient:
``` 

FOR DEFINITIONS
```
**Good**
def get_user():
def calculate_total():
def fetch_data():

def GetUser():  # Don't use PascalCase
def calculateTotal():  # Don't use camelCase
``` 

FOR CONSTANTS
``` 
**Good**
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
```

FOR VARIABLES
```
**Good**
username
total_count
is_valid
```

These are just conventions for clearer code and because other programming languages can have totally different standards. (For example JS: ```useEffect```)

------

## CORE PYTHON CONCEPTS

Numbers
```
integer = 42
float_num = 3.14
complex_num = 1 + 2j
````

Strings
```
text = "Hello, World!"
multiline = """
This is a multiline string.
    It preserves indentation.
        Like this!
"""
```

Booleans
```
is_valid = True
is_done = False

# None type
empty = None
```

## COLLECTIONS

Lists (mutable, ordered)
```
fruits = ['apple', 'banana', 'orange']
fruits.append('grape')
```
Tuples (immutable, ordered)
```
coordinates = (10, 20)
rgb = (255, 128, 0)
```
Dictionaries (key-value pairs)
```
user = {
    'name': 'John',
    'age': 30,
    'email': 'john@example.com'
}
```
Sets (unique, unordered)
```
unique_numbers = {1, 2, 3, 3}  # {1, 2, 3}
````
----

## TYPE CONVERSIONS

String conversions
```
str_num = str(42)       # "42"
num_from_str = int("42")  # 42
```

Collection conversions
```
list_from_tuple = list((1, 2, 3))
set_from_list = set([1, 2, 2, 3])  # {1, 2, 3}
rounded = int(3.99)
```

Dictionary Conversions
From list of tuples to dict
```
pairs = [('a', 1), ('b', 2)]
dict_from_pairs = dict(pairs)  # {'a': 1, 'b': 2}
```

From two lists to dict
```
keys = ['a', 'b']
values = [1, 2]
dict_from_zip = dict(zip(keys, values))
```

-----

## PYTHON FLOW CONTROL

If statements
```
age = 20
if age < 18:
    print("Minor")
elif age < 21:
    print("Young adult")
else:
    print("Adult")
```
For loops
Range-based
```
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
```

Iterating collections
````
fruits = ['apple', 'banana', 'orange']
for fruit in fruits:
    print(fruit)
````

Dictionary iteration
```
user = {'name': 'John', 'age': 30}
for key, value in user.items():
    print(f"{key}: {value}")
```

While loops (everyones favourite)
```
count = 0
while count < 5:
    print(count)
    count += 1
````

----

## FUNCTION PRINCIPLES

Basic function
```
def greet(name):
    return f"Hello, {name}!"
```

Default params
```
def greet_with_title(name, title="Mr."):
    return f"Hello, {title} {name}!"
```

Multiple returns
```
def divide_and_remainder(a, b):
    return a // b, a % b
````

*args for variable positional arguments
```
def sum_all(*numbers):
    return sum(numbers)
```

**kwargs for variable keyword arguments
```
def create_user(**user_data):
    return {
        "name": user_data.get('name', 'Anonymous'),
        "age": user_data.get('age', 0)
    }

# Example usage:
result = sum_all(1, 2, 3, 4)  # 10
user = create_user(name="John", age=30, city="New York")
```

----

## USING OBJECTS

Basic Class
```
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        return f"{self.name} says woof!"
```

Inheritance
```
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"
```

Properties
```
class BankAccount:
    def __init__(self):
        self._balance = 0
    
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
```

Class Methods and Static Methods (And more...)
```
class DateHandler:
    date_format = "%Y-%m-%d"
    
    @classmethod
    def parse_date(cls, date_str):
        from datetime import datetime
        return datetime.strptime(date_str, cls.date_format)
    
    @staticmethod
    def is_valid_date(date_str):
        try:
            DateHandler.parse_date(date_str)
            return True
        except ValueError:
            return False
```

----

## OPERATIONS 

1. Lists

Creating
```
my_list = [1, 2, 3]
my_list = list()  # Empty list
````

Adding
```
my_list.append(4)      # Add to end: [1, 2, 3, 4]
my_list.insert(0, 0)   # Insert at index: [0, 1, 2, 3, 4]
my_list.extend([5, 6]) # Add multiple: [0, 1, 2, 3, 4, 5, 6]
````

Removing
```
my_list.pop()          # Remove & return last item
my_list.pop(0)         # Remove & return item at index
my_list.remove(3)      # Remove first occurrence of value
del my_list[1]         # Delete at index
my_list.clear()        # Remove all items
```

Accessing
```
first = my_list[0]     # First item
last = my_list[-1]     # Last item
sliced = my_list[1:3]  # Slice: items 1 through 2
````

Information
```
length = len(my_list)
count = my_list.count(2)    # Count occurrences
index = my_list.index(2)    # Find first index of value
````

Ordering
```
my_list.sort()             # Sort in place
my_list.reverse()          # Reverse in place
sorted_list = sorted(my_list)  # Return new sorted list
```
...

2. Dictionary
Creating
```
my_dict = {'a': 1, 'b': 2}
my_dict = dict()  # Empty dictionary
```
Adding/Modifying
```
my_dict['c'] = 3         # Add or update
my_dict.update({'d': 4}) # Add multiple
```
Removing
```
value = my_dict.pop('a')      # Remove & return value
item = my_dict.popitem()      # Remove & return last item
del my_dict['b']             # Delete key
my_dict.clear()              # Remove all items
```
Accessing
```
value = my_dict['a']         # Get value (raises KeyError if missing)
value = my_dict.get('a', 0)  # Get value with default
```
Information
```
keys = my_dict.keys()
values = my_dict.values()
items = my_dict.items()      # Key-value pairs
```
Checking
```
exists = 'a' in my_dict      # Check if key exists
```

3. Strings
Creating
```
my_str = "Hello"
my_str = str(123)  # Convert to string
```

Modifying (creates new string)
```
upper = my_str.upper()
lower = my_str.lower()
no_spaces = my_str.strip()
replaced = my_str.replace('l', 'L')
```

Splitting/Joining
```
words = my_str.split()        # Split on spaces
words = my_str.split(',')     # Split on comma
new_str = ' '.join(words)     # Join with spaces
```

Finding
```
index = my_str.find('l')      # Returns -1 if not found
index = my_str.index('l')     # Raises ValueError if not found
count = my_str.count('l')     # Count occurrences
```

Checking
```
starts = my_str.startswith('H')
ends = my_str.endswith('o')
is_digit = my_str.isdigit()
is_alpha = my_str.isalpha()
```

4. Sets
Creating
```
my_set = {1, 2, 3}
my_set = set()  # Empty set
```
Adding
```
my_set.add(4)           # Add single item
my_set.update([5, 6])   # Add multiple items
```

Removing
```
my_set.remove(4)        # Raises KeyError if missing
my_set.discard(4)       # No error if missing
item = my_set.pop()     # Remove and return arbitrary item
my_set.clear()          # Remove all items
```

Set Operations
```
union = set1 | set2           # Union
intersect = set1 & set2       # Intersection
diff = set1 - set2            # Difference
sym_diff = set1 ^ set2        # Symmetric difference
```

Checking
```
exists = 1 in my_set          # Check if exists
is_subset = set1 <= set2      # Check if subset
```

5. Tuples
Creating
```
my_tuple = (1, 2, 3)
my_tuple = tuple([1, 2, 3])
```
Accessing (immutable, so no changing)
```
first = my_tuple[0]
sliced = my_tuple[1:3]
```
Information
```
length = len(my_tuple)
count = my_tuple.count(2)
index = my_tuple.index(2)
```

Each type has additional methods...
----

MORE ADVANCED FEATURES 

Decorators
```
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Function took {time.time() - start} seconds")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
````

Context Managers
```
class FileHandler:
    def __init__(self, filename):
        self.filename = filename
    
    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
```

Generators
```
def number_generator(n):
    for i in range(n):
        yield i
```

List Comprehensions
```
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]  # [1, 4, 9, 16, 25]
```

Dictionary Comprehensions
```
square_dict = {x: x**2 for x in numbers}  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

Lambda Functions
```
multiply = lambda x, y: x * y
result = multiply(5, 3)  # 15
```

----

TYPE HINTS AND DATA VALIDATIONS

```
from typing import List, Dict, Optional

def process_users(users: List[dict]) -> Dict[str, str]:
    return {user['id']: user['name'] for user in users}

def get_user(user_id: int) -> Optional[dict]:
    # Could return None or a user dict
    pass
```

----

WORKING WITH FILES

Basic file operations
```
with open('file.txt', 'r') as f:
    content = f.read()

import json

with open('data.json', 'w') as f:
    json.dump(data, f)

import csv

with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```


----

HANDLING ERRORS AND DEBUGGING
```
try:
    number = int("not a number")
except ValueError as e:
    print(f"Couldn't convert to number: {e}")
finally:
    print("This always runs")
```

If you're encountering issues with your code I recommend two things:

Add try blocks on what you suspect might be failing to catch errors, see example above. 
Then you can add specific print statements by reverse engineering the the previous elements of failure. 

If you're more of the thorough type you can try something more like this:
LOGGING : Create a double logger! Check out examples loggers.py

-----

COMMENTS FOR CLARITY 
```

### Main Functions ###
def process_data(data):
    ### Check if data is valid first
    if not data:
        return None
    
    ### Process each item in data
    results = []
    for item in data:
        ### Skip invalid items
        if not validate_item(item):
            continue
        
        results.append(transform_item(item))
    
    return results

### Helper Functions ###
def validate_item(item):
    ### Check basic item structure
    if not isinstance(item, dict):
        return False
    
    ### Ensure required fields exist
    required_fields = ['id', 'name']
    return all(field in item for field in required_fields)

def transform_item(item):
    ### Create new dict with transformed data
    return {
        'id': item['id'],
        'name': item['name'].upper(),
        ### Add timestamp for tracking
        'processed_at': time.time()
    }

### Constants ###
MAX_ITEMS = 1000
VALID_TYPES = ['user', 'admin']

### Example usage ###
data = [
    {'id': 1, 'name': 'john'},
    {'id': 2, 'name': 'jane'}
]
results = process_data(data)
````

This will help you:

1. Create pseudo-code 

### Need a def that can capture screen at X interval and return the size of the image
##### Then crop it to REGION (Top,left,width,height)

2. Clearity when you go back to your code. 

---

WORKING WITH BASIC PACKAGES 

Python comes loaded with powerful libraries built-in. 

Always Available (No Import Needed)

Basic types (str, int, list, dict)
Built-in functions (print, len, range)
Basic operators (+, -, *, /)

**Data Formats**
import json         # JSON handling
import csv          # CSV files
import xml         # XML processing
import configparser # Config file parsing
import pickle      # Python object serialization

**System and OS**
import os          # Operating system interface
import sys         # Python runtime
import platform    # System platform info
import subprocess  # Subprocess management
import shutil      # File operations
import tempfile    # Temporary files
import stat        # File permissions
import pwd         # User info (Unix)
import grp         # Group info (Unix)

**Data Types and Algorithms**
import array       # Efficient arrays
import enum        # Enumeration type
import dataclasses # Data classes
import typing      # Type hints
import heapq       # Heap queue algorithm
import bisect      # Array bisection
import contextlib  # Context managers
import copy        # Shallow/deep copying

**Time and Dates**
import time        # Time access/conversions
import calendar    # Calendar functions
import zoneinfo    # Time zone support

**Mathematics**
import math        # Mathematical functions
import cmath       # Complex math
import decimal     # Decimal fixed point
import fractions   # Rational numbers
import random      # Random numbers
import statistics  # Statistical functions

**Networking**
import socket      # Network interface
import ssl         # SSL/TLS wrapper
import email       # Email handling
import smtplib     # SMTP protocol client
import http        # HTTP modules
import urllib      # URL handling
import ftplib      # FTP protocol client
import ipaddress   # IP address manipulation

**Compression and Archiving**
import zlib        # Data compression
import gzip        # gzip compression
import bz2         # bzip2 compression
import lzma        # LZMA compression
import zipfile     # ZIP archives
import tarfile     # TAR archives

**Development Tools**
import unittest    # Unit testing
import doctest     # Test doc strings
import pdb         # Python debugger
import profile     # Profile code
import timeit      # Time small code bits
import trace       # Trace code execution
import pprint      # Pretty print data

**Text Processing**
import string      # String constants
import textwrap    # Text wrapping
import difflib     # Sequence comparison
import unicodedata # Unicode database
import stringprep  # String preparation

**Concurrent Execution**
import threading   # Threading
import multiprocessing  # Process-based parallelism
import concurrent  # Concurrent execution
import asyncio     # Async I/O
import queue      # Queue data structure

**Cryptography**
import hashlib     # Hash functions
import hmac        # HMAC algorithm
import secrets     # Generate secure random numbers

**Database**
import sqlite3     # SQLite database
import dbm         # Interface to Unix DBM

**Internationalization**
import locale      # Internationalization
import gettext     # Multilingual text

You can then use pip to access 600 000 other projects!


----

PERFORMANCE

Threading - Good for I/O-bound tasks # Example: One part of your code NEEDS to be continuous and the other is more static. 
You can then dedicate a thread (cpu core) to a task

```
import threading

def task():
    print("Doing work")

# Create and start a thread
thread = threading.Thread(target=task)
thread.start()
thread.join()  # Wait for completion
```

Multiprocessing - Good for CPU-bound tasks # Example: Image processing
```
import multiprocessing

def cpu_task(num):
    return num * num

# Create a pool of workers
with multiprocessing.Pool() as pool:
    results = pool.map(cpu_task, [1, 2, 3, 4])
```

Asyncio - Modern way to handle concurrency # Example: Web server handling multiple connections
```
import asyncio

async def async_task():
    await asyncio.sleep(1)
    return "Done"

# Run async code
async def main():
    result = await async_task()

asyncio.run(main())
```

Each use case will vary based on:

CPU-bound (Processing Limited)
I/O-bound (Input/Output Limited)
Memory-bound (RAM Limited)

---

### MEM

Memory Units
````
1 bit: Single binary value (0 or 1)
8 bits = 1 byte
1024 bytes = 1 KB (kilobyte)
1024 KB = 1 MB (megabyte)
1024 MB = 1 GB (gigabyte)
1024 GB = 1 TB (terabyte)
````

Binary Numbers
```
Binary numbers start with 0b in Python:
0b1010 = 10 (decimal)
0b1111 = 15 (decimal)
0b10000 = 16 (decimal)
```

Integer Types and Ranges
Signed Integers
```
8-bit (1 byte): -128 to 127
16-bit (2 bytes): -32,768 to 32,767
32-bit (4 bytes): -2.15 billion to 2.15 billion
64-bit (8 bytes): -9.22 quintillion to 9.22 quintillion
```

Unsigned Integers (positive only)
```
8-bit: 0 to 255
16-bit: 0 to 65,535
32-bit: 0 to 4.29 billion
64-bit: 0 to 18.45 quintillion
```
---``
