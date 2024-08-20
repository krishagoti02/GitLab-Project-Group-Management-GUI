import tkinter as tk
from tkinter import messagebox,ttk

import requests

gitlab_url = "https://gitlab.com"
private_token = "Bearer ******"  # Your private token here

def show_all_projects():
    """
    Retrieve and display information about all projects from a GitLab instance.

    This function fetches a list of all projects from the GitLab instance using
    the `get_all_projects` function and displays their IDs and names in a text widget.

    If projects are successfully retrieved, the text widget is enabled and populated
    with project information. If retrieval fails, an error message is displayed using
    a message box.

    Args:
        None

    Returns:
        None
    """
    all_projects = get_all_projects(gitlab_url, private_token)
    if all_projects:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "All Projects:\n")
        for project in all_projects:
            result_text.insert(tk.END, f"Project ID: {project['id']} - Project Name: {project['name']}\n")
        result_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Failed to retrieve projects.")

def show_all_groups():
    """
    Retrieve and display information about all groups from a GitLab instance.

    This function fetches a list of all groups from the GitLab instance using
    the `get_all_groups` function and displays their IDs and names in a text widget.

    If groups are successfully retrieved, the text widget is enabled and populated
    with group information. If retrieval fails, an error message is displayed using
    a message box.

    Args:
        None

    Returns:
        None
    """
    all_groups = get_all_groups(gitlab_url, private_token)
    if all_groups:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "All Groups:\n")
        for group in all_groups:
            result_text.insert(tk.END, f"Group ID: {group['id']} - Group Name: {group['name']}\n")
        result_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Failed to retrieve groups.")

def view_access_levels():
    """
    Display a list of GitLab access levels along with their corresponding numeric values.

    This function creates a dictionary of GitLab access levels and their corresponding
    numeric values. It then generates a formatted string containing the access level names
    and their numeric values, separated by newlines. Finally, it displays a message box
    with the title "Access Levels" and the formatted access level information.

    Args:
        None

    Returns:
        None
    """
    access_levels = {
        "No access": 0,
        "Minimal access": 5,
        "Guest": 10,
        "Reporter": 20,
        "Developer": 30,
        "Maintainer": 40,
        "Owner": 50
    }
    access_list_str = "\n".join([f"{access}: ({value})" for access, value in access_levels.items()])
    messagebox.showinfo("Access Levels", access_list_str)

# Function to display unique usernames from the projects dictionary
def show_unique_usernames():
    """
    Display unique usernames from projects along with their project associations.

    This function retrieves information about all projects with associated user
    usernames from a GitLab instance using the `get_all_projects_with_users` function.
    If projects with users are successfully retrieved, it enables the text widget
    (`result_text`), clears its contents, and inserts a list of unique usernames
    along with their project associations. Finally, it disables the text widget if
    projects with users were retrieved, or displays an error message using a message box.

    Args:
        None

    Returns:
        None
    """
    projects_with_users = get_all_projects_with_users(gitlab_url, private_token)
    if projects_with_users:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Unique Usernames from Projects:\n")
        unique_usernames = set()
        for project, usernames in projects_with_users.items():
            result_text.insert(tk.END, f"{project}: {usernames}\n")
            unique_usernames.update(usernames)
        result_text.insert(tk.END, f"\nUnique Usernames across all Projects: {unique_usernames}\n")
        result_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Failed to retrieve projects or project members.")

