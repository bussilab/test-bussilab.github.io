import json
import requests
from datetime import datetime
import yaml
import os
import sys
import re
import markdown
from html import escape


FEED_URL = "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed"

user_handle="bussilab.bsky.social"
profile_handle="bussilab.bsky.social"
# Configuration
ALLOWED_DOMAINS = ['disq.us', 'bit.ly', 't.co', 'doi.org']
MAX_DISPLAY_LENGTH = 25


def fetch_authorfeed(actor):
    params = {"actor": actor}
    response = requests.get(FEED_URL, params=params)
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

def render_markdown(text):
    """Convert Markdown to HTML."""
    return markdown.markdown(text)

def preformat_text(content):
    """Process text for URLs after rendering Markdown."""
    # Placeholder to temporarily store <a> tags
    anchor_placeholders = []

    # Step 1: Temporarily remove <a> tags
    def replace_anchor(match):
        anchor_placeholders.append(match.group(0))
        return f"ANCHOR_PLACEHOLDER_{len(anchor_placeholders) - 1}"

    content = re.sub(r'<a [^>]+>.*?<\/a>', replace_anchor, content, flags=re.IGNORECASE)

    # Step 2: Process remaining text for URLs
    def format_url(match):
        full_url = match.group(0)

        # Separate trailing punctuation and HTML tags
        trailing_punctuation_match = re.search(r'([.,:!]+)?(<\/?\w+.*?>)?$', full_url)
        trailing_punctuation = trailing_punctuation_match.group(1) if trailing_punctuation_match else ""
        trailing_tag = trailing_punctuation_match.group(2) if trailing_punctuation_match else ""

        # Remove trailing punctuation and tags from the URL
        url_without_trailing = re.sub(r'([.,:!]+)?(<\/?\w+.*?>)?$', '', full_url)

        # Determine if the URL is complete (starts with http/https)
        is_full_url = url_without_trailing.startswith("http://") or \
                      url_without_trailing.startswith("https://")

        # Format the display URL (strip "http://", "https://")
        display_url = re.sub(r'https?://', '', url_without_trailing)
        shortened_display = (display_url[:MAX_DISPLAY_LENGTH] + '...') if len(display_url) > MAX_DISPLAY_LENGTH else display_url

        # Determine final URL (add https:// for partial URLs)
        if not is_full_url:
            domain = url_without_trailing.split('/')[0]  # Extract domain
            if domain in ALLOWED_DOMAINS:
                final_url = f"https://{url_without_trailing}"
            else:
                return full_url  # Leave non-whitelisted partial URLs unchanged
        else:
            final_url = url_without_trailing

        # Return the clickable link with preserved punctuation and trailing HTML tags
        return (
            f'<a href="{final_url}" target="_blank">{shortened_display}</a>'
            + (trailing_punctuation or "")
            + (trailing_tag or "")
        )

    # Regex to match full and partial URLs
    url_pattern = re.compile(
        r'((https?:\/\/[\w.-]+\.[a-z]{2,}(\/\S*)?)|([\w.-]+\.[a-z]{2,}\/\S*))'
    )
    content = re.sub(url_pattern, format_url, content)

    # Step 3: Restore original <a> tags
    def restore_anchor(match):
        index = int(match.group(1))
        return anchor_placeholders[index]

    content = re.sub(r'ANCHOR_PLACEHOLDER_(\d+)', restore_anchor, content)

    return content





def process_posts(posts_file, formatted_file):
    """Process posts to generate a formatted text dictionary."""
    with open(posts_file, 'r') as file:
        posts = yaml.safe_load(file)

    formatted_posts = {}

    for post in posts:
        if 'text' in post:
            original_text = post['text']
            # Step 1: Render Markdown
            rendered_text = render_markdown(original_text)
            # Step 2: Preformat links
            formatted_text = preformat_text(rendered_text)
            # Store the formatted text using the URL as the key
            formatted_posts[post['url']] = formatted_text

    # Write to the formatted posts file
    with open(formatted_file, 'w') as file:
        yaml.safe_dump(formatted_posts, file, allow_unicode=True)

    print(f"Formatted posts saved to {formatted_file}")


if __name__ == "__main__":
    posts_file=sys.argv[1]

    labfeed=fetch_authorfeed(profile_handle)

    print(labfeed)

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
            print(line,end="")

    with open(posts_file) as f:
       text=f.read()


    process_posts(posts_file,re.sub(".yml$","_preformatted_text.yml",posts_file))


