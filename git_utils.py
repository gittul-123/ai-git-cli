import subprocess
import re

def get_git_status():
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    return result.stdout

def get_git_diff():
    result = subprocess.run(["git", "diff"], capture_output=True, text=True)
    return result.stdout

def mask_sensitive_info(text):

    text = re.sub(r"sk-[a-zA-Z0-9]{10,}", "****", text)

    text = re.sub(r"[\w.]+@[\w.]+", "****", text)

    return text

if __name__ == "__main__":
    print("=== git status ===")
    print(get_git_status())
    print("=== git diff ===")
    print(get_git_diff())