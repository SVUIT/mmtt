import os
import requests

folder_path = "./docs"
base_url = "https://svuit.org/mmtt/docs"

def get_urls(folder_path, base_url):
    urls = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                relative_path = os.path.relpath(root, folder_path)
                if relative_path == ".":
                    relative_path = ""
                url_path = os.path.join(relative_path, file).replace("\\", "/")
                url = f"{base_url}/{url_path}".replace(".md", ".html")
                urls.append(url)
    return urls