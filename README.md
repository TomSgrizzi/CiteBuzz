# LingBuzz Citation Generator

## Overview

CiteBuzz is a Flask-based web application designed to generate citations in BibTeX and APA formats for papers hosted on the LingBuzz website. The app scrapes the necessary details from the provided LingBuzz URL and returns formatted citations.

## Features

- **Generate BibTeX Citation:** Retrieve a BibTeX citation from a LingBuzz paper URL.
- **Generate APA Citation:** Retrieve an APA citation from a LingBuzz paper URL.
- **Mobile-friendly Interface:** Simple mobile interface available on mobile devices.

## Installation

To run this application locally, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/TomSgrizzi/CiteBuzz.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd master
    ```

3. **Install Dependencies:**

    Make sure you have Python 3 installed. Install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

    Create a `requirements.txt` file with the following contents:

    ```text
    Flask==2.3.4
    requests==2.31.0
    beautifulsoup4==4.12.2
    ```

4. **Run the Application:**

    Start the Flask server:

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:5000/`.

## Usage

    Simply paste your LingBuzz link in the input field and select your preferred citation style.
    
- **Generate BibTeX Citation:**
- 
    Example response:

    ```json
    {
        "bibtex": "@article{author_year,\n    title={Paper Title},\n    doi={some-doi},\n    year={2024},\n    author={Author, A.},\n    link={https://lingbuzz.net/some-paper},\n    note = {Published in: Some Journal},\n    journal=LingBuzz\n}"
    }
    ```

- **Generate APA Citation:**

    Example response:

    ```json
    {
        "apa": "Author, A. (2024). Paper Title. Some Journal. Retrieved from https://lingbuzz.net/some-paper"
    }
    ```

## Error Handling

The application handles the following errors:

- **Invalid URL:** If the provided URL does not start with `https://lingbuzz.net/`, an error message is returned:

    ```json
    {
        "error": "Not a LingBuzz link"
    }
    ```

- **Failed Retrieval:** If the request to the LingBuzz URL fails (e.g., non-200 HTTP status code), an error message is returned:

    ```json
    {
        "error": "Failed to retrieve the webpage. Status code: [status_code]"
    }
    ```

- **Missing Content:** If required content cannot be found on the page, an error message is returned:

    ```json
    {
        "error": "The required content could not be found on the page."
    }
    ```

- **Missing URL Parameter:** If the `url` parameter is not provided in the request, a 400 Bad Request error is returned:

    ```json
    {
        "error": "URL is required"
    }
    ```

## Development

Feel free to contribute to this project by submitting issues or pull requests. For local development, ensure that you follow best practices for Python and Flask application development.


## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework I used.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - For HTML parsing.
- [Requests](https://requests.readthedocs.io/) - For HTTP requests.

