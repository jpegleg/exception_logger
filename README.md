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

## Log format

Each logged exception follows this structure:

```
ISO-8601-Timestamp - UUIDv4 - function_name - [logged args: key1: value1, key2: value2] - ERROR: ExceptionType: message (File: filename.py, Line: line_number)
```

Example without logged arguments:
```
2026-02-08T08:14:36.013748+00:00 - 4b1274be-0428-4d11-ae0d-6402542ba7f6 - process_data - ERROR: KeyError: 'required_field' (File: app.py, Line: 42)
```

Example with logged arguments:
```
2026-02-08T08:13:51.620325+00:00 - f011e24d-0ae3-4982-8cf5-db39c056c905 - process_api_request - logged args: ip_address: 192.168.1.100, request_id: req_abc123, user_id: 12345 - ERROR: KeyError: 'required_field' (File: api_handler.py, Line: 95)
```

## Installation

Install with pip or uv:

```
uv add exception_logger
```

```
pip install exception_logger
```

Or include the module as `exception_logger.py` in your project, along with the MIT license.

## Usage

The decorator automatically:
- Accepts a UUID for logging or generates one if one isn't provided
- Detects the function name and logs it
- Logs any exception with full details
- Adds specified custom args to log lines
- Re-raises the exception (unless the 'quiet' version is used)

There are two different functions available to decorate with, `exception_handler` and `exception_handler_quiet`.

The `_quiet` version suppresses most tracebacks and does not re-raise the error. The only type of traceback that won't be surpressed are
tracebacks outside of the fucnction that is decorated. So even if you decorate 'main', a syntax error that makes the file invalid Python
will still have a traceback.

Use caution with the `_quiet` version, as no further error handling is done in that case!

Typically we want to use `exception_handler` instead of `exception_handler_quiet` so that the error is re-raised, but the quiet version
is useful in cases where the function being decorated is the top level, such as when decorating main in the final script.

The quiet version can be nice when we want to keep our log files very homogenous and single line, and completely in STDOUT.
Of course we can still keep log files nice with the regular version too, with a little bit of work to handle our raised exceptions appropriately, like normal.

### Slap the decorator on main

First let's look at a brutishly simple approach that logs all errors in the whole program and removes tracebacks from main and everything main calls.

```python
from exception_logger import exception_handler_quiet

@exception_handler_quiet
def main():
    # do everything normally and reap the benfits of the exception logging!
```

If you decorate the main function, then there normally wouldn't be a need to decorate specific functions as that could duplicate error logs.

While decorating main is _super easy_ and actually awesome in some cases, in many cases you might want to customize the usage further and decorate individual functions.

Using the `_quiet` version on main (or any function) can be dangerous since errors won't propagate any further.

### Decorating a function

```python
from exception_logger import exception_handler

@exception_handler
def risky_operation(data):
    # Your code here
    return data['key']  # May raise KeyError
```


### Custom exception id and function name

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

### Contextual logging with `log_this_*` arguments

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

### Manual exception handling

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

### Correlated exception tracking

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

### Nested function calls

Each function maintains its own exception handling:

```python
@exception_handler
def parent_function(data, exception_id=None, func_name=None):
    return child_function(data)

@exception_handler
def child_function(data, exception_id=None, func_name=None):
    return data['key']  # May raise KeyError
```

## Covered exception types

The module handles all standard Python built-in exceptions, including:

### System exceptions
- `KeyboardInterrupt`
- `SystemExit`
- `SystemError`

### OS and I/O exceptions
- `FileNotFoundError`
- `FileExistsError`
- `PermissionError`
- `IsADirectoryError`
- `NotADirectoryError`
- `TimeoutError`
- `ConnectionError` and subclasses
- `OSError` and all subclasses

### Arithmetic exceptions
- `ZeroDivisionError`
- `FloatingPointError`
- `OverflowError`
- `ArithmeticError`

