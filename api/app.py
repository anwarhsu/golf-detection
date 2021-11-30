# macOS
# python3 -m venv .venv
# source .venv/bin/activate

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import torch
from utils import *





UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__,static_folder='instance/htmlfi',
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"
os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)



@app.route('/api',methods=["GET"])
def api():
  return {
    'userID' : 2,
    'title': 'Flask React fsa',
    'completed': False
  }

  
@app.route('/upload', methods=['POST'])
def fileUpload():
  print("POST")
  f = request.files['file']
  print(f)
  f.save(os.path.join(app.instance_path, 'htmlfi', secure_filename(f.filename)))

  # uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file))


  return "Upload complete"    


@app.route('/edit', methods=['POST'])
def editData():
  print("POST")
  data = request.get_json(force=True)
  print(data)
  img_width = 700
  x = abs(data['userBox']['left_x'] + data['userBox']['right_x']) / 2
  y = abs(data['userBox']['left_y'] + data['userBox']['right_y']) / 2
  x = x/img_width
  y = y/img_width
  width = abs(data['userBox']['left_x'] - data['userBox']['right_x'])/img_width
  hieght = abs(data['userBox']['left_y'] - data['userBox']['right_y'])/img_width
  print(x,y,width,hieght)

  x = torch.tensor(x)
  y = torch.tensor(y)
  width = torch.tensor(width)
  hieght = torch.tensor(hieght)

  path = './instance/box.pt'
  model = torch.load(path)

  new_box = [x,y,width,hieght,torch.tensor(1.0000),torch.tensor(1.0000),torch.tensor(0)]
  model.append(new_box)
  torch.save(model, './instance/box.pt')
  print("EDIT")
  os.system('python edit.py')
  
  # y = 
  # width = 
  # height = 
  # uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file))


  return "hi"    

@app.route('/yolo', methods=['get'])
def yolo():
  print("YOLO")
  os.system('python YOLO.py')


  return {
    'userID' : 2,
    'title': 'Flask React fsa',
    'completed': False
  }

@app.route('/distance', methods=['get'])
def distance():
  print("distance")
  os.system('python distance.py')


  return {
    'userID' : 2,
    'title': 'Flask React fsa',
    'completed': False
  }

  # uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file))



  


if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.debug = True
    app.run()