import os

# Path to the directory containing PDFs
pdf_directory = '/Users/angad/DFG/data'

# List all files in the directory
all_files = os.listdir(pdf_directory)

# Filter out non-PDF files
pdf_files = [f for f in all_files if f.endswith('.pdf')]

# Rename each PDF file with a prefix and a number
for idx, pdf_file in enumerate(pdf_files, start=1):
    new_name = f"pdf_{idx}.pdf"
    old_path = os.path.join(pdf_directory, pdf_file)
    new_path = os.path.join(pdf_directory, new_name)
    os.rename(old_path, new_path)

print(f"Renamed {len(pdf_files)} PDF files.")
