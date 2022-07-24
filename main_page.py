import streamlit as st
import torch
from PIL import Image
import cv2
import numpy as np
from utilsPerso import load_image, get_colors, CLASSES
from streamlit_tags import st_tags

def newImage():
  st.session_state['img_index'] += 1

def squarePred(preds, CLASSES, userInput, npImg):
  for pred in preds:
    x1,y1 = int(pred[0]), int(pred[1])
    x2,y2 = int(pred[2]), int(pred[3])

    label = CLASSES[int(pred[5])]

    if (label not in userInput):
      continue

    color = colors[label]
    
    if st.session_state['accuracy']:
      label += ":{}%".format(int(pred[4] * 100))

    cv2.rectangle(npImg, (x1, y1), (x2, y2), color, 3)

    text_color = (0,0,0) if (color[0]*0.299 + color[0]*0.587 + color[0]*0.114 > 186) else (255,255,25)

    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

    offset = 0 if y1 > 20 else 20
    cv2.rectangle(npImg, (x1, y1 - 20 + offset), (x1 + w, y1 + offset), color, -1)
    cv2.putText(npImg, label, (x1, y1 - 5 + offset),
    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1)

def revealPred(labels):
  st.text(labels)

main, settings = st.tabs(["Main", "Settings"])

with main:
    main.markdown("# VirtuaAI 🧠")
    st.sidebar.markdown("# Main page 🧠")

    if 'img_index' not in st.session_state:
      st.session_state['img_index'] = 0

    image_files = st.sidebar.file_uploader("Load Images", type=["png","jpg","jpeg"], accept_multiple_files=True)

    if len(image_files) > st.session_state['img_index']:
      image_file = image_files[st.session_state['img_index']]
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

      c = main.container()

      userInput = st_tags(label="## Describe the picture :",
        text='Press enter to add more',
        value=[],
        suggestions=CLASSES,
        key='1',
        maxtags=len(labels)
      )

      userInput = [x for x in userInput if x in labels]

      squarePred(preds, CLASSES, userInput, npImg)
    
      info = main.empty()

      score = round(len(userInput) / len(labels) * 100)
      textScore = 'you have found {}% of the words, there are {} left'.format(score, len(labels) - len(userInput)) if (score != 100) else "🎉 Congratulations, you found everything ! 🎉"
      
      main.progress(len(userInput) / len(labels))

      if (score != 100):
        info.warning(textScore)
      else:
        info.success(textScore)

      if main.button("Reveal"):
        squarePred(preds, CLASSES, labels, npImg)
        revealPred(labels)
      
      main.button(label="Next", on_click=newImage)
      
      c.image(npImg)

with settings:
  settings.markdown("# Settings ⚙️")

  if 'accuracy' not in st.session_state:
    st.session_state['accuracy'] = True

  if 'suggestion' not in st.session_state:
    st.session_state['suggestion'] = True

  st.session_state['accuracy'] = settings.checkbox("Accuracy percent visible", st.session_state['accuracy'])
  st.session_state['suggestion'] = settings.checkbox("Suggestion available", st.session_state['suggestion'])