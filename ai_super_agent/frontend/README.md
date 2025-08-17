# Frontend UIs

Three UI options are provided. All connect to the FastAPI backend at `http://127.0.0.1:8000`.

## PyQt6

```bash
cd frontend/pyqt6_app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Flet (desktop or web)

```bash
cd frontend/flet_app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py  # desktop
# Or run web:
# flet run --web main.py
```

Themes:
- official: بسيط ورَسمي
- cyberpunk: نيون + contrast
- golden: درجات ذهبية

## Flutter

See `frontend/flutter_app/README.md`.