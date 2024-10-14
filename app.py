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
