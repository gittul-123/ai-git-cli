import subprocess
# 테스트용 주석

def get_git_status():
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    return result.stdout

def get_git_diff():
    result = subprocess.run(["git", "diff"], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    print("=== git status ===")
    print(get_git_status())
    print("=== git diff ===")
    print(get_git_diff())