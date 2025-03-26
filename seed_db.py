import asyncio
from app.db.database import engine, Base, AsyncSession
from app.db.seed import seed_data
from app.models import models  # Import models to register them with Base

async def main():
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create a session and seed the data
    async with AsyncSession(engine) as session:
        await seed_data(session)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
