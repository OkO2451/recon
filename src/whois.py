import pandas as pd
import os 
import subprocess


# open data/crt.csv and take a list of the domaine colomn
def get_crt_domains():
    df = pd.read_csv("data/crt.csv")
    return df["Domain"].tolist()

def execute_command(command):
    # print working directory
    print(os.getcwd())
    # Ensure url_target is not empty

    
    
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
        
        
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# the who is command

command = [
    "whois",
    "-H"
]

def whoIS(domaine):
    command.append(domaine)
    execute_command(command)
    
# test

