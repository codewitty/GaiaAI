import sys
import os
import argparse
from World import World
from ManualAI import ManualAI
from RandomAI import RandomAI
from ZyAI import MyAI
import time


print("HElllo")
obj = MyAI(8, 8, 10, 2, 2) 
print(obj.getAction(2))
