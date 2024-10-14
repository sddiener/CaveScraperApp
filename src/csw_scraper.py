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
    description: str
    trip_suggestions: str
    warnings: str
    access_details: str


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

        # Save raw HTML
        save_raw_html(url, response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return CaveInfo("", "", "", "", "")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract cave name
    cave_name = extract_cave_name(soup)

    # Extract main content
    main_content = extract_main_content(soup)

    # Extract specific sections
    description = extract_section(main_content, "Description")
    trip_suggestions = extract_section(main_content, "Trip Suggestions")
    warnings = extract_section(main_content, "Warnings")
    access_details = extract_section(main_content, "Access")

    return CaveInfo(cave_name, description, trip_suggestions, warnings, access_details)


def extract_cave_name(soup: BeautifulSoup) -> str:
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text(strip=True)
    elif soup.title:
        return soup.title.get_text(strip=True)
    return 'Unknown Cave'


def extract_main_content(soup: BeautifulSoup) -> BeautifulSoup:
    main_content = soup.find('div', {'id': 'caveInfo'})
    if not main_content:
        main_content = soup.find('div', {'id': 'content'})
    if not main_content:
        main_content = soup.body
    return main_content


def extract_section(content: BeautifulSoup, section_name: str) -> str:
    section = content.find(lambda tag: tag.name in ["h2", "div"] and section_name.lower() in tag.text.lower())
    if section:
        section_content = []
        for sibling in section.find_next_siblings():
            if sibling.name in ["h2", "div"] and any(header in sibling.text.lower() for header in ["description", "history", "location", "access", "tackle", "warnings"]):
                break
            section_content.append(sibling.get_text(strip=True))
        return "\n".join(filter(None, section_content))
    return ""


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.strip().replace(' ', '_')


def save_raw_html(url: str, content: bytes):
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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <URL>")
        print("Error: URL must be provided as a command-line argument.")
        sys.exit(1)

    url = sys.argv[1]
    cave_info = fetch_cave_info(url)

    sanitized_name = sanitize_filename(cave_info.name)
    output_filename = f"{sanitized_name}_info.txt"

    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(f"Cave Name: {cave_info.name}\n\n")
            file.write(f"Description:\n{cave_info.description}\n\n")
            file.write(f"Trip Suggestions:\n{cave_info.trip_suggestions}\n\n")
            file.write(f"Warnings:\n{cave_info.warnings}\n\n")
            file.write(f"Access Details:\n{cave_info.access_details}\n")
        print(f"Cave information successfully saved to '{output_filename}'")
    except IOError as e:
        print(f"Error writing to file '{output_filename}': {e}")
