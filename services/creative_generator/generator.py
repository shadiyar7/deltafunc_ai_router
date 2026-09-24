import os
import json
from groq import Groq
import asyncio
from PIL import Image, ImageDraw, ImageFont

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

async def generate_creatives(offer_text: str):
    print(f"Start generating creatives for: {offer_text}")
    
    prompt = f"""
    You are an expert Media Buyer. 
    Take this offer description: "{offer_text}"
    
    Generate exactly 1 short, punchy Facebook Ad text.
    Translate it into: English, Spanish, Russian.
    
    Output in strict JSON format:
    {{
        "English": "text here",
        "Spanish": "texto aqui",
        "Russian": "текст здесь"
    }}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an AI that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"},
        )
        
        result = json.loads(chat_completion.choices[0].message.content)
        
        os.makedirs("output_banners", exist_ok=True)
        
        # Draw images for each language
        for lang, text in result.items():
            # Create a simple 800x800 background (e.g. gradient or solid color)
            img = Image.new('RGB', (800, 800), color = (73, 109, 137))
            d = ImageDraw.Draw(img)
            
            # Using default font since we don't know what fonts are installed on Windows
            # and Pillow's default font doesn't support Cyrillic well, but it's a prototype
            font = ImageFont.load_default()
            
            # Since the default font is tiny, let's just write it
            d.text((50,400), text.encode('ascii', 'ignore').decode('ascii') + f" [{lang}]", fill=(255,255,0), font=font)
            
            img_path = f"output_banners/banner_{lang}.png"
            img.save(img_path)
            print(f"Saved banner to {img_path}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(generate_creatives("Nike Air Max Spring Clearance - 30% off!"))
