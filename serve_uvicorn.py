
import uvicorn
# import gunicorn
# import uvicorn.workers.UvicornWorker

from python_fastapi_firebase_authentication.core.env import UVI_PORT, UVI_SERVER_HOST, UVI_LOG_LEVEL, UVI_ACCESS_LOG, UVI_RELOAD


def uvi_server():
    
    uvicorn.run(
        "main:app",
        host=UVI_SERVER_HOST,
        port=UVI_PORT,
        reload=UVI_RELOAD,
        use_colors=True,
        access_log=UVI_ACCESS_LOG,
        log_level=UVI_LOG_LEVEL
    )

    # gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
