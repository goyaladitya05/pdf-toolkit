class PdfOperationError(Exception):
    """Base class for recoverable, user-facing PDF errors."""


class InvalidPdfError(PdfOperationError):
    """File could not be parsed as a PDF."""


class WrongPasswordError(PdfOperationError):
    """The supplied password did not unlock the PDF."""


class AlreadyEncryptedError(PdfOperationError):
    """The PDF is already encrypted and must be decrypted first."""
