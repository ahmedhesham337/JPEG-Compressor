from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
import os
import string
import random
import json
import base64
import numpy as np

import JPEG
import compression

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

UPLOAD_FOLDER = "./upload"
OUTPUT_FOLDER = "./output"

app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getRandomName():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@app.route("/image/<imageid>", methods=["GET"])
def returnImage(imageid):
    path = "{}/{}.jpeg".format(OUTPUT_FOLDER, imageid)
    if os.path.exists(path):
        return send_file(path)
    else:
        return 404

@app.route("/stats/<imageid>", methods=["GET"])
def returnStats(imageid):
    
    if imageid == "default":
        x = {
            "new_size": 92858,
            "original_size": 1075997,
            "ratio": 91.37
        }
        return jsonify(x)
    
    path = "{}/{}.json".format(OUTPUT_FOLDER, imageid)
    if os.path.exists(path):
        with open(path, "r") as f:
            dat = f.read()
        x = json.loads(dat)
        return jsonify(x)
    else:
        return 404

@app.route("/default/<imageType>", methods=['GET'])
def returnDefault(imageType):
    if imageType == "original":
        return send_file("./defaults/orig.png")
    elif imageType == "compressed":
        return send_file("./defaults/comp.jpeg")
    else:
        return 404

@app.route("/compress", methods=["POST"])
def doCompress():

    imageFile            = request.files["img"]
    blockSize            = int(request.form["blockSize"])
    quantizaionScale     = int(request.form["quantizationScale"])
    compressionAlgorithm = compression.COMPRESSION_ALGORITHMS(int(request.form["compressionAlgorithm"]))
    useDefaultMatrix     = bool(int(request.form["useDefaultMatrix"]))
    downSampleColor      = bool(int(request.form["downSampleColor"]))

    print(quantizaionScale)
    print(useDefaultMatrix)

    fileExtension    = imageFile.filename.split(".")[-1] if len(imageFile.filename.split(".")) > 1 else "unknown"
    randomName       = getRandomName()
    fileName         = "{}.{}".format(randomName, fileExtension)

    path = os.path.join(app.config['UPLOAD_FOLDER'], fileName)
    imageFile.save(path)

    encoder = JPEG.JPEGEncoder(
        path, blockSize, quantizaionScale, compressionAlgorithm, useDefaultMatrix, downSampleColor
    )
    encoder.compress()
    encoder.save_compressed_file("{}/{}".format(OUTPUT_FOLDER, randomName))
    compressed = encoder.get_compressed_image()
    comppstats = encoder.get_stats()

    decoder = JPEG.JPEGDecoder(
        compressed, 
        comppstats["block_size"], 
        comppstats["quantization_matrix"],
        comppstats["trans_shape"],
        comppstats["compression"],
        comppstats["color_downsampled"]
    )
    decoder.decompress()
    decoder.save_decompressed_image("{}/{}".format(OUTPUT_FOLDER, randomName))

    oldsz = os.path.getsize(path)
    newsz = os.path.getsize("{}/{}.jpeg".format(OUTPUT_FOLDER, randomName))
    compr = round((1 - (newsz / oldsz)) * 100, 2)

    decompstats = {
        "original_size": oldsz,
        "new_size": newsz,
        "ratio": compr
    }

    del comppstats["original_file_name"]
    del comppstats["compressed_blob_size"]

    with open("{}/{}.json".format(OUTPUT_FOLDER, randomName), "w") as f:
        f.write(json.dumps(decompstats))
    
    with open("{}/{}.metadata".format(OUTPUT_FOLDER, randomName), "w") as f:
        f.write(base64.b64encode(json.dumps(comppstats, cls=NumpyArrayEncoder).encode()).decode())

    return randomName

def main():
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    
    app.run()

if __name__ == "__main__":
    main()