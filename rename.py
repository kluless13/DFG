import os

def rename_files(directory):
    """Rename all PDF files in the given directory to a numbered sequence."""
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    
    for i, filename in enumerate(sorted(pdf_files), 1):
        new_name = f"{i}.pdf"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)

if __name__ == "__main__":
    directory = "/Users/angad/DFG/data"
    rename_files(directory)
