from bs4 import BeautifulSoup
import requests

def main():
    print(search("simpsons"))

def search(name):
    #TODO: build proper link function
    URL = "https://ev01.sx/search/" + name

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
        show["link"] = a_tag.get("href")
        show["title"] = a_tag.get("title")

        #gets all span elements
        span_elements = show_html.find_all("span")


        shows.append(show)

    return shows_html[0]


if __name__ == "__main__":
    main()