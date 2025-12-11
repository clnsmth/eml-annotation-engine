import os
import pytest
from unittest.mock import patch, MagicMock
from webapp.run import send_email_notification, ProposalRequest, TermDetails, SubmitterInfo
from webapp.config import Config

@pytest.fixture
def proposal_request():
    return ProposalRequest(
        target_vocabulary="TestVocab",
        term_details=TermDetails(
            label="TestLabel",
            description="TestDescription",
            evidence_source="TestSource"
        ),
        submitter_info=SubmitterInfo(
            email="test@example.com",
            orcid_id="0000-0000-0000-0000",
            attribution_consent=True
        )
    )

def test_send_email_notification_success(monkeypatch, proposal_request):
    monkeypatch.setenv("PROPOSAL_RECIPIENT_EMAIL", Config.VOCABULARY_PROPOSAL_RECIPIENT)
    monkeypatch.setenv("SMTP_USER", "user@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "password")

    mock_smtp = MagicMock()
    monkeypatch.setattr("smtplib.SMTP", lambda *args, **kwargs: mock_smtp)

    send_email_notification(proposal_request)
    assert mock_smtp.starttls.called
    assert mock_smtp.login.called
    assert mock_smtp.sendmail.called
    assert mock_smtp.quit.called

# def test_send_email_notification_missing_recipient(monkeypatch, proposal_request, capsys):
#     monkeypatch.delenv("PROPOSAL_RECIPIENT_EMAIL", raising=False)
#     monkeypatch.setenv("SMTP_USER", "user@example.com")
#     monkeypatch.setenv("SMTP_PASSWORD", "password")
#     send_email_notification(proposal_request)
#     captured = capsys.readouterr()
#     assert "PROPOSAL_RECIPIENT_EMAIL not set" in captured.out
#     assert "Payload received" in captured.out

# def test_send_email_notification_missing_credentials(monkeypatch, proposal_request, capsys):
#     monkeypatch.setenv("PROPOSAL_RECIPIENT_EMAIL", Config.VOCABULARY_PROPOSAL_RECIPIENT)
#     monkeypatch.delenv("SMTP_USER", raising=False)
#     monkeypatch.delenv("SMTP_PASSWORD", raising=False)
#     send_email_notification(proposal_request)
#     captured = capsys.readouterr()
#     assert "SMTP credentials not set" in captured.out

def test_send_email_notification_exception(monkeypatch, proposal_request, capsys):
    monkeypatch.setenv("PROPOSAL_RECIPIENT_EMAIL", Config.VOCABULARY_PROPOSAL_RECIPIENT)
    monkeypatch.setenv("SMTP_USER", "user@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "password")
    class FailingSMTP:
        def starttls(self): pass
        def login(self, u, p): pass
        def sendmail(self, u, r, t): raise Exception("SMTP error")
        def quit(self): pass
    monkeypatch.setattr("smtplib.SMTP", lambda *args, **kwargs: FailingSMTP())
    send_email_notification(proposal_request)
    captured = capsys.readouterr()
    assert "Failed to send email" in captured.out

# if __name__ == "__main__":
#     from webapp.config import Config
#     from webapp.run import ProposalRequest, TermDetails, SubmitterInfo, send_email_notification
#     import sys
#     print("Running live email notification test...")
#     proposal = ProposalRequest(
#         target_vocabulary="TestVocab",
#         term_details=TermDetails(
#             label="LiveTestLabel",
#             description="Live test of email notification system.",
#             evidence_source="UnitTest"
#         ),
#         submitter_info=SubmitterInfo(
#             email=Config.VOCABULARY_PROPOSAL_RECIPIENT,
#             orcid_id="0000-0000-0000-0000",
#             attribution_consent=True
#         )
#     )
#     send_email_notification(proposal)
#     print("Live email notification test completed.")
