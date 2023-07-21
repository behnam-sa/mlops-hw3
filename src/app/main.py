from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import torch
from torchvision import transforms
from torchvision.models import inception_v3, Inception_V3_Weights

from PIL import Image
from io import BytesIO

from label_names import label_names

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = inception_v3(weights=Inception_V3_Weights.DEFAULT)
model.eval()

@app.post("/predict")
def predict(image: UploadFile = File(...)):
    image_bytes = image.file.read()
    tensor = preprocess_image(image_bytes)
    output = model(tensor)
    _, predicted_idx = torch.max(output.data, 1)
    predicted_idx = predicted_idx.item()
    predicted_name = label_names[predicted_idx]
    
    return { "label": predicted_idx, "labelName": predicted_name }


def preprocess_image(image_bytes: bytes) -> torch.Tensor:
    # Preprocessing logic
    # Convert image_bytes to torch.Tensor
    image = Image.open(BytesIO(image_bytes))

    transform = transforms.Compose([
        transforms.Resize(299),
        transforms.CenterCrop(299),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    tensor = transform(image)
    
    return tensor.unsqueeze(0)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
