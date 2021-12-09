# macOS
# python3 -m venv .venv
# source .venv/bin/activate

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import torch
from utils import *
from glob import glob





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
  store_path = os.path.join(app.instance_path,'htmlfi')
  files = glob(os.path.join(store_path,'*.jpg'))
  for file in files:
    os.remove(file)
  f.save(os.path.join(app.instance_path, 'htmlfi', secure_filename(f.filename)))
  files = glob(os.path.join(store_path,'*.jpg'))
  os.rename(files[0],store_path+"/golf.jpg")

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

  pts = glob('./instance/*.pt')
  num_pts = len(pts)
  curr_pt_name = './instance/box%d'%num_pts
  path = curr_pt_name+".pt"
  model = torch.load(path)

  new_box = [x,y,width,hieght,torch.tensor(1.0000),torch.tensor(1.0000),torch.tensor(0)]
  model.append(new_box)
  torch.save(model, path)
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
  txtfile1 = "./instance/box1.txt"
  txtfile2 = "./instance/box2.txt"
  print("distance")
  pred_files = glob('./instance/*.txt')

  if(len(pred_files)==2 and os.path.exists(txtfile1) and os.path.exists(txtfile2)):
    for file in glob("./instance/*.csv"):
      if(os.path.isfile(file)):
        os.remove(file)
    os.system('python distance.py')
    for file in glob("./instance/*.pt"):
      if(os.path.isfile(file)):
        os.remove(file)
    os.remove(txtfile1)
    os.remove(txtfile2)
  else:
    error_message = {0:"No prediction text files generated. Please input two images",\
                     1: "Only 1 prediction text files generated. Please input image from the second angle"}
    assert False, error_message[len(pred_files)]

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