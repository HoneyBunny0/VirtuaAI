import streamlit as st
import torch
from PIL import Image
import cv2
import numpy as np
from pages.settings import *
from utilsPerso import load_image, get_colors, CLASSES
from streamlit_tags import st_tags

def newImage():
  return

if __name__ == '__main__':
    st.markdown("# VirtuaAI 🧠")
    st.sidebar.markdown("# Main page 🧠")

    image_file = st.sidebar.file_uploader("Load Images", type=["png","jpg","jpeg"])

    if image_file is not None:
      # To See details
      file_details = {"filename":image_file.name, "filetype":image_file.type,
                      "filesize":image_file.size}

      # To View Uploaded Image with details
      st.sidebar.image(load_image(image_file), width=250)
      st.sidebar.write(file_details)

      img = Image.open(image_file)

      # Get the model (pre trained for the moment)
      model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

      # Get predictions
      preds = model([img])
      preds = preds.xyxy[0].cpu().numpy() # rectangle pixels, accuracy, label id

      npImg = np.squeeze(img)

      labels = list(set([CLASSES[int(preds[i][5])] for i in range(len(preds))]))
      colors = get_colors(CLASSES)
      
      c = st.container()

      userInput = st_tags(label="## Describe the picture :",
        text='Press enter to add more',
        value=[],
        suggestions=labels,
        key='1',
        maxtags=len(labels)
      )

      for pred in preds:
        x1,y1 = int(pred[0]), int(pred[1])
        x2,y2 = int(pred[2]), int(pred[3])

        label = CLASSES[int(pred[5])]

        if (label not in userInput):
          continue

        color = colors[label]
        
        if getAccuracyVisible:
          label += ":{0:.2f}%".format(pred[4])

        cv2.rectangle(npImg, (x1, y1), (x2, y2), color, 3)

        text_color = (0,0,0) if (color[0]*0.299 + color[0]*0.587 + color[0]*0.114 > 186) else (255,255,25)

        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

        offset = 0 if y1 > 20 else 20
        cv2.rectangle(npImg, (x1, y1 - 20 + offset), (x1 + w, y1 + offset), color, -1)
        cv2.putText(npImg, label, (x1, y1 - 5 + offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1)
    
      c.image(npImg)
      info = st.empty()

      score = round(len(userInput) / len(labels) * 100)
      textScore = 'you have found {}% of the words, there are {} left'.format(score, len(labels) - len(userInput)) if (score != 100) else "🎉 Congratulations, you found everything ! 🎉"
      #st.markdown(f"<h4 style='text-align: center; color: green;'>{textScore}</h4>", unsafe_allow_html=True)
      st.progress(len(userInput) / len(labels))

      if (score != 100):
        info.warning(textScore)
      else:
        info.success(textScore)

      st.button(label="Next", on_click=newImage)