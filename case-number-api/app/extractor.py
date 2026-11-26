import re
from email import policy
from email.parser import BytesParser

CASE_NUMBER_PATTERNS = (
    # Korean patent/application number: 10-2024-0012345
    re.compile(r"(?<!\d)\d{2}-\d{4}-\d{7}(?!\d)"),
    # US serial number: 18/300,230
    re.compile(r"(?<!\d)\d{2}/\d{3},\d{3}(?!\d)"),
    # Your Ref. No.: OPB2020-004US-CON
    re.compile(r"(?<![A-Z0-9])[A-Z]{2,}\d{4}-\d{3,}[A-Z]{2,}(?:-[A-Z0-9]+)*(?![A-Z0-9])", re.IGNORECASE),
    # Our Ref. No.: NVA0010USC
    re.compile(r"(?<![A-Z0-9])[A-Z]{2,}\d{4}[A-Z]{2,}(?![A-Z0-9])", re.IGNORECASE),
)

def extract_subject(eml_bytes: bytes) -> str:
    if not eml_bytes:
        raise ValueError("EML file is empty")
    message = BytesParser(policy=policy.default).parsebytes(eml_bytes)
    return str(message.get("Subject", "")).strip()

def extract_case_numbers(subject: str) -> list[str]:
    if not subject:
        return []

    matches: list[tuple[int, str]] = []
    for pattern in CASE_NUMBER_PATTERNS:
        matches.extend((match.start(), match.group(0)) for match in pattern.finditer(subject))

    matches.sort(key=lambda item: item[0])
    return list(dict.fromkeys(value for _, value in matches))
