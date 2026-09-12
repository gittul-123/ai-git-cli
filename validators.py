def validate_commit_title(title):
    if len(title) > 72:
        print(f"[WARN] 커밋 제목이 72자를 초과하여 잘라냅니다. (원래 {len(title)}자)")
        title = title[:72]

    elif len(title) > 50:
        print(f"[WARN] 커밋 제목이 권장 길이(50자)를 초과했습니다. ({len(title)}자)")

    return title

def validate_pr_title(title):
    if len(title) > 80:
        print(f"[WARN] PR 제목이 80자를 초과하여 잘라냅니다. (원래 {len(title)}자)")
        title = title[:80]
    return title

def validate_pr_body(body):
    required_sections = ["Why", "What", "How to Test"]
    for section in required_sections:
        if section not in body:
            print(f"[WARN] PR 본문에 '{section}' 섹션이 없습니다.")
    return body