import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
from torchvision import models, transforms
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

try:
    model = model = torch.load("D:/Major Project/KneeOA/final_kneeOA_model.pth", map_location=device, weights_only=False)  # Ensure weights_only=False

    model.to(device)
    model.eval()
except:
    model = models.densenet121(pretrained=False)
    model.load_state_dict(torch.load("D:/Major Project/KneeOA/final_kneeOA_model.pth", map_location=device), strict=False)
    model.to(device)
    model.eval()

class_names = ['Normal', 'Mild', 'Moderate', 'Severe']

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self.hook_layers()

    def hook_layers(self):
        def forward_hook(module, input, output):
            self.activations = output

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0]

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_backward_hook(backward_hook)

    def generate_heatmap(self, input_image, class_idx):
        self.model.zero_grad()
        output = self.model(input_image)
        class_score = output[0, class_idx]
        class_score.backward()

        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        activations = self.activations[0]

        for i in range(activations.shape[0]):
            activations[i] *= pooled_gradients[i]

        heatmap = torch.mean(activations, dim=0).cpu().detach().numpy()
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)

        return heatmap


grad_cam = GradCAM(model, model.features[-1])

# Image preprocessing
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3), 
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])  
])

def apply_grad_cam(image_path, model, class_names):
    image = Image.open(image_path).convert("L")  
    input_tensor = transform(image).unsqueeze(0).to(device)


    output = model(input_tensor)
    class_idx = torch.argmax(output).item()


    heatmap = grad_cam.generate_heatmap(input_tensor, class_idx)

    
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    heatmap = cv2.resize(heatmap, (224, 224))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)


    result_path = image_path.replace("uploads", "results")
    cv2.imwrite(result_path, superimposed_img)

    return result_path, class_names[class_idx]
