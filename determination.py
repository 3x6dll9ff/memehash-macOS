import pyautogui
import time
from PIL import ImageGrab

def get_pixel_color():
    # Получаем текущие координаты мыши
    x, y = pyautogui.position()
    
    # Захватываем скриншот экрана
    screenshot = ImageGrab.grab(bbox=(x-1, y-1, x+1, y+1))  # Получаем небольшой скриншот вокруг позиции
    pixel_color = screenshot.getpixel((0, 0))  # Получаем цвет пикселя в центре

    return x, y, pixel_color

def monitor_mouse_position():
    print("Начало мониторинга... Для завершения нажмите Ctrl+C.")
    try:
        while True:
            x, y, color = get_pixel_color()
            print(f"Координаты: ({x}, {y}) - Цвет: {color}")
            time.sleep(5)  # Интервал в 5 секунд
    except KeyboardInterrupt:
        print("Мониторинг завершен пользователем.")

if __name__ == "__main__":
    monitor_mouse_position()



# Координаты: (1698, 377) - Цвет: (255, 253, 187, 255) вейтинг
# Координаты: (1698, 377) - Цвет: (192, 250, 187, 255) майнинг
# Координаты: (1698, 377) - Цвет: (238, 117, 107, 255) лоу енерджи


# Координаты: (1713, 484) - Цвет: (238, 117, 107, 255) - стоп майнинг
# Координаты: (1713, 484) - Цвет: (180, 186, 250, 255) - старт майнинг