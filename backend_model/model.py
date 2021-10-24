import PIL
import torch
import torchvision
import torchvision.transforms as T


def assess_image(img: PIL.Image):
    cuda_avail = torch.cuda.is_available()
    device = None
    if cuda_avail:
        device = "cuda"
    else:
        device = "cpu"
    img = img.resize((100, 100))
    img = T.ToTensor()(img)
    img = T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(img)
    img = torch.unsqueeze(img, dim=0)
    num_classes = 195
    model = torchvision.models.resnet34(pretrained=True).to(device)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load("model_weights.pt"))
    model.eval()
    pred = model(img)
    return convert_country_code(torch.argmax(pred, dim=1).item())

def convert_country_code(ind):
    return ind