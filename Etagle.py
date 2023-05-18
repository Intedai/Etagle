# Selenium related imports:
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as ffOptions
from selenium.webdriver.chrome.options import Options as chOptions
from selenium.webdriver.chrome.service import Service

import configparser
from ast import literal_eval
from time import sleep  # for waiting between chats
import threading
from utils import *

# for printing the count
message_count = 0


# User agents for the bot
def read_config():
    """
    # Reads config file and sets global variables
    """

    # Create a ConfigParser object and read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    browser = config['BROWSER']['browser'].lower()

    ch_path = config['BROWSER']['Chrome_PATH']

    # Gets the message that the bot will send from the config file
    message = literal_eval(config['MESSAGE']['Message'])

    # Gets the waiting time from the config file
    before = config['WAITING']['Before']
    after = config['WAITING']['After']

    # If the before and after waiting times can be converted into integers, convert them
    try:
        before = int(before)
        after = int(before)

    # If not, prompt the user to enter an integer value
    except ValueError:
        while True:
            try:
                before = int(input(
                    f"  {Colors.BLUE}Enter the Waiting time in seconds before sending each message, must be an integer:{Colors.RESET} "))

                after = int(input(
                    f"  {Colors.BLUE}Enter the Waiting time in seconds after sending each message, must be an integer:{Colors.RESET} "))

                break
            except ValueError:
                print(f"\n  {Colors.FAIL}Invalid input. Please enter integers.{Colors.RESET}\n")

    # Check if input equals true and if yes give the user an input entry for the topics
    if config['TOPICS'].getboolean('Input'):
        topics = str(input(f"  {Colors.BLUE}Topics:{Colors.RESET} "))

    # Otherwise get the topics from the config file
    else:
        topics = config['TOPICS']['Topics']

    # Gets the thread count from the config file
    thread_count = config['THREADING']['Thread_Count']

    # If the threads can be converted into integers, convert them
    try:
        thread_count = int(thread_count)

    # If not, prompt the user to enter an integer value
    except ValueError:
        while True:
            try:
                thread_count = input(
                    f"  {Colors.BLUE}Enter the amount of sessions (threads) that will run, must be an integer:{Colors.RESET} ")
                thread_count = int(thread_count)
                break
            except ValueError:
                print(f"\n  {Colors.FAIL}Invalid input. Please enter an integer.{Colors.RESET}\n")

    return message, before, after, topics, thread_count, browser, ch_path


def send_messages(driver, message, before, after):
    """
    Sends message and disconnects from chat,
    also prints the current message count
    """

    global message_count

    # Find the text box for sending messages
    chatbox = driver.find_element(By.CLASS_NAME, "chatmsg")

    # Send the message
    for message in message:
        chatbox.send_keys(message)
        chatbox.send_keys(Keys.ENTER)
        # Wait before sending each message
        sleep(before)

    # Update the message count
    message_count += 1

    # Clear the terminal screen and print the message count
    clear_terminal()
    print_logo()
    print(f"{Colors.RESET}  Sent {Colors.BLUE}{message_count}{Colors.RESET} times")

    sleep(after)

    # Find the button for disconnecting from a chat and starting a new one
    disconnect_button = driver.find_element(By.CLASS_NAME, "disconnectbtn")

    # click on the button 2 times to end the chat and 1 time to start a new one
    for i in range(3):
        disconnect_button.click()


def session(topics, message, before, after, browser, ch_path):
    """
    Single Omegle Spam Session, opens Firefox and Omegle and then sends messages
    """

    # Firefox options
    match browser:
        case Browsers.CHROME:
            opts = chOptions()
            opts.add_argument(f"user-agent={next(agent_cycle)}")
            opts.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(service=Service(ch_path), options=opts)
        case Browsers.FIREFOX:
            opts = ffOptions()
            opts.set_preference("general.useragent.override", next(agent_cycle))
            driver = webdriver.Firefox(options=opts)
        case _:
            clear_terminal()
            print_logo()
            print(f"{Colors.FAIL}Invalid browser, please change the browser in config.ini to Firefox or Chrome{Colors.RESET}\n")
            print("Closing in 10 seconds...")
            time.sleep(10)
            exit(1)


    driver.get('https://www.omegle.com/')

    # Find the input box that takes the topics for the chats
    bar = driver.find_element(By.CLASS_NAME, 'newtopicinput')

    # Enter the topics
    bar.send_keys(topics)
    bar.send_keys(Keys.ENTER)

    # Click on the chat button to start chatting
    driver.find_element(By.ID, "textbtn").click()

    """
    Find all the checkboxes by using the XPath for checkboxes
    because the checkboxes for agreeing to the TOS don't have a class or an id
    """
    checkboxes = driver.find_elements(By.XPATH, '//input[@type="checkbox"]')

    # Click on every checkbox
    for checkbox in checkboxes:

        # Try clicking because not every checkbox is enabled and disabled checkboxes raise exceptions when clicked
        try:
            checkbox.click()

        # Don't do anything if a checkbox is disabled
        except Exception:
            pass

    """ 
    Find an input element with the XPath of the specified because the button
    doesn't have a tag but it has this value and clicks on it
    """
    driver.find_element(By.XPATH, '//input[@value = "Confirm & continue"]').click()

    # Minimizes the session's window, user can open a window if wanted
    driver.minimize_window()

    while True:
        # Tries because the text box might have not loaded yet and that will raise an exception
        try:
            send_messages(driver, message, before, after)

        # does nothing so the bot will just try again until he succeeds
        except Exception:
            pass


def main():
    """
    Main function, creates threads for the sessions and starts them
    """

    print_logo()

    # Read the config and sets the variable that will be used in each section
    message, before, after, topics, thread_count, browser, ch_path = read_config()

    print(f"\n\n  {Colors.GREEN}Starting...\n\n")

    # Thread's target, session func with config values
    t_session = lambda: session(topics, message, before, after, browser, ch_path)

    threads = []

    for i in range(thread_count):
        try:
            t = threading.Thread(target=t_session)
            t.start()
            threads.append(t)

        # General Exception because it can range through exceptions when working
        except Exception:
            print(
                f"{Colors.FAIL}A thread was blocked by Omegle or there was an ERROR.\nTrying to launch this thread:{Colors.RESET} \n\n")
            for attempt in range(10):
                try:
                    t = threading.Thread(target=t_session)
                    t.start()
                    threads.append(t)
                    print(f"{Colors.GREEN}SUCCESS!\n{Colors.RESET}")
                    sleep(1)
                    break
                except Exception:
                    # don't do anything just try another iteration
                    if attempt == 9:
                        print(f"{Colors.FAIL}DIDN'T SUCCEED, LAUNCHING WITHOUT THIS THREAD{Colors.RESET}")

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
