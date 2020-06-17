from __future__ import print_function
import json
import pycurl
import re
import requests
import sys
import webbrowser
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import spynner
import pyquery
import au

def smart_spider_search(subject) :
    url = "http://www.google.com/search?q=" + subject #Root query to Google Search Engine
    source_code = requests.get(url) #Goes to url
    plain_text = source_code.text #Turns script to text
    soup = BeautifulSoup(plain_text, "html.parser") #Organize/align page data

    i = -1
    results = []
    for header in soup.findAll("h3", {"class" : 'r'}) : #!!!EVERY CLASS KEY-ITEM MUST HAVE '-title' APPENDED VAR. IN THIS CASE, VAR = 'desc'!!!
        anchor = header.find_next('a') #Find the next anchor tag, which is its corresponding link
        link = anchor.get("href")[7:] #Obtain the hypertext reference, excluding the first extraneous seven characters
        #STRIP LINK OF GARBAGE IN URL HERE
        if link[0:4] != "http" or nonTextSite(link) :
            continue #Invalid url, so skip

        try :
            link = link[0: link.index('&')]
            link = link[0: link.index('%')]
        except ValueError as e :
            z = 0


        if i > -1 and i < 11 : #Only appends to link to results list with length 11
            results.append(link)
            peruse(link)
            #break
        elif i >= 11 : #Sentinel condition
            break

        i += 1 #Increment
    for site in results :
        print(site + '\n')

def nonTextSite(address) :
    if ("facebook" in address or
        "instagram" in address or
        "twitter" in address or
        "youtube" in address or
        "rollingstone" in address or
        "imdb" in address or
        "deezer" in address
        ) : return 1
    else :
        return 0

def peruse(webpage) :
    print(webpage)
    source_code = requests.get(webpage) #Goes to url
    plain_text = source_code.text #Turns script to text
    soup = BeautifulSoup(plain_text, "html.parser") #Organize/align page data

    for context in soup.findAll('p') : #!!!EVERY CLASS KEY-ITEM MUST HAVE '-title' APPENDED VAR. IN THIS CASE, VAR = 'desc'!!!
        text = context.text # Grab text between markup, convert to string
        text = textSiteFilter(webpage, text)
        print(text)

def textSiteFilter(site, content) :
    #if ("wikipedia" in site) :
    content = re.sub(r'([a-z])\. ([a-z])', '\g<1> \g<2>', content)  # Substitutes or subtracts textual patterns like (i.e Inc. is...) to (i.e Inc is...)
    content = re.sub(r'["()[\]{}“”]', '', content) #Subtract special characters

    content = re.sub(r'(&add;)', '+', content) # Replaces HTML code with +
    content = re.sub(r'(&amp;)', '&', content) # Replaces HTML code with &
    content = re.sub(r'(&apos;)', '\'', content) # Replaces HTML code with '
    content = re.sub(r'(&equal;)', '=', content) # Replaces HTML code with =
    content = re.sub(r'(&exclamation;)', '!', content) # Replaces HTML code with !
    content = re.sub(r'(&gt;)', '>', content) # Replaces HTML code with >
    content = re.sub(r'(&lt;)', '<', content) # Replaces HTML code with <
    content = re.sub(r'(&percent;)', '%', content) # Replaces HTML code with %
    content = re.sub(r'(&quot;)', '\"', content) # Replaces HTML code with "

    content = re.sub(r'([A-Z]+)([a-z]{1,3})([.])+([ ])*([a-z0-9])', '\g<1>\g<2>_ \g<4>\g<5>', content)

    ### BEGINNING OF COMMA FILTERING - ONLY , IS BETWEEN TWO NUMBERS ###
    content = re.sub(r'([0-9.]+)[,]([ ])*([A-z])', '\g<1> \g<2>\g<3>', content)
    content = re.sub(r'([A-z.]+)[,]([ ])*([A-z])', '\g<1> \g<2>\g<3>', content)
    content = re.sub(r'([A-z.]+)[,]([ ])*([0-9])', '\g<1> \g<2>\g<3>', content)
    ### END COMMA FILTERING ###

    content = re.sub(r'([A-Z]+)([.])([ ]+)([A-Z]+)', '\g<1>_\g<3>\g<4>', content) # Changes abbrev. like D.J. Khalid to D_J_ Khalid
    ### ENCASE TITLE ABBREVIATIONS TO PROTECT FROM ALTERATIONS ###
    content = re.sub(r'(Dr[.])|(Esq[.])|(Hon[.])|(Jr[.])|(Mr[.])|(Mrs[.])|(Ms[.])|(Messrs[.])|(Mmes[.])|(Msgr[.])|(Prof[.])|(Rev[.])|(Rt[.]Hon[.])|(Sr[.])', '&\g<1>;', content)

    content = re.sub(r'\. ', '.\n', content) # Changes every ending to a sentence to start on a new line for readability
    content = re.sub(r'[&;]', '', content) # Remove any encasing
    content = re.sub(r'_', '.', content) # Changes _ back to .
    content = re.sub(r'([ ]+)', ' ', content) # Subtracts extraneous spaces
    content = re.sub(r'(\n+)', '\n', content) # Subtracts extraneous newlines

    return content

def smart_spider_define(subject):
    url = "http://www.google.com/search?q=define+" + subject # Root query to Google Search Engine for defining something
    #url = 'http://avi.im/stuff/js-or-no-js.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text)

    print(soup)

    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)

    CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application"
    CHROMEDRIVER_PATH = "C:\\Users\\Nick\PycharmProjects\PythonTutorials\chromedriver.exe"
    WINDOW_SIZE = "1920,1080"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              port=0,
                              options=None,
                              service_args=None,
                              desired_capabilities=None,
                              service_log_path=None,
                              chrome_options=chrome_options
                              )

    driver.get("http://www.google.com")

    driver.get_screenshot_as_file("capture.png")
    driver.close()

    # check out the docs for the kinds of things you can do with 'find_all'
    # this (untested) snippet should find tags with a specific class ID
    # see: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class
    print(soup)
    soup = BeautifulSoup(page, 'html.parser')
    source_code = requests.get(url) # Goes to url, set timeout to 5 millisecs to grab info before javascript adjust HTML script
    plain_text = source_code.text # Turns script to text
    soup = BeautifulSoup(plain_text, "html.parser") # Organize/align page data

    # Loop lists the definition(s)
    print(url)
    for tag in soup.findAll("ol", {"style" : "padding-left:20px"}) :
        for definition in tag.findAll('li', {"style" : "list-style-type:decimal"}) : #Find all HMTL tag(s) with corresponding attribute
            text = definition.text # For each HTML tag of this type, grab text between markup, convert to string
            print(text)


smart_spider_search('michael+jackson')
smart_spider_define('artist')
html = urlopen("https://www.facebook.com/")
print(html.read())
print('hi')
browser = spynner.Browser(debug_level=spynner.INFO)
browser.create_webview()
browser.show()
browser.load("http://www.wordreference.com")
browser.load_jquery(True)
browser.choose("input[name=lr=lang_es]")
browser.click("input[name=enit]")
browser.click("a[class=l]:first")
d = pyquery.PyQuery(browser.html)
d.make_links_absolute(base_url=browser.url)
href = d('a:last').attr('href')
print(href)
print(len(browser.download(href)))
browser.browse()