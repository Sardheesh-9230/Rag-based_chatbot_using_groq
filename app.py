import os
import sys
import subprocess
import threading
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from utils.document_processor import DocumentProcessor
from chatbot import RAGChatbot

# Create Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt'}

# Make sure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global chatbot instance
chatbot_instance = None

def get_chatbot():
    """Get or initialize the chatbot instance"""
    global chatbot_instance
    if chatbot_instance is None:
        try:
            chatbot_instance = RAGChatbot()
        except Exception as e:
            print(f"Error initializing chatbot: {e}")
            return None
    return chatbot_instance

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Homepage with upload form and chat interface"""
    # Get list of files in data directory
    files = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], file)) and \
           file.split('.')[-1].lower() in app.config['ALLOWED_EXTENSIONS']:
            files.append(file)
    
    # Check if index exists
    index_exists = os.path.exists('faiss_index.pkl') and os.path.exists('documents_data.pkl')
    
    return render_template('index.html', files=files, index_exists=index_exists)

@app.route('/chat')
def chat_page():
    """Dedicated chat page"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get chatbot instance
        chatbot = get_chatbot()
        if chatbot is None:
            return jsonify({'error': 'Chatbot not initialized. Please upload documents and build index first.'}), 500
        
        # Get response from chatbot
        result = chatbot.chat(message)
        
        return jsonify({
            'response': result['response'],
            'response_points': result['response_points'],
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    files = request.files.getlist('file')
    
    if not files or files[0].filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    file_count = 0
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_count += 1
    
    if file_count > 0:
        flash(f'Successfully uploaded {file_count} file(s)')
    else:
        flash('No valid files were uploaded')
    
    return redirect(url_for('index'))

@app.route('/process', methods=['POST'])
def process_documents():
    """Process documents to build vector index"""
    try:
        # Initialize document processor
        processor = DocumentProcessor(data_dir=app.config['UPLOAD_FOLDER'])
        
        # Process documents
        index, data = processor.process_documents()
        
        # Reset chatbot instance to reload new index
        global chatbot_instance
        chatbot_instance = None
        
        # Count document chunks
        num_chunks = len(data['texts'])
        
        flash(f'Successfully processed documents. Created {num_chunks} chunks.')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Error processing documents: {str(e)}')
        return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Delete a file from the data directory"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'File {filename} deleted successfully')
        else:
            flash(f'File {filename} not found')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}')
    
    return redirect(url_for('index'))

@app.route('/status', methods=['GET'])
def get_status():
    """Get the status of the data and index"""
    files = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], file)) and \
           file.split('.')[-1].lower() in app.config['ALLOWED_EXTENSIONS']:
            files.append(file)
    
    index_exists = os.path.exists('faiss_index.pkl') and os.path.exists('documents_data.pkl')
    
    status = {
        'files': files,
        'index_exists': index_exists,
        'file_count': len(files)
    }
    
    return jsonify(status)

@app.route('/run_chatbot', methods=['GET'])
def run_chatbot():
    """Redirect to chat page instead of running terminal chatbot"""
    return redirect(url_for('chat_page'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(debug=True, port=5000)