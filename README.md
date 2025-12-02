# Pokémon Type Predictor

A web application that predicts Pokémon types from images using multiple CNN models. Users can upload Pokémon images (including fan-made fakemon) and see predictions from different models, compare them, and store past predictions locally in the browser.

---

## Features

- **Upload & Predict**: Upload any image and get predicted types from multiple models.
- **Multiple Models**: Compare predictions across five different models (A–E).
- **IndexedDB Caching**: Stores predictions and images locally for fast retrieval.
- **Interactive Dex**: Browse uploaded images and view predictions with quick access.

---

## How It Works

1. **Upload Image**: Users uploads an image of their "Pokemon" and selection of model.
2. **Model Prediction**: The image is sent to the backend, where CNN models predict type probabilities.
3. **Store Locally**: Predictions and images are saved in IndexedDB.
4. **Compare Models**: Users can toggle between different trained models to see variation in predictions.

---

## Training & Models

- **Base Models**: EfficientNetB0 (Models A–C), ResNet50 (Models D–E)
- **Architecture**:
  - Base pretrained on ImageNet
  - Frozen convolutional layers
  - GlobalAveragePooling → Dropout → Dense(18, sigmoid)
- **Loss & Metrics**:
  - Binary Cross-Entropy for multi-label classification
  - AUC (Area Under the Curve) for evaluation
- **Dataset**:
  - Training: 721 images, 18 possible types
  - Validation: 280 fan-made Pokémon/fakemon images
  - Random augmentation: rotations, reflections, brightness, etc.
  - Note: Imbalanced type distribution (e.g., 118 water types, 37 ice types)

---

## Technology Used

- **Frontend**:
  - [Next.js](https://nextjs.org/) – React framework
  - [Tailwind CSS](https://tailwindcss.com/) – Utility-first CSS framework
  - [AugmentedUI](https://augmented-ui.com/) – Enhanced UI styling
- **Backend**:
  - [Flask](https://flask.palletsprojects.com/) – Python web framework
- **Machine Learning**:
  - [TensorFlow](https://www.tensorflow.org/) + [Keras](https://keras.io/) – CNN models for image classification
- **Storage**:
  - IndexedDB – Browser-side caching of predictions and images

---
