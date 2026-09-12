import argparse
from git_utils import get_git_status, get_git_diff, mask_sensitive_info
from ai_client import generate_text

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

    diff_text = get_git_diff()

    if args.safe_mode:
        diff_text = mask_sensitive_info(diff_text)

    if not diff_text.strip():
        print("변경 사항이 없습니다.")
        return

    if args.command == "commit":
        prompt = f"다음 git diff를 보고 커밋 메시지를 작성해줘:\n{diff_text}"

    elif args.command == "pr":
        prompt = f"다음 git diff를 보고 PR 제목과 Why/What/How to Test 구조로 본문을 작성해줘:\n{diff_text}"

    result = generate_text(
        prompt,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    print(result)

if __name__ == "__main__":
    main()
