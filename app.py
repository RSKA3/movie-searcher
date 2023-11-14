# lib imports
import sys

# file imports
import sites.EV01 as EV01

def main():
    user_input = get_input("Show or movie: ")
    link = EV01.get_link(user_input)
    shows = EV01.search(link)
    

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