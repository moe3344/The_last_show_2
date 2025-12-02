"""
Integration test script for The Last Show API
Tests obituary creation with AI, image upload, and TTS
"""

import httpx
import asyncio
import base64
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test User"

async def test_full_flow():
    """Test the complete flow: register -> login -> create obituary"""

    async with httpx.AsyncClient(timeout=120.0) as client:
        print("=" * 60)
        print("INTEGRATION TEST: The Last Show API")
        print("=" * 60)

        # Step 1: Register user
        print("\n1. Registering new user...")
        try:
            register_response = await client.post(
                f"{API_BASE_URL}/auth/register",
                json={
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD,
                    "full_name": TEST_NAME
                }
            )
            if register_response.status_code == 201:
                print("   ✓ User registered successfully")
            elif register_response.status_code == 400 and "already registered" in register_response.text:
                print("   ℹ User already exists, proceeding to login")
            else:
                print(f"   ✗ Registration failed: {register_response.status_code}")
                print(f"     Response: {register_response.text}")
        except Exception as e:
            print(f"   ✗ Registration error: {e}")
            return

        # Step 2: Login
        print("\n2. Logging in...")
        try:
            login_response = await client.post(
                f"{API_BASE_URL}/auth/login",
                json={
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD
                }
            )
            if login_response.status_code == 200:
                token_data = login_response.json()
                access_token = token_data["access_token"]
                print("   ✓ Login successful")
                print(f"     Token: {access_token[:50]}...")
            else:
                print(f"   ✗ Login failed: {login_response.status_code}")
                print(f"     Response: {login_response.text}")
                return
        except Exception as e:
            print(f"   ✗ Login error: {e}")
            return

        # Step 3: Create obituary with all features
        print("\n3. Creating obituary (AI + Image + TTS)...")
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            # Create multipart form data
            files = {
                "image": ("test_image.jpg", create_test_image(), "image/jpeg")
            }
            data = {
                "name": "John Doe",
                "birth_date": "1950-01-15",
                "death_date": "2024-11-30",
                "is_public": "true"
            }

            print("   → Generating AI obituary text...")
            print("   → Uploading image to S3...")
            print("   → Converting to speech with Amazon Polly...")

            create_response = await client.post(
                f"{API_BASE_URL}/obituaries/",
                headers=headers,
                data=data,
                files=files
            )

            if create_response.status_code == 201:
                obituary = create_response.json()
                print("   ✓ Obituary created successfully!")
                print(f"\n   Obituary Details:")
                print(f"   - ID: {obituary['id']}")
                print(f"   - Name: {obituary['name']}")
                print(f"   - Birth: {obituary['birth_date']}")
                print(f"   - Death: {obituary['death_date']}")
                print(f"   - Text preview: {obituary['obituary_text'][:100]}...")
                print(f"   - Image URL: {obituary.get('image_url', 'None')}")
                print(f"   - Audio URL: {obituary.get('audio_url', 'None')}")

                # Verify features
                print(f"\n   Feature Status:")
                print(f"   {'✓' if obituary['obituary_text'] else '✗'} AI Text Generation")
                print(f"   {'✓' if obituary.get('image_url') else '✗'} Image Upload to S3")
                print(f"   {'✓' if obituary.get('audio_url') else '✗'} Text-to-Speech (Polly)")

                return obituary
            else:
                print(f"   ✗ Creation failed: {create_response.status_code}")
                print(f"     Response: {create_response.text}")
                return None
        except Exception as e:
            print(f"   ✗ Creation error: {e}")
            import traceback
            traceback.print_exc()
            return None

        # Step 4: Get user's obituaries
        print("\n4. Fetching user's obituaries...")
        try:
            list_response = await client.get(
                f"{API_BASE_URL}/obituaries/my-obituaries",
                headers=headers
            )
            if list_response.status_code == 200:
                data = list_response.json()
                print(f"   ✓ Found {data['total']} obituaries")
            else:
                print(f"   ✗ Fetch failed: {list_response.status_code}")
        except Exception as e:
            print(f"   ✗ Fetch error: {e}")

def create_test_image():
    """Create a minimal test JPEG image"""
    # Minimal valid JPEG header + data
    jpeg_data = base64.b64decode(
        "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcU"
        "FhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgo"
        "KCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIA"
        "AhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEB"
        "AQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwABmQ/9k="
    )
    return jpeg_data

if __name__ == "__main__":
    print("\nMake sure your backend is running on http://localhost:8000")
    print("Start it with: cd backend && uvicorn app.main:app --reload\n")

    try:
        asyncio.run(test_full_flow())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
    except Exception as e:
        print(f"\n\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)
