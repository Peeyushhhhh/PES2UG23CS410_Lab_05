import json
from datetime import datetime

# Global variable
stock_data = {}


def addItem(item="default", qty=0, logs=None):
    """Add qty of item to stock_data. `logs` is a list that will receive text logs."""
    if logs is None:
        logs = []

    # normalize item to string
    if item is None:
        return logs

    item = str(item)

    # try to coerce qty to int; if it fails, warn and skip
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        print(f"Warning: qty for item '{item}' is not an integer ({qty}); skipping add.")
        return logs

    # update stock
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    return logs


def removeItem(item, qty):
    """Remove qty of item from stock_data if present. If qty >= current stock, remove the key."""
    if item not in stock_data:
        # nothing to do
        return

    try:
        qty = int(qty)
    except (TypeError, ValueError):
        print(f"Warning: qty for removal of '{item}' is not an integer ({qty}); skipping remove.")
        return

    stock_data[item] -= qty
    if stock_data[item] <= 0:
        del stock_data[item]


def getQty(item):
    """Return quantity of item (0 if not present)."""
    return stock_data.get(item, 0)


def loadData(file="inventory.json"):
    """Load stock_data from a JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        # no file yet — keep empty stock_data
        stock_data = {}
    except json.JSONDecodeError:
        print(f"Warning: file '{file}' contains invalid JSON. Keeping empty inventory.")
        stock_data = {}


def saveData(file="inventory.json"):
    """Save stock_data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f)


def printData():
    """Pretty-print the inventory."""
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])


def checkLowItems(threshold=5):
    """Return list of items whose stock is below threshold."""
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result


def main():
    logs = []
    addItem("apple", 10, logs)
    addItem("banana", -2, logs)        # still allowed (could be interpreted as correction)
    addItem(123, "ten", logs)          # qty "ten" cannot be coerced -> will be skipped with warning
    removeItem("apple", 3)
    removeItem("orange", 1)            # safe: orange not present
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    # removed unsafe eval; replaced with a safe status message
    print("Status: finished running main()")


if __name__ == "__main__":
    main()
