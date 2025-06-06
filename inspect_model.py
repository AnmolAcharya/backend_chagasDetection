from ultralytics import YOLO

# Load the model
model = YOLO("best_chagas.pt")

# Print model architecture summary
model.info()

# Print class names (what the model detects)
print("Classes:", model.names)
