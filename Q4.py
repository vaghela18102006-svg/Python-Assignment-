import csv
from datetime import datetime
from collections import defaultdict

def main():
    file_path = input().strip()

    balances = defaultdict(float)
    errors = []
    credits = []
    debits = []

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                tid = row["tid"]
                acc = row["acc"]
                transaction_type = row["type"].upper()
                amount = float(row["amount"])
                timestamp = row["time"]

                if not tid or not acc:
                    raise ValueError("Missing transaction or account ID")

                if transaction_type not in ("CREDIT", "DEBIT"):
                    raise ValueError("Invalid transaction type")

                if amount <= 0:
                    raise ValueError("Amount must be greater than 0")

                datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

                if transaction_type == "CREDIT":
                    credits.append(row)
                    balances[acc] += amount
                else:
                    debits.append(row)
                    balances[acc] -= amount

            except Exception as e:
                row["reason"] = str(e)
                errors.append(row)

    with open("credit.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["tid", "acc", "type", "amount", "time"]
        )
        writer.writeheader()
        writer.writerows(credits)

    with open("debit.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["tid", "acc", "type", "amount", "time"]
        )
        writer.writeheader()
        writer.writerows(debits)

    with open("error.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["tid", "acc", "type", "amount", "time", "reason"]
        )
        writer.writeheader()
        writer.writerows(errors)

    result = sorted(
        balances.items(),
        key=lambda x: (-abs(x[1]), x[0])
    )

    for account, balance in result:
        if balance.is_integer():
            balance = int(balance)
        print(account, balance)

    print("Files created: credit.csv, debit.csv, error.csv")


if __name__ == "__main__":
    main()
