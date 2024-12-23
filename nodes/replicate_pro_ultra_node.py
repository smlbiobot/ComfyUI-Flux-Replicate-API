import configparser
import os

import replicate

from .base_node import SMLFluxBaseNode


class SMLFluxProUltraReplicateNode(SMLFluxBaseNode):
    api_token: str = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "aspect_ratio": (
                    [
                        "21:9",
                        "16:9",
                        "3:2",
                        "4:3",
                        "5:4",
                        "1:1",
                        "4:5",
                        "3:4",
                        "2:3",
                        "9:16",
                        "9:21",
                        "custom"
                    ],
                    {
                        "default": "1:1"
                    }
                ),
                "width": ("INT", {"default": 1024, "min": 256, "max": 1440}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 1440}),
                "steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "output_quality": ("INT", {"default": 100, "min": 1, "max": 100}),
                "image_prompt_strength": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0}),
                "interval": ("INT", {"default": 2, "min": 1, "max": 4}),
                "safety_tolerance": ("INT", {"default": 6, "min": 1, "max": 6}),
                "raw": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "😃 SML"

    def set_api_token(self):
        if self.api_token is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            config_path = os.path.join(parent_dir, "config.ini")

            config = configparser.ConfigParser()
            config.read(config_path)

            try:
                replicate_api_token = config['API']['REPLICATE_API_TOKEN']
                os.environ["REPLICATE_API_TOKEN"] = replicate_api_token
                self.api_token = replicate_api_token
            except KeyError:
                print("Error: REPLICATE_API_TOKEN not found in config.ini")

    def generate_image(self,
                       prompt,
                       aspect_ratio,
                       width,
                       height,
                       steps,
                       output_quality,
                       guidance,
                       interval,
                       safety_tolerance,
                       prompt_upsampling,
                       seed=-1
                       ):
        input = dict(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            output_quality=output_quality,
            width=width,
            height=height,
            output_format='png',
            steps=steps,
            safety_tolerance=safety_tolerance,
            guidance=guidance,
            interval=interval,
            disable_safety_checker=True,
            prompt_upsampling=prompt_upsampling,
        )

        self.set_api_token()

        if seed != -1:
            input["seed"] = seed

        try:

            result = replicate.run(
                "black-forest-labs/flux-1.1-pro-ultra",
                input=input,
            )

            return self.process_result(result)

        except Exception as e:
            print(f"Error generating image with FluxPro: {str(e)}")
            return self.create_blank_image()


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "SML_FluxProUltra_Replicate_Standalone": SMLFluxProUltraReplicateNode,
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "SML_FluxProUltra_Replicate_Standalone": "😃 SML Flux Pro Ultra 1.1 (Replicate)",
}
