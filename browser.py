import sys
import os
import requests
import bs4
from colorama import init, deinit, Fore
from bs4 import BeautifulSoup

# write your code here

save_dir = ""

print(sys.argv)

if len(sys.argv) == 2:
    save_dir = sys.argv[1]
    try:
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, save_dir)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
    except OSError:
        print("Creation of the directory %s failed" % save_dir)

# create history
history = []

# init colorama
init()


def call_page(url):
    if not url.startswith("https://"):
        full_url = "https://" + url

    history.append(full_url)
    soup = BeautifulSoup(requests.get(full_url).content, 'html.parser')
    # print(soup.get_text())
    text = parse_html("", soup)
    with open(os.path.join(final_directory, full_url.partition("//")[2].split(".")[0]), "w") as cachefile:
        cachefile.write(text)
    print(text)


taglist = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"]


def parse_html(init_string, content):
    if isinstance(content, bs4.BeautifulSoup) or isinstance(content, bs4.element.Tag):
        for child in content.contents:
            if child.name in taglist:
                if child.string is not None:
                    if child.name == "a":
                        init_string = init_string + Fore.BLUE + child.string + Fore.RESET + "\n"
                    else:
                        init_string = init_string + child.string + "\n"
            if isinstance(content, bs4.element.Tag):
                init_string = parse_html(init_string, child)
    return init_string


alive = True


while alive:
    url = input()
    if url == "exit":
        deinit()
        alive = False
    elif url == "back":
        # print("going back")
        history.pop()
        call_page(history.pop())
    elif "." not in url:
        if not os.path.isfile(url):
            print("Error: Incorrect URL")
        else:
            with open(url, "r") as cachefile:
                for line in cachefile:
                    print(line.strip())
    else:
        call_page(url)
