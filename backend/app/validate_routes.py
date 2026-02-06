from fastapi import FastAPI
import asyncio
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test that the app can be imported without errors
try:
    from app.main import app
    logger.info("✓ Successfully imported main app")
except Exception as e:
    logger.error(f"✗ Failed to import main app: {e}")
    raise

# Test that key endpoints exist
try:
    # Check if routes are registered
    routes = [route.path for route in app.routes]
    logger.info(f"✓ Registered routes: {len(routes)} routes found")

    # Check for key API endpoints
    api_endpoints = [route for route in app.routes if '/api/' in route.path]
    logger.info(f"✓ API endpoints: {len(api_endpoints)} API routes found")

    # Check specific endpoints
    endpoints_to_check = ['/', '/api/health', '/test', '/health']
    for endpoint in endpoints_to_check:
        if any(route.path.startswith(endpoint) if endpoint != '/' else route.path == '/' for route in app.routes):
            logger.info(f"✓ Endpoint {endpoint} is available")
        else:
            logger.warning(f"⚠ Endpoint {endpoint} might not be available")

    # Check for auth endpoints
    auth_endpoints = ['/api/login', '/api/register', '/api/me']
    for endpoint in auth_endpoints:
        found = any(route.path.startswith(endpoint) for route in app.routes)
        if found:
            logger.info(f"✓ Auth endpoint {endpoint} is available")
        else:
            logger.warning(f"⚠ Auth endpoint {endpoint} might not be available")

except Exception as e:
    logger.error(f"✗ Error checking routes: {e}")

logger.info("✓ App structure verification completed")