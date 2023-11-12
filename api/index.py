import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import camelot
import re
import fitz
import mysql.connector
from mysql.connector import errorcode


# Replace 'your_url_here' with the actual URL of the webpage you want to scrape
url = 'https://www.contraloria.gov.co/resultados/notificaciones-y-citaciones/notificaciones-por-estado/unidad-de-responsabilidad-fiscal-de-regalias'
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# Send a GET request to the URL
response = requests.get(url, headers=HEADERS)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first link on the page that contains the word "ESTADO"
    selected_link = soup.find('a', string=lambda s: 'ESTADO' in s.upper() if s else False)

    # Extract the href attribute from the selected link
    if selected_link:
        newest_link = selected_link.get('href')
        print("\nEl Estado más reeciente es el siguiente:", newest_link)

        # Now, you can open this link using a web browser or perform further actions

        # Make a second request using a different variable
        response2 = requests.get(newest_link, headers=HEADERS)

        # Check if the request was successful (status code 200)
        if response2.status_code == 200:
            # Parse the HTML content of the second page
            soup2 = BeautifulSoup(response2.text, 'html.parser')

            # Find the first link on the second page that contains the word "Descargar"
            selected_link2 = soup2.find('a', string=lambda s: 'Descargar' in s if s else False)

            # Extract the href attribute from the selected link on the second page
            if selected_link2:
                # Make the link an absolute URL by combining it with the base URL
                newest_link2 = urljoin(url, selected_link2.get('href'))
                print("\nEl link de descarga del Estado más reciente es este:", newest_link2)
                    # Download the PDF file
                pdf_response = requests.get(newest_link2, headers=HEADERS)
                with open("downloaded_file.pdf", "wb") as pdf_file:
                    pdf_file.write(pdf_response.content)

                # Now, use camelot to extract tables from the PDF
                tables = camelot.read_pdf("downloaded_file.pdf", flavor='stream', pages='all')
                
                # Print a custom title
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
                    else:
                        print("No relevant entries found.")
                # Now, you can open this link using a web browser or perform further actions
            else:
                print("No se pudo encontrar el link de Descarga del Estado. Particularmente no aparece la palabra 'Descargar'.")

        else:
            print(f"No se pudo abrir el segundo link. Status code: {response2.status_code}")

    else:
        print("No hay un link en la primera página que contenta la palabra 'ESTADO'.")

else:
    print(f"Fue imposible abrir el link de la página web. Status code: {response.status_code}")
# Open the PDF using PyMuPDF
pdf_document = fitz.open("downloaded_file.pdf")

# Extract the first line containing the word "ESTADO" from the entire PDF
original_pdf_text = ""
for page_number in range(pdf_document.page_count):
    page = pdf_document[page_number]
    original_pdf_text += page.get_text()

pattern = re.compile(r'(NOTIFICACIÓN POR ESTADO No\. \d+ DEL \w+ \d+ DE [A-Z]+ DE \d{4})', re.IGNORECASE)

match = pattern.search(original_pdf_text)

if match:
    estado_info = match.group(1)

    # Extracting information using regex
    match_info = re.match(r'NOTIFICACIÓN POR ESTADO No\. (\d+) DEL (\w+) (\d+) DE ([A-Z]+) DE (\d+)', estado_info, re.IGNORECASE)

    if match_info:
        Estado_ID = match_info.group(1)
        DAY = match_info.group(3)
        
        # Mapping month names to numerical values
        month_names = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
        MONTH = str(month_names.index(match_info.group(4)) + 1)  # Adding 1 to convert 0-based index to 1-based index

        YEAR = match_info.group(5)

        print(f"\nEstado_ID: {Estado_ID}")
        print(f"DAY: {DAY}")
        print(f"MONTH: {MONTH}")
        print(f"YEAR: {YEAR}")
    else:
        print("Failed to extract information from the matched line.")
else:
    print("No matching line found in the entire PDF.")