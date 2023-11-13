import pdfplumber

# Open the PDF file
with pdfplumber.open('corrupcion.pdf') as pdf:
    # Iterate through all pages
    for page_number in range(len(pdf.pages)):
        # Extract the table from the current page
        page = pdf.pages[page_number]
        table = page.extract_table()

        # Extract a specific column (modify column_index as needed)
        column_index = 1
        column_data = [row[column_index] for row in table]

        # Print the extracted column data for the current page
        print(f"Page {page_number + 1} - Column Data: {column_data}")
