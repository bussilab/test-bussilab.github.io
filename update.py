import json
import requests
from datetime import datetime
import yaml
import os

LOGIN_URL = "https://bsky.social/xrpc/com.atproto.server.createSession"
FEED_URL = "https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed"

user_handle="bussilab.bsky.social"
profile_handle="bussilab.bsky.social"
posts_file="_data/posts.yml"
bsky_token=os.environ["BSKY_TOKEN"]

def get_access_token(username, password):
    data = {"identifier": username, "password": password}
    response = requests.post(LOGIN_URL, json=data)
    if response.status_code == 200:
        return response.json().get("accessJwt")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def fetch_authorfeed(access_token, actor):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"actor": actor}
    response = requests.get(FEED_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to format the text with the '|' style
def convert_to_yaml(data):
    if len(data)==0: return ""

    # Customize the YAML dumper to always use the block scalar style for multiline text
    class IndentedTextDumper(yaml.Dumper):
        def represent_scalar(self, tag, value, style=None):
            if "\n" in value:  # Use block style for multiline text
                style = "|"
            return super().represent_scalar(tag, value, style)

    # Dump the data to YAML
    return yaml.dump(data, Dumper=IndentedTextDumper, sort_keys=False)

def processfeed(profile_handle,feed):
    posts=[]
    for post in feed["feed"]:
        if not "reason" in post and not "reply" in post:
            timestamp=post["post"]["record"]["createdAt"]
            date=datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            uri=post["post"]["uri"]
            post_id = uri.split("/")[-1]  # Extracts "3lbei2pbnok2y"
            url = f"https://bsky.app/profile/{profile_handle}/post/{post_id}"
            posts.append(
                {"date":  str(date),
                 "text": post["post"]["record"]["text"],
                 "uri": uri,
                 "url": url
                })
    return posts

def get_current_urls(path):
    with open(path) as f:
        urls=[]
        for post in yaml.safe_load(f):
            if "url" in post:
                urls.append(post["url"])
        return urls


if __name__ == "__main__":

    token=get_access_token(user_handle,"dzmt-mf66-cthq-rfvg")
    labfeed=fetch_authorfeed(token,profile_handle)

    current_urls=get_current_urls(posts_file)
    posts=[item for item in processfeed(profile_handle,labfeed) if not item["url"] in current_urls]
    add_posts=convert_to_yaml(posts)

    with open(posts_file) as f:
        lines = [line for line in f]

    newlines=[]
    done=False
    for line in lines:
        if not done and line[0]=="-":
            newlines.append(add_posts)
            done=True
        newlines.append(line)
    if not done:
        newlines.append(add_posts)
    with open(posts_file,"w") as f:
        for line in newlines:
            print(line,end="",file=f)

