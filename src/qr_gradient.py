import asyncio
import qrcode
from PIL import Image, ImageDraw
import cv2
from pyzbar.pyzbar import decode


class QR_grad:
    @staticmethod
    async def create_gradient_qr(data: str, image_path: str):
        """
        Асинхронно создает QR-код с градиентом от розового к лазурному и закругленными краями.

        Args:
            data (str): Данные для кодирования в QR-код
            image_path (str): Путь для сохранения результата
        """

        def generate_qr():
            # Создаем базовый QR-код
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=2,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Создаем изображение QR-кода
            qr_image = qr.make_image(fill_color="black", back_color="white").convert(
                "RGB"
            )

            # Создаем градиентную маску
            width, height = qr_image.size
            gradient = Image.new("RGB", (width, height), color=0)
            draw = ImageDraw.Draw(gradient)

            # Розовый и лазурный цвета в RGB
            pink = (255, 105, 180)
            azure = (0, 191, 255)

            # Рисуем линейный градиент слева направо
            for x in range(width):
                # Вычисляем интерполированный цвет
                r = int(pink[0] + (azure[0] - pink[0]) * x / width)
                g = int(pink[1] + (azure[1] - pink[1]) * x / width)
                b = int(pink[2] + (azure[2] - pink[2]) * x / width)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

            # Накладываем градиент на QR-код используя маску
            qr_pixels = qr_image.load()
            gradient_pixels = gradient.load()

            for y in range(height):
                for x in range(width):
                    if qr_pixels[x, y] == (0, 0, 0):  # Черные пиксели QR-кода
                        qr_pixels[x, y] = gradient_pixels[x, y]

            # Добавляем закругленные края
            mask = Image.new("L", (width, height), 0)
            mask_draw = ImageDraw.Draw(mask)
            radius = min(width, height) // 10  # Радиус скругления
            mask_draw.rounded_rectangle([(0, 0), (width, height)], radius, fill=255)
            result = Image.new("RGB", (width, height), (255, 255, 255))
            result.paste(qr_image, (0, 0), mask)
            # Сохраняем результат
            result.save(image_path, "PNG")

        # Запускаем в отдельном потоке чтобы не блокировать event loop
        await asyncio.to_thread(generate_qr)

    @staticmethod
    async def decode_qr_code(path: str) -> str:
        """
        Асинхронно декодирует данные из QR-кода на изображении.

        Args:
            path (str): Путь к изображению с QR-кодом

        Returns:
            str: Декодированные данные из QR-кода

        Raises:
            ValueError: Если QR-код не найден или не может быть декодирован
        """

        def decode_image():
            # Загружаем изображение
            image = cv2.imread(path)
            if image is None:
                raise ValueError(f"Не удалось загрузить изображение: {path}")

            # Конвертируем в grayscale для лучшего распознавания
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Пробуем разные методы предобработки для улучшения распознавания
            decoded_objects = decode(gray)

            # Если не нашли в grayscale, пробуем оригинальное изображение
            if not decoded_objects:
                decoded_objects = decode(image)

            # Если все еще не нашли, пробуем дополнительные методы обработки
            if not decoded_objects:
                # Пробуем увеличить контраст
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced = clahe.apply(gray)
                decoded_objects = decode(enhanced)

            # Если нашли QR-код, возвращаем данные
            if decoded_objects:
                for obj in decoded_objects:
                    if obj.type == "QRCODE":
                        return obj.data.decode("utf-8")
            # Если ничего не нашли
            raise ValueError("QR-код не найден или не может быть декодирован")

        # Запускаем декодирование в отдельном потоке
        return await asyncio.to_thread(decode_image)
