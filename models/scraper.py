from bs4 import BeautifulSoup
import requests
import urllib.request
import time

def get_html(url):
    """
    Retrieve the HTML from the website.
    """
    response = requests.get(url)
    if (200 <= response.status_code < 300):
        return response.text
    else:
        return None

def get_clubs_html():
    """
    Get the HTML of online clubs with Penn.
    """
    url = 'https://ocwp.pennlabs.org'
    return get_html(url)

def soupify(html):
    """
    Load HTML into BeautifulSoup so we can extract data more easily

    Note that for the rest of these functions, whenever we refer to a "soup", we're refering
    to an HTML document or snippet which has been parsed and loaded into BeautifulSoup so that
    we can query what's inside of it with BeautifulSoup.
    """
    return BeautifulSoup(html, "html.parser")

def get_elements_with_class(soup, elt, cls):
    """
    Returns a list of elements of type "elt" with the class attribute "cls" in the
    HTML contained in the soup argument.

    For example, get_elements_with_class(soup, 'a', 'navbar') will return all links
    with the class "navbar".

    Important to know that each element in the list is itself a soup which can be
    queried with the BeautifulSoup API. It's turtles all the way down!
    """
    return soup.findAll(elt, {'class': cls})

def get_clubs(soup):
    """
    This function should return a list of soups with each soup corresponding to the html
    for a single club.
    """
    return get_elements_with_class(soup, "div", "box")

def get_club_name(club):
    """
    Returns the string of the name of a club, when given a soup containing the data for a single club.

    We've implemented this function for you to demonstrate how to use the provided utility functions.
    """
    elts = get_elements_with_class(club, 'strong', 'club-name')
    if len(elts) < 1:
        return ''
    return elts[0].text

def get_club_description(club):
    """
    Extract club description from a soup containing a single club.
    """
    desc = club.findAll('em')
    if len(desc) < 1:
        return ""
    return desc[0].text

def get_club_tags(club):
    """
    Get the tag labels for all tags associated with a single club.
    """
    return list(map(lambda x: x.text, club.findAll('span')))
