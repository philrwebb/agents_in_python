# Python Language Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Basic Syntax](#basic-syntax)
4. [Data Types](#data-types)
5. [Control Flow](#control-flow)
6. [Functions](#functions)
7. [Data Structures](#data-structures)
8. [Object-Oriented Programming](#object-oriented-programming)
9. [Modules and Packages](#modules-and-packages)
10. [File Operations](#file-operations)
11. [Error Handling](#error-handling)

---

## Introduction
- **What is Python?**
  - High-level, interpreted programming language
  - Developed by Guido van Rossum
  - Created in 1991
  - Known for simplicity and readability
- **Key Features:**
  - Readable syntax
  - Dynamic typing
  - Built-in data structures
  - Extensive standard library
  - Cross-platform compatibility
  - Large community and ecosystem

## Getting Started
### Installation
- **PyPI (Python Package Index)** - pip installer
- **Official Python Site** - python.org
- **Package Managers:**
  - pip (Python Package Installer)
  - conda (Anaconda/Miniconda)

### Your First Program
```python
# Simple print statement
print("Hello, World!")
```

### Running Python Code
- Interactive Shell (REPL)
- Script file execution
- IDE (Integrated Development Environment)

### Basic Development Tools
- **Popular IDEs:**
  - VS Code (Visual Studio Code)
  - PyCharm
  - Jupyter Notebook
  - JupyterLab

## Basic Syntax
### Comments
- Single-line comment: `# comment`
- Multi-line comment: `""" comment """` or `''' comment '''`
- Inline comment: `print("This is a print statement # with comment")`

### Variables
- No type declaration required
- Dynamic typing
- Variable naming rules:
  - Lowercase or uppercase letters
  - Underscore (_) for multi-word
  - Cannot start with number
  - Cannot be Python keywords

```python
x = 10          # Integer
y = 3.14        # Float
name = "Alice"  # String
is_active = True # Boolean
```

### Expressions and Operators
#### Arithmetic Operators
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `//` Floor Division
- `%` Modulus
- `**` Exponentiation

#### Assignment Operators
- `=` Assignment
- `+=` Add and Assign
- `-=` Subtract and Assign
- `*=` Multiply and Assign
- `**=` Power and Assign

### Mathematical Functions
- `abs(x)` - Absolute value
- `round(x, ndigits)` - Round a number
- `pow(x, y)` - Power function

### String Manipulation
- Slicing: `string[1:3]` (first two characters)
- Concatenation: `a + b`
- Repetition: `a * n`
- String methods: `.upper()`, `.lower()`, `.strip()`, `.split()`

## Data Types
### Primitive Data Types
1. **Number**
   - `int` - Integer
   - `float` - Floating-point number
   - `complex` - Complex number (real + imaginary)

2. **String**
   - Immutably sequence of characters
   - Enclosed in quotes (single or double)
   - Unicode support

3. **Boolean**
   - `True` or `False`
   - Derived from integers (True=1, False=0)

### Special Number Types
- `NoneType` - Represents None
- `bytes` - Byte string

### Complex Number
```python
z = 3 + 2j
x = complex(2, 5)
```

### Zero-Value Values
- `0` - Zero
- `0.0` - Zero as float
- `0j` - Zero as complex
- `True` - Boolean True (equivalent to 1)
- `False` - Boolean False (equivalent to 0)
- `""` - Empty string (falsy)
- `[]` - Empty list (falsy)
- `{}` - Empty dict (falsy)
- `None` - None value (falsy)

### Check Data Type
```python
type(variable)       # Returns type object
isinstance(obj, Type)  # True/False
```

### Unpacking Values
```python
a, b = 1, 2
x, y, z = 1, 2, 3
a = [1, 2], [3, 4]  # Nested unpacking
```

## Control Flow
### Conditional Statements
#### `if` Statement
```python
if condition:
    # execute if condition is True
    pass

elif additional_condition:
    # execute if previous conditions are False
    pass

else:
    # execute if all conditions are False
    pass
```

#### Comparison Operators
- `==` Equal
- `!=` Not Equal
- `>` Greater Than
- `<` Less Than
- `>=` Greater Than or Equal
- `<=` Less Than or Equal

#### Logical Operators
- `and` - Logical AND
- `or` - Logical OR
- `not` - Logical NOT
- Short-circuit evaluation

### Boolean Operators
```python
x > 0 and y < 10        # True if both
x < 0 or y > 10         # True if any
not (x == 0)            # True if x is not 0
```

### Ternary Operator
```python
result = x if condition else y
```

### For Loop
```python
# Basic loop
for i in range(10):
    print(i)

# With start and stop
for i in range(5, 10):
    print(i)

# With step
for i in range(0, 10, 2):
    print(i)

# Iterate over sequence
for item in iterable:
    print(item)

# Iterate with index
for i, item in enumerate(iterable):
    print(i, item)
```

### While Loop
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

### Break and Continue
```python
for i in range(10):
    if i == 5:
        break  # exit loop
    if i == 3:
        continue  # skip iteration
    print(i)
```

### Pass Statement
- No-op statement
- Used as placeholder in empty blocks
- Commonly used in function stubs and empty if blocks

### Other Control Flow Statements
- `assert` - Assertion (debugging)
- `try`, `except`, `finally` - Error handling
- `yield` - Generator expression

## Functions
### Function Definition
```python
def function_name(parameters):
    # function body
    pass

# Function call
result = function_name(arg1, arg2)
```

### Parameters
#### Regular Parameters
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"
```

#### *Args (Variable Arguments)
```python
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

# def add(a, *b):
```

#### **Args (Keyword Arguments)
```python
def create_profile(**kwargs):
    # use keyword arguments
    print(kwargs)

# def x(y=0, **z):
```

#### Default Values
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"
```

### Function Signature
```python
def function(name, count, *args, **kwargs):
    pass
```

### Functions with No Parameters
```python
def print_greeting():
    pass
```

### Functions with No Return Value
```python
def greet():
    print("Hello!")
    pass
```

### Functions with Return Value
```python
def add(x, y):
    return x + y
```

### Function Scope and Global Scope
- Local variables inside functions
- Global variables outside functions
- `global` keyword to modify global variables in functions

### Lambda Functions
```python
# Lambda (anonymous function)
add = lambda x, y: x + y

# Using lambda in list comprehension
squared = [x**2 for x in numbers]
```

### Higher-Order Functions
```python
# map()
squared = list(map(lambda x: x**2, numbers))

# filter()
evens = list(filter(lambda x: x % 2 == 0, numbers))

# reduce()
total = functools.reduce(lambda x, y: x + y, numbers)
```

## Data Structures
### Lists
- Ordered, mutable collection of items
```python
# Create list
fruits = ["apple", "banana", "cherry"]
empty_list = []
mixed_list = [1, "two", True]

# Access elements
first_fruit = fruits[0]
first_fruit_last = fruits[0][0]

# Slice
slice = fruits[1:3]

# Modify list
fruits.append("date")
fruits.insert(1, "blueberry")
fruits[0] = "apricot"

# List comprehension
squares = [x**2 for x in range(10)]

# List methods
len(fruits)
fruits.count("apple")
fruits.index("banana")
fruits.remove("banana")
fruits.clear()
```

### Tuples
- Ordered, immutable collection
```python
# Create tuple
coordinates = (10, 20)
empty_tuple = ()
mixed_tuple = (1, "two", True)

# Access tuple
x, y = coordinates
```

### Sets
- Unordered collection of unique items
```python
# Create set
numbers = {1, 2, 3, 3}
empty_set = set()

# Set operations
s1 = {1, 2, 3}
s2 = {3, 4, 5}

s1 | s2      # Union
s1 & s2     # Intersection
s1 - s2     # Difference
s1 ^ s2     # Symmetric difference
```

### Dictionary
- Key-value mapping
```python
# Create dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Access values
name = person["name"]
age = person.get("age")
city = person["city"]

# Modify dictionary
person["city"] = "Los Angeles"
person["email"] = "alice@example.com"

# Add key-value pair
person["age"] = 31

# Check if key exists
if "age" in person:
    print("Age exists")
```

### Multidimensional Data Structures
#### List of Lists
```python
matrix = [
    [1, 2],
    [3, 4],
    [5, 6]
]
```

#### Nested Dictionary
```python
profile = {
    "personal": {
        "name": "Alice",
        "age": 30
    },
    "work": {
        "title": "Developer",
        "company": "ABC Corp"
    }
}
```

### OrderedDict (Ordered Dictionary)
- Preserves insertion order
- Accessible by key or index

### DefaultDict
- Efficiently handles missing keys
- Inherits from dictionary

## Object-Oriented Programming
### Class Definition
```python
class Car:
    # Class variables
    color = "red"
    wheels = 4

    # Constructor
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    # Class methods
    def drive(self):
        print(f"Driving {self.make} {self.model}")

    # Static method
    @staticmethod
    def make_noise():
        return "Vroom!"
```

### Inheritance
```python
class ElectricCar(Car):
    def __init__(self, make, model, year, battery_capacity):
        super().__init__(make, model, year)
        self.battery_capacity = battery_capacity

    def drive(self):
        print(f"Electric driving {self.make} {self.model}")
```

### Multiple Inheritance
```python
class Vehicle:
    def __init__(self, wheels):
        self.wheels = wheels

class Car:
    def __init__(self, make, model, wheels):
        self.make = make
        self.model = model
        self.wheels = wheels

class ElectricCar(Vehicle, Car):
    def __init__(self, make, model, wheels, battery):
        Vehicle.__init__(self, wheels)
        Car.__init__(self, make, model, wheels)
        self.battery = battery
```

### Polymorphism
- Same interface, different implementation
- Duck typing: "If it looks like a duck, acts like a duck"

### Encapsulation
- Private variables with `_` prefix (convention)
- Protected variables with `__` prefix (name mangling)

### Meta Classes
- Creates or modifies classes dynamically
- Override `__new__` and `__init__`

### Advanced Concepts
- Abstract Base Classes
- Property decorators
- Descriptors

## Modules and Packages
### Importing Modules
```python
# Import entire module
import math

# Import specific function
from math import sqrt, pi

# Import as alias
import math as m

# Relative import
from mymodule import my_function
from . import submodule
```

### Installing Modules
```bash
pip install module_name
```

### Common Built-in Modules
- `math` - Mathematical functions
- `sys` - System-related functions
- `os` - Operating system interfaces
- `datetime` - Date/time handling
- `json` - JSON encoding/decoding
- `re` - Regular expressions
- `random` - Random numbers
- `collections` - Various container types
- `functools` - Function tools
- `itertools` - Iterators and tools
- `operator` - Function manipulators

### Creating Modules
```python
# main.py
def greet(name):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    greet("World")
```

### Creating Packages
- Directory with `__init__.py` file
- Can be imported as package
```python
# mypackage/__init__.py
from mypackage.module1 import func1
from mypackage.module2 import func2
```

### Virtual Environments
- Isolate dependencies
- `venv` module
```bash
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
pip install -r requirements.txt
```

## File Operations
### Opening Files
```python
# Write mode
with open('file.txt', 'w') as f:
    f.write("Hello World")

# Read mode
with open('file.txt', 'r') as f:
    content = f.read()

# Read lines
lines = f.readlines()
line = next(f)

# Append mode
with open('file.txt', 'a') as f:
    f.write("\nMore content")

# Binary mode
with open('file.bin', 'wb') as f:
    f.write(b'binary data')
```

### Path Operations
- `os.path.join()` - Join path components
- `os.path.getsize()` - File size
- `os.path.exists()` - Check if exists
- `os.makedirs()` - Create directories

### Reading and Writing Text Files
```python
# Read file as text
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Write file as text
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write(text)

# Read multiple lines
lines = open('file.txt', 'r').readlines()

# Open file object
f = open('file.txt', 'r')
f.close()
```

### File Patterns
- Text mode (default) - `r`
- Binary mode - `rb`
- Write mode - `w`
- Append mode - `a`

### os and pathlib Modules
```python
import os
import os.path as osp

# List files in directory
files = os.listdir('.')

# Create directory
os.makedirs('new_dir')

# Get file properties
stats = os.stat('file.txt')
size = os.path.getsize('file.txt')
```

### shutil Module
```python
# Copy file
shutil.copy('src.txt', 'dest.txt')

# Copy directory
shutil.copytree('src', 'dest')

# Remove file
shutil.rmtree('temp')
```

## Error Handling
### try-except-finally
```python
try:
    # Code that might raise exception
    result = 1 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An error occurred: {e}")

# Finally executes regardless
try:
    risky_operation()
finally:
    cleanup()
```

### raise Exception
```python
# Raise exception
raise ValueError("Invalid value")

# Re-raise exception
raise  # Re-raises last exception
```

### Custom Exceptions
```python
class MyError(Exception):
    pass

class CustomError(MyError):
    def __init__(self, message):
        super().__init__(message)
```

### try-except-finally best practices
- Catch specific exceptions
- Use `else` for code after try block
- Avoid bare `except:`
- Use `finally` for cleanup
- Don't catch `KeyboardInterrupt` in most cases

### assert statements
```python
# Assert condition
assert x > 0, "x must be positive"
assert x == y, "x and y must be equal"
assert callable(x)
```

---

## References
- [Python Documentation](https://docs.python.org/3/)
- [Python.org](https://www.python.org/)
- [Real Python](https://realpython.com/)
- [W3Schools Python](https://www.w3schools.com/python/)
- [Codecademy Python](https://www.codecademy.com/python)

---

*Last updated: January 2025*