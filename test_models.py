#!/usr/bin/env python3
"""Quick test to find working Gemini models"""

import os
import sys
sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

def test_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key found")
        return
        
    genai.configure(api_key=api_key)
    
    # First, list available models
    print("Listing available models...")
    try:
        models = list(genai.list_models())
        print(f"Found {len(models)} models:")
        for model in models[:10]:
            print(f"  - {model.name}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"    Methods: {model.supported_generation_methods}")
        print()
    except Exception as e:
        print(f"Failed to list models: {e}")
    
    # Try the actual available models from the API
    models_to_try = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash',
        'models/gemini-2.0-flash-001',
        'models/gemini-2.5-pro',
        'gemini-2.5-flash',
        'gemini-2.0-flash'
    ]
    
    for model_name in models_to_try:
        try:
            print(f"Testing {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            print(f"✅ {model_name} works! Response: {response.text[:50]}")
            return model_name
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)[:100]}")
    
    print("No working models found")
    return None

if __name__ == "__main__":
    working_model = test_models()