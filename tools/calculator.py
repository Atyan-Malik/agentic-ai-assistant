
import ast
import math
import operator


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

MAX_EXPRESSION_LENGTH = 200
MAX_ABS_VALUE = 1e100


def _evaluate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(
            node.value, (int, float)
        ):
            raise ValueError("Only numeric constants are allowed.")

        value = node.value

    elif isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported mathematical operator.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        if isinstance(node.op, ast.Pow):
            if abs(right) > 1000:
                raise ValueError("Exponent is too large.")

        value = operation(left, right)

    elif isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported unary operator.")

        value = operation(_evaluate(node.operand))

    else:
        raise ValueError("Unsupported expression.")

    if isinstance(value, complex) or not math.isfinite(value):
        raise ValueError("Result must be a finite real number.")

    if abs(value) > MAX_ABS_VALUE:
        raise ValueError("Result is too large.")

    return value


def calculate(expression: str) -> dict:
    """Safely evaluate a mathematical expression."""
    try:
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Provide a mathematical expression.")

        if len(expression) > MAX_EXPRESSION_LENGTH:
            raise ValueError("Expression is too long.")

        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)

        return {
            "success": True,
            "expression": expression,
            "result": result,
        }

    except (
        ValueError,
        SyntaxError,
        ZeroDivisionError,
        OverflowError,
    ) as exc:
        return {
            "success": False,
            "error": str(exc),
        }
