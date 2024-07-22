#!/usr/bin/env python3
import sys
from dnsDumpster import *


import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Domain reconnaissance tool.')
    parser.add_argument('--mode', choices=['passive', 'active'], required=True, help='Reconnaissance mode (passive or active).')
    parser.add_argument('--dictionary', help='Path to the dictionary file (required for active mode).')
    parser.add_argument('domain', help='The target domain for reconnaissance.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.mode == "passive":
        result = passive_action(args.domain)
    elif args.mode == "active":
        if not args.dictionary:
            print("Error: Active mode requires a dictionary file.")
            # sys.exit(1)
        result = active_action(args.domain, args.dictionary)
    else:
        print("Invalid mode selected. Please choose 'passive' or 'active'.")
        sys.exit(1)
    


if __name__ == "__main__":
    main()
    
# ./main.py --mode passive emi.ac.ma