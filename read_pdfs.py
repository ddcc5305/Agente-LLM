import pypdf
import sys
import glob

def extract(pdf_path, out_path):
    print(f"Extracting {pdf_path}")
    try:
        reader = pypdf.PdfReader(pdf_path)
        with open(out_path, 'w', encoding='utf-8') as f:
            for i, p in enumerate(reader.pages):
                text = p.extract_text()
                f.write(f"--- PAGE {i} ---\n{text}\n")
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")

pdfs = glob.glob("docs/*.pdf")
for i, pdf in enumerate(pdfs):
    extract(pdf, f"pdf_text_{i}.txt")
