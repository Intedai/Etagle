from os import system, name
from itertools import cycle
import json
import random


# Colors
class Colors:
    GREEN = "\033[92m"
    FAIL = "\033[91m"
    RESET = "\033[0m"  # Resets the colors of the next characters
    BLUE = "\033[94m"


class Browsers:
    CHROME = "chrome"
    FIREFOX = "firefox"

# Function to clear the terminal screen
def clear_terminal():
    system('cls' if name == 'nt' else 'clear')


# Enables the colors to appear on the terminal, will run on any file that imports utils
system("")


def print_logo():
    """
    Print the logo to the terminal in blue and adds 3 line breaks
    """

    # prints the ascii logo with the description
    print(f"""{Colors.BLUE}
  ███████╗████████╗ █████╗  ██████╗ ██╗     ███████╗
  ██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██║     ██╔════╝
  █████╗     ██║   ███████║██║  ██╗ ██║     █████╗  
  ██╔══╝     ██║   ██╔══██║██║  ╚██╗██║     ██╔══╝  
  ███████╗   ██║   ██║  ██║╚██████╔╝███████╗███████╗
  ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
{Colors.RESET}
  A multithreaded Omegle spam bot that:
  • Uses custom and random user-agents
  • Clear and well made config file
  • Has Firefox and Chrome support
  • Can send messages in a sequence
  • Can save logs{Colors.BLUE}
""")


# get user agents from the user-agents.json file
with open("user-agents.json", 'r') as json_agents:
    agent_list = json.load(json_agents)

    # Randomize order of user agents in the list of agents
    random.shuffle(agent_list)

    # Create a cycle for the list of agents
    agent_cycle = cycle(agent_list)

# For testing purposes
if __name__ == "__main__":
    print_logo()
    print(next(agent_cycle))