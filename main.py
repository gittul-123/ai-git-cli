import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="AI 기반 커밋/PR 생성기")
    subparsers = parser.add_subparsers(dest="command")

    # commit 명령어
    commit_parser = subparsers.add_parser("commit")
    commit_parser.add_argument("-model", default="claude-sonnet-4")
    commit_parser.add_argument("-temperature", type=float, default=0.7)
    commit_parser.add_argument("-max-tokens", type=int, default=1024)

    # pr 명령어
    pr_parser = subparsers.add_parser("pr")
    pr_parser.add_argument("-model", default="claude-sonnet-4")
    pr_parser.add_argument("-temperature", type=float, default=0.7)
    pr_parser.add_argument("-max-tokens", type=int, default=1024)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(args)