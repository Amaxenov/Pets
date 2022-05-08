from torchvision.models import detection
import numpy as np
import torch as tr
import cv2 as cv


class HumanChecker:
    def __init__(self, device='cuda', thr=0.6):
        self.DEV = tr.device(device)
        self.THR = float(thr)
        self.model = detection.retinanet_resnet50_fpn(pretrained=True)
        self.model.eval()
        self.model = self.model.to(self.DEV)

    def preprocess_image(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = image.transpose((2, 0, 1))
        image = image / 255.0
        image = tr.FloatTensor(image)
        return image
        
    def __call__(self, image):
        input_image = self.preprocess_image(image)
        input_image = input_image.to(self.DEV)
        with tr.no_grad():
            result = self.model([input_image])
        boxes, scores, labels = (
            result[0]['boxes'].cpu().numpy().astype(np.int32),
            result[0]['scores'].cpu().numpy(),
            result[0]['labels'].cpu().numpy()
                                )
        detected = [(b, s, l) for b, s, l in zip(boxes, scores, labels) if s > self.THR and l == 1]
        contains_human = len(detected) > 0
        vis_image = image.copy()
        for bbox, score, label in detected:
            vis_image = cv.rectangle(vis_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                                (0, 255, 0), thickness=2)
        return contains_human, vis_image

if __name__ == '__main__':
    human_checker = HumanChecker(device='cuda', thr=0.6)

    image = cv.imread('_image150.jpg')
    with_human, vis_image = human_checker(image)
    cv.imwrite('test_out.jpg', vis_image)
    print(with_human)
