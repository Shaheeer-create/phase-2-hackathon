import asyncio
from sqlmodel import Session, select
from src.core.database import engine, get_session
from src.models.user import User
from src.models.task import Task
from sqlalchemy.sql import func

async def test_database_connection():
    """
    Test script to verify database connection with Neon
    """
    print("Testing database connection...")

    try:
        # Get a session using the generator
        from src.core.database import get_session
        session_gen = get_session()
        session = next(session_gen)

        # Test by querying for any existing users
        statement = select(User).limit(1)
        results = session.exec(statement)
        users = results.all()

        print(f"Successfully connected to database. Found {len(users)} users.")

        # Test counting users to verify read access
        user_count_stmt = select(func.count(User.id))
        user_count = session.exec(user_count_stmt).one()

        print(f"Total user count: {user_count}")

        # Close the session
        session.close()

        print("Database connection test completed successfully!")
        return True

    except Exception as e:
        print(f"Database connection test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_database_connection())