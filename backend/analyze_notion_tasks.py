from datetime import datetime
from notion_client import Client
import os
from dotenv import load_dotenv
from src.services.insights.timeline_forecaster import TimelineForecaster

load_dotenv()

async def analyze_task_patterns():
    notion = Client(auth=os.getenv('NOTION_API_KEY'))
    tasks_db_id = os.getenv('NOTION_TASKS_DATABASE_ID')

    # Query completed tasks
    tasks = notion.databases.query(
        database_id=tasks_db_id,
        filter={
            "property": "Complete",
            "checkbox": {
                "equals": True
            }
        }
    ).get('results', [])

    print(f"\nAnalyzing {len(tasks)} completed tasks")

    formatted_tasks = []
    for task in tasks:
        props = task['properties']
        created_time = props['Created']['created_time']
        due_date = props['Due Date']['date']
        project = props['Project']['relation']
        status = props['Status']['status']

        # Handle dates with timezone normalization
        if due_date:
            due_date = datetime.fromisoformat(due_date['start']).replace(tzinfo=None)

        formatted_task = {
            'id': task['id'],
            'Title': props['Name']['title'][0]['text']['content'] if props['Name']['title'] else '',
            'CreatedDate': datetime.fromisoformat(created_time.replace('Z', '+00:00')).replace(tzinfo=None),
            'DueDate': due_date,
            'CompletionDate': datetime.fromisoformat(task['last_edited_time'].replace('Z', '+00:00')).replace(tzinfo=None),
            'Project': project[0]['id'] if project else None,
            'Status': status['name'] if status else None,
            'TimeEstimate': props['Time Estimate']['number']
        }
        formatted_tasks.append(formatted_task)

    # Analyze completion patterns
    print("\nCompletion Time Analysis:")
    for task in formatted_tasks:
        completion_time = (task['CompletionDate'] - task['CreatedDate']).total_seconds() / 3600
        print(f"\nTask: {task['Title']}")
        print(f"Time to Complete: {completion_time:.1f} hours")
        if task['DueDate']:
            due_diff = (task['CompletionDate'] - task['DueDate']).total_seconds() / 3600
            print(f"Completed {'early' if due_diff < 0 else 'late'} by {abs(due_diff):.1f} hours")
        if task['TimeEstimate']:
            accuracy = completion_time / task['TimeEstimate']
            print(f"Estimate Accuracy: {accuracy:.1f}x")

    # Calculate averages
    total_tasks = len(formatted_tasks)
    tasks_with_estimates = [t for t in formatted_tasks if t['TimeEstimate']]
    tasks_with_due_dates = [t for t in formatted_tasks if t['DueDate']]

    print("\nSummary:")
    print(f"Total Completed Tasks: {total_tasks}")
    print(f"Tasks with Time Estimates: {len(tasks_with_estimates)}")
    print(f"Tasks with Due Dates: {len(tasks_with_due_dates)}")

    if tasks_with_estimates:
        avg_estimate_accuracy = sum(
            (t['CompletionDate'] - t['CreatedDate']).total_seconds() / 3600 / t['TimeEstimate']
            for t in tasks_with_estimates
        ) / len(tasks_with_estimates)
        print(f"Average Estimate Accuracy: {avg_estimate_accuracy:.1f}x")

if __name__ == "__main__":
    import asyncio
    asyncio.run(analyze_task_patterns())
