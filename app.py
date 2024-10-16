import pdfkit
from jinja2 import Environment, FileSystemLoader
import streamlit as st
from src.csw_scraper import fetch_cave_info, CaveInfo  # Assuming CaveInfo is your dataclass

# Streamlit app for scraping cave info
st.set_page_config(layout="wide")  # Set wide layout for better visualization

# Title of the app
st.title("Cave Info Scraper")

# Use session state to persist cave_info across interactions
if "cave_info" not in st.session_state:
    st.session_state.cave_info = None
    st.session_state.formatted_text = {}

# Sidebar for inputs
with st.sidebar:
    # Input field for URL
    url = st.text_input("Enter the Cave Info URL:", "")

    # Button to fetch cave info
    if st.button("Fetch Cave Info"):
        if url:
            # Fetch cave info from the provided URL
            cave_info = fetch_cave_info(url)

            if cave_info and cave_info.name:
                st.session_state.cave_info = cave_info  # Store in session state
                st.session_state.formatted_text = {
                    "overview": cave_info.overview,
                    "history": cave_info.history,
                    "location": cave_info.location,
                    "access": cave_info.access,
                    "description": cave_info.description,
                    "warnings": cave_info.warnings,
                    "tackle": cave_info.tackle,
                }
                st.success(f"Successfully fetched data for: {cave_info.name}")
            else:
                st.error("Failed to fetch cave info. Please check the URL.")
        else:
            st.warning("Please enter a URL.")

    # User input for selecting sections
    st.header("Select Sections to Include")
    sections_to_include = {
        'overview': st.checkbox('Include Overview', value=True),
        'history': st.checkbox('Include History', value=False),
        'location': st.checkbox('Include Location', value=True),
        'access': st.checkbox('Include Access Details', value=True),
        'description': st.checkbox('Include Description', value=True),
        'warnings': st.checkbox('Include Warnings', value=True),
        'tackle': st.checkbox('Include Tackle', value=True),
    }

    # Buttons for formatting options
    if st.session_state.cave_info:
        if st.button("AI Format Text"):
            # Placeholder for AI formatting (can call an AI API or function here)
            for key in st.session_state.formatted_text:
                if sections_to_include.get(key, False):
                    # Here you would replace this with the AI formatted text
                    st.session_state.formatted_text[key] = f"**Formatted**: {st.session_state.formatted_text[key]}"

        if st.button("Reset to Original Text"):
            cave_info = st.session_state.cave_info
            for key in st.session_state.formatted_text:
                st.session_state.formatted_text[key] = getattr(cave_info, key)

# Main content area
if st.session_state.cave_info:
    cave_info = st.session_state.cave_info  # Retrieve from session state

    # Display selected sections
    st.header(f"Preview: {cave_info.name}")
    for section, include in sections_to_include.items():
        if include and st.session_state.formatted_text.get(section):
            st.subheader(section.capitalize())
            st.write(st.session_state.formatted_text[section])

    # Set up the environment for Jinja2
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('a4_template.html')

    # Filter selected sections for Jinja2
    filtered_info = {
        'cave_name': cave_info.name,
        'overview': st.session_state.formatted_text['overview'] if sections_to_include['overview'] else '',
        'history': st.session_state.formatted_text['history'] if sections_to_include['history'] else '',
        'location': st.session_state.formatted_text['location'] if sections_to_include['location'] else '',
        'access': st.session_state.formatted_text['access'] if sections_to_include['access'] else '',
        'description': st.session_state.formatted_text['description'] if sections_to_include['description'] else '',
        'warnings': st.session_state.formatted_text['warnings'] if sections_to_include['warnings'] else '',
        'tackle': st.session_state.formatted_text['tackle'] if sections_to_include['tackle'] else '',
    }

    # Render the HTML content using Jinja2
    rendered_html = template.render(**filtered_info)

    # Convert to PDF and provide download link
    if st.button("Generate A4 PDF"):
        try:
            pdf_output_path = "output.pdf"
            # Try generating the PDF
            pdfkit.from_string(rendered_html, pdf_output_path)

            # Display the PDF as a download button
            with open(pdf_output_path, 'rb') as pdf_file:
                st.download_button("Download A4 PDF", data=pdf_file, file_name="cave_info_a4.pdf")
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
