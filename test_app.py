#!/usr/bin/env python3
"""
Simple test script to verify the AI Myth-Buster WhatsApp Bot structure
"""

import os
import sys

def test_project_structure():
    """Test if all required files and directories exist"""
    
    required_files = [
        'app/__init__.py',
        'app/main.py',
        'app/config.py',
        'app/models.py',
        'app/routes/__init__.py',
        'app/routes/webhook.py',
        'app/services/__init__.py',
        'app/services/twilio_service.py',
        'app/services/message_service.py',
        'requirements.txt',
        'Dockerfile',
        '.env.example',
        'README.md',
        '.gitignore'
    ]
    
    print("🔍 Testing AI Myth-Buster WhatsApp Bot Project Structure...")
    print("=" * 60)
    
    all_good = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_good = False
    
    print("=" * 60)
    
    if all_good:
        print("🎉 All required files are present!")
        print("\n📋 Next Steps:")
        print("1. Create a virtual environment: python -m venv venv")
        print("2. Activate it: source venv/bin/activate (macOS/Linux) or venv\\Scripts\\activate (Windows)")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Copy .env.example to .env and fill in your Twilio credentials")
        print("5. Run the app: uvicorn app.main:app --reload")
        print("6. Set up ngrok for webhook testing")
        return True
    else:
        print("❌ Some files are missing. Please check the project structure.")
        return False

def test_import_structure():
    """Test if the Python modules can be imported (basic syntax check)"""
    
    print("\n🐍 Testing Python Module Structure...")
    print("=" * 60)
    
    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())
    
    modules_to_test = [
        ('app.models', 'app/models.py'),
        ('app.config', 'app/config.py'),
    ]
    
    for module_name, file_path in modules_to_test:
        try:
            # Try to compile the file to check for syntax errors
            with open(file_path, 'r') as f:
                code = f.read()
            
            compile(code, file_path, 'exec')
            print(f"✅ {module_name} - Syntax OK")
            
        except SyntaxError as e:
            print(f"❌ {module_name} - Syntax Error: {e}")
        except FileNotFoundError:
            print(f"❌ {module_name} - File not found")
        except Exception as e:
            print(f"⚠️  {module_name} - Warning: {e}")

if __name__ == "__main__":
    print("🤖 AI Myth-Buster WhatsApp Bot - Project Test")
    print("=" * 60)
    
    structure_ok = test_project_structure()
    
    if structure_ok:
        test_import_structure()
        
        print("\n🚀 Project Setup Complete!")
        print("\n📖 Read the README.md for detailed setup instructions.")
        print("🔗 GitHub: https://github.com/m-adil172000/AI-Myth-Buster")
    
    print("\n" + "=" * 60)
