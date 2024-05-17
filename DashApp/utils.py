import base64
import io
import pandas as pd

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Procesar archivo CSV
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'parquet' in filename:
            # Procesar archivo Parquet
            df = pd.read_parquet(io.BytesIO(decoded))
        else:
            return None
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None
    return df
