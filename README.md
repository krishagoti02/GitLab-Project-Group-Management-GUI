# **GitHub**

## Overview

GitHub Project is a tool designed to extract and summarize user activities from GitHub repositories. By utilizing the GitHub API, this project fetches data related to a user's repositories, contributions, and other activities. The summarized data can be used for various purposes, such as creating activity reports, generating analytics, or providing insights into a developer's work.

This project also allows you to manage team members in a GitHub repository through both the GitHub web interface (GUI) and programmatically via the GitHub API. You can easily add or remove members from your project.

## Features

- Retrieves user contribution data, such as commits and pull requests.
- Generates summary reports of a user's GitHub activity.
- Manage team members, including adding and removing collaborators via the GUI or programmatically using the GitHub API.

## Managing Members in the Project
 Adding/Removing Members Using the GitHub GUI

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.x
- `requests` library (`pip install requests`)

## GitHub API Access

To use the GitHub API in this project, you'll need to obtain a GitHub Personal Access Token (PAT). This token allows you to authenticate and interact with GitHub's API programmatically.

### Steps to Obtain a GitHub Personal Access Token:

1. **Log in to GitHub:**
   - Go to [GitHub's website](https://github.com) and log in with your account credentials.

2. **Navigate to Developer Settings:**
   - Click on your profile picture in the top right corner of the page, and select "Settings" from the dropdown menu.
   - Scroll down and find "Developer settings" in the sidebar, then click on it.

3. **Create a New Token:**
   - In the "Developer settings" menu, select "Personal access tokens" and then click on "Generate new token".
   - Provide a descriptive name for your token and select the appropriate scopes (permissions) needed for your project. Common scopes include `repo` (for repository access) and `user` (for user data access).

4. **Copy Your Token:**
   - After generating the token, **copy it immediately** as it will only be shown once. Store it securely, as it will be used to authenticate your API requests.

## Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/github-activity-summary.git
   cd github-activity-summary

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt

3. **Run the Script**:
 - Replace your_token_here in the script with your GitHub Personal Access Token.
 - Execute the script:

   ```bash
   python main.py
