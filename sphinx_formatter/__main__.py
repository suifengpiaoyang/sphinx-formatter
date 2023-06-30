import os
import sys


path = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(path))

from sphinx_formatter import main

if __name__ == '__main__':
    main()
