import subprocess
import os
import shutil


def git_pull():
    master_checkout_cmd = f"git -C C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation checkout master"
    master_checkout_res = subprocess.run(master_checkout_cmd, shell=True, capture_output=True,text=True)
    print(master_checkout_res.stdout)

    pull_process = subprocess.run(["git", "-C", "C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation","pull", "origin", "master"], capture_output=True, text=True)
    if pull_process.stdout:
        print(pull_process.stdout)
    else:
        print(pull_process.stderr)

def check_branch_exists(repo_url, branch_name):
    # Check if the branch exists in the remote repository
    remote_command = f"git -C C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation ls-remote --heads {repo_url} {branch_name}"
    remote_result = subprocess.run(remote_command, shell=True, capture_output=True,text=True)
    # Check if the branch exists locally
    local_command = f"git -C C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation show-ref --verify --quiet refs/heads/{branch_name}"
    local_result = subprocess.run(local_command, shell=True, capture_output=True,text=True)

    # Return True if both conditions satisfy
    return remote_result.returncode == 0 and local_result.returncode == 0


def git_create_branch(repo_url, branch_name):
    flag = 0
    if check_branch_exists(repo_url, branch_name) == 1:
        print(f"Branch - {branch_name} Already Exsist!")
    else: 
        subprocess.run(["git", "-C", "C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation", "checkout", "-b", branch_name])
        flag = 1
        print(f"Branch - {branch_name} Created!")
    return flag
    
def git_add_commit_push(branch_name, commit_message):
    subprocess.run(["git", "-C", "C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation", "add", "."])
    subprocess.run(["git", "-C", "C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation", "status", "."])
    subprocess.run(["git", "-C", "C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation", "commit", "-m", commit_message])
    subprocess.run(["git", "-C", "C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation", "push", "-u", "origin", branch_name])


# File Replacement Function
def replace_file(input_file_path, destination_path):
    try:
        shutil.copy2(input_file_path, destination_path)
        print(f"File '{input_file_path}' has been successfully replaced at '{destination_path}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist.")


if __name__ == "__main__":
    # Replace these values with your actual file path, content, and Bitbucket repository URL
    modified_file_path = "C:/Users/PC/Desktop/Bitbucket-Automation/code/sample.txt"
    destination_file_path = "C:/Users/PC/Desktop/Bitbucket-Automation/bitbucket-automation/sample.txt"
    repo_url = "https://Vijay0707@bitbucket.org/myworkspace0707/bitbucket-automation.git"
    print("------------------ Git Automation ------------------")

    # Step 1: Pull the latest changes from the master branch
    print("------------------ 1. Git Pull ------------------")
    git_pull()
    
    # Step 2: Create a feature branch
    feature_branch_name = "feature/test1"

    print("------------------ 2. Git Branch Creation ------------------")
    flag = git_create_branch(repo_url,feature_branch_name)

    if flag == 1:    
        # Step 3: Replace the modified file
        print("------------------ 3. File Replacement ------------------")
        replace_file(modified_file_path, destination_file_path)

        # Step 4: Add, commit, and push the changes to the feature branch
        commit_message = "Replace modified file"
        print("------------------ 4. Git Commit and Add ------------------")
        git_add_commit_push(feature_branch_name, commit_message)
