# Hello world

define a function hello
print hello world

```python
def hello():
  print('hello world')
```

# Is palindrome

make a function called is palindrome that takes one argument called s
let reversed be s followed by open bracket colon colon negative one close bracket
return reversed equals s

```python
def is_palindrome(s):
  reversed = s[::-1]
  return reversed == s
```

# fibonnaci

Define a function fibonacci that takes one argument n
If n is less than or equal to two
Return n
Else
Return fibonacci of n minus one plus fibonacci of n minus two

```python
def fibonacci(n):
  if n <= 2:
    return n
  else:
    return fibonacci(n-1) + fibonacci(n-2)

```

# file IO

with open filename as file
print file dot read

```python
with open(filename) as file: # with open filename as file
  print(file.read()) # print file dot read
```

# map/list comp

maked doubled be the result of applying double to every element in the list

```python
doubled = [double(element) for element in list]
```

# dictionary

set dictionary sam to 22

```python
dictionary['sam'] = 22
```

# OO

define a class vehicle with two attributes mileage and gas remaining

```python
class Vehicle:
  def __init__(self, mileage, gas):
    self.mileage = mileage
    self.gas = gas
```

define a class car inheriting from vehicle that adds an attribute called doors

```python
class Car(Vehicle):
  def __init__(self, mileage, gas, doors):
    super().__init__(mileage, gas)
    self.doors = doors
```

# greeting function

define a function greet that takes an argument name
print hello space name

```python
def greet(name):
  print('hello ' + name)
```


# Notes

function with no arguments
gimme
function hello world argument n -> no 'one'
otherwise to else
return fib with n minus one plus fib with n minus two -> return fib with n minus one plus fib n minus two

x one -> x plus one

* but we can get around this by not letting people assign variables like this?