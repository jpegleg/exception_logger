"""
Generic Exception Handler and Logger Module

Provides a decorator for automatic exception handling and logging with detailed
information for all standard Python built-in exceptions.
"""

import functools
import sys
from datetime import datetime, timezone
from typing import Callable, Any, Optional
import uuid


def log_exception(
    exception_id: str,
    func_name: str,
    exc_type: type,
    exc_value: Exception,
    exc_info: tuple,
    logged_args: dict = None
) -> None:
    """
    Log exception details in a structured format.

    Args:
        exception_id: UUIDv4 string for tracking this exception
        func_name: Name of the function where exception occurred
        exc_type: Type of the exception
        exc_value: The exception instance
        exc_info: Exception info tuple from sys.exc_info()
        logged_args: Dictionary of log_this_* arguments to include in log
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    # Extract helpful information
    exc_msg = str(exc_value) if str(exc_value) else "No message provided"

    # Get line number if available
    tb = exc_info[2]
    line_no = tb.tb_lineno if tb else "Unknown"

    # Format logged arguments if present
    logged_args_str = ""
    if logged_args:
        # Sort for consistent ordering in logs
        sorted_args = sorted(logged_args.items())
        args_parts = [f"{k}: {v}" for k, v in sorted_args]
        logged_args_str = f"logged args: {', '.join(args_parts)} - "

    # Format the log message
    log_msg = (
        f"{timestamp} - {exception_id} - {func_name} - "
        f"{logged_args_str}"
        f"ERROR: {exc_type.__name__}: {exc_msg} (Line: {line_no})"
    )

    print(log_msg, file=sys.stdout)


def exception_handler(func: Callable) -> Callable:
    """
    Decorator that wraps a function with comprehensive exception handling.

    The decorated function should accept 'exception_id' and 'func_name' as
    keyword arguments, or they will be auto-generated/detected.

    Usage:
        @exception_handler
        def my_function(arg1, arg2, exception_id=None, func_name=None):
            # function code here
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract or generate tracking information
        exception_id = kwargs.pop('exception_id', str(uuid.uuid4()))
        func_name = kwargs.pop('func_name', func.__name__)

        # Extract all log_this_* arguments
        logged_args = {}
        keys_to_remove = []
        for key in kwargs:
            if key.startswith('log_this_'):
                # Remove the 'log_this_' prefix for cleaner logging
                clean_key = key[9:]  # len('log_this_') = 9
                logged_args[clean_key] = kwargs[key]
                keys_to_remove.append(key)

        # Remove log_this_* arguments from kwargs
        for key in keys_to_remove:
            kwargs.pop(key)

        try:
            return func(*args, **kwargs)

        # Concrete Exceptions - Most Specific First

        # System Exit Exceptions
        except KeyboardInterrupt as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, KeyboardInterrupt, e, exc_info, logged_args)
            raise

        except SystemExit as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, SystemExit, e, exc_info, logged_args)
            raise

        # OS and I/O Exceptions
        except FileNotFoundError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, FileNotFoundError, e, exc_info, logged_args)
            raise

        except FileExistsError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, FileExistsError, e, exc_info, logged_args)
            raise

        except IsADirectoryError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, IsADirectoryError, e, exc_info, logged_args)
            raise

        except NotADirectoryError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, NotADirectoryError, e, exc_info, logged_args)
            raise

        except PermissionError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, PermissionError, e, exc_info, logged_args)
            raise

        except ProcessLookupError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ProcessLookupError, e, exc_info, logged_args)
            raise

        except TimeoutError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, TimeoutError, e, exc_info, logged_args)
            raise

        except InterruptedError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, InterruptedError, e, exc_info, logged_args)
            raise

        except ChildProcessError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ChildProcessError, e, exc_info, logged_args)
            raise

        except BlockingIOError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, BlockingIOError, e, exc_info, logged_args)
            raise

        except ConnectionError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ConnectionError, e, exc_info, logged_args)
            raise

        except BrokenPipeError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, BrokenPipeError, e, exc_info, logged_args)
            raise

        except ConnectionAbortedError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ConnectionAbortedError, e, exc_info, logged_args)
            raise

        except ConnectionRefusedError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ConnectionRefusedError, e, exc_info, logged_args)
            raise

        except ConnectionResetError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ConnectionResetError, e, exc_info, logged_args)
            raise

        except OSError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, OSError, e, exc_info, logged_args)
            raise

        # Arithmetic Exceptions
        except ZeroDivisionError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ZeroDivisionError, e, exc_info, logged_args)
            raise

        except FloatingPointError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, FloatingPointError, e, exc_info, logged_args)
            raise

        except OverflowError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, OverflowError, e, exc_info, logged_args)
            raise

        # Type and Value Exceptions
        except TypeError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, TypeError, e, exc_info, logged_args)
            raise

        except ValueError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ValueError, e, exc_info, logged_args)
            raise

        except UnicodeError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, UnicodeError, e, exc_info, logged_args)
            raise

        except UnicodeDecodeError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, UnicodeDecodeError, e, exc_info, logged_args)
            raise

        except UnicodeEncodeError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, UnicodeEncodeError, e, exc_info, logged_args)
            raise

        except UnicodeTranslateError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, UnicodeTranslateError, e, exc_info, logged_args)
            raise

        # Lookup Exceptions
        except KeyError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, KeyError, e, exc_info, logged_args)
            raise

        except IndexError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, IndexError, e, exc_info, logged_args)
            raise

        except AttributeError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, AttributeError, e, exc_info, logged_args)
            raise

        except NameError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, NameError, e, exc_info, logged_args)
            raise

        except UnboundLocalError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, UnboundLocalError, e, exc_info, logged_args)
            raise

        # Import Exceptions
        except ModuleNotFoundError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ModuleNotFoundError, e, exc_info, logged_args)
            raise

        except ImportError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ImportError, e, exc_info, logged_args)
            raise

        # Memory and Resource Exceptions
        except MemoryError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, MemoryError, e, exc_info, logged_args)
            raise

        except RecursionError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, RecursionError, e, exc_info, logged_args)
            raise

        # Runtime Exceptions
        except NotImplementedError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, NotImplementedError, e, exc_info, logged_args)
            raise

        except StopIteration as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, StopIteration, e, exc_info, logged_args)
            raise

        except StopAsyncIteration as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, StopAsyncIteration, e, exc_info, logged_args)
            raise

        except GeneratorExit as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, GeneratorExit, e, exc_info, logged_args)
            raise

        # Syntax and Indentation Exceptions
        except SyntaxError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, SyntaxError, e, exc_info, logged_args)
            raise

        except IndentationError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, IndentationError, e, exc_info, logged_args)
            raise

        except TabError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, TabError, e, exc_info, logged_args)
            raise

        # System Exceptions
        except SystemError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, SystemError, e, exc_info, logged_args)
            raise

        except ReferenceError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ReferenceError, e, exc_info, logged_args)
            raise

        # Buffer and EOFError
        except BufferError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, BufferError, e, exc_info, logged_args)
            raise

        except EOFError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, EOFError, e, exc_info, logged_args)
            raise

        # Assertion Error
        except AssertionError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, AssertionError, e, exc_info, logged_args)
            raise

        # Runtime Error and Warning
        except RuntimeError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, RuntimeError, e, exc_info, logged_args)
            raise

        except RuntimeWarning as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, RuntimeWarning, e, exc_info, logged_args)
            raise

        # Lookup Error (parent class - catch after specific lookup errors)
        except LookupError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, LookupError, e, exc_info, logged_args)
            raise

        # Arithmetic Error (parent class - catch after specific arithmetic errors)
        except ArithmeticError as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, ArithmeticError, e, exc_info, logged_args)
            raise

        # Base Exception classes (catch last)
        except Exception as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, Exception, e, exc_info, logged_args)
            raise

        except BaseException as e:
            exc_info = sys.exc_info()
            log_exception(exception_id, func_name, BaseException, e, exc_info, logged_args)
            raise

    return wrapper


