# Conway's Game of Life

A small Python project with a DearPyGui interface and a NumPy-based engine.

## Project structure

- `engine/game.py`: game rules and board state management
- `gui/app.py`: UI layout, drawing, and callbacks
- `tests/test_engine.py`: engine regression tests
- `main.py`: app entry point

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

## Test

```powershell
python -m unittest discover -s tests -p "test_*.py"
```
