import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from csv import writer
from time import sleep
from random import choice
import re
import numpy as np

base_url = "https://gbf.wiki"
tier_url = "https://gbf.wiki/SSR_Characters_List"
url = '/'
dr = webdriver.Chrome()
all_names = []

def get_all_names():
    dr.get(f"{tier_url}")
    print(f"Now Scraping {tier_url}")
    soup = BeautifulSoup(dr.page_source, "html.parser")
    table = soup.find("table")
    rows = table.find_all(['tr'])
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 2:
            all_names.append(columns[1].get_text())
    return print(all_names)

get_all_names()


all_titles = []



while url:
    if all_names:
        new_name = choice(all_names)
        all_names.remove(new_name)
        url = "/" + new_name
        sleep(.52)
    else:
        url = None
    dr.get(f"{base_url}{url}")
    print(f"Now Scraping {base_url}{url}")
    soup = BeautifulSoup(dr.page_source, "html.parser")
    current_title = soup.find(class_="char-title")
    current_title_in_brackets = re.findall(r"\[(.*?)\]", current_title.get_text())
    print(current_title_in_brackets)
    all_titles.append({
        "name" : "".join(ch for ch in url if ch.isalnum()),
        "title": current_title_in_brackets
        })
    
selected_title = choice(all_titles)
remaining_guesses = 3
print("This title is: ")
print(selected_title['title'])

guess = ''
while guess.lower() != selected_title["name"].lower() and remaining_guesses > 0:
    guess = input(
        f"Who's title is this? Guesses remaining {remaining_guesses}"
    )

    if guess == selected_title["name"]:
        print("CORRECT")
        break
    remaining_guesses -= 1

    if remaining_guesses == 3:
        print(f"Nope, {remaining_guesses} guesses left")
    elif remaining_guesses == 2:
        print(f"Nope, {remaining_guesses} guesses left")
    elif remaining_guesses == 1:
        print(f"Nope, {remaining_guesses} guesses left")
    else:
        print(f"Sorry, out of guesses. The character with this title is {selected_title['name']}")