# Convenience function for manual exception handling
def handle_exception(
    exception_id: Optional[str] = None,
    func_name: Optional[str] = None,
    **logged_args
) -> None:
    """
    Manually log the current exception.

    Call this within an except block to log the exception with the same
    format as the decorator.

    Args:
        exception_id: Optional UUID for tracking. Generated if not provided.
        func_name: Optional function name. Detected from caller if not provided.
        **logged_args: Any additional context to log (e.g., user_id=123, rate=0.5)

    Example:
        try:
            risky_operation()
        except Exception:
            handle_exception(
                exception_id="custom-uuid",
                func_name="my_function",
                user_id=12345,
                request_id="abc-123"
            )
            raise
    """
    import inspect

    exc_info = sys.exc_info()
    if exc_info[0] is None:
        print("Warning: handle_exception called outside of exception context",
              file=sys.stdout)
        return

    if exception_id is None:
        exception_id = str(uuid.uuid4())

    if func_name is None:
        frame = inspect.currentframe()
        if frame and frame.f_back:
            func_name = frame.f_back.f_code.co_name
        else:
            func_name = "unknown"

    log_exception(exception_id, func_name, exc_info[0], exc_info[1], exc_info, logged_args)


if __name__ == "__main__":
    # Example usage and testing

    @exception_handler
    def test_division_by_zero():
        """Test ZeroDivisionError handling"""
        return 1 / 0

    @exception_handler
    def test_file_not_found():
        """Test FileNotFoundError handling"""
        with open("/nonexistent/file.txt", "r") as f:
            return f.read()

    @exception_handler
    def test_key_error():
        """Test KeyError handling"""
        d = {"a": 1}
        return d["b"]

    @exception_handler
    def test_with_custom_id(data, exception_id=None, func_name=None, log_this_user=None, log_this_rate=None):
        """Test with custom exception_id, func_name, and log_this_* arguments"""
        return data[10]  # Will raise IndexError

    print("Testing exception_logger module...\n")

    # Test 1: ZeroDivisionError
    print("Test 1: Division by zero")
    try:
        test_division_by_zero()
    except ZeroDivisionError:
        print("Caught and re-raised as expected\n")

    # Test 2: FileNotFoundError
    print("Test 2: File not found")
    try:
        test_file_not_found()
    except FileNotFoundError:
        print("Caught and re-raised as expected\n")

    # Test 3: KeyError
    print("Test 3: Key error")
    try:
        test_key_error()
    except KeyError:
        print("Caught and re-raised as expected\n")

    # Test 4: Custom exception_id and func_name
    print("Test 4: Custom tracking info")
    custom_uuid = str(uuid.uuid4())
    try:
        test_with_custom_id([1, 2, 3],
                           exception_id=custom_uuid,
                           func_name="custom_function_name",
                           log_this_user="frank",
                           log_this_rate=0.125)
    except IndexError:
        print("Caught and re-raised as expected\n")

    print("All tests completed!")
