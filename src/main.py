import argparse
import os
import subprocess
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="auto enumeration.")
    parser.add_argument("-u", "--url", required=True, help="Target URL for directory enumeration")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file to save the results")
    parser.add_argument("--dns", action="store_true", help="Perform DNS enumeration instead of directory enumeration")
    return parser.parse_args()

def check_wordlist(wordlist_path):
    if not os.path.isfile(wordlist_path) or os.path.getsize(wordlist_path) == 0:
        print(f"Wordlist file is invalid or empty: {wordlist_path}")
        sys.exit(1)

def getDIrectories(url, wordlist, output, dns=False):
    pass

def getSubdomains(url, wordlist, output):
    pass

def recursiveDirectory(url, wordlist, output):
    pass

def getFiles(url, wordlist, output):
    pass

def 


# extract the subdomains from the results file
def extract_subdomains():
    # check if "data/subdomain_results.txt" exists
    if os.path.exists("data/subdomain_results.txt"):
        # open the file in read mode
        with open("data/subdomain_results.txt", "r") as file:
            # read all the lines from the file
            lines = file.readlines()
            # iterate over the lines
            for line in lines:
                # split the line by space
                parts = line.split(" ")
                # check if the line contains "Found: "
                if "Found: " in parts:
                    # print the subdomain
                    print(parts[-1].strip())
                    
# extract the directories from the results file
def extract_directories():
    # check if "data/directory_results.txt" exists
    if os.path.exists("data/directory_results.txt"):
        # open the file in read mode
        with open("data/directory_results.txt", "r") as file:
            # read all the lines from the file
            lines = file.readlines()
            # iterate over the lines
            for line in lines:
                # split the line by space
                parts = line.split(" ")
                # check if the line contains "Found: "
                if "Found: " in parts:
                    # print the directory
                    print(parts[-1].strip())

# removes the destiation files for cleanup
def cleanup():
    # check if "data/subdomain_results.txt" exists and remove it
    if os.path.exists("data/subdomain_results.txt"):
        os.remove("data/subdomain_results.txt")
    # check if "data/directory_results.txt" exists and remove it
    if os.path.exists("data/directory_results.txt"):
        os.remove("data/directory_results.txt")


def main():
    args = parse_arguments()
    check_wordlist(args.wordlist)
    getDIrectories(args.url, args.wordlist, args.output, args.dns)

if __name__ == "__main__":
    main()