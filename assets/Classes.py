import pyautogui
import asyncio
import win32gui, win32con, keyboard, aiohttp, json

# Assets
from assets.Tables import Buttons, Webhooks, StopKey # Start from the main.py file, if started from here it will cause some errors :)
# I'll be totally honest with you, I used AI to explain these function bcs im lazy lol (also i want to sleep its 12:21AM)

class Tools:
    
    def __init__(self, name):
        self.name = name

    @staticmethod
    def center_xy(left, top, width, height):
        """Calculates the center coordinates (x, y) of a given rectangle."""
        _x = left + width // 2
        _y = top + height // 2
        return _x, _y
    
    @staticmethod
    def center_mouse():
        """Moves the mouse cursor to the center of the screen."""
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        pyautogui.moveTo(center_x, center_y)

    @staticmethod
    async def find_image(img, conf:float=0.7, label:str=None):
        """
        Tries to locate an image on the screen.

        Args:
        - img (str): Path to the image file or image name.
        - conf (float): Confidence threshold for image recognition.
        - label (str): Label or identifier for the image.

        Returns:
        - True if image is found, False otherwise.
        """
        if not img:
            return asyncio.run(Tools.Discord.send_error(
                content=f"find_image({img}, {conf}, {label}) -> Image is None"
            ))
        
        autoload_loop = 1
        title = label if label else img
        Buttons[title] = None

        while True:
            if keyboard.is_pressed(StopKey):
                print("Macro stopped by user.")
                return False

            try:
                Buttons[title] = pyautogui.locateOnScreen(image=img, confidence=conf)
                if Buttons[title]:
                    print(f"Image found in {autoload_loop} loops!")
                    break
                else:
                    raise Exception("Image not found")
            except Exception as e:
                print(e)
                print(f"Loop {autoload_loop}: Error, couldn't find image. Retrying...")
                autoload_loop += 1


    class Mouse:
        """Contains mouse-related operations."""
        
        def __init__(self):
            self.mouse_delay = 0.1

        async def move(self, x, y):
            """Moves the mouse cursor to the specified coordinates."""
            pyautogui.moveTo(x, y, duration=self.mouse_delay)
            await asyncio.sleep(self.mouse_delay)

        @staticmethod
        async def _click(x, y, button='left'):
            """Simulates a mouse click at the specified coordinates."""
            pyautogui.click(x, y, button=button)
            await asyncio.sleep(0.1)

        @staticmethod
        async def _focus_window(window_title):
            """Focuses on a specified window by bringing it to the foreground."""
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                await asyncio.sleep(0.5)

        @staticmethod
        async def click(window_title, x, y, center:bool=True, button:str='left'):
            """
            Moves the mouse to a specific point and clicks.

            Args:
            - window_title (str): Title of the window to interact with.
            - x, y (int): Coordinates to click within the window.
            - center (bool): Whether to focus the window before clicking.
            - button (str): Which mouse button to click ('left', 'right', 'middle').
            """
            await Tools.Mouse._focus_window(window_title)
            await Tools.Mouse._click(x, y, button)

    class Discord:
        """Handles interactions with Discord webhooks."""
        
        @staticmethod
        async def send_log(content:str, embed:bool=False, color:str=None, img:str=None, webhook_url:str=Webhooks["main"]):
            """
            Sends a log message to a Discord webhook.

            Args:
            - content (str): Text content of the message.
            - embed (bool): Whether to use an embed for the message.
            - color (str): Hex color code for embed message.
            - img (str): Path to an image file to include in the message.
            - webhook_url (str): URL of the Discord webhook to send the message to.
            """
            async with aiohttp.ClientSession() as session:
                if img:
                    data = aiohttp.FormData()
                    data.add_field('payload_json', json.dumps({
                        "embeds": [{
                            "description": content,
                            "color": int(color.replace("#", ""), 16) if color else None,
                            "image": {"url": "attachment://screenshot.png"}
                        }]
                    }))
                    data.add_field('file', open(img, 'rb'), filename="screenshot.png")
                else:
                    data = json.dumps({
                        "content": content,
                        "embeds": [{
                            "description": content,
                            "color": int(color.replace("#", ""), 16) if color else None,
                        }]
                    })
                    headers = {"Content-Type": "application/json"}

                async with session.post(webhook_url, data=data) as response:
                    if response.status != 204 and response.status != 200:
                        print(f"Failed to send message: {response.status}")
                    else:
                        print("Message sent successfully")

        @staticmethod
        async def send_error(content:str, img:str=None, webhook_url:str=Webhooks["main"]):
            """Sends an error log to Discord."""
            await Tools.Discord.send_log(
                content=content, 
                embed=True, 
                color="#f14c4c",
                img=img,
                webhook_url=webhook_url
            )

        @staticmethod
        async def send_info(content:str, img=None, webhook_url=str(Webhooks["main"])):
            """Sends an informational log to Discord."""
            await Tools.Discord.send_log(
                content=content, 
                embed=True, 
                color="#77b0e6",
                img=img,
                webhook_url=webhook_url
            )