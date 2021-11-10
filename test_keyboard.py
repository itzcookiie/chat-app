import sys

import keyboard

chars = []
keyboard.on_press(lambda x: chars.append(x.name) if len(x.name) == 1 else None)
b = input()
print('input = ', b)
a = keyboard.record('p')
print(a)
print(chars)
keyboard.play(a)

# for line in sys.stdin:
#     print(line)