import curses
from bs4 import BeautifulSoup
import requests as req

Kategorien = ['Startseite', 'Inland', 'Ausland', 'Wirtschaft', 'Wissen', 'Faktenfinder', 'Investigativ']

def print_news(stdscr, selected_row_idx):
    url = 'https://www.tagesschau.de/' + Kategorien[selected_row_idx].lower() if selected_row_idx != 0 else 'https://www.tagesschau.de'
    r = req.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.find_all('span', class_='teaser__headline')

    curses.curs_set(0)
    for i, title in enumerate(titles):
        print_center(stdscr, title.text, i)

    stdscr.getch()

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(Kategorien):
        x = w//2 - len(row)//2
        y = h//2 - len(Kategorien)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def print_center(stdscr, text, y_offset=0):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

def main(screen):
    url = 'https://www.tagesschau.de'
    r = req.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.find_all('span', class_='teaser__headline')

    curses.curs_set(0)
    h,w = screen.getmaxyx()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)

    text=titles[0].text
    x = w//2 - len(text)//2
    y = h//2
    screen.attron(curses.color_pair(1))
    screen.addstr(y, x, text)
    screen.attroff(curses.color_pair(1))

    current_row_idx = 0
    print_menu(screen, current_row_idx)

    while 1:
        key = screen.getch()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(Kategorien)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # print_center(screen, "You selected '{}'".format(Kategorien[current_row_idx]))
            # screen.getch()
            print_news(screen, current_row_idx)

            
        print_menu(screen, current_row_idx)


    screen.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