### Type and value exceptions
- `TypeError`
- `ValueError`
- `UnicodeError` and subclasses
  - `UnicodeDecodeError`
  - `UnicodeEncodeError`
  - `UnicodeTranslateError`

### Lookup exceptions
- `KeyError`
- `IndexError`
- `AttributeError`
- `NameError`
- `UnboundLocalError`
- `LookupError`

### Import exceptions
- `ModuleNotFoundError`
- `ImportError`

### Memory and resource exceptions
- `MemoryError`
- `RecursionError`

### Runtime exceptions
- `NotImplementedError`
- `StopIteration`
- `StopAsyncIteration`
- `GeneratorExit`
- `RuntimeError`
- `RuntimeWarning`

### Syntax exceptions
- `SyntaxError`
- `IndentationError`
- `TabError`

### Other exceptions
- `AssertionError`
- `BufferError`
- `EOFError`
- `ReferenceError`
- `Exception` (base class)
- `BaseException` (ultimate base)

## More examples

### API request handler
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

### Database transaction
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

### ML model serving
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

## Best practices

1. **Use `log_this_*` for important context**: Include relevant business context like user IDs, transaction IDs, request IDs, etc. This makes debugging much easier.

2. **Use consistent exception_id for related operations**: This helps trace errors across distributed systems or complex workflows.

3. **Let exceptions propagate**: The decorator re-raises all exceptions after logging, ensuring proper error handling up the call stack.

4. **Use descriptive function names**: Since the function name appears in logs, clear names help with debugging.

5. **Monitor stdout**: All logs are written to stdout.

6. **Parse logs programmatically**: The structured format makes it easy to parse logs for monitoring and alerting systems.

7. **Don't overload with log_this_* arguments**: Include only the most relevant context. Too many fields can make logs hard to read.

8. **Use consistent naming**: If you log `user_id` in one function, use the same name in others for easier log searching.

9. **Only use the quiet version if the error doesn't need to be raised any further.


## Example Log Output

### Without context arguments
```
2026-02-08T08:14:36.013748+00:00 - 4b1274be-0428-4d11-ae0d-6402542ba7f6 - test_division_by_zero - ERROR: ZeroDivisionError: division by zero (File: test.py, Line: 14)
2026-02-08T08:14:36.013911+00:00 - 46cd01e0-fdf2-4186-bc6c-f4930627b58e - test_file_not_found - ERROR: FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/file.txt' (File: test.py, Line: 22)
2026-02-08T08:14:36.014010+00:00 - 76ed8968-e799-4b84-afa9-3a75a80ea120 - test_key_error - ERROR: KeyError: 'b' (File: test.py, Line: 30)
```

### With context arguments (log_this_*)
```
2026-02-08T08:13:51.620325+00:00 - f011e24d-0ae3-4982-8cf5-db39c056c905 - process_api_request - logged args: ip_address: 192.168.1.100, request_id: req_abc123, user_id: 12345 - ERROR: KeyError: 'required_field' (File: log_this_examples.py, Line: 30)
2026-02-08T08:13:51.620590+00:00 - 59f947e5-fbf4-4450-a797-19b82f7467e6 - process_payment - logged args: amount: 15000, currency: USD, merchant_id: merch_999, payment_method: credit_card, user_id: 54321 - ERROR: ValueError: Amount exceeds limit: 15000 (File: log_this_examples.py, Line: 69)
2026-02-08T08:13:51.620759+00:00 - 3ff961d3-6952-4c74-8312-fbfbc6135917 - process_uploaded_file - logged args: file_size: 2048576, filename: document.pdf, mime_type: application/pdf, uploader_id: 88888 - ERROR: FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/file.txt' (File: log_this_examples.py, Line: 85)
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Project information

This project is usees the MIT License.

This project is reviewed and maintained by a human.

Feel free to contribute with Issues or PRs on Github. The project is maintained as best as is reasonable.
