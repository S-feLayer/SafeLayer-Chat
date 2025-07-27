from .redact_per_pdf import redact_pdf
from .redact_text import redact_text
from .redact_code import redact_code_file
from .redact_content import redact_content, get_supported_formats

try:
    import importlib.metadata
    __version__ = importlib.metadata.version("secureai")
except ImportError:
    __version__ = "unknown"

__all__ = [
    "redact_pdf",
    "redact_text", 
    "redact_code_file",
    "redact_content",
    "get_supported_formats"
]
