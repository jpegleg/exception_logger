![cdlogo](https://carefuldata.com/images/cdlogo.png)

# Exception Logger

Rather than needing to remember all of the exception types or do "catch all" exceptions, and rather than having to reimplement logging formats constantly,
this module provides consistent and comprehensive logging and error handing approach.

## Features

- **Decorator-based exception handling**: Simply add `@exception_handler` to any function
- **Comprehensive coverage**: Handles all standard Python built-in exceptions
- **Structured logging**: ISO timestamps, UUIDs, function names, and error details
- **Exception correlation**: Track related errors across multiple function calls with shared UUIDs
- **Automatic re-raising**: Logs exceptions and re-raises them for proper error propagation
- **Manual logging support**: For legacy code that can't use decorators

## Log Format

Each logged exception follows this structure:

```
ISO-8601-Timestamp - UUIDv4 - function_name - [logged args: key1: value1, key2: value2 - ]ERROR: ExceptionType: message (Line: line_number)
```

Example without logged arguments:
```
2026-02-08T05:55:31.756539+00:00 - ef4bd3f2-4333-4349-b10e-e16dc7b7e7f4 - process_data - ERROR: KeyError: 'required_field' (Line: 42)
```

Example with logged arguments:
```
2026-02-08T07:13:50.984493+00:00 - d0149a36-a774-4728-b9a6-fb01c2092596 - process_api_request - logged args: ip_address: 192.168.1.100, request_id: req_abc123, user_id: 12345 - ERROR: KeyError: 'required_field' (Line: 95)
```

## Installation

Install with pip or uv:

```
uv add exception_logger
```

## Basic Usage

### Using the Decorator

```python
from exception_logger import exception_handler

@exception_handler
def risky_operation(data):
    # Your code here
    return data['key']  # May raise KeyError
```

The decorator automatically:
- Accepts a UUID for logging or generates one if none is passed
- Detects the function name and logs it
- Logs any exception with full details
- Adds specified custom args to log lines
- Re-raises the exception

### Custom Exception ID and Function Name

Pass custom values for correlation across multiple operations:

```python
@exception_handler
def database_query(query, exception_id=None, func_name=None):
    # Your code here
    pass

# Call with custom tracking
transaction_id = str(uuid.uuid4())
database_query("SELECT * FROM users", exception_id=transaction_id)
```

### Contextual Logging with `log_this_*` Arguments

Automatically include important context in error logs by using `log_this_*` prefixed arguments. These are automatically extracted, logged, and removed before your function executes:

```python
@exception_handler
def process_payment(
    amount,
    user_id,
    exception_id=None,
    func_name=None,
    log_this_user_id=None,
    log_this_transaction_id=None,
    log_this_amount=None,
    log_this_currency=None
):
    # Your business logic here
    if amount > 10000:
        raise ValueError("Amount exceeds limit")
    return process_charge(amount)

# Call with context
process_payment(
    amount=5000,
    user_id=12345,
    log_this_user_id=12345,
    log_this_transaction_id="txn_abc123",
    log_this_amount=5000,
    log_this_currency="USD"
)
```

If an exception occurs, the log will include:
```
2026-02-08T07:13:50.984742+00:00 - 15babb32-2b96-430a-8914-c7b15d2b955a - process_payment - logged args: amount: 5000, currency: USD, transaction_id: txn_abc123, user_id: 12345 - ERROR: ValueError: Amount exceeds limit (Line: 42)
```

**Benefits:**
- Automatically includes relevant context without manual string formatting
- Self-documenting - function signature shows what gets logged
- Searchable logs - easily find errors by user_id, transaction_id, etc.
- Clean code - no log message construction cluttering your business logic
- Type-safe - works with IDE autocomplete

### Manual Exception Handling

For legacy code or special cases, you can manually log exceptions with context:

```python
from exception_logger import handle_exception
import uuid

def legacy_function(user_id, transaction_id):
    operation_id = str(uuid.uuid4())
    try:
        # Risky operation
        result = some_operation()
    except Exception:
        handle_exception(
            exception_id=operation_id,
            func_name="legacy_function",
            user_id=user_id,
            transaction_id=transaction_id,
            operation="payment_processing"
        )
        raise
```

Note: When using `handle_exception()`, you can pass any keyword arguments as context (not just `log_this_*` prefixed ones).

## Advanced Usage

### Correlated Exception Tracking

Track multiple related operations with a shared UUID:

```python
@exception_handler
def step_1(data, exception_id=None, func_name=None):
    return data.process()

@exception_handler
def step_2(data, exception_id=None, func_name=None):
    return data.validate()

def workflow(input_data):
    # Use same UUID for entire workflow
    workflow_id = str(uuid.uuid4())

    result1 = step_1(input_data, exception_id=workflow_id)
    result2 = step_2(result1, exception_id=workflow_id)

    return result2
```

All exceptions in this workflow will share the same `workflow_id`, making it easy to track related errors in logs.

### Nested Function Calls

Each function maintains its own exception handling:

```python
@exception_handler
def parent_function(data, exception_id=None, func_name=None):
    return child_function(data)

@exception_handler
def child_function(data, exception_id=None, func_name=None):
    return data['key']  # May raise KeyError
```

## Covered Exception Types

The module handles all standard Python built-in exceptions, including:

### System Exceptions
- `KeyboardInterrupt`
- `SystemExit`
- `SystemError`

### OS and I/O Exceptions
- `FileNotFoundError`
- `FileExistsError`
- `PermissionError`
- `IsADirectoryError`
- `NotADirectoryError`
- `TimeoutError`
- `ConnectionError` and subclasses
- `OSError` and all subclasses

### Arithmetic Exceptions
- `ZeroDivisionError`
- `FloatingPointError`
- `OverflowError`
- `ArithmeticError`

### Type and Value Exceptions
- `TypeError`
- `ValueError`
- `UnicodeError` and subclasses
  - `UnicodeDecodeError`
  - `UnicodeEncodeError`
  - `UnicodeTranslateError`

### Lookup Exceptions
- `KeyError`
- `IndexError`
- `AttributeError`
- `NameError`
- `UnboundLocalError`
- `LookupError`

### Import Exceptions
- `ModuleNotFoundError`
- `ImportError`

### Memory and Resource Exceptions
- `MemoryError`
- `RecursionError`

### Runtime Exceptions
- `NotImplementedError`
- `StopIteration`
- `StopAsyncIteration`
- `GeneratorExit`
- `RuntimeError`
- `RuntimeWarning`

### Syntax Exceptions
- `SyntaxError`
- `IndentationError`
- `TabError`

### Other Exceptions
- `AssertionError`
- `BufferError`
- `EOFError`
- `ReferenceError`
- `Exception` (base class)
- `BaseException` (ultimate base)

## Real-World Usage Examples

### API Request Handler
```python
@exception_handler
def handle_api_request(
    request_data,
    exception_id=None,
    func_name=None,
    log_this_user_id=None,
    log_this_request_id=None,
    log_this_endpoint=None,
    log_this_method=None,
    log_this_ip_address=None
):
    """Handle API request with full context logging."""
    result = validate_and_process(request_data)
    return result

# Usage
handle_api_request(
    request_data={"action": "update_profile"},
    log_this_user_id=12345,
    log_this_request_id="req_abc123",
    log_this_endpoint="/api/v1/users/profile",
    log_this_method="POST",
    log_this_ip_address="192.168.1.100"
)
```

### Database Transaction
```python
@exception_handler
def execute_transaction(
    query,
    params,
    exception_id=None,
    func_name=None,
    log_this_transaction_id=None,
    log_this_table=None,
    log_this_operation=None,
    log_this_user_id=None
):
    """Execute database transaction with context."""
    return db.execute(query, params)

# Usage with shared transaction ID
txn_id = str(uuid.uuid4())
execute_transaction(
    "UPDATE users SET status = ? WHERE id = ?",
    ["active", 123],
    exception_id=txn_id,
    log_this_transaction_id=txn_id,
    log_this_table="users",
    log_this_operation="UPDATE",
    log_this_user_id=123
)
```

### ML Model Serving
```python
@exception_handler
def predict(
    model_input,
    exception_id=None,
    func_name=None,
    log_this_model_name=None,
    log_this_model_version=None,
    log_this_request_id=None,
    log_this_batch_size=None
):
    """Run model inference with tracking."""
    predictions = model.predict(model_input)
    return predictions

# Usage
predict(
    model_input={"features": [1, 2, 3]},
    log_this_model_name="fraud_detector",
    log_this_model_version="v2.1.0",
    log_this_request_id="pred_xyz789",
    log_this_batch_size=1
)
```

## Best Practices

1. **Use `log_this_*` for important context**: Include relevant business context like user IDs, transaction IDs, request IDs, etc. This makes debugging much easier.

2. **Use consistent exception_id for related operations**: This helps trace errors across distributed systems or complex workflows.

3. **Let exceptions propagate**: The decorator re-raises all exceptions after logging, ensuring proper error handling up the call stack.

4. **Use descriptive function names**: Since the function name appears in logs, clear names help with debugging.

5. **Monitor stdout**: All logs are written to stdout.

6. **Parse logs programmatically**: The structured format makes it easy to parse logs for monitoring and alerting systems.

7. **Don't overload with log_this_* arguments**: Include only the most relevant context. Too many fields can make logs hard to read.

8. **Use consistent naming**: If you log `user_id` in one function, use the same name in others for easier log searching.

## Example Log Output

### Without Context Arguments
```
2026-02-08T05:55:31.756539+00:00 - ef4bd3f2-4333-4349-b10e-e16dc7b7e7f4 - test_division_by_zero - ERROR: ZeroDivisionError: division by zero (Line: 70)
2026-02-08T05:55:31.756749+00:00 - ff65a001-2bae-4ba2-b462-663e1c03b2ce - test_file_not_found - ERROR: FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/file.txt' (Line: 70)
2026-02-08T05:55:31.756921+00:00 - 3a671744-b8e3-4bf5-b339-7278884dd5af - test_key_error - ERROR: KeyError: 'b' (Line: 70)
```

### With Context Arguments (log_this_*)
```
2026-02-08T07:13:50.984493+00:00 - d0149a36-a774-4728-b9a6-fb01c2092596 - process_api_request - logged args: ip_address: 192.168.1.100, request_id: req_abc123, user_id: 12345 - ERROR: KeyError: 'required_field' (Line: 95)
2026-02-08T07:13:50.984742+00:00 - 15babb32-2b96-430a-8914-c7b15d2b955a - process_payment - logged args: amount: 15000, currency: USD, merchant_id: merch_999, payment_method: credit_card, user_id: 54321 - ERROR: ValueError: Amount exceeds limit: 15000 (Line: 95)
2026-02-08T07:13:50.984881+00:00 - 65107e0f-d46a-4ad2-94ba-fd1af824eb34 - process_uploaded_file - logged args: file_size: 2048576, filename: document.pdf, mime_type: application/pdf, uploader_id: 88888 - ERROR: FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/file.txt' (Line: 95)
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Project Information

This project is usees the MIT License.

This project is reviewed and maintained by a human.

Feel free to contribute with Issues or PRs on Github. The project is maintained as best as is reasonable.
