from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import shutil
import os

app = FastAPI()

# Allow frontend access (React dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] to be more strict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your YOLOv8 model
model = YOLO("best_chagas.pt")

# Ensure uploads folder exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------- ROUTE 1: Return JSON detection data --------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    input_path = f"{UPLOAD_DIR}/{file.filename}"
    output_path = f"{UPLOAD_DIR}/annotated_{file.filename}"

    # Save uploaded image
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run model
    results = model(input_path)
    results[0].save(filename=output_path)  # Save image with bounding boxes

    # Return detection data as JSON
    return JSONResponse(content=results[0].tojson())

# -------- ROUTE 2: Return annotated image --------
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    input_path = f"{UPLOAD_DIR}/{file.filename}"
    output_path = f"{UPLOAD_DIR}/annotated_{file.filename}"

    # Save uploaded image
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run model
    results = model(input_path)
    results[0].save(filename=output_path)

    # Return image file
    return FileResponse(output_path, media_type="image/jpeg")

# ###################Correctly returned code base below: #################################################

# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from ultralytics import YOLO
# import shutil
# import os

# app = FastAPI()
# model = YOLO("best_chagas.pt")  # Load your trained model

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     UPLOAD_DIR = "uploads"
#     input_path = f"{UPLOAD_DIR}/{file.filename}"
#     output_path = f"{UPLOAD_DIR}/annotated_{file.filename}"

#     with open(input_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     results = model(input_path)
#     results[0].save(filename=output_path)  # ✅ save fixed

#     return JSONResponse(content=results[0].tojson())

################################################################older code base below ####################

# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from ultralytics import YOLO
# import shutil
# import uuid
# import os

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # frontend dev URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# model = YOLO('yolov8n.pt')  # Simulated model

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# import traceback

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     try:
#         file_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex}_{file.filename}"
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         results = model(file_path)  # returns a list of results
#         results[0].save(save_dir=UPLOAD_DIR)  # fix: save the first result

#         for f in os.listdir(UPLOAD_DIR):
#             if "_result" in f and f.endswith(".jpg"):
#                 result_path = os.path.join(UPLOAD_DIR, f)
#                 return FileResponse(path=result_path, media_type="image/jpeg")

#         return {"error": "No result image found"}
    
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return {"error": str(e)}


# # @app.post("/predict")
# # async def predict(file: UploadFile = File(...)):
# #     file_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex}_{file.filename}"
# #     with open(file_path, "wb") as buffer:
# #         shutil.copyfileobj(file.file, buffer)

# #     # Run YOLOv8 (fake prediction on random model)
# #     results = model(file_path)
# #     results_path = file_path.replace(".jpg", "_result.jpg")
# #     results.save(save_dir=UPLOAD_DIR)

# #     # Find generated annotated file (typically saved with same name inside dir)
# #     for f in os.listdir(UPLOAD_DIR):
# #         if "_result" in f and f.endswith(".jpg"):
# #             return FileResponse(path=f"{UPLOAD_DIR}/{f}", media_type="image/jpeg")

# #     return {"error": "No result image generated"}
