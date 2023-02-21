"""
Ein kleines Programm, das die Nachrichten der Tagesschau anzeigt.
"""

import curses
from bs4 import BeautifulSoup
import requests as req

Kategorien = ['Startseite',
              'Inland',
              'Ausland',
              'Wirtschaft',
              'Wissen',
              'Faktenfinder',
              'Investigativ']

def print_news(stdscr, selected_row_idx):
    """ gibt die Nachrichten der ausgewählten Kategorie aus """
    url = 'https://www.tagesschau.de/'
    if selected_row_idx != 0:
        url += Kategorien[selected_row_idx].lower()
    response = req.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('span', class_='teaser__headline')

    curses.curs_set(0)
    print_center_list(stdscr, titles)

    stdscr.refresh()
    stdscr.getch()

def print_menu(stdscr, selected_row_idx):
    """ gibt die Menüauswahl aus für die Kategorien """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    # stdscr.addstr(height//2 - 3, width//2 - len('Themen')//2, 'Themen')
    stdscr.addstr(0, 0, 'Themenauswahl')
    for idx, kategorie in enumerate(Kategorien):
        x_position = (width//2 - len(kategorie)//2)
        y_position = height//2 - len(Kategorien)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y_position, x_position, kategorie)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y_position, x_position, kategorie)
    stdscr.refresh()

def print_center(stdscr, text):
    """ gibt den Text in der Mitte des Bildschirms aus """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    x_position = width//2 - len(text)//2
    y_position = height//2
    stdscr.addstr(y_position, x_position, text)
    stdscr.refresh()

def print_center_list(stdscr, content):
    """ gibt die Liste in der Mitte des Bildschirms aus """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    for i, row in enumerate(content):
        x_position = width//2 - len(row)//2
        y_position = height//2 - len(content)//2 + i
        stdscr.addstr(y_position, x_position, row.text)
    stdscr.refresh()

def main(screen):
    """ Hauptprogramm """
    url = 'https://www.tagesschau.de'
    response = req.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('span', class_='teaser__headline')

    curses.curs_set(0)
    height, width = screen.getmaxyx()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)

    text=titles[0].text
    x_position = width//2 - len(text)//2
    y_position = height//2
    screen.attron(curses.color_pair(1))
    screen.addstr(y_position, x_position, text)
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
