import sys
import urllib.request
import json


def fetch_activity(username):
    """Fetches the recent public activity of a GitHub user."""
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 204:  # No Content
                print(f"No recent activity found for user: {username}")
                return

            data = json.loads(response.read().decode())
            if not data:
                print(f"No recent activity found for user: {username}")
            else:
                display_activity(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"User '{username}' not found.")
        else:
            print(f"Failed to fetch activity. HTTP Error: {e.code}")
    except urllib.error.URLError:
        print("Network error. Please check your internet connection.")
    except json.JSONDecodeError:
        print("Failed to decode the response. Try again later.")


def display_activity(events):
    """Displays the fetched activity in a user-friendly format."""
    for event in events:
        event_type = event["type"]
        repo_name = event["repo"]["name"]

        if event_type == "PushEvent":
            commit_count = len(event["payload"]["commits"])
            print(f"Pushed {commit_count} commit(s) to {repo_name}")

        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            print(f"{action.capitalize()} an issue in {repo_name}")

        elif event_type == "WatchEvent":
            print(f"Starred {repo_name}")

        elif event_type == "ForkEvent":
            print(f"Forked {repo_name}")

        elif event_type == "CreateEvent":
            ref_type = event["payload"]["ref_type"]
            print(f"Created a new {ref_type} in {repo_name}")

        else:
            print(f"{event_type} occurred in {repo_name}")


def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
        return

    username = sys.argv[1]
    fetch_activity(username)


if __name__ == "__main__":
    main()
