# Knee Osteoarthritis Severity Prediction using Deep Learning
📌 Project Overview

Knee Osteoarthritis (OA) is a progressive degenerative joint disease that causes chronic pain, stiffness, and reduced mobility. Accurate early diagnosis and severity assessment are crucial for effective treatment planning.

This project presents an 🤖 AI-powered web application that automatically predicts Knee OA severity from 🩻 X-ray images using Deep Learning and provides 🔍 explainable visual insights using Grad-CAM.
The system follows the 📊 Kellgren–Lawrence (KL) grading scale and generates an 📝 automated medical report, which is 📧 sent directly to the user via email.

🎯 Objectives
- Predict Knee Osteoarthritis severity from X-ray images using deep learning
- Provide model interpretability using Grad-CAM heatmaps
- Build a user-friendly Flask web application
- Automatically generate and email diagnostic reports
- Support early detection and better clinical decision-making

✨ Key Features

- Upload knee X-ray image
- Validates whether the image is a knee X-ray
- Predicts OA severity (KL-1 to KL-4)
- Generates Grad-CAM heatmap for explainability
- Auto-generates diagnostic report
- Sends report directly via email

📊 Severity Classification (KL Scale)
KL Grade	Description
KL-0	Normal
KL-1	Doubtful
KL-2	Mild
KL-3	Moderate
KL-4	Severe

🔄 Workflow

📤 User uploads knee X-ray image

✅ Image validation (Knee vs Non-Knee)

⚙️ Preprocessing & resizing

🧠 Severity prediction using DenseNet-121

🔥 Grad-CAM heatmap generation

📝 Automated report creation

📧 Report sent to user via email

## #Model Weights
⚠️ The trained deep learning model file (`.pth`) is not included in this repository.
You can download the model from Google Drive using the link below and place it in the project directory before running the application.

🔗 Google Drive: <https://drive.google.com/file/d/1h-ZTKo_HAD9PRcY9ytrBUkdr9vpd-Nia/view?usp=drive_link> or 
If you require access to the model, please contact:
📧 lakshmideepak.vattipalli@mail.com


⚠️ Disclaimer

🚨 This project is intended only for academic and research purposes and should not be used for real medical diagnosis.
