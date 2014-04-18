"""
Downloads and parses the variables table from the documentation
author: chris @ sihrc
"""

#Python Modules
import urllib2, unicodedata
from bs4 import BeautifulSoup as Soup

#Local Modules
import config
from wrappers import debug

@debug
def download(datafile):
    """
    From get_features.py\n
    Downloads the documentation as text file from HTML
    """
    page = urllib2.urlopen(config.tables.format(datafile.lower())).read()
    with open(config.path("..","data",datafile,"data", "tables.txt"), 'wb') as f:
        f.write(page)
    return page


@debug
def read_tables(datafile):
    """
    From get_features.py\n
    Parses the HTML as plain text
    Returns dictionary of {titles:variables}
    """
    path = config.path("..","data",datafile,"data", "tables.txt")
    if not config.os.path.exists(path):
        page = download(datafile)
    else:
        with open(path, 'rb') as f:
            page = f.read()
    start = page.find("<a name=\"DVariable\">D. Variable-Source Crosswalk</a>")
    page = page[start:]
    end = page.find("<a name=\"Appendix1\">")
    soup = Soup(page[:end])
    titles = [str(title.text) for title in soup.find_all("p",{"class":"contentStyle"})][2:]
    # print page[:end][:1000]
    tables = []
    for line in soup.find_all("table",{"class":"contentStyle"}):
        tables.append([str(tag.text) for tag in line.find_all("th")][3:])
    
    variables = dict(zip(titles,tables))
    return variables

if __name__ == "__main__":
    read_tables("H147")