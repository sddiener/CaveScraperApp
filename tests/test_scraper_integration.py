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

    # Check if other fields are populated
    assert cave_info.description != ""
    assert "The cave consists of a series of low crawls" in cave_info.description

    assert cave_info.trip_suggestions != ""

    assert cave_info.warnings != ""
    assert "The cave is located on the Castlemartin Firing Range" in cave_info.warnings

    assert cave_info.access_details != ""
    assert "Cavers should now contact the Cambrian Caving Council" in cave_info.access_details

    # Print the extracted info for manual verification
    print(f"Cave Name: {cave_info.name}")
    print(f"Description: {cave_info.description[:100]}...")  # First 100 characters
    print(f"Trip Suggestions: {cave_info.trip_suggestions[:100]}...")
    print(f"Warnings: {cave_info.warnings[:100]}...")
    print(f"Access Details: {cave_info.access_details[:100]}...")
