import uvicorn

from lb.journey_finder_fastapi.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)