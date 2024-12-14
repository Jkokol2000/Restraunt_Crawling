import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from csv import writer
from time import sleep
from random import choice
import re
import numpy as np

dr = webdriver.Chrome()

all_titles = []

all_names = ["Michael", "Percival_(Grand)", "Wamdus_(Holiday)", "Zeta_(Grand)", "Gabriel", "Payila", "Olivia", "Raziel_(Summer)", "Uriel", "Galleon_(Summer)", "Narmaya_(Grand)", "Vania_(Yukata)", "Nehan", "Sandalphon", "Ilsa_(Yukata)"]

base_url = "https://gbf.wiki"

url = '/Arulumaya'

while url:
    dr.get(f"{base_url}{url}")
    print(f"Now Scraping{base_url}{url}")
    soup = BeautifulSoup(dr.page_source, "html.parser")
    current_title = soup.find(class_="char-title")
    current_title_in_brackets = re.findall(r"\[(.*?)\]", current_title.get_text())
    print(current_title_in_brackets)
    all_titles.append({
        "name" : "".join(ch for ch in url if ch.isalnum()),
        "title": current_title_in_brackets
        })
    if all_names:
        new_name = choice(all_names)
        all_names.remove(new_name)
        url = "/" + new_name
        sleep(2)
    else:
        url = None
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