# Femirins Budget CLI

A minimalist, scriptable budgeting tool for power users who prefer keyboard-driven workflows.

## Features
- **Zero-Setup Local Storage:** SQLite database for transactions and budgets.
- **Scriptable:** Import/export via CSV/JSON for automation.
- **Minimalist:** No GUI bloat; keyboard-driven.
- **Extensible:** Plugin system for custom features (e.g., subscriptions, shared budgets).
- **Open-Source:** MIT License for community contributions.

## Installation
```bash
# Clone the repository
 git clone https://github.com/femirins/femirins-budget.git
 cd femirins-budget

# Initialize the database
 python3 main.py init
```

## Usage
### Add a Transaction
```bash
python3 main.py add --date 2026-05-25 --description "Groceries" --amount 50.00 --category "Food" --tags "essential"
```

### List Transactions
```bash
python3 main.py list
```

### Export Transactions
```bash
python3 main.py export --format csv > transactions.csv
```

## Technical Architecture
- **Database:** SQLite (local file: `~/.femirins-budget.db`)
- **Language:** Python 3
- **Dependencies:** None (standard library only)
- **Extensibility:** Plugin system (planned for v2)

## Roadmap
- [ ] Plugin system for custom features (e.g., subscriptions, shared budgets)
- [ ] AI categorization (via local LLM)
- [ ] Recurring transactions
- [ ] Multi-user support

## Note
This repository was published under `fairyfemirins` due to GitHub namespace restrictions. A transfer to `femirins` is pending.

To request a transfer, open an issue in this repository or contact `@femirins` on GitHub.

---

## License
MIT