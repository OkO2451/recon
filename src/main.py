#!/usr/bin/env python3
import argparse
import sys
import pandas as pd
import subprocess
import datetime
import requests
from bs4 import BeautifulSoup


from dnsDumpster import *


def parse_arguments():
    parser = argparse.ArgumentParser(description='Domain reconnaissance tool.')
    parser.add_argument('--mode', '-m', choices=['passive', 'active'],
                        required=True, help='Reconnaissance mode (passive or active).')
    parser.add_argument(
        '--dictionary', '-d', help='Path to the dictionary file (required for active mode).')
    parser.add_argument('domain', help='The target domain for reconnaissance.')
    parser.add_argument(
        '-o', '--output', help='Output file to save the results.')
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.mode == "passive":
        result = passive_action(args.domain)
        print(result)
    elif args.mode == "active":
        if not args.dictionary:
            print("Error: Active mode requires a dictionary file.")
            sys.exit(1)
        result = active_action(args.domain, args.dictionary)
        print(result)
    else:
        print("Invalid mode selected. Please choose 'passive' or 'active'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
