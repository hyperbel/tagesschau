import curses
from bs4 import BeautifulSoup
import requests as req

def main():
    url = 'https://www.tagesschau.de'
    r = req.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.find_all('span', class_='teaser__headline')
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    # print titles
    stdscr = curses.initscr()
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(0, 0, 'Press q to quit')
    for i, title in enumerate(titles):
        stdscr.addstr(i+1, 0, title.text)

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
    curses.endwin()

if __name__ == "__main__":
    main()
