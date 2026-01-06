### Mocking with Moq

**Prefer Moq** for injected dependencies. Avoid creating manual `MockXxx` or `FakeXxx` classes unless justified.

```csharp
// Preferred - Using Moq
private readonly Mock<IRepository> _repositoryMock = new();

[Fact]
public void GetItem_ValidId_CallsRepository()
{
    // Arrange
    _repositoryMock
        .Setup(x => x.Get(It.IsAny<string>()))
        .Returns(new Item { Id = "123", Name = "test" });

    var service = new Service(_repositoryMock.Object);

    // Act
    var result = service.GetItem("123");

    // Assert
    _repositoryMock.Verify(x => x.Get("123"), Times.Once);
    Assert.Equal("test", result.Name);
}

// Capturing arguments
[Fact]
public void Save_ValidData_PassesCorrectData()
{
    // Arrange
    Item? capturedItem = null;
    _repositoryMock
        .Setup(x => x.Save(It.IsAny<Item>()))
        .Callback<Item>(item => capturedItem = item);

    var service = new Service(_repositoryMock.Object);

    // Act
    service.Save(new Item { Name = "new" });

    // Assert
    Assert.NotNull(capturedItem);
    Assert.Equal("new", capturedItem.Name);
}

// Common Moq patterns
mock.Verify(x => x.Method(), Times.Once);
mock.SetupSequence(x => x.GetValue()).Returns(1).Returns(2);
mock.SetupGet(x => x.IsConnected).Returns(true);
```

**When a concrete Fake is acceptable:**
- Complex state to maintain between calls
- Domain-specific validation logic
- Mock setup exceeds 10 lines and becomes unreadable

Document the choice in a comment.