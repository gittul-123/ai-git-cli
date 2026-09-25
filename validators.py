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
    required_sections = ["Why", "What", "How to Test"]
    for i, section in enumerate(required_sections):
        if section not in body:
            print(f"[WARN] PR 본문에 '{section}' 섹션이 없습니다.")
            continue

        start = body.find(section)

        if i + 1 < len(required_sections):
            end = body.find(required_sections[i+1])

        else:
            end = len(body)

        section_text = body[start:end]

        if "-" not in section_text and "*" not in section_text:
            print(f"[WARN] '{section}' 섹션에 불릿이 없어 자동으로 추가합니다.")
            lines = section_text.split("\n")
            lines[1] = "- " + lines[1]
            new_section_text = "\n".join(lines)
            body = body.replace(section_text, new_section_text)

    return body