# Get all projects
def get_all_projects(gitlab_url, private_token):
    """
    Retrieve a list of all private projects from a GitLab instance.

    This function makes an API request to the specified GitLab instance's API endpoint
    to retrieve a list of all private projects. It uses the provided GitLab URL and
    private token for authentication.

    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A list of project information in JSON format, or None if an error occurs.
    :rtype: list[dict] or None
    """
    api_url = f"{gitlab_url}/api/v4/projects"
    headers = {"Authorization": private_token}
    params = {"visibility": "private"}  # Add this query parameter to filter private projects

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Check for any errors in the API response

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Get all groups
def get_all_groups(gitlab_url, private_token):
    """
    Retrieve a list of all private groups from a GitLab instance.

    This function makes an API request to the specified GitLab instance's API endpoint
    to retrieve a list of all private groups. It uses the provided GitLab URL and
    private token for authentication.

    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A list of group information in JSON format, or None if an error occurs.
    :rtype: list[dict] or None
    """
    api_url = f"{gitlab_url}/api/v4/groups"
    headers = {"Authorization": private_token}
    params = {"visibility": "private"}  # Add this query parameter to filter private groups

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Check for any errors in the API response

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def add_member_to_group():
    """
    Add a member to a GitLab group.

    This function retrieves input values from the GUI (Group ID, username, and access level),
    then calls the `add_member_to_group_by_username` function to add a member to the specified
    GitLab group. It displays a success message if the member is added successfully, or an error
    message if the operation fails.

    :param None
    :return: None
    """
    group_id = group_id_entry.get().strip()
    username = username_entry.get().strip()
    access_level = access_level_entry.get().strip()

    if group_id and username and access_level:
        added_member = add_member_to_group_by_username(group_id, username, access_level, gitlab_url, private_token)
        if added_member:
            messagebox.showinfo("Success", f"Added member to the group: {added_member['name']} - {added_member['username']}")
        else:
            messagebox.showerror("Error", "Failed to add member to the group.")
    else:
        messagebox.showerror("Error", "Invalid input. Please provide valid Group ID, username, and access level.")

def delete_group_member():
    """
    Delete a member from a GitLab group.

    This function retrieves input values from the GUI (Group ID and username),
    then calls the `delete_group_member_by_username` function to remove a member
    from the specified GitLab group. It displays a success message if the member is
    deleted successfully, or an error message if the operation fails.

    :param None
    :return: None
    """
    group_id = group_id_entry.get().strip()
    username = username_entry.get().strip()

    deleted_member = delete_group_member_by_username(group_id, username, gitlab_url, private_token)
    if deleted_member:
        messagebox.showinfo("Success", f"Deleted member from the group: {deleted_member['name']} - {deleted_member['username']}")
    else:
        messagebox.showerror("Error", "Member not found in the group.")

# Add member to project
def add_member_to_project():
    """
    Add a member to a GitLab project.

    This function retrieves input values from the GUI (selected project, username, and access level),
    then calls the `add_member_to_project_by_username` function to add a member to the specified
    GitLab project. It displays a success message if the member is added successfully, or an error
    message if the operation fails.

    :param None
    :return: None
    """
    project_name_id = project_dropdown.get()
    project_id = extract_project_id_from_dropdown(project_name_id)
    username = username_entry.get().strip()
    access_level = access_level_entry.get().strip()

    if project_id and username and access_level:
        added_member = add_member_to_project_by_username(project_id, username, access_level, gitlab_url, private_token)
        if added_member:
            messagebox.showinfo("Success", f"Added member to the project: {added_member['name']} - {added_member['username']}")
        else:
            messagebox.showerror("Error", "Failed to add member to the project.")
    else:
        messagebox.showerror("Error", "Invalid input. Please provide valid Project and username, and access level.")

def delete_project_member():
    """
    Delete a member from a GitLab project.

    This function retrieves input values from the GUI (selected project and username),
    then calls the `delete_project_member_by_username` function to remove a member
    from the specified GitLab project. It displays a success message if the member is
    deleted successfully, or an error message if the operation fails.

    :param None
    :return: None
    """
    project_name_id = project_dropdown.get()
    project_id = extract_project_id_from_dropdown(project_name_id)
    username = username_entry.get().strip()

    deleted_member = delete_project_member_by_username(project_id, username, gitlab_url, private_token)
    if deleted_member:
        messagebox.showinfo("Success", f"Deleted member from the project: {deleted_member['name']} - {deleted_member['username']}")
    else:
        messagebox.showerror("Error", "Member not found in the project.")

