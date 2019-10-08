import sys
import client

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 13050
    reservation = sys.argv[3] if len(sys.argv) > 3 else None
    test = len(sys.argv) > 4

    if test:
        import pyautogui
        pyautogui.hotkey('alt', 'tab')
        pyautogui.sleep(2)
        for _ in range(3):
            pyautogui.press('tab')
        pyautogui.press('down')
        for _ in range(3):
            pyautogui.press('tab')
        pyautogui.press('enter')

    client = client.Client(host, port)

    if reservation is None or reservation == "":
        client.join_any_game()
    else:
        client.join_reservation(reservation)
