def validate_commit_title(title):
    if len(title) > 72:
        print(f"[WARN] 커밋 제목이 72자를 초과하여 잘라냅니다. (원래 {len(title)}자)")
        title = title[:72]

    elif len(title) > 50:
        print(f"[WARN] 커밋 제목이 권장 길이(50자)를 초과했습니다. ({len(title)}자)")

    return title