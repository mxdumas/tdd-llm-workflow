### Mocking with Jest

**Prefer Jest mocks** for dependencies. Avoid creating manual mock classes unless justified.

```typescript
// Preferred - Using Jest mocks
const mockRepository = {
  get: jest.fn(),
  save: jest.fn(),
};

describe('Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should call repository with correct id', () => {
    // Arrange
    mockRepository.get.mockReturnValue({ id: '123', name: 'test' });
    const service = new Service(mockRepository as any);

    // Act
    const result = service.getItem('123');

    // Assert
    expect(mockRepository.get).toHaveBeenCalledWith('123');
    expect(result.name).toBe('test');
  });

  it('should pass correct data to save', () => {
    // Arrange
    const service = new Service(mockRepository as any);

    // Act
    service.save({ name: 'new' });

    // Assert
    expect(mockRepository.save).toHaveBeenCalledWith(
      expect.objectContaining({ name: 'new' })
    );
  });
});

// Mocking modules
jest.mock('./api', () => ({
  fetchData: jest.fn().mockResolvedValue({ status: 'ok' }),
}));

// Async mocks
mockRepository.get.mockResolvedValue({ id: '123' });
mockRepository.get.mockRejectedValue(new Error('Not found'));
```

**When a concrete Fake is acceptable:**
- Complex state to maintain between calls
- Domain-specific validation logic
- Mock setup exceeds 10 lines and becomes unreadable

Document the choice in a comment.