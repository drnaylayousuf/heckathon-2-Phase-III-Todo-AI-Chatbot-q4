#!/usr/bin/env python3
"""
Simple test script to verify backend components can be imported
"""

def test_imports():
    """Test that all critical modules can be imported"""
    print("Testing backend imports...")

    try:
        from app.config import settings
        print("[OK] Config imported successfully")
    except Exception as e:
        print(f"[FAIL] Config import failed: {e}")
        return False

    try:
        from app.core.logging_config import get_logger
        logger = get_logger(__name__)
        print("[OK] Logger imported successfully")
    except Exception as e:
        print(f"[FAIL] Logger import failed: {e}")
        return False

    try:
        from app.database.session import get_engine, get_session
        print("[OK] Database session imported successfully")
    except Exception as e:
        print(f"[FAIL] Database session import failed: {e}")
        return False

    try:
        from app.core.auth import verify_password, get_password_hash
        print("[OK] Authentication functions imported successfully")
    except Exception as e:
        print(f"[FAIL] Authentication functions import failed: {e}")
        return False

    try:
        from app.core.ai_service import gemini_service
        print("[OK] AI service imported successfully")
    except Exception as e:
        print(f"[FAIL] AI service import failed: {e}")
        return False

    print("\nAll imports successful! Backend should be ready to run.")
    return True

if __name__ == "__main__":
    test_imports()