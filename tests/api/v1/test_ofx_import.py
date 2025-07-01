import pytest
from ninja.testing import TestClient
from backend.api.v1.routers.ofx_import import router
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


@pytest.fixture
def client():
    return TestClient(router)


def test_import_ofx_success(client):
    # Create a mock OFX file
    ofx_content = b"""
    OFXHEADER:100
    DATA:OFXSGML
    VERSION:102
    SECURITY:NONE
    ENCODING:USASCII
    CHARSET:1252
    COMPRESSION:NONE
    OLDFILEUID:NONE
    NEWFILEUID:NONE

    <OFX>
        <SIGNONMSGSRSV1>
            <SONRS>
                <STATUS>
                    <CODE>0</CODE>
                    <SEVERITY>INFO</SEVERITY>
                </STATUS>
                <DTSERVER>20240101120000</DTSERVER>
                <LANGUAGE>POR</LANGUAGE>
            </SONRS>
        </SIGNONMSGSRSV1>
        <BANKMSGSRSV1>
            <STMTTRNRS>
                <TRNUID>1</TRNUID>
                <STATUS>
                    <CODE>0</CODE>
                    <SEVERITY>INFO</SEVERITY>
                </STATUS>
                <STMTRS>
                    <CURDEF>BRL</CURDEF>
                    <BANKACCTFROM>
                        <BANKID>123</BANKID>
                        <ACCTID>456</ACCTID>
                        <ACCTTYPE>CHECKING</ACCTTYPE>
                    </BANKACCTFROM>
                    <BANKTRANLIST>
                        <DTSTART>20240101120000</DTSTART>
                        <DTEND>20240101120000</DTEND>
                        <STMTTRN>
                            <TRNTYPE>DEBIT</TRNTYPE>
                            <DTPOSTED>20240101120000</DTPOSTED>
                            <TRNAMT>-100.00</TRNAMT>
                            <FITID>12345</FITID>
                            <MEMO>Test Transaction</MEMO>
                        </STMTTRN>
                    </BANKTRANLIST>
                </STMTRS>
            </STMTTRNRS>
        </BANKMSGSRSV1>
    </OFX>
    """
    uploaded_file = SimpleUploadedFile(
        "test.ofx", ofx_content, content_type="application/octet-stream"
    )

    with patch("backend.api.v1.routers.ofx_import.ofx_reader") as mock_ofx_reader:
        mock_ofx_reader.return_value = [{"transaction": "data"}]
        response = client.post("/ofx", FILES={"file": uploaded_file})

    assert response.status_code == 200
    assert response.json() == [{"transaction": "data"}]
    mock_ofx_reader.assert_called_once()


def test_import_ofx_invalid_file(client):
    # Create a mock invalid file
    invalid_content = b"this is not an ofx file"
    uploaded_file = SimpleUploadedFile(
        "test.txt", invalid_content, content_type="text/plain"
    )

    with patch("backend.api.v1.routers.ofx_import.ofx_reader") as mock_ofx_reader:
        mock_ofx_reader.side_effect = ValueError("Invalid OFX file")
        with pytest.raises(ValueError):
            client.post("/ofx", FILES={"file": uploaded_file})
