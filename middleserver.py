from flask import Flask, request, jsonify
import json,os,requests
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/message/sendtext",methods=['POST'])
def process_text():
    url = os.environ['jaredurl']+'/message'
    payload = {'body':{'message':request.form.getlist('message')[0]},'recipient':{'handle':request.form.getlist('handle')[0]}}
    print('\n',payload,'\n')
    r = requests.request('POST',url,data=json.dumps(payload))
    print('\n',r,r.text)
    return(f"Jared says {r}")   

@app.route("/message/sendimage", methods=["POST"])
def process_image():
    # This API will receive a photo, save it, then tell Jared to send it
    saveloc = os.environ['HOME']+'/Pictures/'
    file = request.files['image'] # Needs to be a tuple. 'images':('requestedsavelocation',open(filename,'rb'),'image/jpeg')
    names = file.filename.split('/') # Split the passed filename by /
    filename = names[-1] # This works for multiple subfolders and just an image name
    if len(names) > 1: # Rebuild the directory path without the image name
        for subdir in names[:-1]:
            saveloc = os.path.join(saveloc,subdir)
    if not os.path.exists(saveloc): # If the directory path doesn't exist, build it
        print('Creating directory',saveloc)
        os.makedirs(saveloc)
    saveloc = os.path.join(saveloc,filename) # Join the saveloc (whether changed or original) with the image name
    file.save(saveloc)
    url = os.environ['jaredurl']+'/message'

    payload = {"attachments":[{"filePath": saveloc}],'recipient':{'handle':request.form.get('recipient')}}
    r = requests.request('POST',url,data=json.dumps(payload))
    print('\n',r,r.text)
    return(f"Jared says {r}")

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, host='0.0.0.0', port = 3005, ssl_context="adhoc")






