


# Path: tests/test_app.py

def test_app():
    import fastapi
    app = fastapi.FastAPI()
    assert app is not None
