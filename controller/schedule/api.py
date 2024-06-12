from contextlib import asynccontextmanager
from fastapi import FastAPI,BackgroundTasks

from src.ddqn import MultiPathTask


multiPathTask:MultiPathTask

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    global multiPathTask
    multiPathTask=MultiPathTask()
    yield
    # Clean up the ML models and release the resources
    multiPathTask.close()
    

app = FastAPI(lifespan=lifespan)

@app.post("/start_m_p")
def start_task(background_tasks: BackgroundTasks):
    if multiPathTask.isRunning:
        return "已经启动，无法再次启动"
    else:
        background_tasks.add_task(multiPathTask.run)
        return "启动"
