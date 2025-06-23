"""Wikipedia service exceptions and error handling."""

from typing import Any


class WikipediaServiceError(Exception):
    """Base exception for Wikipedia service errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        self.details = details or {}
        super().__init__(message)

    def __str__(self) -> str:
        if self.details:
            return f"{super().__str__()} | Details: {self.details}"
        return super().__str__()


class WikipediaAPITimeoutError(WikipediaServiceError):
    """Raised when the Wikipedia API request times out."""

    def __init__(self, timeout: float, url: str | None = None):
        message = f"Request timed out after {timeout} seconds"
        if url:
            message += f" while calling {url}"
        super().__init__(message, {"timeout": timeout, "url": url})


class WikipediaAPIError(WikipediaServiceError):
    """Raised when the Wikipedia API returns an error."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: dict | None = None,
        url: str | None = None,
        method: str = "GET",
    ):
        self.status_code = status_code
        self.response = response
        self.url = url
        self.method = method

        details = {
            "status_code": status_code,
            "url": url,
            "method": method,
            "response": response,
        }
        super().__init__(f"Wikipedia API error: {message}", details)


class WikipediaRateLimitError(WikipediaAPIError):
    """Raised when rate limited by the Wikipedia API."""

    def __init__(self, retry_after: int, **kwargs):
        message = f"Rate limited. Please retry after {retry_after} seconds"
        super().__init__(message, status_code=429, **kwargs)
        self.retry_after = retry_after


class WikipediaValidationError(WikipediaServiceError):
    """Raised when data validation fails."""

    def __init__(self, message: str, field: str | None = None, value: Any = None):
        details = {"field": field, "value": value} if field is not None else {}
        super().__init__(f"Validation error: {message}", details)
        self.field = field
        self.value = value
