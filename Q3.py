import re
import sys

variables = {}
memo = {}
visiting = set()

def tokenize(expression):
    return re.findall(r'\d+|[A-Za-z_]\w*|[()+\-*]', expression)

def evaluate_variable(name):
    if name in memo:
        return memo[name]

    if name in visiting:
        raise ValueError("CYCLE")

    if name not in variables:
        raise ValueError("INVALID")

    visiting.add(name)

    try:
        tokens = tokenize(variables[name])
        value, pos = parse_expression(tokens, 0)

        if pos != len(tokens):
            raise ValueError("INVALID")

        memo[name] = value
        return value

    finally:
        visiting.remove(name)

def parse_expression(tokens, pos):
    value, pos = parse_term(tokens, pos)

    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        operator = tokens[pos]
        right, pos = parse_term(tokens, pos + 1)

        if operator == '+':
            value += right
        else:
            value -= right

    return value, pos

def parse_term(tokens, pos):
    value, pos = parse_factor(tokens, pos)

    while pos < len(tokens) and tokens[pos] == '*':
        right, pos = parse_factor(tokens, pos + 1)
        value *= right

    return value, pos

def parse_factor(tokens, pos):
    if pos >= len(tokens):
        raise ValueError("INVALID")

    token = tokens[pos]

    if token == '(':
        value, pos = parse_expression(tokens, pos + 1)

        if pos >= len(tokens) or tokens[pos] != ')':
            raise ValueError("INVALID")

        return value, pos + 1

    if token.isdigit():
        return int(token), pos + 1

    if re.fullmatch(r'[A-Za-z_]\w*', token):
        return evaluate_variable(token), pos + 1

    raise ValueError("INVALID")

def main():
    v = int(input())

    for _ in range(v):
        line = input()

        if '=' not in line:
            print("INVALID")
            return

        name, expression = line.split('=', 1)
        name = name.strip()
        expression = expression.strip()

        if not re.fullmatch(r'[A-Za-z_]\w*', name):
            print("INVALID")
            return

        variables[name] = expression

    expression = input()

    try:
        tokens = tokenize(expression)
        value, pos = parse_expression(tokens, 0)

        if pos != len(tokens):
            print("INVALID")
        else:
            print(value)

    except ValueError as error:
        print(str(error))


if __name__ == "__main__":
    main()
