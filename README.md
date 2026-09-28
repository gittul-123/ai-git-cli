# AI 기반 Git 커밋/PR 메시지 자동 생성기

Git 변경 사항(`git status`, `git diff`)을 수집해 AI가 커밋 메시지와 Pull Request 초안을 자동으로 작성해주는 터미널(CLI) 도구입니다. 웹 화면 없이 터미널에서만 실행됩니다.

- 개발 환경: Python 3.10 이상
- 외부 패키지: `requests`

## 1. 설치 및 실행 방법

```bash
# 1) 저장소 클론
git clone https://github.com/gittul-123/ai-git-cli.git
cd ai-git-cli

# 2) 필요한 패키지 설치
pip install requests

# 3) 환경변수(API Key) 설정 (아래 2번 항목 참고)

# 4) 실행 (Git이 초기화된 프로젝트 루트에서 실행해야 합니다)
python3 main.py commit
```

> 실행 명령의 Python 이름은 환경마다 다릅니다. macOS는 `python3`, Windows는 `python`을 사용합니다. 이 문서의 예시는 `python3` 기준입니다.

> `commit` 또는 `pr` 중 하나를 반드시 지정해야 합니다. 명령 없이 `python3 main.py`만 실행하면 오류가 납니다.

## 2. 환경변수(API Key) 설정 방법

AI API Key는 코드에 직접 작성하지 않고, 환경변수 `AI_API_KEY`로만 관리합니다.

**macOS / Linux (현재 터미널 세션에서만 유효)**
```bash
export AI_API_KEY="발급받은_API_키"
echo $AI_API_KEY        # 설정 확인
```

**macOS / Linux (영구 설정)**: `~/.zshrc` (또는 `~/.bashrc`) 맨 아래에 위 `export` 줄을 추가한 뒤 `source ~/.zshrc`를 실행합니다.

**Windows 명령 프롬프트(cmd)**
```cmd
set AI_API_KEY=발급받은_API_키
echo %AI_API_KEY%
```
cmd에서는 따옴표를 쓰지 않고, `=` 앞뒤에 공백을 두지 않습니다.

**Windows PowerShell**
```powershell
$env:AI_API_KEY="발급받은_API_키"
echo $env:AI_API_KEY
```

세 방법 모두 **설정한 터미널 창에서만** 유효합니다. 창을 닫으면 사라지므로 새 창에서는 다시 설정해야 합니다.

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
| `-temperature` | 생성 결과의 창의성 정도 (0에 가까울수록 일관적, 1에 가까울수록 다양) | `0.7` |
| `-max-tokens` | 응답 최대 길이(토큰 수). 상한선이며 너무 작으면 답변이 잘릴 수 있음 | `1024` |
| `-safe-mode` | diff 안의 민감정보(API 키, 이메일)를 마스킹한 뒤 AI에 전송 | 꺼짐 |

```bash
python3 main.py commit -temperature 0.3 -safe-mode
python3 main.py pr -model claude-sonnet-4 -max-tokens 1500
```

옵션은 `commit` / `pr` 뒤에 붙입니다. 옵션 이름은 하이픈 **한 개**(`-model`)입니다.

## 4. 출력 예시

### 커밋 메시지 생성
```
$ python3 main.py commit
[INFO] Git status 수집 완료: 2개 파일 변경 감지
--- 결과 ---
[주의] 아래 내용은 AI가 생성한 초안입니다. 검토 후 적용해주세요.
git status를 --short 옵션으로 변경하고 변경 파일 수 출력 추가

git status 명령에 --short 옵션을 적용해 출력을 간결하게 만들고,
main.py에서 status 결과를 파싱해 변경된 파일 수를 콘솔에 출력하도록 했다.
이를 통해 실행 시 몇 개의 파일이 변경됐는지 사용자가 바로 확인할 수 있다.
-----------
```

### PR 제목/본문 생성
```
$ python3 main.py pr
[INFO] Git status 수집 완료: 2개 파일 변경 감지
--- 결과 ---
[주의] 아래 내용은 AI가 생성한 초안입니다. 검토 후 적용해주세요.
PR 본문 섹션 누락 시 AI 재요청 및 validate_pr_body 파싱 로직 개선

Why
- 기존 validate_pr_body는 문자열 find() 기반으로 섹션 경계를 계산해 헤더 이름이 본문 내용에 포함될 경우 잘못된 범위를 참조하는 버그가 있었음
- 섹션이 누락된 채로 PR 본문이 생성되어도 재시도 없이 그대로 출력되어 품질이 일관되지 않았음
- 불릿 자동 추가 로직이 section_text 기준으로 동작해 원본 body에 반영이 불안정했음

What
- validators.py의 validate_pr_body를 줄 단위 파싱 방식으로 전면 재작성하여 헤더 감지와 섹션 범위 계산의 정확도를 높임
- 불릿 자동 추가 시 lines 리스트를 직접 수정한 뒤 join하는 방식으로 변경해 원본 반영 신뢰성을 확보함
- find_missing_pr_sections 함수를 신규 추가하여 Why, What, How to Test 세 섹션의 누락 여부를 반환하도록 함
- main.py의 pr 커맨드 실행 흐름에 누락 섹션 감지 후 1회 AI 재요청 로직을 추가함

How to Test
- 세 섹션이 모두 포함된 정상 응답에서는 재요청이 발생하지 않고 generate_text 호출이 1회에 그치는지 확인함
- 섹션 내 불릿이 없는 경우 [WARN] 메시지 출력 후 첫 번째 내용 줄에 "- "가 자동으로 붙는지 결과 문자열을 출력해 확인함
- 섹션 내용이 아예 없는 경우 내용이 없다는 [WARN] 메시지가 출력되고 크래시 없이 정상 종료되는지 확인함
-----------
```

