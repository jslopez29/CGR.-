import logging
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import camelot
import re
import fitz
import mysql.connector
from mysql.connector import errorcode
import pdfplumber
import io


# UNIDAD RESPONSABILIDAD FISCAL REGALÍAS
CONTRALORIA = 2
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
        print("\nEl Estado más reciente es el siguiente:", newest_link)

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

                # Save the PDF content to a file
                with open('regalias.pdf', 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)

                # Open the saved PDF file with pdfplumber
                with pdfplumber.open('regalias.pdf') as pdf:
                    # Initialize an empty list to store entries from all pages
                    all_entries = []

                    # Iterate through all pages
                    for page_number in range(len(pdf.pages)):
                        # Extract the table from the current page
                        page = pdf.pages[page_number]
                        table = page.extract_table()

                        # Extract a specific column (modify column_index as needed)
                        column_index = 1
                        column_data = [row[column_index].replace('\n', '') for row in table if row and row[column_index] and (row[column_index].startswith("P") or row[column_index].startswith("U"))]

                        # Add the entries from the current page to the list
                        all_entries.extend(column_data)

                # Concatenate all entries and save as a variable
                Novedades_Regalias = "\n".join(all_entries)

                # Now you can use the variable "Novedades_Regalias" for further processing
                print("Concatenated Entries")
                print(Novedades_Regalias)
            else:
                print("No se pudo encontrar el link de Descarga del Estado. Particularmente no aparece la palabra 'Descargar'.")

        else:
            print(f"No se pudo abrir el segundo link. Status code: {response2.status_code}")

    else:
        print("No hay un link en la primera página que contenta la palabra 'ESTADO'.")

else:
    print(f"Fue imposible abrir el link de la página web. Status code: {response.status_code}")

# Open the PDF using PyMuPDF
pdf_document = fitz.open("regalias.pdf")

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

    else:
        print("Failed to extract information from the matched line.")
else:
    print("No matching line found in the entire PDF.")

print(f"Las variables que he guardado hasta el momento son:")
print(f"\nEstado_ID: {Estado_ID}")
print(f"DAY: {DAY}")
print(f"MONTH: {MONTH}")
print(f"YEAR: {YEAR}")
print(f"\nNovedades:\n{Novedades_Regalias}")
print(f"\nContraloría:\n{CONTRALORIA}")

# Establish a connection to the MySQL server
try:
    cnx = mysql.connector.connect(user='jslo_cgrhost', password='&$r6W6&qGnMG',
                                  host='juansebastianlopez.com', database='jslo_cgr')
    cursor = cnx.cursor()

    # Crear tabla si no existe
    create_table_query = (
        "CREATE TABLE IF NOT EXISTS NovedadesCGR ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  Estado_ID INT,"
        "  DAY INT,"
        "  MONTH INT,"
        "  YEAR INT,"
        "  Novedades TEXT,"
        "  Link VARCHAR(255),"
        "  CONTRALORIA INT"  # Include CONTRALORIA in the table
        ")"
    )

    cursor.execute(create_table_query)

    # Query para insertar
    insert_query = ("INSERT INTO NovedadesCGR "
                    "(Estado_ID, DAY, MONTH, YEAR, Novedades, Link, CONTRALORIA) "  # Include CONTRALORIA in the columns
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    # Chequear si Estado_ID ya exista en la base de datos
    check_query = ("SELECT COUNT(*) FROM NovedadesCGR WHERE Estado_ID = %s AND CONTRALORIA = %s")
    cursor.execute(check_query, (Estado_ID, CONTRALORIA))
    result = cursor.fetchone()

    if result and result[0] > 0:
        print(f"Este Estado_ID ({Estado_ID}) ya existe en la base de datos con la misma CONTRALORIA. No data inserted.")
    else:
        # Insertar data en MySQL table
        data = (Estado_ID, DAY, MONTH, YEAR, Novedades_Regalias, newest_link2, CONTRALORIA)
        cursor.execute(insert_query, data)
        cnx.commit()
        print("Data inserted into MySQL successfully.")


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

finally:
    # Close the cursor and connection
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()


# Configure the logging module
logging.basicConfig(filename='script_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("El Estado más reciente es el siguiente: %s", newest_link)
logging.info("El link de descarga del Estado más reciente es este: %s", newest_link2)
logging.info("Los procesos que reportan novedad en el Estado más reciente son:")
logging.info("Estado_ID: %s", Estado_ID)
logging.info("DAY: %s", DAY)
logging.info("MONTH: %s", MONTH)
logging.info("YEAR: %s", YEAR)
logging.info("Novedades:\n%s", Novedades_Regalias)
logging.info("Contraloría:\n%s", CONTRALORIA)
logging.info("Data inserted into MySQL successfully.")
logging.info("Script completed successfully.")
