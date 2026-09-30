import re

def main():
    b = int(input())
    banned_words = [input().strip().lower() for _ in range(b)]

    n = int(input())

    for i in range(1, n + 1):
        password = input().strip()

        if len(password) < 6 or len(password) > 12:
            print(f"{i}: WEAK_LENGTH")
            continue

        lower = re.search(r"[a-z]", password)
        upper = re.search(r"[A-Z]", password)
        digit = re.search(r"\d", password)
        special = re.search(r"[$#@]", password)

        if not (lower and upper and digit and special):
            print(f"{i}: WEAK_PATTERN")
            continue

        password_lower = password.lower()

        compromised = False
        for word in banned_words:
            if word in password_lower:
                compromised = True
                break

        if compromised:
            print(f"{i}: COMPROMISED")
            continue

        if re.search(r"(.)\1\1\1", password):
            print(f"{i}: WEAK_PATTERN")
            continue

        print(f"{i}: STRONG")


if __name__ == "__main__":
    main()
