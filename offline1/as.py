#!/bin/python3
from Crypto.Util import number
from Crypto.Random import random
def generateCurve(bits:int):
   p = number.getPrime(128)
   a = number.getRandomRange(1, p)
   temp = (4 * a**3 ) % p
   b = number.getRandomRange(1, p)
   while (temp + 27 * b*b) % p == 0:
       b = number.getRandomRange(1, p)
   return p,a,b
def curve(x:int, a:int, b:int, p:int):
   y2 =  (x**3 + a*x + b) % p
   if pow(y2, (p-1)//2, p) == 1:
       return pow(y2, (p-1)//4, p)
   else:
       return None
def generateG(p:int , a:int, b:int):
   gx = number.getRandomRange(1, p)
   gy = curve(gx, a, b, p)
   while not gy:
       gx = number.getRandomRange(1, p)
       gy = curve(gx, a, b, p)
   return gx,gy
def add(x1, y1, x2, y2, p:int):
   t1 = number.inverse(x2-x1, p)
   s = (y2-y1) * t1 % p
   x3 = (s*s - x1 - x2) % p
   y3 = (s*(x1-x3) - y1) % p
   return x3,y3

def multiply(x1, y1, a:int, p:int):
   t1 = number.inverse(2*y1, p)
   s = (3*x1*x1+a) * t1 % p
   x3 = (s*s - x1 - x1) % p
   y3 = (s*(x1-x3) - y1) % p
   return x3,y3
def ecc_power(x1, y1, power, a:int, b:int, p:int):
   nbits = power.bit_length()
   resx, resy = x1, y1
   for i in reversed(range(0, nbits-1)):
       resx, resy = multiply(resx, resy, a, p)
       if power & 1 << i:
           resx, resy = add(resx, resy, x1, y1, p)
   return resx, resy

nbits = 128
p,a,b = generateCurve(nbits)
gx, gy = generateG(p,a,b)
prk = random.getrandbits(nbits)
pubk = ecc_power(gx, gy, prk, a, b, p)
print(p,a,b,gx,gy)
print(prk, pubk)