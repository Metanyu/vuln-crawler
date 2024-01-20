import requests
import json
from bs4 import BeautifulSoup
import re
import js2py
import ast 

def get_link(soup):
    links = []
    for link in soup.find_all('a'):
        commit_url  = link.get('href')
        links.append(commit_url)
        
        # if re.match(commit_link_pattern, commit_url):
        #     return commit_url
    return links


def Cleaning(data):
    for key in data:
        if type(data[key]) == dict:
            Cleaning(data[key])
        
        elif type(data[key]) == str :
            soup = BeautifulSoup(data[key], 'html.parser')
            if(key == 'References'):
                data[key] = get_link(soup)
            else:
                data[key] = soup.get_text(separator=' ')
                data[key] = data[key].replace('\n', ' ')
                data[key] = data[key].replace('\t', ' ')
    replacements = {
        r',\s*}': '}',
        r',\s*\]': ']',
        " +": " "
    }
    for old, new in replacements.items():
        data = re.sub(old, new, str(data))
    return  ast.literal_eval(data)


def get_data(url = 'https://security.snyk.io/vuln/SNYK-PHP-MOODLEMOODLE-6141131'):
    # The URL of the web page
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the script tag with the '__NUXT__' function
    script_tag = soup.find('script', text=re.compile('__NUXT__'))
    # Extract the JavaScript code from the script tag
    js_code = script_tag.string
    # Use js2py to evaluate the JavaScript code
    result = js2py.eval_js(js_code)
    # Turn result into dict
    result = ast.literal_eval(str(result))['data'][0]
    result = Cleaning(result)
    return result 
