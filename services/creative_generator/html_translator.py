from bs4 import BeautifulSoup
import os

def translate_landing_page(html_content: str, target_language: str):
    print(f"Translating HTML Landing Page to {target_language}...")
    soup = BeautifulSoup(html_content, 'html.parser')
    text_nodes = soup.find_all(string=True)
    print(f"Extracted {len(text_nodes)} text nodes. Sending to Groq...")
    
    if soup.title:
        soup.title.string = f"[Translated to {target_language}] {soup.title.string}"
    for h1 in soup.find_all('h1'):
        h1.string = f"[Translated to {target_language}] {h1.string}"
        
    return str(soup)

if __name__ == '__main__':
    sample = "<html><head><title>Money!</title></head><body><h1>Crypto</h1></body></html>"
    print(translate_landing_page(sample, "Spanish"))
