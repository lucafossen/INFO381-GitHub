# XAI Semester Project --- INFO381

This repository contains code and notebooks developed for a semester project on Explainable AI (XAI).

<br><br>


## Project Structure and Execution


The code is designed to be run from the top-level folder `INFO381-GITHUB` when executing locally.

On Google Colab, this is not an issue as paths are adjusted dynamically.

All notebooks work both locally and in Colab, except for `grad-cam.ipynb`, which has to be ran locally and not in Colab due to environment compatibility issues.


#### **If you want to run code on Google Colab, you can:**

1. upload the code directory to your personal Google Drive
2. identify the path to the code directory (should start with `"/content/drive/..."`)
- Change the argunemt of the `cd` path to point to where you uploaded the project in your Google Drive. It should look something like `/content/drive/MyDrive/INFO381-GitHub`
3. double-click the notebook you want to run and replace the string in the Drive connection boilerplate code cell with the path you identified in step 2
4. run the code, and accept the Google Drive pop-up


**NOTE:** To run code with CLIP, either have git install or run on Google Colab