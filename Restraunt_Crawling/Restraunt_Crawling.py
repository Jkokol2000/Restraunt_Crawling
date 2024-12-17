import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from random import choice
import re

last_name = ""
base_url = "https://gbf.wiki"
tier_url = "https://gbf.wiki/SSR_Characters_List"
dr = webdriver.Chrome()
all_names = []
all_titles = []
class GBFCharacter:
    def __init__(self, name, title):
        self.name = name
        self.title = title
    def __str__(self):
        return f"{self.name} : {self.title}"
    def __iter__(self):
        return iter([self.name, self.title])

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

def get_all_titles_and_create_classes():
    url = '/'
    while url:
        if all_names:
            new_name = choice(all_names)    
            last_name = new_name    
            all_names.remove(new_name)
            url = "/" + new_name
            sleep(3)
        else:
            url = None
        dr.get(f"{base_url}{url}")
        print(f"Now Scraping {base_url}{url}")
        soup = BeautifulSoup(dr.page_source, "html.parser")
        current_title = soup.find(class_="char-title")
        current_title_in_brackets = re.findall(r"\[(.*?)\]", current_title.get_text())
        print(current_title_in_brackets)
        characterObject = GBFCharacter(new_name, current_title_in_brackets)
        all_titles.append(characterObject)
        print(all_titles)
        

def create_csv(arr):
    with open("titles.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for char in arr:
            writer.writerow(list(char))

get_all_names()
get_all_titles_and_create_classes()
create_csv(all_titles)





selected_character = choice(all_titles)
remaining_guesses = 3
print("This title is: ")
print(selected_character.title)

guess = ''
while guess.lower() != selected_character.name.lower() and remaining_guesses > 0:
    guess = input(
        f"Who's title is this? Guesses remaining {remaining_guesses}"
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

