#!/usr/bin/env python3
"""
AI Test Script - Tests Deepseek and Gemini API integration
"""

import os
import sys
sys.path.append('/Users/admin/Desktop/ba218hfg321ncm/bacfuzz/fuzzer')

from config import Config
from AICaller import AICaller

def test_ai_integration():
    print("=" * 60)
    print("🤖 BACFuzz AI Integration Test")
    print("=" * 60)
    
    # Environment variables check
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    print(f"🔑 DEEPSEEK_API_KEY: {'✅ Available' if deepseek_key else '❌ Not found'}")
    print(f"🔑 GEMINI_API_KEY: {'✅ Available' if gemini_key else '❌ Not found'}")
    print()
    
    # Config test
    config = Config()
    print(f"🎯 Selected AI Model: {config.AIModel}")
    print()
    
    # AI Caller test
    try:
        ai_caller = AICaller(config.AIModel)
        print(f"✅ AICaller created successfully")
        
        # Simple test prompt
        test_prompt = {
            "system": "You are a security expert.",
            "user": "Hello, provide brief information about web security."
        }
        
        print("🔄 Testing AI model...")
        response_text, prompt_tokens, response_tokens = ai_caller.call_model(test_prompt, max_tokens=150)
        
        print(f"✅ AI Test Successful!")
        print(f"📝 Prompt Tokens: {prompt_tokens}")
        print(f"📝 Response Tokens: {response_tokens}")
        print(f"💬 AI Response: {response_text[:200] if response_text else 'Empty response'}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Test Error: {e}")
        return False

def show_setup_instructions():
    print("\n" + "=" * 60)
    print("🚀 AI API Key Setup Instructions")
    print("=" * 60)
    print()
    print("For Deepseek:")
    print("export DEEPSEEK_API_KEY='your_deepseek_api_key_here'")
    print()
    print("For Gemini:")
    print("export GEMINI_API_KEY='your_gemini_api_key_here'")
    print("# or")
    print("export GOOGLE_API_KEY='your_google_api_key_here'")
    print()
    print("After setting API keys:")
    print("source ~/.zshrc  # or ~/.bashrc for bash")
    print()

if __name__ == "__main__":
    print("🧪 Starting AI integration test...")
    
    # API key check
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    if not deepseek_key and not gemini_key:
        print("⚠️  No AI API keys found!")
        show_setup_instructions()
        sys.exit(1)
    
    # Run test
    success = test_ai_integration()
    
    if success:
        print("\n🎉 AI integration completed successfully!")
        print("🚀 You can now use AI-powered payload analysis in BACFuzz!")
    else:
        print("\n❌ AI integration test failed!")
        show_setup_instructions()
