import requests, os, re
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file
gist_token = os.getenv("GIST_TOKEN")  
Gist_id = os.getenv("GIST_ID")  

def get_json_gist(): # Function to get the JSON content of a Gist file where we store the GHL tokens
    headers = {
        "Authorization": f"Bearer {gist_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Make the request
    url = f"https://api.github.com/gists/{Gist_id}"
    response = requests.get(url, headers=headers)

    return response.json()  # Return the JSON response

def update_tks_in_gist(t, r_t): # Function to update the Gist file with new tokens when expired
    url = f"https://api.github.com/gists/{Gist_id}"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {gist_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
        "files": {
            "gistfile1.txt": {
                "content":  f"Token: {t}\nRefresh_token: {r_t}\n"
            }  
        }
    }
    return requests.patch(url, headers=headers, json=data).json()  # Return the JSON response of the update request

def retrieve_tks_json(json_file): # Function to retrieve tokens from the JSON content of the Gist file

    Tokens = json_file['files']['gistfile1.txt']['content']  # Get the content of the gist file

    # Regular expression pattern to retrieve both token and refresh_token
    pattern = r"Token: ([^\n]+)\nRefresh_token: ([^\n]+)"

    # Check if there's a match between pattern and file content 
    match = re.search(pattern, Tokens)

    if match:
        t = match.group(1)  # Retrieves the Token value
        refresh_t = match.group(2)  # Retrieves the Refresh_token value
        return t, refresh_t
    else:
        print("No tokens found!")
        return "", ""  # Return None for both if not found




