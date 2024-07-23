import pandas as pd
import os
import subprocess


# open data/crt.csv and take a list of the domaine colomn
def get_crt_domains():
    df = pd.read_csv("data/crt.csv")
    return df["Domain"].tolist()


def execute_command(command):

    try:
        # Debug output: print the command
        print(f"Running command: {' '.join(command)}")

        # Execute the command and capture output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Debug output: print result codes and output
        """print(f"Command exited with code: {result.returncode}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")"""
        final = f"{result.stdout} \n {result.stderr}"
        if result.returncode != 0:
            print("Command encountered an error:")
            # print(result.stderr)
            return "Command execution failed or returned no output."

        return final

    except Exception as e:
        # print(f"An error occurred: {e}")
        return "An error occurred during command execution."


# the who is command


def whoIS(domaine):
    command = ["whois", "-H", domaine]
    return execute_command(command)


def gobust(domaine, dictionary="/usr/src/app/src/dictionary.txt"):
    command = ["gobuster",
               "dns",
               "-d",
               domaine,
               "-w",
               dictionary, 
               "-t", 
               "100", 
               "-q"]
    return execute_command(command)


def nmap(domaine):
    command = ["nmap", "-sV",
               "-Pn",
               "-sC",
               domaine]
    return execute_command(command)


# test
# res = whoIS("emi.ac.ma")
