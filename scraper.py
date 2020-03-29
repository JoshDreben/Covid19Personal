#!/usr/bin/env python

"""Provides a formatted display of new cases in Woodland Hills,
West hills, and Santa Monica. Information is web-scraped from
the Los Angeles County Department of Public Health.
"""
from bs4 import BeautifulSoup
import sys
import requests

__author__ = "Josh Dreben"
__date__ = "2020 March 28"
__license__ = "MIT"
__version__ = "1.1.0"


class scraper:

    def update_data(self, wdh, wsh, sm):
        """Updates the old data with the current data
        Args: 
            wdh: this object's woodland hills object
            wsh: this object's west hills object
            sm: this object's santa monica object
        """
        new = [int(wdh.td.get_text()), int(
            wsh.td.get_text()), int(sm.td.get_text())]
        with open('./olddata.txt', 'w') as f:
            for x in new:
                s = str(x) + '\n'
                f.write(s)

    def get_difference(self, wdh, wsh, sm):
        """Gets the difference in cases between 
        the day before and this data
        Args:
            wdh: this object's woodland hills object
            wsh: this object's west hills objectt
            sm: this objet's santa monica objectt
        Returns:
             the differences as an array in the order of the cities 
        """
        old = []
        with open('./olddata.txt', 'r') as f:
            for line in f:
                old.append(int(line.replace('\n', '')))
        diff = [int(wdh.td.get_text())-old[0],
                int(wsh.td.get_text())-old[1],
                int(sm.td.get_text())-old[2]]
        return diff

    def display_info(self, ts, wdh, wsh, sm, u):
        """Displays the cases of each city in a specific format
        Args:
            ts: time stamp of last updated
            wdh: this object's woodland hills object
            wsh: this object's west hills object
            sm: this object's santa monica object
        """
        if u == 1:
            self.update_data(wdh, wsh, sm)
        diff = self.get_difference(wdh, wsh, sm)
        print('--------------------------')
        print('|', 'Cases', list(ts)[0].strip())
        print('|                         ')
        print('| Woodland Hills: ', wdh.td.get_text(), diff[0])
        print('| West Hills: ', wsh.td.get_text(), diff[1])
        print('| Santa Monica: ', sm.td.get_text(), diff[2])
        print('--------------------------')

    def get_locations(self, rows):
        """Helper method that finds specific cities from the rows
        Args:
            rows: the rows of all the cities
        Returns:
            an array of row objects, each being the specific cities
        """
        for row in rows:
            if(row.th.get_text() == 'Los Angeles - Woodland Hills'):
                self.woodland_hills = row
            if(row.th.get_text() == 'Los Angeles - West Hills'):
                self.west_hills = row
            if(row.th.get_text() == 'City of Santa Monica'):
                self.santa_monica = row
        return [self.woodland_hills, self.west_hills, self.santa_monica]

    def get_page(self, url):
        """Gets the web page at the specified url
        Args:
            url: the url address of the website
        Returns:
            the requests response object form the url
        """
        page = requests.get(url)
        return page

    def get_time_stamp(self, page):
        """Gets the time stamp for when the data was last updated
        Args:
            page: the requests response object of the url
        Returns:
            the updated time stamp
        """
        soup = BeautifulSoup(page.content, 'html.parser')
        dte = soup.find('caption')
        return dte

    def get_location_info(self, page):
        """Uses BeautifulSoup to find the table of cities
        Args:
            page: the requests response object of the website
        Returns:
            the three specified locations as objects
        """
        rows = BeautifulSoup(page.content, 'html.parser').find(
            id='content').tbody.find_all('tr')
        return self.get_locations(rows)

    def __init__(self, update):
        """Constructor
        Initializes the url, gets the time stamp and locations, displays the information
        """
        self.url = 'http://publichealth.lacounty.gov/media/Coronavirus/locations.htm'
        time_stamp = self.get_time_stamp(self.get_page(self.url))
        locations = self.get_location_info(self.get_page(self.url))
        self.display_info(
            time_stamp, locations[0], locations[1], locations[2], update)


def command_line_help():
    print('--------------------------')
    print('| How to use this program:       ')
    print('| Show Data + Change: -sc       ')
    print('| Update Old Data: -u       ')
    print('|-------------------------')


if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        command_line_help()
    else:
        opts = [opt for opt in sys.argv[1:] if opt.startswith('-')]
        if '-u' in opts:
            s = scraper(1)
        elif '-sc' in opts:
            s = scraper(0)
        else:
            print('Whoops! Unrecognized command line arg')
            command_line_help()
