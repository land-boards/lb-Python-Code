#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import json
import argparse

DEBUG = False
VERBOSE = False

class LibOfCongBookRetriever:
    """
        Gets a book's info from LOC
    """
    def __init__(self, driver):
        self.driver = driver

    def rows_to_py_object(self, rows):
        """
            Converts senenium driver results (rows) to a python dictionary
        """
        py_object = {}
        for row in rows:
            td_elements = row.find_elements_by_tag_name("td")
            th_elements = row.find_elements_by_tag_name("th")

            if len(th_elements) == 0 or len(td_elements) == 0: continue
            if len(td_elements[0].text) == 0: continue
            key, value = self.translate_key(th_elements[0].text), td_elements[0].text

            if key not in py_object:
                py_object[key] = value

        return py_object

    def translate_key(self, key):
        """
            Translates key from english to a more acceptable key format
        """
        return key.lower().replace(" ", "_").replace(":", "").replace(".", "").replace("--_", "")

    def get_book_by_call_number(self, call_number):
        """
            GIven a call number, try to get that book. Returns None if none is found
        """
        self.driver.get("http://catalog.loc.gov/")
        search_box = self.driver.find_element_by_name("Search_Arg")
        search_box.send_keys(call_number)
        search_box.send_keys(Keys.RETURN)

        table = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form[1]/table/tbody")))

        # Check to make sure that the book was found
        try:
            self.driver.find_element_by_class_name("nohits")
            return None
        except:
            pass

        rows = table.find_elements_by_tag_name("tr")
        return self.rows_to_py_object(rows)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rip book info from loc')
    parser.add_argument('-i', default="book_batch.pyon", metavar="<input file>", help='pyon file containing a list of call numbers')
    parser.add_argument('-o', default="book_info.json", metavar="<output file>", help='json file where the book info will be written')
    parser.add_argument('--verbose', dest="verbose", help="shows outputs", action="store_true")
    args = parser.parse_args()

    VERBOSE = args.verbose

    driver = webdriver.PhantomJS() if not DEBUG else webdriver.Firefox()
    retriever = LibOfCongBookRetriever(driver)

    with open(args.i, 'r') as f:
        call_numbers = eval(f.read())
        if VERBOSE: print "Read:", args.i

    results = []
    for call_number in call_numbers:
        if VERBOSE: print "Processing:", call_number
        book = retriever.get_book_by_call_number(call_number)
        if book:
            if VERBOSE: print "Found:", call_number
            results.append(book)
        else:
            if VERBOSE: print "Could not find:", call_number

    with open(args.o, 'w') as f:
        f.write(json.dumps(results, sort_keys=True, indent=4, separators=(',', ': ')))
        if VERBOSE: print "Wrote:", args.o

    driver.close()
