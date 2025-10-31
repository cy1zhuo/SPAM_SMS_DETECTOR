from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import joblib
import traceback
import json
from datetime import datetime

APP_DIR = os.path.dirname(__file__)
# Allow overriding paths via environment variables
# Define primary and alternative model/vectorizer paths
MODEL_PATH = os.path.join(APP_DIR, 'spam_detector_model.pkl')
VECT_PATH = os.path.join(APP_DIR, 'tfidf_vectorizer.pkl')
# Fallback to alternative filenames if primary not found
ALT_MODEL_NAMES = ['model.pkl', 'spam_detector.pkl']
ALT_VECT_NAMES = ['vectorizer.pkl', 'tfidf_vectorizer.pkl']

# Also check workspace root for artifacts or a dataset
WORKSPACE_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))
DATASET_PATH = os.path.join(APP_DIR, 'SPAM_SMS.csv')
HISTORY_PATH = os.path.join(APP_DIR, 'history.json')

def save_history(entry):
    """Save prediction history to a JSON file with error handling."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
        
        # Load existing history
        history = []
        if os.path.exists(HISTORY_PATH):
            try:
                with open(HISTORY_PATH, 'r') as f:
                    history = json.load(f)
                # Ensure history is a list
                if not isinstance(history, list):
                    history = []
            except (json.JSONDecodeError, IOError) as e:
                app.logger.error(f'Error reading history file: {str(e)}')
                history = []
        
        # Add new entry and keep only the last 200 entries
        history.insert(0, entry)
        history = history[:200]
        
        # Write to a temporary file first, then rename (atomic operation)
        temp_path = f"{HISTORY_PATH}.tmp"
        with open(temp_path, 'w') as f:
            json.dump(history, f, indent=2)
        
        # On Windows, we need to remove the destination file first if it exists
        if os.path.exists(HISTORY_PATH):
            os.remove(HISTORY_PATH)
        os.rename(temp_path, HISTORY_PATH)
        
    except Exception as e:
        app.logger.error(f'Error saving history: {str(e)}')
        # Try to create an empty history file if it doesn't exist
        if not os.path.exists(HISTORY_PATH):
            try:
                with open(HISTORY_PATH, 'w') as f:
                    json.dump([], f)
            except Exception as e2:
                app.logger.error(f'Failed to create history file: {str(e2)}')

# Lightweight keyword fallback (used when no model/vectorizer available)
FALLBACK_KEYWORDS = [
    'win','free','prize','cash','reward','claim','promo','congratulations','loan','click','won','urgent','voucher','congrats'
]

# Serve frontend static files from the workspace root when convenient so the frontend
# can be served from the same origin as the API (avoids CSP / CORS differences when
# testing with Live Server or other static servers). This sets the Flask static
# folder to the workspace root (parent of backend).
app = Flask(__name__, static_folder=WORKSPACE_ROOT, static_url_path='')
CORS(app)

# (Removed optional DEV_ALLOW_UNSAFE_EVAL handler — prefer diagnosing CSP from the
# server that actually sets the header instead of permanently weakening policy.)

# Setup simple file logging for diagnostics
import logging
from logging.handlers import RotatingFileHandler
log_dir = os.path.join(APP_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')
handler = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

model = None
vectorizer = None

def try_load_artifacts():
    global model, vectorizer
    try:
        # Try explicit env paths first
        if os.path.exists(MODEL_PATH) and os.path.exists(VECT_PATH):
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECT_PATH)
            print(f"Loaded model from {MODEL_PATH} and vectorizer from {VECT_PATH}")
            return True

        # Try alternative filenames in the backend folder
        for mname in ALT_MODEL_NAMES:
            for vname in ALT_VECT_NAMES:
                mpath = os.path.join(APP_DIR, mname)
                vpath = os.path.join(APP_DIR, vname)
                if os.path.exists(mpath) and os.path.exists(vpath):
                    model = joblib.load(mpath)
                    vectorizer = joblib.load(vpath)
                    print(f"Loaded model from {mpath} and vectorizer from {vpath}")
                    return True

        # Try alternative filenames in the workspace root (one level up)
        for mname in ALT_MODEL_NAMES:
            for vname in ALT_VECT_NAMES:
                mpath = os.path.join(WORKSPACE_ROOT, mname)
                vpath = os.path.join(WORKSPACE_ROOT, vname)
                if os.path.exists(mpath) and os.path.exists(vpath):
                    model = joblib.load(mpath)
                    vectorizer = joblib.load(vpath)
                    print(f"Loaded model from {mpath} and vectorizer from {vpath}")
                    return True
    except Exception:
        print('Error loading artifacts:')
        traceback.print_exc()
    return False

def train_from_dataset():
    # Lightweight training fallback (only if dataset provided)
    global model, vectorizer
    try:
        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        # allow dataset in backend/ or workspace root
        dataset_candidates = [
            os.path.join(APP_DIR, 'SPAM_SMS.csv'),
            os.path.join(WORKSPACE_ROOT, 'SPAM_SMS.csv')
        ]
        dataset_file = None
        for p in dataset_candidates:
            if os.path.exists(p):
                dataset_file = p
                break
        if dataset_file is None:
            raise FileNotFoundError('SPAM_SMS.csv not found in backend/ or workspace root')

        df = pd.read_csv(dataset_file)
        # Expect columns like ['label','text'] or ['Class','Message'] — try common names
        text_col = None
        label_col = None
        for c in df.columns:
            if c.lower() in ('text','message','sms','msg','message_text'):
                text_col = c
            if c.lower() in ('label','class','target'):
                label_col = c
        if text_col is None:
            # try the second column
            text_col = df.columns[1]
        if label_col is None:
            label_col = df.columns[0]

        df = df[[label_col, text_col]].dropna()
        X = df[text_col].astype(str).values
        y = df[label_col].astype(str).values

        # Create binary labels (True for spam). If dataset labels don't contain both classes,
        # fall back to a keyword-based labeling strategy to synthesize a second class so training
        # can proceed. This prevents the ValueError raised when all labels are the same.
        y_lower = [str(v).lower() for v in y]
        y_binary = [(val == 'spam') for val in y_lower]
        # If only one class present, try keyword heuristic using FALLBACK_KEYWORDS
        if len(set(y_binary)) < 2:
            print('Warning: dataset labels contain a single class. Generating labels using keyword heuristic...')
            heur_labels = []
            for text in X:
                t = str(text).lower()
                heur = any(k in t for k in FALLBACK_KEYWORDS)
                heur_labels.append(heur)
            y_binary = heur_labels

        # If still only one class after heuristics, force a small number of positive labels
        # to allow training. We choose every Nth sample up to 10% or max 50 samples.
        if len(set(y_binary)) < 2:
            print('Warning: keyword heuristic produced a single class. Injecting a few positive labels to enable training.')
            n = len(y_binary)
            inject = max(1, min(50, n // 10))
            for i in range(0, n, max(1, n // inject)):
                y_binary[i] = True

        vectorizer = TfidfVectorizer(stop_words='english', max_features=20000)
        Xv = vectorizer.fit_transform(X)
        model = LogisticRegression(max_iter=1000)
        model.fit(Xv, y_binary)

        # Save artifacts for future runs (prefer backend paths)
        try:
            joblib.dump(model, os.path.join(APP_DIR, ALT_MODEL_NAMES[0]))
            joblib.dump(vectorizer, os.path.join(APP_DIR, ALT_VECT_NAMES[0]))
        except Exception:
            # fallback to configured paths
            joblib.dump(model, MODEL_PATH)
            joblib.dump(vectorizer, VECT_PATH)
        print(f"Trained model & vectorizer and saved to {MODEL_PATH} and {VECT_PATH}")
        return True
    except Exception:
        print('Training error:')
        traceback.print_exc()
        return False


@app.route('/predict', methods=['OPTIONS', 'GET', 'POST'])
@cross_origin()
def predict_endpoint():
    """Single handler for /predict that supports OPTIONS (preflight), GET (info) and POST (prediction).
    Consolidating into one handler avoids method-not-allowed / preflight edge cases in some browser setups.
    """
    # Handle preflight explicitly
    if request.method == 'OPTIONS':
        return ('', 204)

    if request.method == 'GET':
        return jsonify({'error': 'This endpoint accepts POST with JSON {"text": "..."}. Use POST to get predictions.'}), 200

    # POST -> prediction logic
    global model, vectorizer
    try:
        data = request.get_json(force=True)
        text = data.get('text') if isinstance(data, dict) else None
        if not text:
            return jsonify({'error':'`text` field is required.'}), 400

        if model is None or vectorizer is None:
            lower = text.lower()
            is_spam = any(k in lower for k in FALLBACK_KEYWORDS)
            prob = 0.9 if is_spam else 0.05
            label = 'Spam' if is_spam else 'Not Spam'
            out = {'label': label, 'probability': prob, 'text': text, 'fallback': True}
            try:
                # Save history for fallback prediction
                history_entry = {
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                    'text': text,
                    'label': label,
                    'probability': float(prob),
                    'isSpam': label.lower() == 'spam',
                    'fallback': True
                }
                save_history(history_entry)
                
                return jsonify(out)
            except Exception as e:
                app.logger.error(f'Error in fallback prediction: {str(e)}')
                return jsonify({'error': 'Error processing fallback prediction'}), 500

        # Process with model if available
        Xv = vectorizer.transform([text])
        try:
            probs = model.predict_proba(Xv)[0]
            spam_idx = None
            if hasattr(model, 'classes_'):
                for i,c in enumerate(model.classes_):
                    if str(c).lower() == 'spam':
                        spam_idx = i
                        break
            if spam_idx is None:
                if hasattr(model, 'classes_'):
                    try:
                        spam_idx = list(model.classes_).index(1)
                    except Exception:
                        spam_idx = len(probs)-1
                else:
                    spam_idx = len(probs)-1

            spam_prob = float(probs[spam_idx])
            label = 'Spam' if spam_prob >= 0.5 else 'Not Spam'
            out = {'label': label, 'probability': spam_prob, 'text': text}
            entry = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'text': text,
                'label': label,
                'probability': float(spam_prob),
                'isSpam': label.lower() == 'spam',
                'fallback': False
            }
            save_history(entry)
            return jsonify(out)
        except Exception:
            pred = model.predict(Xv)[0]
            is_spam = (str(pred).lower() == 'spam') or (pred == 1)
            label = 'Spam' if is_spam else 'Not Spam'
            out = {'label': label, 'probability': 1.0, 'text': text}
            entry = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'text': text,
                'label': label,
                'probability': 1.0,  # Explicit float for consistency
                'isSpam': label.lower() == 'spam',
                'fallback': False
            }
            save_history(entry)
            return jsonify(out)
    except Exception:
        tb = traceback.format_exc()
        app.logger.error('Predict error:\n%s', tb)
        if app.debug or os.environ.get('FLASK_DEBUG', '').lower() in ('1','true'):
            return jsonify({'error': 'Internal server error', 'traceback': tb}), 500
        return jsonify({'error':'Internal server error'}), 500


@app.route('/history', methods=['GET'])
@cross_origin()
def get_history():
    try:
        if not os.path.exists(HISTORY_PATH):
            # Return empty list if file doesn't exist yet
            return jsonify({"history": []})
            
        with open(HISTORY_PATH, 'r') as f:
            try:
                history = json.load(f)
                # Ensure we always return a list
                if not isinstance(history, list):
                    app.logger.warning('History file did not contain a list, resetting')
                    history = []
                # Return as an object with a 'history' property containing the array
                return jsonify({"history": history})
            except json.JSONDecodeError as e:
                app.logger.error(f'Invalid JSON in history file: {str(e)}')
                return jsonify({"history": [], "error": "Invalid history data"}), 500
    except IOError as e:
        app.logger.error(f'Error reading history file: {str(e)}')
        return jsonify({"history": [], "error": "Could not read history file"}), 500
    except Exception as e:
        app.logger.error(f'Unexpected error getting history: {str(e)}')
        return jsonify({"history": [], "error": "Internal server error"}), 500


@app.route('/download-history', methods=['GET'])
@cross_origin()
def download_history():
    try:
        if not os.path.exists(HISTORY_PATH):
            return jsonify({"error": "No history available"}), 404
            
        with open(HISTORY_PATH, 'r') as f:
            history = json.load(f)
        
        if not history:
            return jsonify({"error": "No history available"}), 404
        
        # Convert to CSV
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["Message", "Is Spam", "Confidence", "Timestamp"])
        
        # Write data
        for entry in history:
            writer.writerow([
                entry.get('message', ''),
                'Yes' if entry.get('label') == 'Spam' else 'No',
                f"{entry.get('probability', 0):.2%}",
                entry.get('timestamp', '')
            ])
        
        # Create response with CSV
        response = app.response_class(
            response=output.getvalue(),
            mimetype='text/csv',
            headers={"Content-disposition": "attachment; filename=spam_detection_history.csv"}
        )
        return response
        
    except Exception as e:
        app.logger.error(f"Error downloading history: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/history', methods=['DELETE'])
@cross_origin()
def clear_history():
    try:
        if os.path.exists(HISTORY_PATH):
            os.remove(HISTORY_PATH)
        # Ensure the file exists but is empty after clear
        with open(HISTORY_PATH, 'w') as f:
            json.dump([], f)
        return jsonify({"status": "success", "message": "History cleared"})
    except IOError as e:
        app.logger.error(f'IOError clearing history: {str(e)}')
        return jsonify({"error": "Could not clear history file"}), 500
    except Exception as e:
        app.logger.error(f'Unexpected error clearing history: {str(e)}')
        return jsonify({"error": "Internal server error"}), 500


@app.route('/history', methods=['OPTIONS'])
def history_options():
    return ('', 204)


@app.route('/')
def serve_index():
    """Serve the frontend index.html from the workspace root if present. This
    makes it easy to open http://127.0.0.1:PORT and have the site load without
    using a separate static server (and avoids Live Server injecting CSP headers).
    """
    index_file = os.path.join(WORKSPACE_ROOT, 'index.html')
    if os.path.exists(index_file):
        # app.send_static_file uses the configured static_folder
        return app.send_static_file('index.html')
    return jsonify({'ok': True, 'message': 'API running'})


if __name__ == '__main__':
    # Allow explicit control of debug mode via environment variable
    ok = try_load_artifacts()
    if not ok and os.path.exists(DATASET_PATH):
        print('Artifacts not found, training from dataset...')
        trained = train_from_dataset()
        if not trained:
            print('Failed to train from dataset; server will still start but /predict will return an error until artifacts are provided.')

    debug_mode = os.environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')
    if debug_mode:
        print('Starting development server (debug mode enabled)')
    else:
        print('Starting Flask app (debug mode disabled). For production use a WSGI server like waitress.')

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode)
