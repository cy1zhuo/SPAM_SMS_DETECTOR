# SPAM_SMS_DETECTOR
SMS Spam Detector A machine learning web app that identifies spam messages with >95% accuracy. Built with Python (Flask) and JavaScript, it features real-time classification, a clean interface, and a RESTful API. The model uses TF-IDF and Logistic Regression to filter unwanted messages. Perfect for learning NLP and ML deployment.
<div align="center">
  <h1>📱 SMS Spam Detection System</h1>
  <p>
    <strong>A machine learning-powered solution for detecting spam SMS messages</strong>
  </p>
  <p>
    <a href="#features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#api-documentation">API</a> •
    <a href="#development">Development</a>
  </p>
  
  [![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
  [![Flask](https://img.shields.io/badge/flask-2.0.1-green.svg)](https://flask.palletsprojects.com/)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
</div>

## ✨ Features

- 🚀 **Real-time Detection**: Instantly classify SMS messages as spam or ham
- 🎯 **High Accuracy**: Powered by machine learning with TF-IDF and Logistic Regression
- 🖥️ **User-Friendly Interface**: Clean, responsive web interface for easy interaction
- ⚙️ **Flexible Deployment**: Supports both pre-trained models and on-the-fly training
- 🔄 **RESTful API**: Seamless integration with other applications
- 📊 **CSV Support**: Easy model training from labeled datasets
- 🔒 **CORS Enabled**: Secure cross-origin requests for development

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, or Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SPAM-SMS-Detector.git
   cd SPAM-SMS-Detector
   ```

2. **Set up a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Run the application**
   ```bash
   # Start the Flask backend
   python backend/app.py
   ```
   Then open `index.html` in your browser to access the web interface.

## 📂 Project Structure

```
SPAM-SMS-Detector/
├── index.html          # Frontend interface
├── style.css           # Styling for the web interface
├── script.js           # Frontend JavaScript logic
└── backend/
    ├── app.py          # Flask application
    ├── requirements.txt # Python dependencies
    ├── model.pkl       # Pre-trained model (generated)
    └── vectorizer.pkl  # Text vectorizer (generated)
```

## 🔍 Usage

### Using Pre-trained Models
1. Place your trained `model.pkl` and `vectorizer.pkl` in the `backend/` directory
2. Start the Flask backend: `python backend/app.py`
3. Open `index.html` in your browser
4. Enter an SMS message and click "Check" to see the classification

### Training a New Model
1. Place your `SPAM_SMS.csv` in the `backend/` folder with 'label' and 'text' columns
2. Delete any existing `model.pkl` and `vectorizer.pkl` files
3. Start the application - it will automatically train a new model

## 📚 API Documentation

### `POST /predict`
Classify an SMS message as spam or ham.

**Request:**
```json
{
    "message": "Your SMS text here"
}
```

**Response:**
```json
{
    "prediction": "spam" | "ham",
    "confidence": 0.95
}
```

## 🛠 Development

### Running Tests
```bash
# Coming soon
```

### Production Deployment
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 'backend.app:create_app()'
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Made with ❤️ by [Your Name] | [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyourusername%2FSPAM-SMS-Detector)](https://twitter.com/intent/tweet?text=Check%20out%20this%20awesome%20SMS%20Spam%20Detector!%20%F0%9F%94%A5&url=https%3A%2F%2Fgithub.com%2Fyourusername%2FSPAM-SMS-Detector)
</div>
- Cross-Origin Resource Sharing (CORS) enabled

    ├── app.py          # Flask application
    ├── requirements.txt # Python dependencies
    ├── model.pkl       # Trained model (generated)
    └── vectorizer.pkl  # Text vectorizer (generated)
```

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, or Edge)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd SPAM_SMS-Project
   ```

2. Create and activate a virtual environment:
   - Windows:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Install the required Python packages:
   ```bash
   pip install -r backend/requirements.txt
   ```

## Usage

### Option 1: Using Pre-trained Models
1. Place your trained `model.pkl` and `vectorizer.pkl` files in the `backend/` directory.
2. Start the Flask backend:
   ```bash
   python backend/app.py
   ```
3. Open `index.html` in your web browser.
4. Enter an SMS message and click "Check" to see if it's classified as spam.

### Option 2: Automatic Model Training
1. Place your `SPAM_SMS.csv` dataset in the `backend/` folder with 'label' and 'text' columns.
2. Start the application (the backend will automatically train a new model if no model files are found).

## Model Training

The system uses a TF-IDF vectorizer and Logistic Regression classifier by default. The model is trained to classify messages as either "spam" or "ham" (not spam).

### Training Data Format
Your training CSV should include:
- `label`: 'spam' or 'ham'
- `text`: The SMS message content

## API Endpoints

- `POST /predict`: Classify an SMS message
  - Request body: `{"message": "Your SMS text here"}`
  - Response: `{"prediction": "spam" | "ham"}`

## Development

### Running Tests
To be implemented.

### Building for Production
For production deployment, consider using a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 'backend.app:create_app()'
```

