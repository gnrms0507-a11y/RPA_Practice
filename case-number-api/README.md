# EML Case Number API

메일 제목에서 다음 형식의 사건번호와 참조번호를 추출하는 독립 FastAPI 서비스입니다.


해상도 1920* 1080 / 배율 100% 기준에서 실행 - 이지팻 이미지 클릭


- `10-2024-0012345`
- `18/300,230`
- `OPB2020-004US-CON`
- `NVA0010USC`

## 설치 및 실행

```powershell
cd case-number-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Swagger는 `http://localhost:8000/docs`, 상태 확인은 `http://localhost:8000/health`입니다.

## EML 파일 호출

```powershell
$form = @{ file = Get-Item "C:\mail\sample.eml" }
Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8000/api/emails/extract-case-number" `
  -Form $form
```

응답 예시:

```json
{
  "success": true,
  "subject": "[특허] 사건번호 10-2024-0012345 통지서",
  "caseNumber": "10-2024-0012345",
  "caseNumbers": ["10-2024-0012345"]
}
```

제목만 테스트하려면 `POST /api/subjects/extract-case-number`에 아래 JSON을 보냅니다.

```json
{"subject":"[특허] 사건번호 10-2024-0012345 통지서"}
```

## 테스트

```powershell
python -m unittest discover -s tests -v
```

## UiPath 설정

- HTTP Request Method: `POST`
- Endpoint: `http://API서버:8000/api/emails/extract-case-number`
- Body: `multipart/form-data`
- 파일 필드 이름: `file`
- JSON 응답에서 사용할 속성: `caseNumber`

운영 환경에서는 HTTPS와 API Key 또는 JWT 인증을 추가하세요.
