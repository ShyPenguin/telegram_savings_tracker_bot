import re

def extract_google_doc_id(url: str) -> str:
    """
    Extract Google Document ID from a URL.
    
    Args:
        url: Google Docs URL string
        
    Returns:
        The extracted document ID
        
    Raises:
        ValueError: If no valid document ID can be extracted from the URL
    """
    patterns = [
        r'/d/([a-zA-Z0-9_-]{10,})',  # Standard docs URL
        r'id=([a-zA-Z0-9_-]{10,})',   # Alternative format
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match and match.group(1):
            return match.group(1)
    
    raise ValueError("Invalid Google Docs URL. Could not extract document ID.")