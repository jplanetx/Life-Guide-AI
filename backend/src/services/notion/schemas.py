GOALS_SCHEMA = {
    "name": "Goals",
    "properties": {
        "Title": {"type": "title"},
        "Description": {"type": "rich_text"},
        "Brain Area": {
            "type": "select",
            "options": [
                {"name": "Active Brain", "color": "blue"},
                {"name": "Automatic Brain", "color": "green"},
                {"name": "Creative Brain", "color": "purple"},
                {"name": "Daily Brain", "color": "yellow"},
                {"name": "Memory Brain", "color": "gray"}
            ]
        },
        "PARA Location": {
            "type": "select",
            "options": [
                {"name": "Projects", "color": "blue"},
                {"name": "Areas", "color": "green"},
                {"name": "Resources", "color": "orange"},
                {"name": "Archive", "color": "gray"}
            ]
        },
        "Category": {
            "type": "select",
            "options": [
                {"name": "Career", "color": "blue"},
                {"name": "Personal", "color": "green"},
                {"name": "Health", "color": "red"},
                {"name": "Learning", "color": "yellow"}
            ]
        },
        "Target Date": {"type": "date"},
        "Progress": {"type": "number", "number_format": "percent"},
        "Status": {
            "type": "select",
            "options": [
                {"name": "Not Started", "color": "gray"},
                {"name": "In Progress", "color": "yellow"},
                {"name": "Completed", "color": "green"},
                {"name": "Blocked", "color": "red"}
            ]
        },
        "Related Tasks": {"type": "relation", "collection_id": "tasks"}
    }
}

INSIGHTS_SCHEMA = {
    "name": "AI Coach Insights",
    "properties": {
        "Title": {"type": "title"},
        "Date": {"type": "date"},
        "Brain Process": {
            "type": "select",
            "options": [
                {"name": "Pattern Recognition", "color": "blue"},
                {"name": "Decision Making", "color": "green"},
                {"name": "Learning", "color": "yellow"},
                {"name": "Memory Formation", "color": "purple"}
            ]
        },
        "Type": {
            "type": "select",
            "options": [
                {"name": "Task Pattern", "color": "blue"},
                {"name": "Goal Progress", "color": "green"},
                {"name": "Behavior Pattern", "color": "purple"},
                {"name": "Recommendation", "color": "yellow"}
            ]
        },
        "Content": {"type": "rich_text"},
        "Impact Score": {"type": "number", "number_format": "number"},
        "Related Goals": {"type": "relation", "collection_id": "goals"},
        "Action Items": {"type": "rich_text"},
        "Status": {
            "type": "select",
            "options": [
                {"name": "Active", "color": "green"},
                {"name": "Archived", "color": "gray"}
            ]
        }
    }
}
