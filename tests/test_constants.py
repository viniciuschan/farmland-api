from src.constants import BrazilianState, CultivationType, DocumentType


def test_document_type_items():
    expected_result = [
        "CNPJ",
        "CPF",
    ]
    assert list(item.name for item in DocumentType) == expected_result


def test_cultivation_type_items():
    expected_result = [
        "COFFEE",
        "CORN",
        "COTTON",
        "SOY",
        "SUGAR_CANE",
    ]
    assert list(item.name for item in CultivationType) == expected_result


def test_brazilian_state_items():
    expected_result = [
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
    ]
    assert list(item.name for item in BrazilianState) == expected_result
