from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tempfile
import os
import requests
from PIL import Image
import torch
from typing import List, Dict
from groundingdino.util.inference import load_model, load_image, predict
from ultralytics import YOLO
import supervision as sv
from dotenv import load_dotenv
import uvicorn  

load_dotenv()

app = FastAPI()

class ImageRequest(BaseModel):
    model: str
    image_url: str

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

# Initialize models
DINO_CONFIG = "/home/share/MODELS/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
DINO_CHECKPOINT = "/home/share/MODELS/GroundingDINO/weights/groundingdino_swint_ogc.pth"
YOLO_MODEL = "/home/share/MODELS/YOLOv11/yolo11x.pt"

# Initialize DINO 
TEXT_PROMPT = "cat."
BOX_TRESHOLD = 0.35
TEXT_TRESHOLD = 0.25

dino_model = load_model(DINO_CONFIG, DINO_CHECKPOINT)
yolo_model = YOLO(YOLO_MODEL)

def download_image(url: str) -> str:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Create temporary file
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "temp_image.jpg")
        
        # Save image to temporary file
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return temp_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to download image: {str(e)}")

def process_dino(image_path: str) -> List[BoundingBox]:
    image_source, image = load_image(image_path)

    boxes, logits, phrases = predict(
        model=dino_model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )
    
    return [
        BoundingBox(x1=box[0], y1=box[1], x2=box[2], y2=box[3])
        for box in boxes
    ]

def process_yolo(image_path: str) -> List[BoundingBox]:
    results = yolo_model(image_path)[0]
    detections = sv.Detections.from_ultralytics(results)
    
    boxes = []
    for i in range(len(detections.xyxy)):
        if (detections.data['class_name'][i] == "cat"):  # Assuming 15 is the class ID for "cat"
            box = detections.xyxy[i]
            boxes.append(BoundingBox(
                x1=float(box[0]),
                y1=float(box[1]),
                x2=float(box[2]),
                y2=float(box[3])
            ))
    
    return boxes

@app.post("/detect")
async def detect_cats(request: ImageRequest) -> Dict[str, List[BoundingBox]]:
    # Download image to temporary directory
    temp_path = download_image(request.image_url)
    
    try:
        # Process with selected model
        if request.model.upper() == "DINO":
            boxes = process_dino(temp_path)
        elif request.model.upper() == "YOLO":
            boxes = process_yolo(temp_path)
        else:
            raise HTTPException(status_code=400, detail="Invalid model specified")
        
        return {"cat": boxes}
    
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
        os.rmdir(os.path.dirname(temp_path))


if __name__ == "__main__":
    # 設定 uvicorn 配置
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",  # 允許外部訪問
        port=int(os.getenv("PORT", "8000")),
        reload=True     # 開發模式下啟用熱重載
    )
    
    
    # 啟動 server
    server = uvicorn.Server(config)
    server.run()