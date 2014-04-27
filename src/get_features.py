"""
Downloads and parses the variables table from the documentation
author: chris @ sihrc
"""

#Python Modules
import urllib2, unicodedata, re, sys
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
    try:
        page = urllib2.urlopen(config.tables.format(datafile.lower())).read()
    except:
        print "HTTP Failed: Check your connection to the internet or check the name of the datafile"
        sys.exit()
    with open(config.path("..","data",datafile,"data", "tables.txt"), 'wb') as f:
        f.write(page)
    return page

@debug
def read_tables(datafile):
    """
    From get_features.py
    Parses the HTML as plain text
    Returns dictionary of {titles:variables}
    """
    path = config.path("..","data",datafile,"data", "tables.txt")
    if not config.os.path.exists(path):
        page = download(datafile)
    else:
        with open(path, 'rb') as f:
            page = f.read()
    start = page.find("<a name=\"DVariable\">")
    if start == -1:
        start = page.rfind("Variable-Source Crosswalk</a>")
    page = page[start:]
    end = page.rfind("<a name=\"Appendix")
    soup = Soup(page[:end])
    titles, tables = [], []
    found_tables = soup.find_all("table", summary= re.compile("This table identifies the variable .*"))
    for table in found_tables:
        title = table.caption if table.caption != None else table.find_previous_sibling("p", {"class":"contentStyle"})
        titles.append(title.text.encode("utf-8"))
        tables.append([var.text.encode("utf-8") for var in table.find_all("th")[3:]])

    if not (len(titles) == len(tables) and titles != [] and [] not in tables):
        return False

    return dict(zip(titles,tables))


if __name__ == "__main__":
    print read_tables(sys.argv[1])