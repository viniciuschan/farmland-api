from abc import ABC, abstractmethod

from validate_docbr import CNPJ, CPF

from src.exceptions import InvalidDocumentTypeError


class DocumentValidatorInterface(ABC):
    @abstractmethod
    def validate(self, document_value: str) -> bool:
        pass


class CPFValidator(DocumentValidatorInterface):
    def validate(self, document_value: str) -> bool:
        return CPF().validate(document_value)


class CNPJValidator(DocumentValidatorInterface):
    def validate(self, document_value: str) -> bool:
        return CNPJ().validate(document_value)


class DocumentValidator:
    def __init__(self, document_type: str):
        self.validator = self.get_validator(document_type)

    def get_validator(self, document_type: str) -> DocumentValidatorInterface:
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

    def clean_punctuations(self, value: str) -> str:
        return value.replace(".", "").replace("-", "").replace("/", "").strip()


class FarmValidator:
    def __init__(self, farm_data: dict):
        self.farm_data = farm_data

    def validate_areas(self) -> bool:
        total_area = self.farm_data["total_area_hectares"]
        cultivable_area = self.farm_data["cultivable_area_hectares"]
        vegetation_area = self.farm_data["vegetation_area_hectares"]
        return all(
            [
                total_area > 0,
                cultivable_area >= 0,
                vegetation_area >= 0,
                (cultivable_area + vegetation_area) <= total_area,
            ]
        )
