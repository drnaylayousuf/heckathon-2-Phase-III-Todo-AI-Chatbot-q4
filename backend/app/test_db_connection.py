import asyncio
import logging
from sqlalchemy import text
from app.database.session import get_engine

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_database_connection():
    """Test if database connection works"""
    try:
        logger.info("Testing database connection...")
        engine = get_engine()

        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row:
                logger.info("✓ Database connection test successful")
                return True
    except Exception as e:
        logger.error(f"✗ Database connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(test_database_connection())
    if success:
        logger.info("✓ Database connectivity test passed")
    else:
        logger.error("✗ Database connectivity test failed")