### 변경 사항이 없을 때
```
$ python3 main.py commit
[INFO] Git status 수집 완료: 0개 파일 변경 감지
변경 사항이 없습니다.
```

### 오류 예시

API Key를 설정하지 않은 경우:
```
[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.
AI 응답 생성에 실패했습니다.
```

API Key가 잘못된 경우 (인증 실패. 상태 코드와 서버가 알려준 원인이 함께 출력됨):
```
[ERROR] API 호출 실패 (상태 코드 : 401): {"type":"error","error":{"type":"authentication_error","message":"Authentication is required.", ...}}
AI 응답 생성에 실패했습니다.
```

## 5. 동작 방식과 검증 규칙

1. `git status --short`로 변경된 파일 수를 확인하고, `git diff`로 변경 내용을 수집합니다. 변경 내용이 없으면 안내 메시지를 출력하고 종료합니다.
2. (`-safe-mode`일 때) 민감정보를 마스킹합니다.
3. 변경 내용을 프롬프트에 담아 AI API를 호출합니다.
4. 응답을 제목과 본문으로 나눈 뒤, 아래 규칙으로 검증하고 다듬습니다 (재생성 또는 후처리).

| 대상 | 규칙 | 규칙을 어겼을 때 |
|---|---|---|
| 커밋 제목 | 50자 이내 권장, 최대 72자 | 50자 초과는 경고, 72자 초과는 잘라냄 |
| 커밋 본문 | `.py` 파일명 언급 또는 불릿이 1개 이상 | 둘 다 없으면 `git diff --name-only`로 얻은 실제 변경 파일 목록을 본문 끝에 추가 |
| PR 제목 | 최대 80자 | 잘라냄 |
| PR 본문 | Why / What / How to Test 섹션 헤더 필수 | 누락 시 빠진 섹션을 명시해 AI에 **1회 재요청** |
| PR 본문 | 각 섹션에 불릿 1개 이상 | 불릿이 없으면 첫 내용 줄 앞에 `- `를 붙임 |

## 6. 오류 처리

| 상황 | 동작 |
|---|---|
| `AI_API_KEY` 환경변수 없음 | 오류 메시지 출력 후 종료 |
| 네트워크 오류 | 오류 원인을 포함한 메시지 출력 후 종료 |
| 서버가 200이 아닌 응답 (예: 인증 실패 401) | 상태 코드와 서버가 알려준 원인을 출력 후 종료 |
| 응답 형식이 예상과 다름 | 오류 메시지 출력 후 종료 |

## 7. 주의사항 (운영 관점)

### 민감정보 포함 가능성과 대응
`git diff`에는 API 키, 이메일 등 민감정보가 실수로 포함될 수 있습니다. `-safe-mode`를 사용하면 diff를 AI에 전송하기 전에 아래 패턴을 `****`로 마스킹합니다.
- API 키 형태의 문자열 (`sk-`로 시작하는 문자열)
- 이메일 주소

```bash
python3 main.py commit -safe-mode
```

민감한 코드를 다루는 저장소에서는 `-safe-mode` 사용을 권장합니다. 다만 규칙에 걸리지 않는 형태의 민감정보는 가려지지 않을 수 있고, 반대로 비슷하게 생긴 일반 문자열이 가려질 수도 있습니다.

### 비용/요청 횟수 제한
- `commit` 명령은 AI API를 **1회**만 호출합니다.
- `pr` 명령도 기본은 1회 호출입니다. 응답에서 Why / What / How to Test 헤더가 빠진 경우에만 1회 재요청하므로 **최대 2회**입니다. 재요청 시 화면에 `[INFO]` 안내가 출력됩니다.
- 그래도 헤더가 빠지면 추가 호출 없이 경고만 출력합니다. 호출이 무한히 늘어나는 것을 막기 위한 설계입니다.
- 짧은 시간에 반복 실행하는 것은 지양해 주세요.

### Git 연동 범위
- 변경 사항 수집은 `git status`, `git diff` 범위로만 수행합니다. (`--short`, `--name-only` 옵션 사용)
- `git diff`는 **아직 `git add`하지 않은 변경**만 보여줍니다. `git add`로 stage하면 diff가 비어서 "변경 사항이 없습니다"가 출력될 수 있습니다. 새로 만든 파일(untracked)도 diff에는 나타나지 않습니다.
- 이 도구는 커밋/PR **초안**을 출력할 뿐, `git commit`, `git push`, GitHub PR 생성은 하지 않습니다.

### 한계
- AI는 지시를 항상 따르지 않으므로, 결과는 반드시 검토 후 사용자가 직접 적용해야 합니다.
- 커밋 본문의 "파일 언급" 판별은 `.py` 파일명만 인식합니다.
- 재요청으로 추가된 PR 섹션은 본문 끝에 붙으므로 섹션 순서가 표준과 다를 수 있습니다.
