

https://github.com/user-attachments/assets/ae0f443e-2fdb-42bf-ad6c-7ac71b44253e

# ASL Fingerspelling Translator

A real-time computer vision application that recognizes **American Sign Language (ASL) fingerspelling** from webcam input and converts recognized handshapes into text.

Built with **PyTorch, ResNet18, YOLOv8, FastAPI, and vanilla JavaScript**.

## Demo



<!-- Upload the demo MP4 directly below this line using GitHub's README editor. -->

## Features

* Real-time webcam-based ASL fingerspelling
* Recognition of **A–Z**
* `space`, `del`, and `nothing` gestures
* YOLOv8 hand detection
* Custom-trained ResNet18 classifier
* Prediction stabilization for live inference
* Repeated-letter handling
* FastAPI inference API
* Input validation and upload-size protection
* Per-IP request rate limiting
* Interactive ASL alphabet guide

## How It Works

The application uses a two-stage computer vision pipeline:

```text
Webcam Frame
     │
     ▼
YOLOv8 Hand Detection
     │
     ▼
Hand Bounding Box
     │
     ▼
Hand Crop
     │
     ▼
ResNet18 Classifier
     │
     ▼
Prediction Stabilization
     │
     ▼
Translated Text
```

### 1. Hand Detection

YOLOv8 identifies the user's hand within each webcam frame.

The detected bounding box is used to isolate the hand before passing it to the classifier.

### 2. ASL Classification

The cropped hand image is passed to a custom-trained **ResNet18** classifier.

The model recognizes **29 classes**:

```text
A  B  C  D  E  F  G  H  I  J  K  L  M
N  O  P  Q  R  S  T  U  V  W  X  Y  Z
del  nothing  space
```

### 3. Prediction Stabilization

Live webcam predictions can fluctuate between frames.

To reduce transient predictions, the application requires consecutive matching predictions before committing a character to the translated text.

For repeated letters, the user briefly moves their hand out of the frame before signing the same letter again.

For example:

```text
H → E → L → L → O

          ↑
   hand leaves and
   re-enters here
```

## Model

### ResNet18

The classifier is based on **ResNet18** with a custom classification head.

The earliest layers of the network were frozen while deeper layers and the classification head were fine-tuned for ASL fingerspelling.

The final classification head uses dropout before the output layer to improve generalization.

### Dataset

The model was trained on approximately **87,000 images** across 29 classes.

The dataset contains:

* A–Z
* `del`
* `nothing`
* `space`

The data was divided into training, validation, and test sets. Image paths and hashes were checked to help prevent duplicate images from appearing across splits.

Training used image augmentation including:

* Random rotation
* Random resized cropping
* Color jitter
* ImageNet normalization

### Evaluation

The final model achieved approximately **99.99% accuracy, precision, recall, and F1 score on the held-out test set**.

## Tech Stack

| Component        | Technology            |
| ---------------- | --------------------- |
| Model            | ResNet18              |
| Object Detection | YOLOv8                |
| ML Framework     | PyTorch               |
| Backend          | FastAPI               |
| Server           | Uvicorn               |
| Frontend         | HTML, CSS, JavaScript |
| Model Hosting    | Hugging Face Hub      |
| Version Control  | Git / GitHub          |

## Project Structure

```text
asl-video-translator/
│
├── app/
│   ├── api/
│   │   └── translation.py
│   │
│   ├── services/
│   │   └── translation_service.py
│   │
│   ├── frontend/
│   │   ├── index.html
│   │   ├── guide.html
│   │   ├── assets/
│   │   └── js/
│   │
│   └── main.py
│
├── src/
│   └── config.py
│
├── data/
│   └── asl_dataset/
│
├── requirements.txt
├── .env.example
└── README.md
```

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Rohanpatel512/asl-video-translator.git

cd asl-video-translator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example` and provide the required model and Hugging Face configuration.

### 5. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 6. Start the frontend

Serve the frontend using a local HTTP server.

For example:

```bash
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## Using the Translator

For the best recognition results:

1. Allow the browser to access your camera.
2. Position yourself toward the side of the camera frame.
3. Keep your signing hand near the centre of the frame.
4. Keep your hand clearly visible.
5. Use adequate lighting.
6. Sign one letter at a time.
7. For repeated letters, briefly move your hand out of the frame and bring it back before repeating the letter.

The application includes an **ASL Fingerspelling Guide** with example images for each recognized handshape.

## API

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Prediction

```http
POST /translate/translation/predict
```

The endpoint accepts a webcam frame as a multipart file and returns the hand-detection and classification results.

## Input Validation

The backend includes several protections around inference requests:

* Frame validation
* Image decoding validation
* Upload-size limits
* HTTP error handling
* Per-IP request rate limiting
* Health monitoring through `/health`

The rate limiter is intended to prevent excessive requests from a single client rather than provide a complete production-grade abuse-prevention system.

## Limitations

This project recognizes **ASL fingerspelling**, not full American Sign Language.

It does not currently interpret:

* Complete ASL signs
* ASL grammar
* Facial expressions
* Body movements
* Continuous sign-language sentences

Recognition can also be affected by:

* Poor lighting
* Hand occlusion
* Incorrect hand positioning
* Significant background clutter
* Unusual camera angles
* Ambiguous handshapes

The repeated-letter system also requires the hand to briefly leave and re-enter the frame when the same letter is signed consecutively.

## What I Learned

This project involved building an end-to-end computer vision application rather than only training a classification model.

Key areas of experience included:

* Large-scale image dataset preparation
* Train/validation/test split validation
* Data augmentation
* Transfer learning with ResNet18
* CNN model evaluation
* Object detection with YOLOv8
* Combining object detection with image classification
* Real-time webcam processing
* FastAPI inference APIs
* Browser-to-backend communication
* Prediction stabilization for live ML systems
* API validation and error handling
* CORS configuration
* Rate limiting
* ML application architecture

## Future Improvements

Potential improvements include:

* More efficient hand detection
* GPU-backed inference
* Client-side model inference
* Improved repeated-letter detection
* Continuous ASL gesture recognition
* Word-level recognition
* Sentence-level sign-language translation
* Additional real-world training data
* Improved robustness across lighting and backgrounds

## License

This project is intended for educational and portfolio purposes.
