import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

async def test_health():
    """Test the health check endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/health") as response:
            logger.info(f"Health Check Status: {response.status}")
            data = await response.json()
            logger.info(f"Health Check Response: {data}")
            return response.status == 200

async def test_tasks():
    """Test the tasks endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/tasks") as response:
            logger.info(f"Tasks Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                logger.info(f"Retrieved {len(data)} tasks")
                for task in data[:3]:  # Show first 3 tasks
                    logger.info(f"Task: {task.get('title')} - "
                              f"Status: {task.get('status')}")
            else:
                error = await response.text()
                logger.error(f"Error: {error}")
            return response.status == 200

async def test_update_task(task_id: str):
    """Test updating a task."""
    test_properties = {
        "Status": {
            "select": {
                "name": "In Progress"
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f"{BASE_URL}/api/tasks/{task_id}/properties",
            json=test_properties
        ) as response:
            logger.info(f"Update Task Status: {response.status}")
            data = await response.json()
            logger.info(f"Update Response: {data}")
            return response.status == 200

async def test_analyze_task(task_id: str):
    """Test task analysis."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BASE_URL}/api/tasks/{task_id}/analyze"
        ) as response:
            logger.info(f"Analyze Task Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                logger.info(f"Analysis: {data}")
            else:
                error = await response.text()
                logger.error(f"Error: {error}")
            return response.status == 200

async def main():
    """Run all tests."""
    logger.info("Starting API tests...")

    # Test health
    logger.info("\n=== Testing Health Check ===")
    health_ok = await test_health()

    if not health_ok:
        logger.error("Health check failed, stopping tests")
        return

    # Test tasks
    logger.info("\n=== Testing Tasks Endpoint ===")
    tasks_ok = await test_tasks()

    if not tasks_ok:
        logger.error("Tasks endpoint failed, stopping tests")
        return

    # Get first task ID for update and analysis tests
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/tasks") as response:
            if response.status == 200:
                tasks = await response.json()
                if tasks:
                    task_id = tasks[0]['id']

                    # Test task update
                    logger.info("\n=== Testing Task Update ===")
                    await test_update_task(task_id)

                    # Test task analysis
                    logger.info("\n=== Testing Task Analysis ===")
                    await test_analyze_task(task_id)
                else:
                    logger.error("No tasks found for testing")
            else:
                logger.error("Could not get tasks for testing")

if __name__ == "__main__":
    asyncio.run(main())
