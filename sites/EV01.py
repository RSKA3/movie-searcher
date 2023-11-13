from bs4 import BeautifulSoup
import requests
import re

def main():

    show_link = "https://ev01.sx/tv/watch-the-fresh-prince-of-belair-online-38438"
    get_episode(show_link)




# given link scrapes site and returns list of shows that are made up of dicts with titles, links etc.
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
        show["link"] = 'https://ev01.sx' + a_tag.get("href")
        show["title"] = a_tag.get("title")

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

    return shows


# given search term string removes bad characters and formats search link
def build_link(user_search):
    #remove all non alphanumeric, or whitespace characters
    fixed_search = re.sub(r"[^a-zA-Z0-9_ .,]", "", user_search)

    #replace all whitespaces with dashes
    fixed_search = re.sub(r" ", "-", fixed_search)

    #returns fixed search link
    return "https://ev01.sx/search/" + fixed_search

#TODO: get seasons and episodes and be able to navigate them
# this will have to be implemented with selenium since the seasons and episodes takes a second to load
# perhaps by making the browser "headless" or using phantomJS and finding the episodes


if __name__ == "__main__":
    main()