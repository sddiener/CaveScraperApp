import pdfkit
from jinja2 import Environment, FileSystemLoader
import streamlit as st
from src.csw_scraper import fetch_cave_info, CaveInfo  # Assuming CaveInfo is your dataclass

# Streamlit app for scraping cave info
st.title("Cave Info Scraper")

# Input field for URL
url = st.text_input("Enter the Cave Info URL:", "")

# Use session state to persist cave_info across interactions
if "cave_info" not in st.session_state:
    st.session_state.cave_info = None

# Button to fetch cave info
if st.button("Fetch Cave Info"):
    if url:
        # Fetch cave info from the provided URL
        cave_info = fetch_cave_info(url)

        if cave_info and cave_info.name:
            st.session_state.cave_info = cave_info  # Store in session state
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

# Only show the next section if cave_info has been successfully fetched
if st.session_state.cave_info:
    cave_info = st.session_state.cave_info  # Retrieve from session state

    # Set up the environment for Jinja2
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('a5_template.html')

    # User input for selecting sections
    st.title("Cave Info A5 Formatter")

    sections_to_include = {
        'overview': st.checkbox('Include Overview', value=True),
        'history': st.checkbox('Include History', value=False),
        'location': st.checkbox('Include Location', value=True),
        'access': st.checkbox('Include Access Details', value=True),
        'description': st.checkbox('Include Description', value=True),
        'warnings': st.checkbox('Include Warnings', value=True),
        'tackle': st.checkbox('Include Tackle', value=True),
    }

    # Filter selected sections for Jinja2
    filtered_info = {
        'cave_name': cave_info.name,
        'overview': cave_info.overview if sections_to_include['overview'] else '',
        'history': cave_info.history if sections_to_include['history'] else '',
        'location': cave_info.location if sections_to_include['location'] else '',
        'access': cave_info.access if sections_to_include['access'] else '',
        'description': cave_info.description if sections_to_include['description'] else '',
        'warnings': cave_info.warnings if sections_to_include['warnings'] else '',
        'tackle': cave_info.tackle if sections_to_include['tackle'] else '',
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
