import os
import shutil

def save_pdf(file_path, output_directory, new_name):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Avoid double .pdf extension
    if new_name.lower().endswith('.pdf'):
        new_file_path = os.path.join(output_directory, new_name)
    else:
        new_file_path = os.path.join(output_directory, new_name + '.pdf')
    # Use shutil.copyfile to copy file exactly without modification
    shutil.copyfile(file_path, new_file_path)
    return new_file_path

def load_pdfs(directory):
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    return [os.path.join(directory, f) for f in pdf_files]
