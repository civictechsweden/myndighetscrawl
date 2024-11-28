import requests
import os
import fitz
import requests
import os
import fitz

import urllib.parse

url = "https://www.aklagare.se/globalassets/dokument/verksamheten-i-hogsta-domstolen/svarsskrivelser-och-forklaringar/amr-9378-23.pdf?_t_tags=language%3Asv%2Csiteid%3A764c28f6-3ce5-48e7-a8ec-b8f5f22e4245&_t_hit.id=Aklagare_Web_Models_Media_PdfFile/_358f6287-9472-4563-92bb-904d5b62bc9c&_t_hit.pos=82"

response = requests.get(url)

# Use BytesIO to read the content directly with fitz and save the PDF
with fitz.open(stream=response.content, filetype="pdf") as doc:
    number_of_pages = doc.page_count

    # Encode the URL to create a safe filename
    safe_filename = urllib.parse.quote_plus(url.replace("https://", "").split("?")[0], safe="")
    output_file_path = f"{safe_filename}.pdf"

    # Save the PDF to a file
    doc.save(output_file_path)
print(f"The PDF has {number_of_pages} pages and has been saved to {output_file_path}.")
