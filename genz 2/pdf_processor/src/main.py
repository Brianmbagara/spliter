import os
import re
import random
import PyPDF2
from pdf_extractor import PDFExtractor, split_pdf_to_single_pages
from utils import load_pdfs, save_pdf

def sanitize_filename(name: str) -> str:
    # Remove only invalid filename characters, keep letters and numbers intact
    sanitized = re.sub(r'[\\\\/*?:"<>|]+', ' ', name)
    sanitized = re.sub(r'\s+', ' ', sanitized)
    return sanitized.strip()

def int_to_roman(input):
    if not isinstance(input, int):
        raise TypeError("expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

def main():
    path = input("Please enter the path to the directory or PDF file: ").strip()
    # Strip surrounding quotes if any
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]

    # Validate input path
    if not os.path.exists(path):
        print(f"Error: The path '{path}' does not exist.")
        return

    if not (os.path.isdir(path) or (os.path.isfile(path) and path.lower().endswith('.pdf'))):
        print(f"Error: The path '{path}' is neither a directory nor a PDF file.")
        return

    pdf_files = []
    if os.path.isdir(path):
        # Path is a directory, load all PDFs
        pdf_files = load_pdfs(path)
        if not pdf_files:
            print(f"Error: No PDF files found in directory '{path}'.")
            return
        print(f"Loaded {len(pdf_files)} PDF files from directory: {path}")
        for f in pdf_files:
            print(f" - {f}")
    else:
        # Path is a file, check if multi-page PDF
        try:
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
        except Exception as e:
            print(f"Error opening or reading PDF: {e}")
            return
        print(f"Number of pages in the document: {num_pages}")
        if num_pages > 1:
            # Split into single-page PDFs
            output_folder = os.path.splitext(path)[0] + "_split"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            pdf_files = split_pdf_to_single_pages(path, output_folder)
            if not pdf_files:
                print(f"Error: No PDF files generated after splitting '{path}'.")
                return
            print(f"Split multi-page PDF into {len(pdf_files)} single-page PDFs in folder: {output_folder}")
        else:
            # Single page PDF, process as is
            pdf_files = [path]
            print(f"Single-page PDF detected: {path}")

    # Generate random roman numeral folder name between 1 and 3999
    random_number = random.randint(1, 3999)
    rename_folder_name = int_to_roman(random_number)
    rename_folder = os.path.join(os.path.dirname(path), rename_folder_name)
    if not os.path.exists(rename_folder):
        os.makedirs(rename_folder)

    # Process files one by one: extract name, rename, save
    saved_count = 0
    existing_names = set()  # To keep track of existing filenames
    for i, pdf_file in enumerate(pdf_files):
        print(f"Processing file {i+1}/{len(pdf_files)}: {pdf_file}")  # Added logging
        try:
            extractor = PDFExtractor(pdf_file)
            full_name = extractor.extract_names()
            if full_name:
                # Use extracted name after salutation for renaming
                sanitized_name = sanitize_filename(full_name)
                new_name = f"{sanitized_name}.pdf"
            else:
                # Use original filename if no name extracted
                original_name = os.path.basename(pdf_file)
                sanitized_original = sanitize_filename(os.path.splitext(original_name)[0])
                new_name = f"{sanitized_original}.pdf"

            # Handle duplicate filenames by adding a counter
            base_name, ext = os.path.splitext(new_name)
            counter = 1
            while new_name in existing_names:
                new_name = f"{base_name}_{counter}{ext}"
                counter += 1

            try:
                save_pdf(pdf_file, rename_folder, new_name)
                print(f"Renamed and saved: {new_name}")
                saved_count += 1
                existing_names.add(new_name)  # Add the new name to the set
            except Exception as e:
                print(f"Error saving file {new_name}: {e}")
        except Exception as e:
            print(f"Error processing PDF file {pdf_file}: {e}")

    print(f"All files have been renamed and saved in the folder: {rename_folder}")
    print(f"Total files saved: {saved_count}")
    print(f"Total files expected: {len(pdf_files)}")
    if saved_count != len(pdf_files):
        print(f"Warning: Number of files saved ({saved_count}) does not match the number of files expected ({len(pdf_files)}).")

if __name__ == "__main__":
    main()