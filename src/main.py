import logging

import random
import time
import string

from fastapi import FastAPI

app = FastAPI()
logger = logging.getLogger("uvicorn")


@app.middleware("http")
async def log_requests(request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.get("/")
def read_root():
    logger.info("test call")
    return {"Hello": "World"}


@app.get("/video")
def read_video():
    try:
        result = "../videos/SampleVideo_1280x720_1mb.mp4"
        logger.info(f"log result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in streaming: {e}")
