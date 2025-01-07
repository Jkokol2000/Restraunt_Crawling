import requests
from pathlib import Path
import csv
import pandas as pd
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from time import sleep
from random import choice
import re

new_name = ""
last_name = ""
base_url = "https://gbf.wiki"
tier_url = "https://gbf.wiki/SSR_Characters_List"
dr = webdriver.Chrome()
all_names = []
all_titles = []
class GBFCharacter:
    def __init__(self, name, title, character_art):
        self.name = name
        self.title = title
        self.character_art = character_art
    def __str__(self):
        return f"{self.name} : {self.title}"
    def __iter__(self):
        return iter([self.name, self.title])

def get_all_names():
    dr.get(f"{tier_url}")
    print(f"Now Scraping {tier_url}")
    soup = BeautifulSoup(dr.page_source, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 2:
                all_names.append(columns[1].get_text())
def remove_dupe_names():
    try:
        df = pd.read_csv("titles.csv", sep = ",")

        if df.empty:
            print("CSV file is empty")
        else:
            unique_names = set(df["name"].values)
            all_names[:] = [name for name in all_names if name not in unique_names]

            print("Duplicate Names Removed")
    except FileNotFoundError:
        print('CSV file does not exist')

def get_all_titles_and_create_classes():
    url = '/'
    while len(all_names) > 0:
        new_name = choice(all_names)
        print(new_name)
        all_names.remove(new_name)
        print(len(all_names))
        name_with_underscore = new_name.replace(' ', '_')
        url = "/" + name_with_underscore
        sleep(3)
        dr.get(f"{base_url}{url}")
        print(f"Now Scraping {base_url}{url}")
        soup = BeautifulSoup(dr.page_source, "html.parser")
        current_title = soup.find(class_="char-title")
        panel= soup.find(class_="tabber__panel")
        art = panel.find('img')
        character_art = art['src']
        current_title_in_brackets = re.findall(r"\[(.*?)\]", current_title.get_text())
        print(current_title_in_brackets)
        characterObject = GBFCharacter(new_name, current_title_in_brackets, character_art)
        all_titles.append({'name' : characterObject.name, 'title': characterObject.title, 'src': characterObject.character_art})
        print(all_titles)
    dr.quit()
    return print("Finished Creating Dictionary")

def create_csv(dict):
    if Path("titles.csv").exists():
        print("File Exists!")
    else:
        dict_frame = pd.DataFrame(dict)
        dict_frame.to_csv('titles.csv', index=False)
        print("Finished Creating CSV")

def add_to_csv(arr):
    df = pd.DataFrame(arr)
    df.to_csv("titles.csv", mode='a', index=False, header=False)

get_all_names()
remove_dupe_names()
get_all_titles_and_create_classes()
create_csv(all_titles)
add_to_csv(all_titles)

df = pd.read_csv("titles.csv")
select_from_csv = df.sample(n=1)
selected_character = GBFCharacter(select_from_csv["name"].values[0], select_from_csv["title"].values[0])
remaining_guesses = 3
print("This title is: ")
print(selected_character.title)
guess = ''
while guess.lower() != selected_character.name.lower() and remaining_guesses > 0:
    guess = input(
        f"Who's title is this? Guesses remaining {remaining_guesses} \n"
    )

    if guess == selected_character.name:
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
        print(f"Sorry, out of guesses. The character with this title is {selected_character.name}")
