### Mocking with unittest.mock

**Prefer unittest.mock** for injected dependencies. Avoid creating manual `MockXxx` or `FakeXxx` classes unless justified.

```python
from unittest.mock import Mock, patch, MagicMock

# Preferred - Using Mock
@pytest.fixture
def mock_repository():
    repo = Mock()
    repo.get.return_value = {"id": "123", "name": "test"}
    return repo

def test_service_calls_repository(mock_repository):
    # Arrange
    service = Service(repository=mock_repository)

    # Act
    result = service.get_item("123")

    # Assert
    mock_repository.get.assert_called_once_with("123")
    assert result["name"] == "test"

# Capturing arguments
def test_service_saves_with_correct_data():
    repo = Mock()
    service = Service(repository=repo)

    service.save({"name": "new"})

    repo.save.assert_called_once()
    saved_data = repo.save.call_args[0][0]
    assert saved_data["name"] == "new"

# Patching module-level functions
@patch("mymodule.external_api.fetch")
def test_with_patched_api(mock_fetch):
    mock_fetch.return_value = {"status": "ok"}
    result = my_function()
    assert result["status"] == "ok"
```

**When a concrete Fake is acceptable:**
- Complex state to maintain between calls
- Domain-specific validation logic
- Mock setup exceeds 10 lines and becomes unreadable

Document the choice in a comment.