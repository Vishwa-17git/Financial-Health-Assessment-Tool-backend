import pandas as pd
import os

try:
    import pdfplumber
except Exception:
    pdfplumber = None


SUPPORTED_EXT = ('.csv', '.xlsx', '.xls', '.pdf')


def read_file_to_df(filepath):
    """Read CSV/XLSX/PDF file into a pandas.DataFrame.

    For PDFs we try to extract tables using `pdfplumber` and concatenate them.
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.csv':
        return pd.read_csv(filepath)

    if ext in ('.xls', '.xlsx'):
        # Let pandas infer sheets; use first sheet
        return pd.read_excel(filepath)

    if ext == '.pdf':
        if not pdfplumber:
            raise RuntimeError("pdfplumber is not installed; cannot parse PDF files")
        tables = []
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        tables.append(df)
        if not tables:
            raise ValueError("No tables found in PDF")
        # Concatenate and try to coerce numeric columns
        df = pd.concat(tables, ignore_index=True)
        return df

    raise ValueError(f"Unsupported file type: {ext}. Supported: {', '.join(SUPPORTED_EXT)}")