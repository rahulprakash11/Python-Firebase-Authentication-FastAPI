import uvicorn
from python_fastapi_firebase_authentication.core.env import UVI_PORT, UVI_SERVER_HOST, UVI_LOG_LEVEL, UVI_ACCESS_LOG



if __name__ == "__main__":

    uvicorn.run(
        "python_fastapi_firebase_authentication.main:app",
        host=UVI_SERVER_HOST,
        port=UVI_PORT,
        reload=True,
        use_colors=True,
        access_log=UVI_ACCESS_LOG,
        log_level=UVI_LOG_LEVEL
    )