def get_all_projects_with_users(gitlab_url, private_token):
    """
    Retrieve a dictionary of projects with associated usernames from a GitLab instance.

    This function calls the `get_all_projects` function to retrieve a list of all projects
    from the GitLab instance using the provided GitLab URL and private token. It then iterates
    through each project, retrieves a list of project members using the `list_project_members`
    function, and creates a dictionary containing project names as keys and sets of associated
    usernames as values.

    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A dictionary mapping project names to sets of associated usernames, or None if an error occurs.
    :rtype: dict[str, set[str]] or None
    """
    all_projects = get_all_projects(gitlab_url, private_token)
    if not all_projects:
        return None

    projects_with_users = {}

    for project in all_projects:
        project_id = project['id']
        project_name = project['name']
        project_members = list_project_members(project_id, gitlab_url, private_token)
        if project_members:
            usernames = {member['username'] for member in project_members}
            projects_with_users[project_name] = list(usernames)

    return projects_with_users

# Add member to group
def add_member_to_group_by_username(group_id, username, access_level, gitlab_url, private_token):
    """
    Add a user to a GitLab group with the specified access level.

    This function makes an API request to add a user to the specified GitLab group
    with the provided access level. It uses the group ID, username, and access level
    to perform the operation. The GitLab URL and private token are used for authentication.

    :param group_id: The ID of the group.
    :type group_id: int
    :param username: The username of the user to be added.
    :type username: str
    :param access_level: The access level to assign to the user in the group.
    :type access_level: int
    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A dictionary containing the added member's information, or None if an error occurs.
    :rtype: dict or None
    """
    api_url = f"{gitlab_url}/api/v4/groups/{group_id}/members"
    headers = {"Authorization": private_token}

    # Retrieve the user ID using the provided username
    user_id = None
    user_search_url = f"{gitlab_url}/api/v4/users?username={username}"
    try:
        response = requests.get(user_search_url, headers=headers)
        response.raise_for_status()
        users = response.json()
        if users:
            user_id = users[0]['id']  # Take the first user's ID (if found)

    except requests.exceptions.RequestException as e:
        print(f"Error while retrieving user ID for username '{username}': {e}")
        return None

    if user_id:
        data = {"user_id": user_id, "access_level": access_level}
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()  # Check for any errors in the API response

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    else:
        print(f"User with username '{username}' not found.")
        return None

# Delete group member by username
def delete_group_member_by_username(group_id, username, gitlab_url, private_token):
    """
    Delete a user from a GitLab group based on their username.

    This function makes an API request to retrieve the list of members in the specified GitLab group,
    then iterates through the members to find the user with the provided username. If a matching user
    is found, the function sends a delete request to remove the user from the group. The GitLab URL and
    private token are used for authentication.

    :param group_id: The ID of the group.
    :type group_id: int
    :param username: The username of the user to be deleted from the group.
    :type username: str
    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A dictionary containing the deleted member's information, or None if the member is not found.
    :rtype: dict or None
    """
    api_url = f"{gitlab_url}/api/v4/groups/{group_id}/members"
    headers = {"Authorization": private_token}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Check for any errors in the API response

        members = response.json()
        for member in members:
            if username.lower() == member['username'].lower():
                member_id = member['id']
                delete_url = f"{gitlab_url}/api/v4/groups/{group_id}/members/{member_id}"
                response = requests.delete(delete_url, headers=headers)
                response.raise_for_status()
                return member
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Delete project member by username
def delete_project_member_by_username(project_id, username, gitlab_url, private_token):
    """
    Delete a user from a GitLab project based on their username.

    This function makes an API request to retrieve the list of members in the specified GitLab project,
    then iterates through the members to find the user with the provided username. If a matching user
    is found, the function sends a delete request to remove the user from the project. The GitLab URL
    and private token are used for authentication.

    :param project_id: The ID of the project.
    :type project_id: int
    :param username: The username of the user to be deleted from the project.
    :type username: str
    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A dictionary containing the deleted member's information, or None if the member is not found.
    :rtype: dict or None
    """
    api_url = f"{gitlab_url}/api/v4/projects/{project_id}/members"
    headers = {"Authorization": private_token}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Check for any errors in the API response

        members = response.json()
        for member in members:
            if username.lower() == member['username'].lower():
                member_id = member['id']
                delete_url = f"{gitlab_url}/api/v4/projects/{project_id}/members/{member_id}"
                response = requests.delete(delete_url, headers=headers)
                response.raise_for_status()
                return member
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Add member to project
def add_member_to_project_by_username(project_id, username, access_level, gitlab_url, private_token):
    """
    Add a user to a GitLab project with the specified access level.

    This function makes an API request to add a user to the specified GitLab project
    with the provided access level. It uses the project ID, username, and access level
    to perform the operation. The GitLab URL and private token are used for authentication.

    :param project_id: The ID of the project.
    :type project_id: int
    :param username: The username of the user to be added.
    :type username: str
    :param access_level: The access level to assign to the user in the project.
    :type access_level: int
    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A dictionary containing the added member's information, or None if an error occurs.
    :rtype: dict or None
    """
    api_url = f"{gitlab_url}/api/v4/projects/{project_id}/members"
    headers = {"Authorization": private_token}

    # Retrieve the user ID using the provided username
    user_id = None
    user_search_url = f"{gitlab_url}/api/v4/users?username={username}"
    try:
        response = requests.get(user_search_url, headers=headers)
        response.raise_for_status()
        users = response.json()
        if users:
            user_id = users[0]['id']  # Take the first user's ID (if found)

    except requests.exceptions.RequestException as e:
        print(f"Error while retrieving user ID for username '{username}': {e}")
        return None

    if user_id:
        data = {"user_id": user_id, "access_level": access_level}
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()  # Check for any errors in the API response

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    else:
        print(f"User with username '{username}' not found.")
        return None

