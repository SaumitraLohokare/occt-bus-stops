from requests import get
from bs4 import BeautifulSoup, Tag

from urls import ROOT_URL, DESTINATIONS_PATH

def contains_link(item):
    return item.a != None

def store_route_stops(route_name):
    file_name = "locations/" + route_name[1:] + ".txt"
    f = open(file_name, "w")
    
    page = get(ROOT_URL + route_name)
    soup = BeautifulSoup(page.content, "html.parser")
    
    table_rows = soup.find_all("tr")

    for row in table_rows[1:]:
        children = row.findChildren()
        if len(list(children)) == 0:
            continue
        try:
            name = children[0].getText()
            link = children[1].a.get("href")
        except:
            print("ERROR in: ", route_name, children[1])
            continue
        try:
            at_index = link.index("@")
            lat_long = link[at_index+1:].split(",")[0:2]
            f.write(f"{name}:{lat_long[0]},{lat_long[1]}\n")
        except:
            print("ERROR in :", route_name, name, link)
    f.close()

if __name__ == "__main__":
    response = get(ROOT_URL + DESTINATIONS_PATH)
    soup = BeautifulSoup(response.content, "html.parser")

    items = filter(contains_link, soup.find_all("p", { "class": "" }))
    for item in items:
        store_route_stops(item.a.get("href"))
    # store_route_stops(list(items)[0].a.get("href"))