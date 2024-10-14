# CaveScraperApp

## Description

A web application that generates formatted cave trip descriptions for caving club members.

## Project Overview

The Cave Trip Planner is designed to streamline the process of creating printable cave trip descriptions. It scrapes data from "Caves of South Wales" website, formats the information into an A5-sized document, and allows users to customize the output.

### Key Features
- Web scraping from "Caves of South Wales" website
- Extraction of essential cave information (name, description, trip suggestions, warnings, access details)
- Formatting of data into A5-sized, print-ready documents
- User-friendly web interface for inputting cave URLs and customizing output
- Docker containerization for easy local deployment

### Future Enhancements
- Support for multiple cave data sources
- Customizable trip planning based on user preferences
- Integration of cave surveys and maps
- Text editing capabilities before printing
- Expanded output format options
- User accounts for saving trip plans
- Online deployment for wider accessibility

## Installation
```
pip install -e .
```

## Usage
TODO: Add usage instructions

## Development
1. Activate the virtual environment:
   ```
   source .venv/bin/activate
   ```
2. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```
3. Run tests:
   ```
   pytest
   ```
