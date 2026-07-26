import io
import logging
from pathlib import Path

from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

MAX_IMAGE_EDGE = 1600
JPEG_QUALITY = 82
SUPPORTED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


class ImageCompressionError(Exception):
    pass


def is_uploaded_image(uploaded_file):
    content_type = getattr(uploaded_file, "content_type", "") or ""
    return isinstance(uploaded_file, UploadedFile) and content_type in SUPPORTED_IMAGE_TYPES


def compress_image_file(
    uploaded_file,
    max_edge=MAX_IMAGE_EDGE,
    quality=JPEG_QUALITY,
):
    if getattr(uploaded_file, "_image_compressed", False):
        return uploaded_file

    if not is_uploaded_image(uploaded_file):
        return uploaded_file

    try:
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)

            if image.mode not in ("RGB", "L"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                if image.mode in ("RGBA", "LA"):
                    background.paste(image, mask=image.getchannel("A"))
                else:
                    background.paste(image.convert("RGB"))
                image = background
            elif image.mode == "L":
                image = image.convert("RGB")

            output = io.BytesIO()
            image.save(output, format="JPEG", quality=quality, optimize=True)
            output.seek(0)

        original_name = Path(uploaded_file.name or "upload.jpg")
        new_name = f"{original_name.stem}.jpg"

        compressed_file = InMemoryUploadedFile(
            file=output,
            field_name=getattr(uploaded_file, "field_name", None),
            name=new_name,
            content_type="image/jpeg",
            size=output.getbuffer().nbytes,
            charset=None,
        )
        compressed_file._image_compressed = True
        return compressed_file
    except Exception as exc:
        logger.warning("Gagal mengompres gambar %s: %s", uploaded_file.name, exc)
        raise ImageCompressionError(str(exc)) from exc


def compress_if_image(uploaded_file, **kwargs):
    try:
        return compress_image_file(uploaded_file, **kwargs)
    except ImageCompressionError:
        return uploaded_file
