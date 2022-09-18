# Start cam capture
# Stop capture, create output files
# Mint NFT with link
# 
# Check provided content if authentic

from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods = ['POST'])
def upload_file():
    f = request.files['file']
    print(f.filename)

app.run(None, 4000)