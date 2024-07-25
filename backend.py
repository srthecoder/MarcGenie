from flask import Flask, request, send_from_directory, jsonify
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Directory to save files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/auto', methods=['POST'])
def process_file():
    if 'marcFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['marcFile']
    output_name = request.form['outputName']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Call your auto.py script with the file
    result = subprocess.run(['python', 'auto.py', file_path, os.path.join(UPLOAD_FOLDER, output_name)],
                            capture_output=True, text=True)
    
    if result.returncode != 0:
        return jsonify({'error': 'Processing failed'}), 500
    
    output_files = {
        'txt': os.path.join(UPLOAD_FOLDER, f'{output_name}.txt'),
        'mrc': os.path.join(UPLOAD_FOLDER, f'{output_name}.mrc'),
        'skipped': os.path.join(UPLOAD_FOLDER, f'{output_name}_SkippedRecords.mrc')
    }
    
    return jsonify(output_files)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
    
    
# from flask import Flask, request, jsonify
# import subprocess
# import os

# app = Flask(__name__)

# @app.route('/auto', methods=['POST'])
# def auto():
#     marc_file = request.files['marcFile']
#     output_name = request.form['outputName']

#     input_filepath = os.path.join('uploads', marc_file.filename)
#     output_txt = output_name + '.txt'
#     output_mrc = output_name + '.mrc'
#     skip_output = output_name + 'SkippedRecords.mrc'

#     # Save the uploaded file
#     marc_file.save(input_filepath)

#     try:
#         # Call the auto.py script
#         subprocess.run(['python3', 'auto.py', input_filepath, output_name], check=True)

#         return f"Processing complete. Files created: {output_txt}, {output_mrc}, {skip_output}"

#     except subprocess.CalledProcessError as e:
#         return str(e), 500

# if __name__ == '__main__':
#     os.makedirs('uploads', exist_ok=True)
#     app.run(debug=True)
