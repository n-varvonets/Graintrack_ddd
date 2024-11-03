from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self):
        return "Application error occurred"


@dataclass(eq=False)
class BusinessRuleViolationException(ApplicationException):
    detail: str

    @property
    def message(self):
        return f"Business rule violation: {self.detail}"