# Helper function to populate project names and IDs for the dropdown
def populate_project_dropdown():
    """
    Populate a dropdown menu with the names and IDs of all GitLab projects.

    This function retrieves a list of all GitLab projects using the provided GitLab URL
    and private token by calling the `get_all_projects` function. It then populates the
    project dropdown menu with the names and IDs of the projects, allowing users to select
    a project for various operations.

    :param None
    :return: None
    """
    all_projects = get_all_projects(gitlab_url, private_token)
    if all_projects:
        for project in all_projects:
            project_name = project['name']
            project_id = project['id']
            project_name_id = f"{project_name} (ID: {project_id})"
            project_dropdown["values"] = (*project_dropdown["values"], project_name_id)


def get_project_id_by_name(project_name):
    """
    Retrieve the ID of a GitLab project based on its name.

    This function searches through the list of all GitLab projects using the provided
    project name and calls the `get_all_projects` function to obtain the project data.
    If a project with a matching name is found, the function returns its ID. If no
    matching project is found, it returns None.

    :param project_name: The name of the project.
    :type project_name: str
    :return: The ID of the project if found, otherwise None.
    :rtype: int or None
    """
    all_projects = get_all_projects(gitlab_url, private_token)
    if all_projects:
        for project in all_projects:
            if project['name'] == project_name:
                return project['id']
    return None

# Helper function to extract project ID from the selected dropdown item
def extract_project_id_from_dropdown(name_id_string):
    """
    Extract and return the project ID from a dropdown item string.

    This function takes a string in the format "Project Name (ID: 123)" and extracts
    the numeric project ID from it. The extracted ID is then returned as an integer.

    :param name_id_string: The dropdown item string containing the project name and ID.
    :type name_id_string: str
    :return: The extracted project ID.
    :rtype: int
    """
    return int(name_id_string.split("ID: ")[-1][:-1])

