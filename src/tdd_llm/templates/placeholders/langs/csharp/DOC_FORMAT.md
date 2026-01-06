**If public APIs:**
- Verify all public types/methods have XML docs
- Add those that are missing

**XML doc format:**
```csharp
/// <summary>
/// Process the input data and return result.
/// </summary>
/// <param name="data">Input data containing ID and value.</param>
/// <param name="cancellationToken">Cancellation token.</param>
/// <returns>Result with success status and processed value.</returns>
/// <exception cref="ValidationException">If data is missing required fields.</exception>
public async Task<Result> ProcessAsync(InputData data, CancellationToken cancellationToken = default)
```