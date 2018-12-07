'''dust.py
Joel Tiura
'''
import sys
from core import Core


if __name__ == "__main__":
    if len(sys.argv) == 2:
        Core(sys.argv[1]).report()
