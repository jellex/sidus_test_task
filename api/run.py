import uvicorn

from api.init_api import init_api
from config import config

app = init_api(config)

if __name__ == "__main__":
    uvicorn.run(
        "api.run:app",
        host="0.0.0.0",
        port=8000,
        workers=config.WORKERS,
        debug=config.IS_DEBUG,
        access_log=config.IS_DEBUG,
    )
