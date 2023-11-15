from bs4 import BeautifulSoup
import requests
import re


def main():
    user_input = "the simpsons"
    link = get_link(user_input)
    shows = search(link)
    print(link)
    seasons = get_seasons(shows[1])
    print(shows[1])
    episodes = get_episodes(seasons["1"])
    print(seasons["1"])
    print(episodes["2"])
    print(watch_link(shows[1], episodes["2"]))
    

# given link scrapes site and returns list of shows that are made up of dicts with titles, links etc. if none found returns false
def search(URL):
    #loads entire page
    page = requests.get(URL)
    page_soup = BeautifulSoup(page.content, 'html.parser')

    #gets all show 
    shows_html = page_soup.find_all("div", {"class": "film-detail"})

    #creates a list for shows
    shows = []
    for show_html in shows_html:
        show = {}

        # gets action tag each element and grabs link and title
        a_tag = show_html.find("a")
        
        #changes link from relative to absolute
        if a_tag.get("href").startswith("/"):
            show["link"] = 'https://ev01.sx' + a_tag.get("href")
        else:
            show["link"] = a_tag.get("href")

        show["title"] = a_tag.get("title")
        show["id"] = show["link"].split("online-")[1]

        #gets all span elements and adds quality
        span_elements = show_html.find_all("span")
        show["quality"] = span_elements[0].text
        
        #checks if show is movie or series
        if span_elements[1].text.startswith("SS"):
            #series
            show["type"] = "series"
            # seasons refers to latest season or in this case number of seasons
            show["seasons"] = span_elements[1].text[3:]
            # episodes refers to latest season
            show["episodes"] = span_elements[2].text[4:]
        else:
            #movie
            show["type"] = "movie"
            #year of release
            show["year"] = span_elements[1].text
            #length in minutes
            show["length"] = span_elements[2].text.removesuffix("m")

        shows.append(show)

    if shows == []:
        return False
    
    return shows


# given search term string removes bad characters and formats search link
def get_link(user_search):
    #remove all non alphanumeric, or whitespace characters
    fixed_search = re.sub(r"[^a-zA-Z0-9_ .,]", "", user_search)

    #replace all whitespaces with dashes
    fixed_search = re.sub(r" ", "-", fixed_search)

    #returns fixed search link
    return "https://ev01.sx/search/" + fixed_search


# takes show and returns list of dicts with season and id
def get_seasons(show):
    #checks if show is of type series and returns error message if wrong
    if not show["type"] == "series":
        return "Error: Not a show"
    
    #creates URL
    URL = "https://ev01.sx/ajax/season/list/" + show["id"]

    #loads entire page
    page = requests.get(URL)
    page_soup = BeautifulSoup(page.content, 'html.parser')

    seasons_html = page_soup.find_all("a")

    seasons = []
    for i, season_html in enumerate(seasons_html):

        # in case of series mr robot series are separated lik so: season_1.0 might be better to just grab text and not do any conversions
        season = season_html.text
        id = season_html.get("id").split("-")[1]

        seasons.append({"title": season, "id": id})

    return seasons

# takes in season_id and fetches episode names and numbers
def get_episodes(season):    
    #creates URL
    URL = "https://ev01.sx/ajax/season/episodes/" + season["id"]

    #loads entire page
    page = requests.get(URL)
    page_soup = BeautifulSoup(page.content, 'html.parser')

    episodes_html = page_soup.find_all("a")

    episodes = []
    for episode_html in episodes_html:
        
        episode, title = episode_html.get("title").split(": ", 1)
        episode = episode.split(" ")[1]
        id = episode_html.get("data-id")

        episodes.append({"title" : title, "id" : id})

    return episodes


def watch_link(show, episode):

    URL = "https://ev01.sx/ajax/episode/servers/" + episode["id"]

    #loads entire page
    page = requests.get(URL)
    page_soup = BeautifulSoup(page.content, 'html.parser')

    if first_tag := page_soup.find("a", {"title" : "Server MegaCloud"}):
        pass
    else:
        first_tag = page_soup.find("a")

    id = first_tag.get("data-id")

    return show["link"].replace("tv", "watch-tv") + "." + id
    

if __name__ == "__main__":
    main()