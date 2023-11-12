import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import camelot
import re

# Constants
BASE_URL = 'https://www.contraloria.gov.co/resultados/notificaciones-y-citaciones/notificaciones-por-estado/unidad-de-responsabilidad-fiscal-de-regalias'
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
KEYWORD_ESTADO = 'ESTADO'
KEYWORD_DESCARGAR = 'Descargar'

def fetch_webpage(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def find_link_by_keyword(soup, keyword):
    selected_link = soup.find('a', string=lambda s: keyword in s.upper() if s else False)
    return selected_link

def find_descargar_link(newest_link, headers):
    response = requests.get(newest_link, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the first link on the second page that contains the word "Descargar"
    selected_link = find_link_by_keyword(soup, KEYWORD_DESCARGAR)
    if selected_link:
        return urljoin(newest_link, selected_link.get('href'))
    else:
        print(f"No se pudo encontrar el link de Descarga del Estado. No aparece la palabra '{KEYWORD_DESCARGAR}'.")
        return None

def download_pdf(url, headers, file_path):
    pdf_response = requests.get(url, headers=headers)
    pdf_response.raise_for_status()
    with open(file_path, "wb") as pdf_file:
        pdf_file.write(pdf_response.content)
    print("PDF downloaded successfully.")

def extract_tables(pdf_path):
    return camelot.read_pdf(pdf_path, flavor='stream', pages='all')

def main():
    # Fetch webpage
    main_page_soup = fetch_webpage(BASE_URL, HEADERS)

    # Find link containing "ESTADO"
    selected_link = find_link_by_keyword(main_page_soup, KEYWORD_ESTADO)
    if not selected_link:
        print(f"No link found containing the keyword '{KEYWORD_ESTADO}'.")
        return

    newest_link = urljoin(BASE_URL, selected_link.get('href'))
    print("\nEl Estado más reciente es el siguiente:", newest_link)

    # Find "Descargar" link on the second page
    descargar_link = find_descargar_link(newest_link, HEADERS)
    if not descargar_link:
        print(f"No link found containing the keyword '{KEYWORD_DESCARGAR}' on the second page.")
        return

    print("\nEl link de descarga del Estado más reciente es este:", descargar_link)

    # Download the PDF file
    download_pdf(descargar_link, HEADERS, "downloaded_file.pdf")

    # Extract tables from PDF using Camelot
    tables = extract_tables("downloaded_file.pdf")
    print("\nLos procesos que reportan novedad en el Estado más reciente son:")
    
    # Iterate through tables and print specific content
    for idx, table in enumerate(tables):
        # Assuming the column you're interested in is the first column
        specific_column = table.df.iloc[:, 1]

        # Concatenate the text from each row in the column
        condensed_content = ''
        current_entry = ''
        for entry in specific_column.dropna():
            if 'PRF' in entry:
                if current_entry:
                    # Remove extra spaces before or after the numbers
                    condensed_content += ' '.join(current_entry.split()).strip() + '\n'
                current_entry = entry
            else:
                current_entry += ' ' + entry

        # Add the last entry after the loop
        if current_entry:
            # Remove extra spaces before or after the numbers
            condensed_content += ' '.join(current_entry.split()).strip() + '\n'

        # Remove lines containing "IDENTIFICACIÓN"
        condensed_content = '\n'.join(line for line in condensed_content.split('\n') if 'IDENTIFICACIÓN' not in line)

        # Print the condensed content for the current table
        if condensed_content:
            # Remove spaces but keep line breaks
            condensed_content = condensed_content.replace(' ', '').strip()
            print(condensed_content)

if __name__ == "__main__":
    main()
