from abc import ABC, abstractmethod

from validate_docbr import CNPJ, CPF

from src.exceptions import InvalidDocumentTypeError


class DocumentValidator(ABC):
    @abstractmethod
    def validate(self, document_value: str) -> bool:
        pass


class CPFValidator(DocumentValidator):
    def validate(self, document_value: str) -> bool:
        return CPF().validate(document_value)


class CNPJValidator(DocumentValidator):
    def validate(self, document_value: str) -> bool:
        return CNPJ().validate(document_value)


class DocumentValidator:
    def __init__(self, document_type: str):
        self.validator = self.get_validator(document_type)

    def get_validator(self, document_type: str) -> DocumentValidator:
        validators = {
            "CPF": CPFValidator(),
            "CNPJ": CNPJValidator(),
        }

        try:
            return validators[document_type]
        except KeyError:
            raise InvalidDocumentTypeError()

    def validate(self, document_value: str) -> bool:
        return self.validator.validate(document_value)
