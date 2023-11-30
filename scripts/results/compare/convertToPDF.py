import os
import pdfkit

input_dir_path = 'results'
output_dir_path = 'pdf'

# Ścieżka do wkhtmltopdf
path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Konfiguracja opcji pdfkit
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

# Opcje PDF dla orientacji poziomej i dopasowania do rozmiaru strony
options = {
    'page-width': '840mm',  # szerokość strony
    'page-height': '500mm',  # wysokość strony
    'no-outline': None,
    'encoding': "UTF-8",
    'disable-smart-shrinking': '',
    'zoom': '1'
}

# Upewnij się, że folder wyjściowy istnieje
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)

# Przetwarzanie każdego pliku HTML w folderze wejściowym
for filename in os.listdir(input_dir_path):
    if filename.endswith('.html'):
        html_file_path = os.path.join(input_dir_path, filename)
        pdf_file_path = os.path.join(output_dir_path, filename.replace('.html', '.pdf'))

        # Konwersja HTML na PDF
        try:
            pdfkit.from_file(html_file_path, pdf_file_path, options=options, configuration=config)
            print(f"Konwersja zakończona: {pdf_file_path}")
        except Exception as e:
            print(f"Błąd podczas konwersji {html_file_path}: {e}")
