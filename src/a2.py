import os
import subprocess

url_target = "https://juice-shop.herokuapp.com/"


command_dns = [
            "gobuster", "dns",
            "-w", "data/subDomaine.txt",
            "-d", url_target,  # Target domain for subdomain enumeration
            "-r",  # Include subdomain results in output
            "-t", "10",  # Number of concurrent threads
            "-o", "data/subdomain_results.txt",
        ]

command_dir = [
            "gobuster", "dir",
            "-w", "data/subDomaine.txt",
            "-u", url_target,  # Target URL for directory enumeration
            "-s", "204,301,302,307,401",  # Valid status codes
            "-b", "",  # Explicitly disable the blacklist
            "-o", "data/directory_results2.txt",
        ]


def invoquer_gobuster( command):
    # Ensure url_target is not empty
    if not command["-u"]:
        print("Url/Domain (-u) must be specified.")
        return []
    
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

# Example usage
# Replace with your target domain


result = invoquer_gobuster(command_dns)
result1 = invoquer_gobuster(command_dir)
