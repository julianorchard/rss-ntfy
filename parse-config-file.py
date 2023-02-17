#!/usr/bin/env python3

## Testing the configuration file
from pathlib import Path
import os

CONFIG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/config"

def main():
    with open(CONFIG_FILE) as f:
        f.read()
    print(f)

if __name__ == "__main__":
    main()
