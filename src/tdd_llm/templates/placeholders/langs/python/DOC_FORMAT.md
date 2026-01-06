**If public APIs:**
- Verify all public types/functions have docstrings
- Add those that are missing

**Docstring format (Google style):**
```python
def process(data: dict, timeout: int = 30) -> Result:
    """Process the input data and return result.

    Args:
        data: Dictionary containing 'id' and 'value' keys.
        timeout: Maximum processing time in seconds.

    Returns:
        Result object with success status and processed value.

    Raises:
        ValidationError: If data is missing required fields.
        TimeoutError: If processing exceeds timeout.
    """
```