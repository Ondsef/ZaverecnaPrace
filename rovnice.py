from random import randint
from sympy import *

a = randint(1, 20)  # člen neznáme x
b = randint(0, 50)  # obsolutní člen
c = randint(1, 100) # pravá strana
x = symbols('x')    # definice proměnné x 

pprint((Eq((a*x + b), c)))  # vrací rovnici
print((solve(Eq((a*x + b), c))))    # vrací výsledek rovnice