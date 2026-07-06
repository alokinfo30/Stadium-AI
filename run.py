# run.py
import os
import sys

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print("=" * 70)
    print("🏟️ AI Stadium Assistant - FIFA World Cup 2026")
    print("=" * 70)
    print(f"🚀 Server running at: http://localhost:{port}")
    print("📱 Open in your browser")
    print("=" * 70)
    print("🤖 AI Agents:")
    print("  1. 🧭 Navigation Agent - Wayfinding and directions")
    print("  2. 👥 Crowd Management Agent - Real-time crowd insights")
    print("  3. ♿ Accessibility Agent - Inclusive access information")
    print("  4. 🚌 Transportation Agent - Transport options")
    print("  5. 🌱 Sustainability Agent - Eco-friendly practices")
    print("  6. 🌐 Multilingual Agent - Language translation")
    print("  7. 📊 Operational Intelligence Agent - Real-time insights")
    print("=" * 70)
    print("🌍 Supported Languages:")
    print("  English, Spanish, French, German, Portuguese")
    print("  Arabic, Hindi, Chinese, Japanese, Korean")
    print("=" * 70)
    print("⚽ Enhancing Stadium Operations & Fan Experience")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=port, debug=debug)