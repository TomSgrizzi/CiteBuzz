from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Let's check the url
def is_lingbuzz_url(url):
    return url.startswith("https://lingbuzz.net/")

# Function to generate BibTeX citation
def generate_bibtex_citation(url):
    if not is_lingbuzz_url(url):
        print(str(url))
        return {"error": "Not a LingBuzz link"}
    
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to retrieve the webpage. Status code: {}".format(response.status_code)}

    soup = BeautifulSoup(response.text, 'html.parser')
    center_tag = soup.find('center')

    if not center_tag:
        return {"error": "The required content could not be found on the page."}
    
    ####       FINDING PUBLISHING INFOs     #####
    prettified = soup.prettify()
    lines = prettified.split('\n')

    # Pattern search:
    pattern = "Published in:"
    index = -1
    for i, line in enumerate(lines):
        if pattern in line:
            index = i
            print("Pattern found")
            break

    # If pattern found:
    if index != -1 and index + 2 < len(lines):
        following_line = lines[index + 3]
        publisher = following_line.strip()
        print(following_line.strip())
    else:
        print("Pattern not found or not enough lines in the content.")

    paper_title = center_tag.find('a').get_text(strip=True) if center_tag.find('a') else "No Title Found"
    authors_links = center_tag.find_all('a')[1:]  # Skip paper title in the first line
    authors = [link.get_text(strip=True) for link in authors_links]
    publication_date = center_tag.contents[-1].strip()

    authors_converted_list = ['{}, {}'.format(' '.join(name.split()[1:]), name.split()[0]) for name in authors]
    authors_converted = ' and '.join(authors_converted_list)

    match = re.search(r'\d{4}', publication_date)
    year = match.group() if match else 'n.d.'

    idarticle = authors[0].split()[1]+"_"+year

    template = """
    @article{{{id_citation},
        title={{{title}}},
        doi={{ {link}}},
        year={{{year}}},
        author={{{author}}},
        link={{{link_extended}}},
        note = {{{published}}},
        journal=LingBuzz
    }}
    """
    filled_template = template.format(id_citation=idarticle, title=paper_title, link=url[21:], year=year, author=authors_converted, link_extended=url, published=publisher)
    return {"bibtex": filled_template}

# Here's the function to generate APA citation
def generate_apa_citation(url):

    if not is_lingbuzz_url(url):
        return {"error": "Not a LingBuzz link"}
        
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to retrieve the webpage. Status code: {}".format(response.status_code)}

    soup = BeautifulSoup(response.text, 'html.parser')
    center_tag = soup.find('center')

    if not center_tag:
        return {"error": "The required content could not be found on the page."}
    
    ####       FINDING PUBLISHING INFOs     #####
    prettified = soup.prettify()
    # Split the prettified HTML into lines for easiness of analysis
    lines = prettified.split('\n')

    # Find the index of the specific pattern
    pattern = "Published in:"
    index = -1
    for i, line in enumerate(lines):
        if pattern in line:
            index = i
            print("Pattern found")
            break

    # If pattern is found then:
    if index != -1 and index + 2 < len(lines):
        following_line = lines[index + 3]
        publisher = following_line.strip()+" ."
        print(following_line.strip())
    else:
        print("Pattern not found or not enough lines in the content.")

    # Here we remove publisher if empty:
    if following_line.strip() == "</td>":
        publisher = ""

    print(publisher)

    paper_title = center_tag.find('a').get_text(strip=True) if center_tag.find('a') else "No Title Found"
    authors_links = center_tag.find_all('a')[1:]  # Let's skip the first link cause it's the paper title
    authors = [link.get_text(strip=True) for link in authors_links]

    authors_converted_list = []
    for author in authors:
        parts = author.split(', ')
        if len(parts) == 2:
            last_name, first_name = parts
            initials = ''.join([name[0] for name in first_name.split()]).upper()
            authors_converted_list.append(f"{last_name}, {initials}.")
        else:
            authors_converted_list.append(author)

    formatted_authors = ', '.join(authors_converted_list[:-1]) + ', & ' + authors_converted_list[-1] if len(authors_converted_list) > 1 else authors_converted_list[0]
    publication_date = center_tag.contents[-1].strip()
    year_match = re.search(r'\d{4}', publication_date)
    year = year_match.group() if year_match else 'n.d.'

    apa_citation = f"{formatted_authors} ({year}). {paper_title}. {publisher} Retrieved from {url}"
    return {"apa": apa_citation}

@app.route('/generate_bibtex', methods=['POST'])
def bibtex():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    result = generate_bibtex_citation(url)
    return jsonify(result)

@app.route('/generate_apa', methods=['POST'])
def apa():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    result = generate_apa_citation(url)
    
    # Inserting line breaks every 76 characters so that the output can stay in the page and not overflow
    formatted_apa = "\n".join([result['apa'][i:i+76] for i in range(0, len(result['apa']), 76)])
    
    result['apa'] = formatted_apa
    return jsonify(result)


@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
