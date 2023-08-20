import os
from os.path import isfile, join

pdf_directory = '/Users/angad/DFG/data'

def truncate_filename(name):
    # Take only the first 50 characters and add the .pdf extension
    return name[:31] + '.pdf'

all_files = [f for f in os.listdir(pdf_directory) if isfile(join(pdf_directory, f))]
pdf_files = [f for f in all_files if f.endswith('.pdf')]

for pdf_file in pdf_files:
    truncated_name = truncate_filename(pdf_file.replace('.pdf', ''))
    os.rename(join(pdf_directory, pdf_file), join(pdf_directory, truncated_name))
