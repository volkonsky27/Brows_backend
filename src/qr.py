import qrcode
import asyncio
import base64
import aiofiles


class QR:
    @staticmethod
    async def make_qr(data: str, image_path: str) -> None:
        def make_img_qr():
            img = qrcode.make(data)
            img.save(image_path)

        data = await asyncio.to_thread(make_img_qr)

    @staticmethod
    async def image_to_base64(path: str) -> str:
        try:
            async with aiofiles.open(path, 'rb') as file:
                image = await file.read()
            base64_encoded = base64.b64encode(image).decode('utf-8')
            return f"data:image/png;base64,{base64_encoded}"
        except:
            return "Not found"