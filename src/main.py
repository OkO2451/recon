#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import re
def parse_arguments():
    parser = argparse.ArgumentParser(description="auto enumeration.")
    parser.add_argument("-u", "--url", required=True, help="Target URL for directory enumeration")
    parser.add_argument("-w", "--wordlist",  help="Path to the wordlist file")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file to save the results")
    parser.add_argument("--dns", action="store_true", help="Perform DNS enumeration instead of directory enumeration")
    # New feature: Verbosity level
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity level (use multiple times for more verbose output)")
    # New feature: Number of threads
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use for enumeration")
    # New feature: Timeout for requests
    parser.add_argument("--timeout", type=int, default=5, help="Timeout for each request in seconds")
    return parser.parse_args()

def check_wordlist(wordlist_path):
    if not os.path.isfile(wordlist_path) or os.path.getsize(wordlist_path) == 0:
        print(f"Wordlist file is invalid or empty: {wordlist_path}")
        sys.exit(1)

def getDIrectories(url, wordlist="data/dir.txt", output="data/directory_results.txt", dns=False):
    command_dir = [
            "gobuster", "dir",
            "-w", wordlist,
            "-u", url,  # Target URL for directory enumeration
            "-s", "204,301,302,307,401",  # Valid status codes
            "-b", "",  # Explicitly disable the blacklist
            "-o", output,
        ]
    result = execute_command(command_dir)

def getSubdomains(url, wordlist="data/subDomaine.txt", output="data/subdomain_results.txt"):
    command_sub = [
            "gobuster", "dns",
            "-w", wordlist,
            "-d", url,  # Target domain for subdomain enumeration
            "-r",  # Include subdomain results in output
            "-t", "10",  # Number of concurrent threads
            "-o", output
        ]
    result = execute_command(command_sub)
    
def getService(url, output="data/nmapResult.txt"):
    
    # lets prepare the url
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    # now we can replace "/" with "" but it can be a problem if the url has too many / in it
    # so we will throw an error if the url has more than 1 /
    if url.count("/") > 1:
        print("Invalid URL")
        return
    # now we can replace the / with ""
    url = url.replace("/", "")
    
    
    command_nmap = [
            "nmap",
            "-sC", "-sV", "-Pn",
            "-o", output,
            url
        ]
    result = execute_command(command_nmap)
    # Split the results into lines for processing
    if isinstance(result, str):
        lines = result.strip().split('\n')
    elif isinstance(result, list):
        # Process each string in the list
        lines = [line.strip() for line in result]
    else:
        raise TypeError("result must be a string or a list of strings")

    # Initialize an empty list to hold the service and version information
    services_versions = []

    # Iterate over each line in the results
    for line in lines:
        # Check if the line contains an open service
        if 'open' in line:
            # Split the line into parts
            parts = line.split()
            # The service name is the third part, and the version starts from the fourth part onwards
            service = parts[2]
            version = ' '.join(parts[3:])
            # Append the service and version to the list
            services_versions.append((service, version))

    # Print the list of services and versions aeromage

    print(services_versions)
            
    
def filterSubdomains(result):
    for r in result:
        if "Found" in r:
            print(r)


def recursiveDirectory(url, wordlist, output):
    pass

def getFiles(url, wordlist, output):
    pass

# execute commands
def execute_command(command):
    # print working directory
    print(os.getcwd())
    # Ensure url_target is not empty

    # Construct the absolute path to the wordlist
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(script_dir, '../data/subDomaine.txt')
    
    # Check if the wordlist file exists and is not empty
    if not os.path.isfile(wordlist_path):
        print(f"Wordlist file does not exist: {wordlist_path}")
        return []
    if os.path.getsize(wordlist_path) == 0:
        print(f"Wordlist file is empty: {wordlist_path}")
        return []
    
    try:
        # Construct the gobuster command for subdomain enumeration
        command = command
        
        # Debug output: print the command
        print(f"Running command: {' '.join(command)}")
        
        # Execute the gobuster command and capture output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Debug output: print result codes and output
        print(f"Command exited with code: {result.returncode}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        
        # Handle errors
        if result.returncode != 0:
            print("Gobuster encountered an error:")
            print(result.stderr)
            return []
        
        # Split the output into a list of lines
        output = result.stdout.split('\n')
        
        # Remove empty lines
        output = [line for line in output if line.strip()]
        
        # Writing the result to a file
        output_file_path = os.path.join(script_dir, '../data/subdomain_results.txt')
        with open(output_file_path, 'w') as f:
            for item in output:
                f.write("%s\n" % item)
        
        return output
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


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
    getService(args.url)

if __name__ == "__main__":
    main()
    
    
    
# srt.sh