```csharp
public sealed class ProcessorTests
{
    [Fact]
    public void Process_ValidData_ReturnsSuccess()
    {
        // Arrange
        var processor = new Processor();
        var data = new InputData("123", 42);

        // Act
        var result = processor.Process(data);

        // Assert
        Assert.True(result.Success);
        Assert.Equal(42, result.Value);
    }

    [Fact]
    public void Process_EmptyId_ThrowsValidationException()
    {
        // Arrange
        var processor = new Processor();
        var data = new InputData("", 42);

        // Act & Assert
        Assert.Throws<ValidationException>(() => processor.Process(data));
    }

    [Fact]
    public void Process_NullData_ThrowsArgumentNullException()
    {
        // Arrange
        var processor = new Processor();

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => processor.Process(null!));
    }
}
```