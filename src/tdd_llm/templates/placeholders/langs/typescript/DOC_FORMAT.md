**If public APIs:**
- Verify all public types/functions have JSDoc comments
- Add those that are missing

**JSDoc format:**
```typescript
/**
 * Process the input data and return result.
 *
 * @param data - Input data containing ID and value.
 * @param options - Optional processing options.
 * @returns Result with success status and processed value.
 * @throws {ValidationError} If data is missing required fields.
 *
 * @example
 * const result = processor.process({ id: '123', value: 42 });
 * console.log(result.success); // true
 */
export function process(data: InputData, options?: ProcessOptions): Result {
```