import os
import re
import PyPDF2

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.name = None

    def extract_names(self):
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if len(reader.pages) == 0:
                    print(f"No pages found in {self.pdf_path}")
                    return None
                # Extract text from all pages to find 'Dear'
                text = ''
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
                if not text:
                    print(f"No text extracted from {self.pdf_path}")
                    return None
                # Normalize whitespace to single spaces
                normalized_text = re.sub(r'\s+', ' ', text)
                #print(f"Normalized extracted text from {self.pdf_path}: {normalized_text[:500]}...")  # print first 500 chars

            # Updated regex to capture names after "Dear" in normalized text
            # Match letters and spaces after 'Dear' until two or more spaces, punctuation, or end of string
            match = re.search(r'Dear\s+((?:\w+\s*){1,3})', normalized_text, re.IGNORECASE)
            if match:
                name_str = match.group(1).strip()
                print(f"Raw matched name string: '{name_str}'")
                name_str = re.sub(r'[^\w\s]', '', name_str)
                self.name = name_str
                print(f"Extracted name: {self.name}")
            else:
                print(f"No name matched in {self.pdf_path}")
                self.name = None
            return self.name
        except Exception as e:
            print(f"Error extracting name from {self.pdf_path}: {e}")
            return None

    def rename_pdf(self):
        if self.name:
            new_name = f"{self.name}.pdf"
            return new_name
        return None

def split_pdf_to_single_pages(pdf_path, output_folder):
    import os
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Splitting PDF: {pdf_path} into folder: {output_folder}")
    files = []
    try:
        with open(pdf_path, 'rb') as infile:
            reader = PyPDF2.PdfReader(infile)
            num_pages = len(reader.pages)
            print(f"Number of pages to split: {num_pages}")
            for i, page in enumerate(reader.pages):
                try:
                    writer = PyPDF2.PdfWriter()
                    writer.add_page(page)
                    output_path = os.path.join(output_folder, f"page_{i+1}.pdf")
                    with open(output_path, 'wb') as outfile:
                        writer.write(outfile)
                    print(f"Written page {i+1} to {output_path}")
                    files.append(output_path)
                except Exception as e:
                    print(f"Error writing page {i+1}: {e}")
        print(f"Total split files created: {len(files)}")
        return files
    except Exception as e:
        print(f"Error splitting PDF: {e}")
        return []