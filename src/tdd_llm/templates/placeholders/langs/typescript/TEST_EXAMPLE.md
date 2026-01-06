```typescript
describe('Processor', () => {
  describe('process', () => {
    it('should return success for valid data', () => {
      // Arrange
      const processor = new Processor();
      const data = { id: '123', value: 42 };

      // Act
      const result = processor.process(data);

      // Assert
      expect(result.success).toBe(true);
      expect(result.value).toBe(42);
    });

    it('should throw ValidationError for empty id', () => {
      // Arrange
      const processor = new Processor();
      const data = { id: '', value: 42 };

      // Act & Assert
      expect(() => processor.process(data)).toThrow(ValidationError);
    });

    it('should throw TypeError for null data', () => {
      // Arrange
      const processor = new Processor();

      // Act & Assert
      expect(() => processor.process(null as any)).toThrow(TypeError);
    });
  });
});
```