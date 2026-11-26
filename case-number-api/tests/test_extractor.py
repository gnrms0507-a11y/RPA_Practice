import unittest
from app.extractor import extract_case_numbers, extract_subject

class ExtractorTests(unittest.TestCase):
    def test_extracts_case_number(self) -> None:
        self.assertEqual(extract_case_numbers("사건번호 10-2024-0012345 통지서"), ["10-2024-0012345"])

    def test_extracts_unique_numbers(self) -> None:
        subject = "10-2024-0012345 / 20-2025-7654321 / 10-2024-0012345"
        self.assertEqual(extract_case_numbers(subject), ["10-2024-0012345", "20-2025-7654321"])

    def test_extracts_foreign_serial_and_reference_numbers(self) -> None:
        subject = (
            "Kind Reminder: INQUIRY - Serial No. 18/300,230; "
            "Your Ref. No.: OPB2020-004US-CON; Our Ref. No.: NVA0010USC"
        )
        self.assertEqual(
            extract_case_numbers(subject),
            ["18/300,230", "OPB2020-004US-CON", "NVA0010USC"],
        )

    def test_rejects_embedded_number(self) -> None:
        self.assertEqual(extract_case_numbers("110-2024-00123450"), [])

    def test_decodes_encoded_subject(self) -> None:
        eml = (b"From: sender@example.com\r\nTo: receiver@example.com\r\n"
               b"Subject: =?utf-8?b?W+2Kue2XiF0g7IKs6rG067KI7Zi4IDEwLTIwMjQtMDAxMjM0NQ==?=\r\n\r\nBody")
        self.assertEqual(extract_subject(eml), "[특허] 사건번호 10-2024-0012345")

if __name__ == "__main__":
    unittest.main()
