from cpu_yolo_api.image_input import DecodedImage
from cpu_yolo_api.schemas import Box, Detection, DetectionPayload


class Detector:
    """Detector interface.

    The initial implementation is a mock. A later work order should replace this
    with ONNX Runtime CPU inference while preserving the output contract.
    """

    def detect(self, image: DecodedImage) -> DetectionPayload:
        width = max(image.width, 1)
        height = max(image.height, 1)

        detection = Detection(
            class_name="mock_object",
            confidence=0.99,
            box=Box(
                x1=0,
                y1=0,
                x2=width,
                y2=height,
            ),
        )

        return DetectionPayload(
            detections=[detection],
            image={
                "width": image.width,
                "height": image.height,
                "media_type": image.media_type,
            },
            metadata={
                "engine": "mock",
                "cpu_only": True,
                "tracking": False,
                "segmentation": False,
            },
        )


detector = Detector()
