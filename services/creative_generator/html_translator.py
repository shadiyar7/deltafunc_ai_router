import os
import zipfile
import shutil
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def translate_html_zip(zip_path: str, target_language: str, output_zip_path: str):
    print(f"Translating landing pages in {zip_path} to {target_language}...")
    extract_dir = "temp_landing"
    
    # 1. Unzip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
    # 2. Translate HTML files
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                
                # Mock translation by prefixing titles
                if soup.title:
                    soup.title.string = f"[{target_language}] {soup.title.string}"
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(soup))
                    
    # 3. Re-zip
    shutil.make_archive(output_zip_path.replace('.zip', ''), 'zip', extract_dir)
    shutil.rmtree(extract_dir)
    print(f"Saved translated archive to {output_zip_path}")

if __name__ == '__main__':
    # Mock usage:
    # translate_html_zip("landing_en.zip", "es", "landing_es.zip")
    pass
