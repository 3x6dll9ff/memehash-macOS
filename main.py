import pyautogui
import time
import tkinter as tk
import threading
from PIL import ImageGrab

# Координаты и цвета для состояний и кнопок
status_coordinates = (1698, 377)  # Координаты для статуса
stop_mining_button_coordinates = (1713, 484)  # Координаты для кнопки "Stop Mining"
start_mining_button_coordinates = (1713, 484)  # Координаты для кнопки "Start Mining"

# Цвета для различных состояний
color_waiting = (255, 253, 187, 255)
color_mining = (192, 250, 187, 255)
color_low_energy = (238, 117, 107, 255)

color_stop_mining_button = (238, 117, 107, 255)
color_start_mining_button = (180, 186, 250, 255)

color_tolerance = 10


root = tk.Tk()
root.title("Таймер мониторинга")
root.configure(bg="black")


timer_width = 200
timer_height = 100


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


root.geometry(f"{timer_width}x{timer_height}+{screen_width - timer_width - 10}+{screen_height - timer_height - 10}")


timer_label = tk.Label(root, text="0:00", font=("Helvetica", 20), fg="white", bg="black")
timer_label.pack(expand=True)


remaining_time = 0


def update_timer():
    """
    Обновляет таймер на экране.
    """
    global remaining_time
    minutes, seconds = divmod(remaining_time, 60)
    timer_label.config(text=f"{minutes:02}:{seconds:02}")
    if remaining_time > 0:
        remaining_time -= 1
    root.after(1000, update_timer)  

def colors_match(color1, color2, tolerance=10):
    """
    Проверяет совпадение двух цветов с учетом допуска.
    """
    return all(abs(a - b) <= tolerance for a, b in zip(color1, color2))


def get_pixel_color(x, y):
    """
    Получает цвет пикселя в заданных координатах.
    """
    screenshot = ImageGrab.grab(bbox=(x-1, y-1, x+1, y+1))  
    pixel_color = screenshot.getpixel((0, 0))  
    return pixel_color


def click_button(x, y):
    """
    Нажимает на кнопку в заданных координатах.
    """
    pyautogui.click(x, y)
    time.sleep(0.5) 
    print(f"Кнопка нажата в координатах: ({x}, {y})")


def wait_for_color_change(coordinates, target_color, tolerance=10, timeout=300):
    """
    Ожидает, пока в заданных координатах цвет не станет целевым.
    
    :param coordinates: Координаты для проверки цвета (x, y).
    :param target_color: Целевой цвет (r, g, b, a).
    :param tolerance: Допуск для проверки цвета.
    :param timeout: Максимальное время ожидания (в секундах).
    :return: True, если цвет совпал, иначе False.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_color = get_pixel_color(*coordinates)
        if colors_match(current_color, target_color, tolerance):
            return True
        time.sleep(0.5)  # Пауза между проверками
    return False


def monitor_and_control_mining():
    """
    Мониторит состояние и выполняет действия в зависимости от цвета в координатах.
    """
    global remaining_time
    print("Запуск мониторинга...")
    while True:
        try:
          
            status_color = get_pixel_color(*status_coordinates)
            print(f"Текущий цвет статуса: {status_color}")

         
            if colors_match(status_color, color_low_energy, color_tolerance):
                print("Обнаружен статус 'Low Energy'. Останавливаем майнинг...")
                click_button(*stop_mining_button_coordinates)

                
                print("Ждем появления кнопки 'Start Mining'...")
                if wait_for_color_change(start_mining_button_coordinates, color_start_mining_button, color_tolerance):
                    print("Кнопка 'Start Mining' готова.")

                    print("Майнинг остановлен. Ожидаем 1.5 часа...")
                    remaining_time = 90 * 60  # Устанавливаем 1.5 часа в секундах
                    time.sleep(90 * 60)  # Ждем 1.5 часа

                   
                    print("Пробуем запустить майнинг...")
                    click_button(*start_mining_button_coordinates)
                else:
                    print("Кнопка 'Start Mining' не стала голубой в течение времени ожидания.")

            elif colors_match(status_color, color_waiting, color_tolerance):
                print("Обнаружен статус 'Waiting'. Запускаем майнинг...")
                click_button(*start_mining_button_coordinates)

            elif colors_match(status_color, color_mining, color_tolerance):
                print("Статус 'Mining'. Майнинг продолжается... Ничего не делаем.")

            time.sleep(1)

        except KeyboardInterrupt:
            print("Мониторинг завершен пользователем.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(1)  


def start_monitoring():
    """
    Функция для запуска мониторинга в отдельном потоке.
    """
    monitoring_thread = threading.Thread(target=monitor_and_control_mining)
    monitoring_thread.daemon = True  
    monitoring_thread.start()


if __name__ == "__main__":
    update_timer()  
    start_monitoring()  
    root.mainloop()  
