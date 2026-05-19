# 🏏 IPL Analysis

A Python-based data analysis project for exploring Indian Premier League (IPL) statistics. Processes match data, generates structured reports, and surfaces insights using pandas — all driven from a clean CLI entry point.

---

## 📊 What It Does

- Loads and parses IPL match/ball-by-ball data from structured files (CSV/YAML)
- Performs statistical analysis on teams, players, matches, and seasons
- Outputs clean tabular reports to the terminal using `tabulate`
- Tracks system resource usage during processing via `psutil`
- Configurable pipeline via YAML config files

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `pandas` | Data loading, transformation, aggregation |
| `pyyaml` | YAML config file parsing |
| `tabulate` | Pretty-print tabular output in terminal |
| `psutil` | System resource monitoring |
| `logging` | Structured log output (stored in `/log`) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/AyushAgro/IplAnalysis.git
cd IplAnalysis

# Install dependencies
make setup
```

Or manually:

```bash
pip install -r requirements.txt
```

### Run

```bash
make run
```

Or directly:

```bash
python src/app.py
```

---

## 📁 Project Structure

```
IplAnalysis/
├── src/
│   └── app.py          # Main entry point
├── extra/              # Extra scripts / experiments
├── log/                # Log output files
├── requirements.txt    # Python dependencies
└── Makefile            # Setup and run commands
```

---

## 🔧 Makefile Commands

| Command | Description |
|---|---|
| `make setup` | Install all Python dependencies |
| `make run` | Run the analysis pipeline |

---

## 📦 Dependencies

```
pandas
pyyaml
tabulate
psutil
logging
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 📝 Logs

Execution logs are stored in the `/log` directory for debugging and audit purposes.

---

## 🤝 Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature/new-analysis`
3. Commit your changes: `git commit -m 'feat: add team win-rate analysis'`
4. Push to the branch: `git push origin feature/new-analysis`
5. Open a Pull Request

---

## 📄 License

This project is private. All rights reserved © Ayush Agrawal.
