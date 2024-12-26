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
                "steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "output_quality": ("INT", {"default": 100, "min": 1, "max": 100}),
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
                       steps,
                       output_quality,
                       interval,
                       safety_tolerance,
                       raw,
                       seed=-1
                       ):
        input = dict(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            output_quality=output_quality,
            output_format='png',
            steps=steps,
            safety_tolerance=safety_tolerance,
            interval=interval,
            disable_safety_checker=True,
            raw=raw,
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
