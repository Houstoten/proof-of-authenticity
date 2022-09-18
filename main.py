# Start cam capture
# Stop capture, create output files
# Mint NFT with link
# 
# Check provided content if authentic

from flask import Flask, request

from server.authentic_minter import check
from in_out.video_verify import video_verify
from werkzeug.utils import secure_filename

def verify_by_link(name, contentlinkToCheck):
    videohashURL = check(name)
    return video_verify(contentlinkToCheck, videohashURL)

app = Flask(__name__)

@app.route('/upload', methods = ['POST'])
def upload_file():
    f = request.files['file']
    name = request.form.get("name")
    if f is not None and name is not None:
        filename = secure_filename(f.filename)
        content_link = "./static/" + filename
        f.save(content_link)

        if verify_by_link(name, content_link):
            return "True"


    return "False"

app.run(None, 4000)


# verify_by_link('cam_video', './static/')