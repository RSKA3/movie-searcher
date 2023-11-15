# lib imports
import sys
import os
import webbrowser
import inquirer

# file imports
from sites import EV01


def main():

    os.system('clear')

    while True:
        user_input = get_input("Show or movie: ")
        link = EV01.get_link(user_input)
        if shows := EV01.search(link):
            break
        else:
            print("No show found with search:", user_input)
    picked_show = choose_show(shows[0:5])

    os.system('clear')

    if picked_show["type"] == "series":
        seasons = EV01.get_seasons(picked_show)
        picked_season = choose_season(seasons)

        os.system('clear')
        episodes = EV01.get_episodes(picked_season)
        picked_episode = choose_episode(episodes)

        URL = EV01.watch_link(picked_show, picked_episode)
    else:
        URL = picked_show["link"]

    os.system('clear')
    print(URL)
    webbrowser.open(URL)
    sys.exit(0)


    
def choose_episode(episodes):
    questions = [
    inquirer.List(
        "episode",
        message="Pick an episode",
        choices = [f"{i+1} {episode['title']}" for i, episode in enumerate(episodes)]
            ),
    ]

    answer = inquirer.prompt(questions)
    return episodes[int(answer["episode"][0])-1]

def choose_season(seasons):

    questions = [
    inquirer.List(
        "season",
        message="Pick a season",
        choices = [f"{i+1} {season['title']}"for i, season in enumerate(seasons)]
            ),
    ]

    answer = inquirer.prompt(questions)
    return seasons[int(answer["season"][0])-1]


def choose_show(shows):
    show_options = []
    for i, show in enumerate(shows):
        option = f"{i} {show['type'].capitalize()}: {show['title']} ({show['year'] if 'year' in show.keys() else show['seasons'] + ' seasons'})"
        show_options.append(option)

    questions = [
    inquirer.List(
        "show",
        message="Pick a show",
        choices = show_options
            ),
    ]

    # gets answer and turns it into the value in shows
    answer = inquirer.prompt(questions)
    answer = answer["show"].split()[0]
    show = shows[int(answer)]
    return show

def get_input(prompt):
    while True:
        try: 
            show = str(input(prompt))
            if len(show) > 0:
                return show
        except ValueError:
            pass
        except (EOFError, KeyboardInterrupt):
            sys.exit("EOFError or KeyboardInterrupt")


if __name__ == "__main__":
    main()