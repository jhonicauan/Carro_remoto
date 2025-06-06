from fastapi import FastAPI
from Components.Camera import Camera
from starlette.responses import StreamingResponse

app = FastAPI()
camera = Camera()

@app.get("/stream")
def stream():
    return StreamingResponse(camera.stream(),media_type="multipart/x-mixed-replace; boundary=frame")