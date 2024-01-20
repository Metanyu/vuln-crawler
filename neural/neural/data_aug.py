import os 
import json
import requests
import re
from datetime import datetime
from getpass import getpass
#API Key: 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
token = getpass('Enter your github token:')
headers = {'authorization': 'Bearer {}'.format(token),
'accept' : 'application/vnd.github+json'
}

def get_first_valid_commit_link(references):
    commit_link_pattern = r'https://github\.com/.+?/commit/[0-9a-f]'
    kernel_link_pattern = r'https://git.kernel.org/.+?/commit/?id=[0-9a-f]'
    links = []
    for commit_url in references:
        #links.append(commit_url)
        
        if re.match(commit_link_pattern, commit_url) or re.match(kernel_link_pattern, commit_url):
            return commit_url
    return None
    
def data_cleaning(data):
    if data.get('semver'):
        data['vulnerableVersions'] = data['semver']['vulnerable']
    if data.get('vulnDescription') and data['vulnDescription'].get('References'):
        link = get_first_valid_commit_link(data['vulnDescription']['References'])
        if link:
            if not (data.get('source_code') and data['source_code'] != []) or not data.get('commitTime'):
                Time, source_code = get_kernel_diff_from_url(link) if 'kernel' in link else get_commit_diff_from_url(link)
                data['commitTime'] = Time
                data['source_code'] = source_code
                
        del data['vulnDescription']['References']
    keys_to_remove = ['description', 'proprietary', 'vulnerableVersions', 'semver', 'packageName', 'breadcrumbItems']
    for key in keys_to_remove:
        if key in data:
            del data[key]
    data = clean_cvss(data)
    reformat_time(data)
    return data
    
def find_file_in_subfolders(directory = 'vuln'):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                data = json.load(f)
            data = data_cleaning(data)
            
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
    print(count)
def get_kernel_diff_from_url(url):
    diff_url = url.replace('commit', 'patch')
    response = requests.get(diff_url, headers=headers)
    diff = response.text
    print(response.status_code)
    # Split the diff into separate files
    if response.status_code != 200:
        raise Exception("No response from server")
    Time = re.search(r'Date: (.*)', diff).group(1)
    files = re.split(r'diff --git a/', diff)[1:]

    # Extract the filename and changes for each file
    diffs = []
    for file in files:
        lines = file.split('\n')
        filename = lines[0].split(' ')[0]
        changes = '\n'.join(line for line in lines if line.startswith('+') or line.startswith('-'))
        diffs.append({'filename': filename, 'diff': changes})
    return Time, diffs
def get_commit_diff_from_url(url):
    # Extract the repo name and commit SHA from the URL    
    parts = url.split('/')
    user = parts[3]
    repo = parts[4]
    sha = parts[6]

    # Construct the API URL
    diff_url = f'https://api.github.com/repos/{user}/{repo}/commits/{sha}'
    print(diff_url)
    # Send the request
    response = requests.get(diff_url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:   
        raise Exception("No response from server")
    # Parse the JSON response
    data = json.loads(response.text)
    Time = data['commit']['committer']['date']
    # Extract the diff from the 'patch' field of each file
    diffs = [{'filename': file['filename'], 'diff': file['patch']} for file in data['files'] if 'patch' in file]
    return Time, diffs
def reformat_time(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if 'Time' in key:
                data[key] = datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
            reformat_time(data[key])
    elif isinstance(data, list):
        for index, item in enumerate(data):
            reformat_time(item)

def remake_cvss(vector):
    elements = vector.split('/')
    result = {key : value for element in elements for key, value in [element.split(':')]}
    key_to_change = {'AV': 'attackVector', 'AC': 'attackComplexity', 'PR': 'privilegesRequired', 'UI': 'userInteraction', 'S': 'scope', 'C': 'confidentiality', 'I': 'integrity', 'A': 'availability'}
    value_to_change = {
        'AV': {'N': 'NETWORK', 'A': 'ADJACENT_NETWORK', 'L': 'LOCAL', 'P': 'PHYSICAL'},
        'AC': {'L': 'LOW', 'H': 'HIGH'},
        'PR': {'N': 'NONE', 'L': 'LOW', 'H': 'HIGH'},
        'UI': {'N': 'NONE', 'R': 'REQUIRED'},
        'S': {'U': 'UNCHANGED', 'C': 'CHANGED'},
        'C': {'N': 'NONE', 'L': 'LOW', 'H': 'HIGH'},
        'I': {'N': 'NONE', 'L': 'LOW', 'H': 'HIGH'},
        'A': {'N': 'NONE', 'L': 'LOW', 'H': 'HIGH'}
    }
    for key, value in result.items():
        if key in value_to_change:
            result[key] = value_to_change[key][value]
    for key, value in key_to_change.items():
        result[value] = result.pop(key)
    return result
    
def clean_cvss(data):
    if data.get('CVSSv3') and isinstance(data['CVSSv3'], str):
        data['CVSSv3'] = remake_cvss(data['CVSSv3'])
    if data.get('cvssDetails'):
        for cvss in data['cvssDetails']:
            cvss.pop('modificationTime', None)
            if isinstance(cvss['cvssV3Vector'], str):
                cvss['cvssV3Vector'] = remake_cvss(cvss['cvssV3Vector'])

    return data

if __name__ == "__main__":
    find_file_in_subfolders()