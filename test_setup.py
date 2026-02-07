"""
Simple test script to verify the Rose Day app setup
"""
import sys

print("🌹 Testing Rose Day Application Setup...\n")

# Test 1: Import dependencies
print("1️⃣ Testing imports...")
try:
    from datetime import datetime, timedelta, timezone
    from fastapi import FastAPI, Form
    from fastapi.responses import HTMLResponse, RedirectResponse
    print("   ✅ FastAPI imports successful")
except Exception as e:
    print(f"   ❌ FastAPI import failed: {e}")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    import os
    print("   ✅ dotenv import successful")
except Exception as e:
    print(f"   ❌ dotenv import failed: {e}")
    sys.exit(1)

# Test 2: Load environment variables
print("\n2️⃣ Testing environment configuration...")
try:
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if supabase_url and supabase_key:
        print(f"   ✅ Environment variables loaded")
        print(f"   📍 Supabase URL: {supabase_url[:30]}...")
    else:
        print("   ⚠️  Warning: SUPABASE_URL or SUPABASE_KEY not set in .env file")
        print("   Please create a .env file with your Supabase credentials")
except Exception as e:
    print(f"   ❌ Environment loading failed: {e}")

# Test 3: Import Supabase client
print("\n3️⃣ Testing Supabase client...")
try:
    from supabase import create_client
    print("   ✅ Supabase package imported successfully")

    if supabase_url and supabase_key:
        try:
            supabase = create_client(supabase_url, supabase_key)
            print("   ✅ Supabase client created successfully")
        except Exception as e:
            print(f"   ⚠️  Could not connect to Supabase: {e}")
            print("   This is expected if you haven't set up Supabase yet")

except Exception as e:
    print(f"   ❌ Supabase import failed: {e}")
    sys.exit(1)

# Test 4: Import main app
print("\n4️⃣ Testing main application...")
try:
    import main
    print("   ✅ Main application imported successfully")
    print(f"   ✅ FastAPI app created: {main.app}")
except Exception as e:
    print(f"   ❌ Main app import failed: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("🎉 All tests passed! Your Rose Day app is ready to run!")
print("="*60)
print("\n📝 Next steps:")
print("   1. Make sure your .env file has valid Supabase credentials")
print("   2. Run the setup.sql in your Supabase SQL Editor")
print("   3. Start the server: uvicorn main:app --reload")
print("   4. Visit: http://127.0.0.1:8000")
print("\n🌹 Happy Rose Day! 💝\n")