# Group member list
def list_group_members(group_id, gitlab_url, private_token):
    """
    Retrieve the list of members in a GitLab group.

    This function makes an API request to obtain the list of members in the specified
    GitLab group using the provided group ID, GitLab URL, and private token. It returns
    the list of group members if the request is successful, or None if an error occurs.

    :param group_id: The ID of the group.
    :type group_id: int
    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A list of group members, or None if an error occurs.
    :rtype: list[dict] or None
    """
    api_url = f"{gitlab_url}/api/v4/groups/{group_id}/members"
    headers = {"Authorization": private_token}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Check for any errors in the API response

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# list members of project
def list_project_members(project_id, gitlab_url, private_token):
    """
    Retrieve the list of members in a GitLab project.

    This function makes an API request to obtain the list of members in the specified
    GitLab project using the provided project ID, GitLab URL, and private token. It returns
    the list of project members if the request is successful, or None if an error occurs.

    :param project_id: The ID of the project.
    :type project_id: int
    :param gitlab_url: The base URL of the GitLab instance.
    :type gitlab_url: str
    :param private_token: The private token for authentication.
    :type private_token: str
    :return: A list of project members, or None if an error occurs.
    :rtype: list[dict] or None
    """
    api_url = f"{gitlab_url}/api/v4/projects/{project_id}/members"
    headers = {"Authorization": private_token}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Check for any errors in the API response

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def exit_program():
    """
    Exit the program and close the GUI window.

    This function destroys the main GUI window, effectively closing the program when called.

    :param None
    :return: None
    """
    root.destroy()

root = tk.Tk()
root.title("GitLab API Interaction")

main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20)

# Menu
menu_frame = tk.Frame(main_frame)
menu_frame.pack()

menu_label = tk.Label(menu_frame, text="Menu:", font=("Helvetica", 14, "bold"))
menu_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

list_projects_button = tk.Button(menu_frame, text="List all Projects", command=show_all_projects)
list_projects_button.grid(row=1, column=0, padx=5, pady=5)

list_groups_button = tk.Button(menu_frame, text="List all Groups", command=show_all_groups)
list_groups_button.grid(row=1, column=1, padx=5, pady=5)

view_access_button = tk.Button(menu_frame, text="View Access Levels", command=view_access_levels)
view_access_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

# Add a new button to display unique usernames
show_unique_usernames_button = tk.Button(menu_frame, text="Show Unique Usernames", command=show_unique_usernames)
show_unique_usernames_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Member Actions
action_frame = tk.Frame(main_frame)
action_frame.pack()

group_id_label = tk.Label(action_frame, text="Group ID:")
group_id_label.grid(row=0, column=0, padx=5, pady=5)

group_id_entry = tk.Entry(action_frame)
group_id_entry.grid(row=0, column=1, padx=5, pady=5)

# Dropdown for selecting projects
project_label = tk.Label(action_frame, text="Select Project:")
project_label.grid(row=0, column=0, padx=5, pady=5)

project_dropdown = ttk.Combobox(action_frame, state="readonly", width=40)
project_dropdown.grid(row=0, column=1, padx=5, pady=5)
populate_project_dropdown()  # Populate the project dropdown initially

username_label = tk.Label(action_frame, text="Username:")
username_label.grid(row=1, column=0, padx=5, pady=5)

username_entry = tk.Entry(action_frame)
username_entry.grid(row=1, column=1, padx=5, pady=5)

access_level_label = tk.Label(action_frame, text="Access Level(Only for adding user):")
access_level_label.grid(row=2, column=0, padx=5, pady=5)

access_level_entry = tk.Entry(action_frame)
access_level_entry.grid(row=2, column=1, padx=5, pady=5)

add_to_group_button = tk.Button(action_frame, text="Add member to Group", command=add_member_to_group)
add_to_group_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

delete_from_group_button = tk.Button(action_frame, text="Delete member from Group", command=delete_group_member)
delete_from_group_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

add_to_project_button = tk.Button(action_frame, text="Add member to Project", command=add_member_to_project)
add_to_project_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

delete_from_project_button = tk.Button(action_frame, text="Delete member from Project", command=delete_project_member)
delete_from_project_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Results
result_frame = tk.Frame(main_frame)
result_frame.pack()

result_text = tk.Text(result_frame, width=50, height=10, state=tk.DISABLED)
result_text.pack()

# Exit
exit_button = tk.Button(main_frame, text="Exit", command=exit_program)
exit_button.pack(pady=10)

root.mainloop()