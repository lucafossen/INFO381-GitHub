# XAI Semester Project --- INFO381

This repository contains code and notebooks developed for a semester project on Explainable AI (XAI).

**To look at examples of our results, run GUI.py**

## Project Structure and Execution


The code is designed to be run from the top-level folder `INFO381-GITHUB` when executing locally.

On Google Colab, this is not an issue as paths are adjusted dynamically.

All notebooks work both locally and in Colab, except for `grad-cam.ipynb`, which has to be ran locally and not in Colab due to environment compatibility issues.


#### **If you want to run code on Google Colab, you can:**

1. upload the code directory to your personal Google Drive
2. identify the path to the code directory (should start with `"/content/drive/..."`)
- Change the argunemt of the `cd` path to point to where you uploaded the project in your Google Drive. It should look something like `/content/drive/MyDrive/INFO381-GitHub`
3. double-click the notebook you want to run and replace the string in the Drive connection boilerplate code cell with the path you identified in step 2
4. run the code, and accept the Google Drive pop-u

**NOTE:** When running on Colab there is no need to unzip the dataset `fake_vs_real.zip`.



#### **If you want to run code locally:**
1. Open top-level folder `INFO381-GITHUB` in your IDE.
2. We suggest to unzip `fake_vs_real.zip` manually. The python file `utils.py` will do it for you, but it takes some time.
3. Run as normal 


### **IMPORTANT TO NOTE:**

To use CLIP locally, you need to have an installation of Git or install CLIP manually from https://github.com/openai/CLIP

### Folder structure

```
INFO381-GITHUB/ 
├── gui_images/ # Images used in the GUI 
├── helper_functions/ # Custom helper modules 
│ ├── model_definitions.py # CLIP model architecture definition
│ └── utils.py # Utility functions 
│
├── models/ # Trained models and checkpoints 
│ ├── clip_classifier_10epochs.pth # Trained CLIP model
│ ├── resnet18_cnn.pth # Trained CNN model
│ ├── performance_evaluation.ipynb # Notebook for model evaluation
│ ├── train_CLIP.ipynb # Notebook to train CLIP model
│ └── train_CNN_resnet18.ipynb # Notebook to train CNN model 
│
├── XAI methods/ # Explainable AI method notebooks 
│ ├── grad-cam.ipynb # XAI - Grad-CAM notebook
│ ├── LIME_xai.ipynb # XAI - LIME notebook
│ └── RISE_xai.ipynb # XAI - RISE notebook
│
├── GUI.py # GUI interface 
├── fake_vs_real.zip # Sample dataset (zipped) 
└── README.md
```
