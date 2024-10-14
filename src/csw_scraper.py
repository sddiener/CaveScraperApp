import sys
import requests
from bs4 import BeautifulSoup
import os
import re
from dataclasses import dataclass
from datetime import date
from urllib.parse import urlparse


@dataclass
class CaveInfo:
    name: str
    overview: str
    history: str
    location: str
    access: str
    description: str
    tackle: str
    video: str
    references: str
    warnings: str
    disclaimer: str


def fetch_cave_info(url: str) -> CaveInfo:
    """
    Fetches cave information from a given URL.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        CaveInfo: A dataclass containing the extracted cave information.

    Raises:
        requests.exceptions.RequestException: If there's an error fetching the URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Save raw HTML and text
        save_raw_html(url, response.content)
        save_raw_text(url, response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return CaveInfo("", "", "", "", "", "", "", "", "", "", "")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract sections
    cave_name = extract_cave_name(soup)
    overview = extract_section(soup, "Overview")
    history = extract_section(soup, "History")
    location = extract_section(soup, "Location")
    access = extract_section(soup, "Access")
    description = extract_section(soup, "Description")
    tackle = extract_section(soup, "Tackle")
    video = extract_video(soup)
    references = extract_references(soup)
    warnings = extract_section(soup, "Warnings")
    disclaimer = extract_section(soup, "Disclaimer")

    return CaveInfo(cave_name, overview, history, location, access, description, tackle, video, references, warnings, disclaimer)


def extract_cave_name(soup: BeautifulSoup) -> str:
    """
    Extracts the cave name from the first header or title tag found.
    """
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text(strip=True)
    elif soup.title:
        return soup.title.get_text(strip=True)
    return 'Unknown Cave'


def extract_section(soup: BeautifulSoup, section_name: str) -> str:
    """
    Extracts text from a section based on a header (div with class 'subheaders').
    """
    section = soup.find('div', class_='subheaders', string=re.compile(section_name, re.IGNORECASE))
    if section:
        section_content = []
        for sibling in section.next_siblings:
            if sibling.name == 'div' and 'subheaders' in sibling.get('class', []):
                break
            if hasattr(sibling, 'get_text'):
                section_content.append(sibling.get_text(strip=True))
            elif isinstance(sibling, str):
                section_content.append(sibling.strip())
        return "\n".join(filter(None, section_content))
    return ""


def extract_video(soup: BeautifulSoup) -> str:
    """
    Extracts video link from a video section, if present.
    """
    section = soup.find('div', class_='subheaders', string=re.compile("Video", re.IGNORECASE))
    if section:
        # Look for a link or embedded video
        video_link = section.find_next('a', href=True)
        if video_link:
            return video_link['href']
    return ""


def extract_references(soup: BeautifulSoup) -> str:
    """
    Extracts references and links from the 'References' section.
    """
    section = soup.find('div', class_='subheaders', string=re.compile("References", re.IGNORECASE))
    if section:
        section_content = []
        for sibling in section.next_siblings:
            if sibling.name == 'div' and 'subheaders' in sibling.get('class', []):
                break
            if hasattr(sibling, 'get_text'):
                section_content.append(sibling.get_text(strip=True))
            if sibling.name == 'a' and sibling.get('href'):
                # Add the link along with the text
                section_content.append(f"Link: {sibling['href']}")
        return "\n".join(filter(None, section_content))
    return ""


def sanitize_filename(name: str) -> str:
    """
    Sanitizes the filename by replacing illegal characters.
    """
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.strip().replace(' ', '_')


def save_raw_html(url: str, content: bytes):
    """
    Saves the raw HTML content of the webpage.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path.strip('/').replace('/', '_')
    today = date.today().isoformat()

    filename = f"{today}_{domain}_{path}.html"
    sanitized_filename = sanitize_filename(filename)

    raw_html_dir = os.path.join('data', 'raw_html')
    os.makedirs(raw_html_dir, exist_ok=True)

    file_path = os.path.join(raw_html_dir, sanitized_filename)

    try:
        with open(file_path, 'wb') as file:
            file.write(content)
        print(f"Raw HTML saved to '{file_path}'")
    except IOError as e:
        print(f"Error saving raw HTML to '{file_path}': {e}")


def save_raw_text(url: str, content: bytes):
    """
    Saves all the text from the webpage.
    """
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator="\n", strip=True)

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path.strip('/').replace('/', '_')
    today = date.today().isoformat()

    filename = f"{today}_{domain}_{path}.txt"
    sanitized_filename = sanitize_filename(filename)

    raw_text_dir = os.path.join('data', 'raw_text')
    os.makedirs(raw_text_dir, exist_ok=True)

    file_path = os.path.join(raw_text_dir, sanitized_filename)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Raw text saved to '{file_path}'")
    except IOError as e:
        print(f"Error saving raw text to '{file_path}': {e}")


def save_parsed_cave_info(cave_info: CaveInfo):
    """
    Saves the parsed cave information to a text file in the 'parsed_cave_info_texts' directory.
    """
    today = date.today().isoformat()
    sanitized_name = sanitize_filename(cave_info.name)
    filename = f"{today}_{sanitized_name}_info.txt"

    parsed_dir = os.path.join('data', 'parsed_cave_info_texts')
    os.makedirs(parsed_dir, exist_ok=True)

    file_path = os.path.join(parsed_dir, filename)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Cave Name: {cave_info.name}\n\n")
            file.write(f"Overview:\n{cave_info.overview}\n\n")
            file.write(f"History:\n{cave_info.history}\n\n")
            file.write(f"Location:\n{cave_info.location}\n\n")
            file.write(f"Access:\n{cave_info.access}\n\n")
            file.write(f"Description:\n{cave_info.description}\n\n")
            file.write(f"Tackle:\n{cave_info.tackle}\n\n")
            file.write(f"Video:\n{cave_info.video}\n\n")
            file.write(f"References:\n{cave_info.references}\n\n")
            file.write(f"Warnings:\n{cave_info.warnings}\n\n")
            file.write(f"Disclaimer:\n{cave_info.disclaimer}\n")
        print(f"Cave information successfully saved to '{file_path}'")
    except IOError as e:
        print(f"Error writing to file '{file_path}': {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <URL>")
        print("Error: URL must be provided as a command-line argument.")
        sys.exit(1)

    url = sys.argv[1]
    cave_info = fetch_cave_info(url)
    save_parsed_cave_info(cave_info)
