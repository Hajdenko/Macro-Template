import asyncio, pyautogui
import keyboard
from pynput.keyboard import Key, Controller

# Assets
from assets.Classes import Tools
from assets.Tables import StopKey, Webhooks

keyboard_controller = Controller()

async def main():
    try:
        while True:

            if keyboard.is_pressed(StopKey):
                print("Macro stopped by user.")
                break

            # Your code

            await asyncio.sleep(10)

    except KeyboardInterrupt:
        print("Macro stopped by user.")

if __name__ == "__main__":
    asyncio.run(Tools.Discord.send_info(
        content="Script started successfully!"
    ))
    asyncio.run(main())
