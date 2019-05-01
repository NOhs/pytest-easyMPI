import inspect


def get_pytest_input(func):
    module = inspect.getmodule(func).__name__

    module = "/".join(module.split(".")) + ".py"
    func = "::".join(func.__qualname__.split("."))

    return f"{module}::{func}"


def get_filename(pytest_input):
    return pytest_input.replace("/", ".").replace(":", ".")
