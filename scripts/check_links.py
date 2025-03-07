import os
import re
import requests
from urllib.parse import urljoin
import time
# Folder containing markdown files
folder_path = "./docs"
# Original URL of the website
base_url = "https://svuit.org/mmtt/docs"
# GitHub repo details
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY") 
GITHUB_TOKEN = os.getenv("ISSUE_API")  

# Browser emulation header to avoid blocking
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_urls_from_folder(folder_path, base_url):
    """Get a list of URLs from markdown files in a directory."""
    urls = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                relative_path = os.path.relpath(root, folder_path).replace("\\", "/")
                url_path = os.path.join(relative_path, file).replace("\\", "/")
                url = f"{base_url}/{url_path}".replace(".md", ".html")
                urls.append(url)
    return urls

def extract_urls_from_markdown(file_path, base_url):
    """Extract all URLs from Markdown file, keeping anchor (#) intact."""
    links = []
    link_pattern = r"\[.*?\]\((.*?)\)"
    
# Get the original URL of the current markdown file
    relative_path = os.path.relpath(file_path, folder_path).replace("\\", "/")
    base_file_url = f"{base_url}/{relative_path}".replace(".md", ".html")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            matches = re.findall(link_pattern, content)
            for match in matches:
                if match.startswith(("http://", "https://")):
                    full_url = match 
                elif match.startswith("#"):
                    full_url = base_file_url + match  # Link anchor 
                elif match.startswith("/"):
                    full_url = urljoin(base_url, match) 
                else:
                    full_url = urljoin(base_file_url, match) 

                links.append(full_url)
    except Exception as e:
        print(f"⚠️Error reading {file_path}: {e}")
    return links

def check_url(url):
    """Check if the URL works."""
    for i in range(3): 
        try:
            response = requests.head(url, timeout=30, headers=HEADERS, allow_redirects=True)
            if 404 <= response.status_code <= 500:
                return False, response.status_code
            return True, response.status_code
        except requests.RequestException as e:
            if i < 2:
                time.sleep(5)
            else:
                return False, str(e)

def create_github_issue(broken_urls):
    """Create an issue on GitHub with a list of broken links."""
    print(f"GITHUB_REPOSITORY: {os.getenv('GITHUB_REPOSITORY')}")
    print(f"ISSUE_API: {'Found' if os.getenv('ISSUE_API') else 'Not found'}")

    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("⚠️GITHUB_TOKEN or GITHUB_REPOSITORY not found. Abandoning issue creation.")
        return

    issue_title = "🚨 Broken Links Detected!"
    issue_body = "List of broken links detected:\n\n"
    for error in broken_urls:
        issue_body += f"- {error}\n"

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": issue_title,
        "body": issue_body,
        "labels": ["broken-links"],
        "assignees": ["hlocuwu", "dynsnsky", "VietHoang-206"]
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("✅Issue created successfully!")
    else:
        print(f"❌Error creating issue: {response.status_code} - {response.text}")

if __name__ == '__main__':
    print("Collecting list of URLs from directories...")

    folder_urls = get_urls_from_folder(folder_path, base_url)
    markdown_links = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                markdown_links.extend(extract_urls_from_markdown(file_path, base_url))

    all_urls = list(set(folder_urls + markdown_links))

    broken_urls = []
    total_count = len(all_urls)
    checked_count = 0

    print(f"🔗Total number of URLs to check: {total_count}")

    for url in all_urls:
        checked_count += 1
        print(f"({checked_count}/{total_count}) Check: {url} ...", end=" ")
        is_available, status = check_url(url)
        if not is_available:
            print(f"❌ERROR ({status})")
            broken_urls.append(f"{url} ➝ Error: {status}")
        else:
            print(f"✅Work ({status})")

    if broken_urls:
        create_github_issue(broken_urls)
    else:
        print("\n🎉All URLs are valid!")
