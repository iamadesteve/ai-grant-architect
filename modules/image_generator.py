import os
import streamlit as st
import io
import json
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import time

def create_placeholder_image(text):
    """Creates a placeholder image with text when generation fails."""
    img = Image.new('RGB', (512, 512), color=(200, 200, 200))
    d = ImageDraw.Draw(img)
    # Basic text centering (approximate)
    d.text((10, 256), text, fill=(0, 0, 0))
    return img

def generate_business_image(prompt, style, api_key):
    """
    Generates an image using Google's Generative AI based on the prompt and style.

    Args:
        prompt (str): The subject prompt for the image.
        style (str): The style of the image (e.g., 'Photorealistic', '3D Isometric', 'Vector Art').
        api_key (str): The Google API Key.

    Returns:
        PIL.Image.Image: The generated image object, or a placeholder if generation fails.
    """
    if not api_key:
        print("Error: No API Key provided.")
        return create_placeholder_image("[Error: Missing API Key]")

    # Configure the library
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring API: {e}")
        return create_placeholder_image(f"[Error: API Config Failed]")

    # Construct the full prompt including style
    # Nano Banana Integration: ensure high quality request
    full_prompt = f"High quality, professional business illustration. {prompt}. Style: {style}. 8k resolution, detailed."

    try:
        # Use a model that supports image generation
        # Prioritize 'imagen-3.0-generate-001' or similar high-quality model
        
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        response = model.generate_content(full_prompt)
        
        # Check if response contains image data
        if response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                    return Image.open(io.BytesIO(image_data))
        
        # Fallback for different response structures
        if hasattr(response, 'images') and response.images:
             return response.images[0]

        print("No image data found in response.")
        return create_placeholder_image("[Image: Generation Failed - No Data]")

    except Exception as e:
        print(f"Error generating image: {e}")
        return create_placeholder_image(f"[Image: Generation Error - {str(e)[:50]}...]")

def analyze_and_generate_visuals(plan_text, visual_style, api_key, model_name="gemini-1.5-flash", progress_callback=None):
    """
    Analyzes the business plan text to identify key sections for visualization,
    generates prompts using Gemini, and then generates images for those prompts.

    Args:
        plan_text (str): The full text of the business plan.
        visual_style (str): The user-selected visual style (e.g., 'Photorealistic').
        api_key (str): The Google API Key.
        progress_callback (function): Optional function to update progress (accepts float 0.0 to 1.0).

    Returns:
        dict: A dictionary of generated images keyed by section name.
    """
    if not api_key:
        return {}

    
    genai.configure(api_key=api_key)

    # 1. Ask Gemini to identify sections and write prompts
    # Model Specification: Use 'gemini-1.5-flash' or 'gemini-pro' for text analysis
    analysis_prompt = f"""
    Analyze the following Business Plan text and identify 10 key sections that would benefit from visual illustrations (e.g., 'The Cover Page', 'Product Demo', 'Team Section', 'Office Location').
    
    For each section, write a specific, detailed image generation prompt based on the visual style: '{visual_style}'.
    
    Return the result strictly as a JSON object with the following structure:
    {{
        "visuals": [
            {{
                "section": "Section Name",
                "prompt": "Detailed image prompt..."
            }},
            ...
        ]
    }}
    
    Business Plan Text (Excerpt):
    {plan_text[:10000]} 
    ... (truncated for analysis efficiency if too long)
    """
    
    try:
        model = genai.GenerativeModel(model_name) # Use selected model
        
        # Retry logic for analysis
        max_retries = 3
        retry_delay = 5
        response = None
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content(analysis_prompt)
                break
            except Exception as e:
                if "429" in str(e) or "ResourceExhausted" in str(e):
                    if attempt < max_retries - 1:
                        wait_time = 2 ** (attempt + 1)
                        time.sleep(wait_time)
                        continue
                    else:
                        print("Error: Quota exceeded for visual analysis.")
                        return {}
                else:
                    raise e
        
        if not response:
             return {}

        # Parse JSON from response
        text_response = response.text
        # Clean up code blocks if present
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0]
        elif "```" in text_response:
            text_response = text_response.split("```")[1]
            
        visual_plan = json.loads(text_response)
        
    except Exception as e:
        print(f"Error analyzing plan for visuals: {e}")
        # Build a safe fallback list if analysis fails
        visual_plan = {
            "visuals": [
                {"section": "The Cover Page", "prompt": f"Professional business cover page, {visual_style}"},
                {"section": "Financial Highlights", "prompt": f"Financial growth chart, {visual_style}"}
            ]
        }

    generated_images = {}
    items = visual_plan.get("visuals", [])
    total_items = len(items)

    # 2. Loop through prompts and generate images
    for index, item in enumerate(items):
        section_name = item.get("section", f"Section {index+1}")
        image_prompt = item.get("prompt")
        
        print(f"Generating image for {section_name}: {image_prompt}")
        
        image = generate_business_image(image_prompt, visual_style, api_key)
        
        if image:
            generated_images[section_name] = image
            
        # Update progress
        if progress_callback:
            progress = (index + 1) / total_items
            progress_callback(progress, f"Generating asset for: {section_name}")

    return generated_images
