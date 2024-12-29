import yaml
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

def check_url(url):
    try:
         response = requests.head(url, timeout=5)
         if 400 <= response.status_code <= 599:
            return False
        else True
        except requests.RequestException:
                return False

def create_issue(repo_name, title, body, github_token):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.create_issue(title=title, body=body)
    return issue

 if __name__ == "__main__":
    folder_path = "./docx"  
    base_url = "https://svuit.org/mmtt/docs"
    github_token = "${{ secrets.GITHUB_TOKEN }}"  
    repo_name = "${{https://github.com/SVUIT/mmtt}}" 

    urls = get_urls(folder_path)
    for url in urls:
        if not check_url(url):
            print(f"URL không hoạt động: {url}")
            title = f"URL không hoạt động: {url}"
            body = f"URL này không hoạt động (trả về mã trạng thái HTTP lỗi): {url}"
            create_github_issue(repo_name, title, body, github_token)   

