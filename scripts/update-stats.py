import requests
from bs4 import BeautifulSoup
import os
import re
from dotenv import load_dotenv
import textwrap

# Load environment variables from .env file if it exists
load_dotenv()

# GitHub API Headers
headers = {
    "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github.v3+json"
}

STARS_SPAN_TEMPLATE = textwrap.dedent('''
<span class="stars">
    <svg aria-hidden="true" height="19" viewBox="0 0 16 16" version="1.1" width="19" data-view-component="true" class="octicon-star-fill">
        <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"></path>
    </svg>
    {{stars}}
</span>
''')

FORKS_SPAN_TEMPLATE = textwrap.dedent('''
    <span class="forks">
    <svg aria-hidden="true" height="19" viewBox="0 0 16 16" version="1.1" width="19" data-view-component="true" class="octicon-repo-forked">
        <path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"></path>
    </svg>
    {{forks}}
</span>
''')

DELIMITER = '''<span class="dot">&#8226</span>'''


def fetch_github_stats(repo_url):
    api_url = f"https://api.github.com/repos/{repo_url}"
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Fetched data for {repo_url}: {data['stargazers_count']} stars, {data['forks_count']} forks")
        return data['stargazers_count'], data['forks_count']
    else:
        print(f"Failed to fetch data for {repo_url}: {response.status_code}")
        return None, None


def update_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    for link in soup.find_all('a', href=True):
        href = link['href']
        if re.match(r'https://github.com/.+/.+', href):
            repo_path = href.replace('https://github.com/', '').strip('/')
            stars, forks = fetch_github_stats(repo_path)

            new_stars_span = BeautifulSoup(STARS_SPAN_TEMPLATE.replace('{{stars}}', str(stars)), 'html.parser')
            new_forks_span = BeautifulSoup(FORKS_SPAN_TEMPLATE.replace('{{forks}}', str(forks)), 'html.parser')
            # new_delimiter = BeautifulSoup(DELIMITER, 'html.parser')

            # Remove the existing "stars" and "forks" spans

            stats_div = link.find_next('div', class_='stats')

            # Remove existing stars and forks spans
            for old_span in stats_div.find_all('span', class_=['stars', 'forks']):
                old_span.decompose()

            # Remove existing delimiters
            for old_delimiter in stats_div.find_all('span', class_='dot'):
                old_delimiter.decompose()

            # If there is already another span in the stats div, add a delimiter
            if (stars or forks) and stats_div.find('span'):
                print('Adding delimiter')
                stats_div.append(BeautifulSoup(DELIMITER, 'html.parser'))

            # Add the new stars and forks spans
            if forks:
                stats_div.append(new_forks_span)
                if stars:
                    print('Adding delimiter')
                    stats_div.append(BeautifulSoup(DELIMITER, 'html.parser'))

            # Add the new stars span
            if stars:
                stats_div.append(new_stars_span)

    # Write the updated HTML back to the file
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify(formatter="html5"))


if __name__ == "__main__":
    html_path = os.path.join(os.path.dirname(__file__), '../index.html')
    update_html(html_path)
