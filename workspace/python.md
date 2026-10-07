# Python OOP Documentation
# ========================
# Basic Object-Oriented Programming Concepts

## Table of Contents
1. Classes and Objects
2. Inheritance
3. Polymorphism
4. Encapsulation
5. Static and Class Methods
6. Best Practices

---

## 1. Classes and Objects

### What is a Class?
A class is a blueprint for creating objects. It defines the properties (attributes) and behaviors (methods) that objects created from the class will have.

### What is an Object?
An object is an instance of a class. It holds the data and can perform actions defined in the class.

### Creating a Class
```python
class Animal:
    """A base class for animals."""
    
    def __init__(self, name, species):
        """Initialize the animal with name and species."""
        self.name = name
        self.species = species
    
    def make_sound(self):
        """Method to make an animal make a sound."""
        return f"The {self.name} makes a sound."

# Creating an object
dog = Animal("Buddy", "Dog")
print(dog.name)  # Buddy
print(dog.make_sound())  # The Buddy makes a sound.
```

### Key Concepts:
- `__init__`: The initializer method, called when creating a new object
- `self`: Refers to the current instance of the class
- `class Body`, `_`, and `__`: Different levels of access control

---

## 2. Inheritance

### What is Inheritance?
Inheritance allows a class to derive its behavior and properties from another class (parent/child relationship).

### Syntax
```python
class Pet:
    """Base class for all pets."""
    def __init__(self, name):
        self.name = name
        self.age = 0
    
    def speak(self):
        return f"{self.name} says meow."

class Dog(Pet):
    """Dog inherits from Pet."""
    
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
        self.age = 0
    
    def speak(self):
        return f"{self.name}, the {self.breed}, speaks."

# Create objects
dog = Dog("Buddy", "Labrador")
print(dog.name)  # Buddy
print(dog.age)   # 0
print(dog.speak())  # Buddy, the Labrador, speaks.
```

### Using `super()`
`super()` is used to call the parent class methods. It's part of the method resolution order (MRO).

### Multiple Inheritance
```python
class Mammal(Pet):
    """A mammal inherits from Pet."""
    
    def has_blood(self):
        return True

class Dog(Pet, Mammal):
    """Dog inherits from both Pet and Mammal."""
    pass
```

---

## 3. Polymorphism

### What is Polymorphism?
Polymorphism means "many forms". It allows objects of different classes to be treated as instances of the same class.

### Type Hints and Overriding Methods
```python
class Shape:
    """Base class for geometric shapes."""
    def area(self):
        raise NotImplementedError("Subclasses must implement area()")

class Rectangle(Shape):
    """Rectangle shape."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    """Circle shape."""
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2

# Create objects
rect = Rectangle(5, 10)
circle = Circle(3)

# Both can be passed to a function
def print_area(shape):
    print(f"Area: {shape.area()}")

print_area(rect)  # Area: 50
print_area(circle)  # Area: 28.27...
```

---

## 4. Encapsulation

### What is Encapsulation?
Encapsulation is the practice of hiding internal data and providing controlled access to it.

### Public, Protected, and Private Access
```python
class BankAccount:
    """A simple bank account."""
    
    def __init__(self, owner, balance):
        self._owner = owner  # Protected
        self.__balance = balance  # Private
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
    
    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
        else:
            print("Insufficient funds")
    
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        self.__balance = value

# Usage
account = BankAccount("Alice", 1000)
account.deposit(200)
print(account.balance)  # 1200

# Cannot access directly
# print(account._BankAccount__balance)  # Private access is restricted
```

### The `@property` Decorator
The `@property` decorator creates a method that can be accessed like an attribute but adds validation/encapsulation.

---

## 5. Static and Class Methods

### Static Methods
Static methods do not receive a reference to an instance and are not bound.

```python
class MathUtils:
    """Utility class with static methods."""
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def multiply(a, b):
        return a * b

# Call without creating an instance
print(MathUtils.add(3, 4))  # 7
print(MathUtils.multiply(5, 2))  # 10
```

### Class Methods
Class methods receive the class rather than an instance and use `cls`.

```python
class Person:
    """Class with class methods."""
    
    _instance_count = 0  # class variable
    
    @classmethod
    def from_name(cls, name):
        """Factory method to create instance."""
        obj = cls(name)
        cls._instance_count += 1
        return obj
    
    def __init__(self, name):
        self.name = name

# Create instances
p1 = Person.from_name("Alice")
p2 = Person.from_name("Bob")

print(p1.name)  # Alice
print(p2.name)  # Bob
print(Person._Person_instance_count)  # 2
```

---

## 6. Best Practices

### 1. Use Method Resolution Order (MRO)
When defining classes that inherit from multiple parents, consider the order they are listed.

### 2. Prefer Composition over Inheritance
Instead of inheriting relationships, consider creating objects that use other objects.

```python
# Instead of:
class Person:
    def add_wine(self, drink):
        self.oinks.append(drink)

# Prefer:
class Wine:
    def add_wine(self, drink):
        return self

class Person:
    def __init__(self):
        self.wines = []

class Wine:
    def __init__(self, name):
        self.name = name
    def add_wine(self, drink):
        pass  # similar logic here
```

### 3. Use Type Hints
Python 3.5+ supports type hints for better code clarity.

```python
from typing import List, Optional

class Calculator:
    def add(self, x: float, y: float) -> float:
        return x + y
    
    def divide(self, x: float, y: float) -> Optional[float]:
        if y == 0:
            return None
        return x / y
```

### 4. Document Your Code
Use docstrings to explain your methods and classes.

```python
class Calculator:
    """A simple calculator class."""
    
    def add(self, x: float, y: float) -> float:
        """Add two numbers and return the sum.
        
        Args:
            x: First number
            y: Second number
        
        Returns:
            Sum of x and y
        
        Raises:
            ValueError: If numbers are not valid
        """
        return x + y
```

### 5. Consider Python's Built-in OOP Features
- `__slots__`: Reduces memory usage
- `__init_subclass__`: Create a base class that will only create a subclass
- `__mro_entries__`: Control the order in which parent classes are searched
- `super()`: Call parent class methods

### 6. Use Dunder (Double Underscore) Methods
Methods starting with `__` have special meaning:

| Method | Purpose |
|--------|---------|
| `__init__` | Initialize objects |
| `__str__` | Convert to string |
| `__repr__` | Create readable representation |
| `__len__` | Return length |
| `__eq__` | Equality check |
| `__lt__`, `__le__`, `__gt__`, `__ge__` | Comparison operations |
| `__add__`, `__sub__`, `__mul__` | Arithmetic operations |
| `__bool__` | Boolean check |
| `__hash__` | Hash value for dict/sets |

---

## Quick Reference

### Access Levels

| Prefix | Access |
|--------|--------|
| `variable` | Public - anyone can access |
| `_variable` | Protected - protected from outside |
| `__variable` | Private - python name mangling |

### Common OOP Patterns

```python
# Singleton Pattern
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Factory Pattern
def create_instance(class_name, **kwargs):
    instance = class_name(**kwargs)
    return instance

# Template Method Pattern
class Template:
    def process(self):
        self.before_step()
        self.do_step()
        self.after_step()
```

---

## Summary

- **Classes** define the structure and behavior
- **Objects** are instances of classes
- **Encapsulation** hides internal state
- **Inheritance** allows code reuse
- **Polymorphism** enables multiple forms
- **Static/Class methods** provide different levels of binding

---

*Documentation generated for Python OOP basics.
*Last updated: 2024*