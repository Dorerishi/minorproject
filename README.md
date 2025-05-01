# Brain Tumor Detection using Vision Transformer (ViT)

## Project Overview

This is a Django-based web application for brain tumor detection using a Vision Transformer (ViT) model.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone "https://github.com/Dorerishi/minorproject.git"
cd minorproject
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Pre-trained Model

#### Kaggle Model Download

1. Download the model from: [Brain Tumor Using ViT Kaggle](https://www.kaggle.com/code/hri0123/brain-tumor-using-vit/output)
2. Place the `best_vit_model.pth` file in the `scans/` directory

#### Manual Download Steps

- Go to the Kaggle link
- Download the `best_vit_model.pth`
- Place the file in `scans/best_vit_model.pth`

### 5. Configure Kaggle Credentials

- Create a `kaggle.json` file in the project root
- Add your Kaggle API credentials
- Ensure this file is kept private and not committed to version control

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Start Development Server

```bash
python manage.py runserver
```

## Project Structure

- `scans/`: Main application directory
- `minorproject/`: Project configuration
- `media/`: User uploaded files
- `static/`: Static files
- `best_vit_model.pth`: Pre-trained Vision Transformer model
