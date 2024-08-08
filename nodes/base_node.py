import io

import numpy as np
import requests
import torch
from PIL import Image


class SMLFluxBaseNode:
    def __init__(self):
        pass

    def process_result(self, result):
        if isinstance(result, list):
            img_url = result[0]
        else:
            img_url = result

        img_response = requests.get(img_url)
        img = Image.open(io.BytesIO(img_response.content))
        img_array = np.array(img).astype(np.float32) / 255.0
        images = []
        images.append(img_array)

        # Stack the images along a new first dimension
        stacked_images = np.stack(images, axis=0)

        # Convert to PyTorch tensor
        img_tensor = torch.from_numpy(stacked_images)

        return (img_tensor,)

    def create_blank_image(self):
        blank_img = Image.new('RGB', (1024, 1024), color='black')
        img_array = np.array(blank_img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_array)[None,]
        return (img_tensor,)
