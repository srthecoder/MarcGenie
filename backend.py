from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/auto', methods=['POST'])
def auto():
    marc_file = request.files['marcFile']
    output_name = request.form['outputName']

    input_filepath = os.path.join('uploads', marc_file.filename)
    output_txt = output_name + '.txt'
    output_mrc = output_name + '.mrc'
    skip_output = output_name + 'SkippedRecords.mrc'

    # Save the uploaded file
    marc_file.save(input_filepath)

    try:
        # Call the auto.py script
        subprocess.run(['python3', 'scripts/auto.py', input_filepath, output_name], check=True)

        return f"Processing complete. Files created: {output_txt}, {output_mrc}, {skip_output}"

    except subprocess.CalledProcessError as e:
        return str(e), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
