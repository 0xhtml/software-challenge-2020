import sys
import client

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 13050
    reservation = sys.argv[3] if len(sys.argv) > 3 else None
    test = sys.argv[4] if len(sys.argv) > 4 else None

    if test == "autoopen":
        import pyautogui
        pyautogui.PAUSE = 0.1
        pyautogui.hotkey("winleft", "6")
        pyautogui.sleep(0.7)
        pyautogui.click(1032, 687)
        pyautogui.click(1658, 689)
        for _ in range(2):
            pyautogui.press("tab")
        pyautogui.press("down")
        for _ in range(3):
            pyautogui.press("tab")
        pyautogui.press("enter")
    elif test == "replay":
        import bot
        import gamestate
        from xml.etree import ElementTree
        xml = ElementTree.parse(input(">"))
        gamestate = gamestate.parse(xml.find("data").find("state"))
        print(bot.Bot().get(gamestate))
        exit()

    client = client.Client(host, port)

    if reservation is None or reservation == "":
        client.join_any_game()
    else:
        client.join_reservation(reservation)
