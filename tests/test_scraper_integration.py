import pytest
from src.csw_scraper import fetch_cave_info


@pytest.mark.integration
def test_fetch_cave_info_integration():
    # Sample URL from Caves of South Wales website
    url = "http://www.ogof.org.uk/ogof-gofan.html"

    # Fetch cave info
    cave_info = fetch_cave_info(url)

    # Assert that we got a valid CaveInfo object
    assert cave_info is not None

    # Check if the cave name is correct
    assert cave_info.name == "Ogof Gofan"

    # Check if the overview is populated
    assert cave_info.overview != ""
    assert "The cave consists of a series of low crawls" in cave_info.overview or "Ogof Gofan is located" in cave_info.overview

    # Check if history is populated
    assert cave_info.history != ""
    assert "first explored by Mel Davies" in cave_info.history

    # Check if location is populated
    assert cave_info.location != ""
    assert "located in the sea cliffs" in cave_info.location

    # Check if access details are populated
    assert cave_info.access != ""
    assert "Cavers should now contact" in cave_info.access

    # Check if description is populated
    assert cave_info.description != ""
    assert "A climb down the slope" in cave_info.description

    # Check if tackle section is populated
    assert cave_info.tackle != ""
    assert "Entrance pitch" in cave_info.tackle

    # Check if the video section has a link (or is empty if no video is present)
    assert cave_info.video == "" or cave_info.video.startswith("http")

    # Check if references contain links or text
    assert cave_info.references != ""
    assert "Cambrian Cave Registry" in cave_info.references or "Link:" in cave_info.references

    # Check if warnings are populated
    assert cave_info.warnings != ""
    assert "The cave is located on the Castlemartin Firing Range" in cave_info.warnings

    # Check if disclaimer is populated
    assert cave_info.disclaimer != ""
    assert "Caving can be a dangerous activity" in cave_info.disclaimer

    # Print the extracted info for manual verification
    print(f"Cave Name: {cave_info.name}")
    print(f"Overview: {cave_info.overview[:100]}...")
    print(f"History: {cave_info.history[:100]}...")
    print(f"Location: {cave_info.location[:100]}...")
    print(f"Access: {cave_info.access[:100]}...")
    print(f"Description: {cave_info.description[:100]}...")
    print(f"Tackle: {cave_info.tackle[:100]}...")
    print(f"Video: {cave_info.video}")
    print(f"References: {cave_info.references[:100]}...")
    print(f"Warnings: {cave_info.warnings[:100]}...")
    print(f"Disclaimer: {cave_info.disclaimer[:100]}...")
