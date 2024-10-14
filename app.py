import os
import pdfkit  # To convert HTML to PDF
from jinja2 import Environment, FileSystemLoader
import streamlit as st
from src.csw_scraper import fetch_cave_info

# Streamlit app for scraping cave info

st.title("Cave Info Scraper")

# Input field for URL
url = st.text_input("Enter the Cave Info URL:", "")

if st.button("Fetch Cave Info"):
    if url:
        # Fetch cave info from the provided URL
        cave_info = fetch_cave_info(url)

        if cave_info.name:
            st.success(f"Successfully fetched data for: {cave_info.name}")

            # Display cave info sections
            st.header("Overview")
            st.write(cave_info.overview or "No Overview available")

            st.header("History")
            st.write(cave_info.history or "No History available")

            st.header("Location")
            st.write(cave_info.location or "No Location available")

            st.header("Access")
            st.write(cave_info.access or "No Access details available")

            st.header("Description")
            st.write(cave_info.description or "No Description available")

            st.header("Tackle")
            st.write(cave_info.tackle or "No Tackle information available")

            st.header("Video")
            if cave_info.video:
                st.markdown(f"[Watch Video]({cave_info.video})")
            else:
                st.write("No Video available")

            st.header("References")
            st.write(cave_info.references or "No References available")

            st.header("Warnings")
            st.write(cave_info.warnings or "No Warnings available")

            st.header("Disclaimer")
            st.write(cave_info.disclaimer or "No Disclaimer available")
        else:
            st.error("Failed to fetch cave info. Please check the URL.")
    else:
        st.warning("Please enter a URL.")


# Load Jinja2 template
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('a5_template.html')

# Cave Info Example
cave_info = {
    'cave_name': 'Ogof Gofan',
    'overview': 'This is an overview of Ogof Gofan.',
    'description': 'A description of the cave.',
    'trip_suggestions': 'Suggestions for trips to Ogof Gofan.',
    'warnings': 'Some warnings.',
    'access': 'Access details.'
}

# User input for selecting sections
st.title("Cave Info A5 Formatter")

sections_to_include = {
    'overview': st.checkbox('Include Overview', value=True),
    'description': st.checkbox('Include Description', value=True),
    'trip_suggestions': st.checkbox('Include Trip Suggestions', value=True),
    'warnings': st.checkbox('Include Warnings', value=True),
    'access': st.checkbox('Include Access Details', value=True)
}

if st.button("Generate A5 PDF"):
    # Filter selected sections for Jinja2
    filtered_info = {k: cave_info[k] for k, v in sections_to_include.items() if v}

    # Render the HTML content using Jinja2
    rendered_html = template.render(**filtered_info)

    # Convert to PDF (you'll need wkhtmltopdf installed)
    pdf_output_path = "output.pdf"
    pdfkit.from_string(rendered_html, pdf_output_path)

    # Display the PDF as a download button
    with open(pdf_output_path, 'rb') as pdf_file:
        st.download_button("Download A5 PDF", data=pdf_file, file_name="cave_info_a5.pdf")
