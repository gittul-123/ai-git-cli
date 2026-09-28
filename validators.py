import re
from git_utils import get_changed_files

def validate_commit_title(title):
    if len(title) > 72:
        print(f"[WARN] 커밋 제목이 72자를 초과하여 잘라냅니다. (원래 {len(title)}자)")
        title = title[:72]

    elif len(title) > 50:
        print(f"[WARN] 커밋 제목이 권장 길이(50자)를 초과했습니다. ({len(title)}자)")

    return title

def validate_commit_body(body):
    if not body.strip():
        return body

    has_file_mention = re.search(r"\w+\.py", body)
    has_bullet = "-" in body or "*" in body

    if not has_file_mention and not has_bullet :
        print("[WARN] 커밋 본문에 변경된 파일 언급이나 불릿 요약이 없어 변경된 파일 목록을 자동으로 추가합니다.")

        files = get_changed_files()
        file_list = files.strip().split("\n")
        file_str = ", ".join(file_list)

        body = body + f"\n\n변경된 파일: {file_str}"

    return body

def validate_pr_title(title):
    if len(title) > 80:
        print(f"[WARN] PR 제목이 80자를 초과하여 잘라냅니다. (원래 {len(title)}자)")
        title = title[:80]
    return title

def validate_pr_body(body):
    sections = ["Why", "What", "How to Test"]
    lines = body.split("\n")

    for section in sections:
        # 1) 줄 전체가 헤더 이름인 줄 찾기
        start = -1
        for idx, line in enumerate(lines):
            if line.strip().strip("#: ") == section:
                start = idx
                break
        if start == -1:
            print(f"[WARN] PR 본문에 '{section}' 섹션이 없습니다.")
            continue

        # 2) 다음 헤더가 나오기 전까지가 이 섹션의 내용
        end = len(lines)
        for idx in range(start + 1, len(lines)):
            if lines[idx].strip().strip("#: ") in sections:
                end = idx
                break

        # 3) 내용 줄 중 불릿으로 시작하는 줄이 있는지, 첫 내용 줄은 어디인지
        has_bullet = False
        first_content = -1
        for idx in range(start + 1, end):
            text = lines[idx].strip()
            if text == "":
                continue
            if first_content == -1:
                first_content = idx
            if text.startswith("-") or text.startswith("*"):
                has_bullet = True

        # 4) 불릿이 없으면 첫 내용 줄 앞에 "- " 붙이기
        if not has_bullet and first_content != -1:
            print(f"[WARN] '{section}' 섹션에 불릿이 없어 자동으로 추가합니다.")
            lines[first_content] = "- " + lines[first_content]
        elif first_content == -1:
            print(f"[WARN] '{section}' 섹션에 내용이 없습니다.")

    return "\n".join(lines)

def find_missing_pr_sections(text):
    header_names = [line.strip().strip("#: ") for line in text.split("\n")]
    missing = []
    for section in ["Why", "What", "How to Test"]:
        if section not in header_names:
            missing.append(section)
    return missing