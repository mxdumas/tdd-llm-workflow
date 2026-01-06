```python
import pytest
from unittest.mock import Mock, patch

class TestProcessor:
    """Tests for Processor class."""

    def test_process_valid_data_returns_success(self):
        """Happy path: valid input returns expected output."""
        # Arrange
        processor = Processor()
        data = {"id": "123", "value": 42}

        # Act
        result = processor.process(data)

        # Assert
        assert result.success is True
        assert result.value == 42

    def test_process_empty_id_raises_validation_error(self):
        """Edge case: empty ID raises error."""
        # Arrange
        processor = Processor()
        data = {"id": "", "value": 42}

        # Act & Assert
        with pytest.raises(ValidationError):
            processor.process(data)

    def test_process_none_data_raises_type_error(self):
        """Error case: None input raises TypeError."""
        # Arrange
        processor = Processor()

        # Act & Assert
        with pytest.raises(TypeError):
            processor.process(None)
```