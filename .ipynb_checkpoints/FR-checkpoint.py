import streamlit as st
from PIL import Image

import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io
import json

st.title('顔認識アプリ')

with open('secret.json') as f:
    secret_json = json.load(f)

subscription_key = secret_json["SUBSCRIPTION_KEY"]
assert subscription_key

face_api_url ='https://yoshifacerec.cognitiveservices.azure.com/face/v1.0/detect'


uploaded_file = st.file_uploader("ここにイメージを挿入",type={'jpg','png'})
if uploaded_file is not None:
    img1 = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img1.save(output,format="JPEG")
        binary_img =output.getvalue()
    headers = {
    'Content-Type':'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key 
}

    params = {
    'returnFaceId':'true',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'

}
    res =requests.post(face_api_url,params=params,
                       headers=headers,data=binary_img) 
    
    draw =ImageDraw.Draw(img1) 
    font_size = 24
    font_name = "C:\Windows\Fonts\meiryo.ttc"
    src = r"pillow_test_src.png"
    dest= r"pillow_test_dest.png"
    
    results =res.json()
    for result in results:
        rect =result['faceRectangle']  
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=5)
        draw_x = rect['left']-30
        draw_y = rect['top']-30

        text = result['faceAttributes']['gender']+'/'+str(result['faceAttributes']['age'])
#         print(age,gender)
        font = ImageFont.truetype(font_name, font_size)
        draw.text((draw_x, draw_y), text,font=font, fill='red')
      
    st.image(img1,caption="認識した写真",use_column_width=True)