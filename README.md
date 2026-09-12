# AI 기반 Git 커밋/PR 메시지 자동 생성기

Git 변경 사항(`git status`, `git diff`)을 분석해, AI가 커밋 메시지와 Pull Request 초안을 자동으로 작성해주는 터미널(CLI) 도구입니다.

## 1. 설치 및 실행 방법

```bash
# 1) 저장소 클론
git clone https://github.com/gittul-123/ai-git-cli.git
cd ai-git-cli

# 2) 필요한 패키지 설치
pip install requests

# 3) 환경변수(API Key) 설정 (아래 2번 항목 참고)

# 4) 실행 (Git 저장소가 초기화된 프로젝트 루트에서 실행해야 합니다)
python3 main.py commit
```

## 2. 환경변수(API Key) 설정 방법

AI API Key는 코드에 직접 작성하지 않고, 환경변수 `AI_API_KEY`로 관리합니다.

**macOS / Linux (임시, 현재 터미널 세션에서만 유효)**
```bash
export AI_API_KEY="발급받은_API_키"
```

**macOS / Linux (영구 설정)**
`~/.zshrc` (또는 `~/.bashrc`) 파일 맨 아래에 위 줄을 추가한 뒤:
```bash
source ~/.zshrc
```

키가 정상 설정됐는지 확인:
```bash
echo $AI_API_KEY
```

> ⚠️ API 키가 설정되지 않은 상태로 실행하면 아래와 같은 에러 메시지가 출력됩니다.
> ```
> [ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.
> ```

## 3. 사용 방법 (명령 예시)

### 커밋 메시지 생성
```bash
python3 main.py commit
```

### PR 제목/본문 생성
```bash
python3 main.py pr
```

### 옵션 (모델, 파라미터 조정)
| 옵션 | 설명 | 기본값 |
|---|---|---|
| `-model` | 사용할 AI 모델 | `claude-sonnet-4` |
| `-temperature` | 생성 결과의 창의성 정도 (0에 가까울수록 일관적, 1에 가까울수록 창의적) | `0.7` |
| `-max-tokens` | 응답 최대 길이(토큰 수) | `1024` |
| `-safe-mode` | diff 안의 민감정보(API 키, 이메일 등)를 마스킹 후 전송 | 꺼짐 |

예시:
```bash
python3 main.py commit -temperature 0.3 -safe-mode
python3 main.py pr -model claude-sonnet-4 -max-tokens 1500
```

## 4. 출력 예시

### 커밋 메시지 생성 예시
```
$ python3 main.py commit
--- 결과 ---
feat: git diff 기반 커밋 메시지 자동 생성 기능 추가

- git diff 결과를 수집해 AI 입력 컨텍스트로 전달하도록 구현
- 커밋 메시지 템플릿 생성 규칙 적용
-----------
```

### PR 제목/본문 생성 예시
```
$ python3 main.py pr
--- 결과 ---
--- 결과 ---
PR 커맨드에 제목/본문 유효성 검사 로직 추가

Why
- PR 생성 시 제목 길이나 본문 구조에 대한 검증이 전혀 없어서 품질이 낮은 PR이 그대로 출력될 수 있었음
- commit 커맨드에는 validate_commit_title이 적용되어 있었지만 pr커맨드에는 동일한 수준의 검증이 없어 일관성이 부족했음

What
- validators.py에 validate_pr_title 함수를 추가하여 PR 제목이 80자를 초과하면 자동으로 잘라내고 경고를 출력하도록 구현
- validators.py에 validate_pr_body 함수를 추가하여 Why, What, Howto Test 섹션이 본문에 포함되어 있는지 확인하고 누락된 섹션에 대해경고를 출력하도록 구현
- main.py의 pr 커맨드 분기에서 위 두 함수를 호출하도록 연결하고,해당 함수들을 import 구문에 추가

How to Test
- python main.py pr 명령을 실행하여 80자를 초과하는 제목이 입력될경우 WARN 메시지와 함께 80자로 잘린 제목이 출력되는지 확인
- Why, What, How to Test 중 하나 이상의 섹션이 빠진 본문이 생성되었을 때 해당 섹션 이름이 포함된 WARN 메시지가 출력되는지 확인
- 모든 섹션이 포함된 정상적인 본문과 80자 이하의 제목이 입력될 경우 경고 없이 결과가 출력되는지 확인
```

### 변경 사항이 없을 때
```
$ python3 main.py commit
변경 사항이 없습니다.
```

## 5. 주의사항 (운영 관점)

### 민감정보 포함 가능성과 대응
`git diff`에는 API 키, 이메일 등 민감정보가 실수로 포함될 수 있습니다. `-safe-mode` 옵션을 사용하면 diff를 AI에 전송하기 전, 아래 패턴을 자동으로 마스킹합니다.
- API 키 형태의 문자열 (예: `sk-`로 시작하는 문자열)
- 이메일 주소

```bash
python3 main.py commit -safe-mode
```

민감한 코드를 다루는 저장소에서는 항상 `-safe-mode`를 함께 사용하는 것을 권장합니다.

### 비용/요청 횟수 제한
- `commit`, `pr` 명령은 각각 AI API를 **1회만 호출**합니다.
- 과도한 비용 발생을 막기 위해, 짧은 시간에 반복 실행하는 것은 지양해 주세요.

### 기타
- 이 도구는 커밋/PR **초안**을 생성할 뿐, `git commit`이나 GitHub PR을 자동으로 생성하지 않습니다. 생성된 텍스트는 반드시 검토 후 사용자가 직접 적용해야 합니다.
- 생성된 텍스트의 길이는 자동 검증됩니다 (커밋 제목 72자 이내, PR 제목 80자 이내, PR 본문 Why/What/How to Test 섹션 필수).