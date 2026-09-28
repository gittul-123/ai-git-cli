import argparse
from git_utils import get_git_status, get_git_diff, mask_sensitive_info
from ai_client import generate_text
from validators import validate_commit_title, validate_commit_body, validate_pr_title, validate_pr_body, find_missing_pr_sections

def parse_args():
    parser = argparse.ArgumentParser(description="AI 기반 커밋/PR 생성기")
    subparsers = parser.add_subparsers(dest="command")

    # commit 명령어
    commit_parser = subparsers.add_parser("commit")
    commit_parser.add_argument("-model", default="claude-sonnet-4")
    commit_parser.add_argument("-temperature", type=float, default=0.7)
    commit_parser.add_argument("-max-tokens", type=int, default=1024)
    commit_parser.add_argument("-safe-mode", action="store_true")

    # pr 명령어
    pr_parser = subparsers.add_parser("pr")
    pr_parser.add_argument("-model", default="claude-sonnet-4")
    pr_parser.add_argument("-temperature", type=float, default=0.7)
    pr_parser.add_argument("-max-tokens", type=int, default=1024)
    pr_parser.add_argument("-safe-mode", action="store_true")

    return parser.parse_args()

def main():
    args = parse_args()

    status_text = get_git_status()
    changed_count = len(status_text.strip().splitlines())
    print(f"[INFO] Git status 수집 완료: {changed_count}개 파일 변경 감지")

    diff_text = get_git_diff()

    if args.safe_mode:
        diff_text = mask_sensitive_info(diff_text)

    if not diff_text.strip():
        print("변경 사항이 없습니다.")
        return

    if args.command == "commit":
        prompt = f"다음 git diff를 보고 커밋 메시지를 작성해줘:\n{diff_text}"
        system_prompt = "마크다운 문법(##, ```, ** 등)을 쓰지 말고 순수 텍스트로만 답해줘. 첫 줄에는 커밋 제목만 쓰고, 그 다음 줄부터 본문을 써줘. "

    elif args.command == "pr":
        prompt = f"다음 git diff를 보고 PR 제목과 Why/What/How to Test 구조로 본문을 작성해줘:\n{diff_text}"
        system_prompt = "마크다운 문법(##, ```, ** 등)을 쓰지 말고 순수 텍스트로만 답해줘. 첫 줄에는 PR 제목만 쓰고, 그 다음 Why, What, How to Test 섹션을 순서대로 써줘. 각 섹션에는 최소 1개 이상의 불릿을 포함해줘."

    result = generate_text(
        prompt,
        system_prompt=system_prompt,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    if not result:
        print("AI 응답 생성에 실패했습니다.")
        return

    if args.command == "pr":
        missing = find_missing_pr_sections(result)
        if missing:
            print(f"[INFO] 누락된 섹션 {missing} 감지: AI에 1회 재요청합니다. (호출 총 2회)")
            retry_prompt = prompt + f"\n\n반드시 {', '.join(missing)} 섹션을 포함해서 다시 작성해줘."
            retry_result = generate_text(
                retry_prompt,
                system_prompt=system_prompt,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )
            if retry_result:
                result = retry_result

    lines = result.split("\n")
    title = lines[0]
    body = "\n".join(lines[1:])

    if args.command == "commit":
        title = validate_commit_title(title)
        body = validate_commit_body(body)

    elif args.command == "pr":
        title = validate_pr_title(title)
        body = validate_pr_body(body)

    print("--- 결과 ---")
    print("[주의] 아래 내용은 AI가 생성한 초안입니다. 검토 후 적용해주세요.")
    print(title)
    print(body)
    print("-----------")

if __name__ == "__main__":
    main()

