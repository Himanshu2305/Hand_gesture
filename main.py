import cv2
import mediapipe as mp
import pyautogui

import subprocess
import time
import os
import psutil

import win32gui
import win32con
import win32process

from hand_gesture import (
    finger_states,
    count_fingers,
    thumb_only
)


# =========================================================
# MEDIAPIPE SETUP
# =========================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# =========================================================
# CAMERA
# =========================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()


# =========================================================
# GESTURE SETTINGS
# =========================================================

last_gesture = None
last_action_time = 0

GESTURE_COOLDOWN = 2.0


# =========================================================
# GENERIC WINDOW FUNCTIONS
# =========================================================

def is_window_active(hwnd):
    """
    Check whether a window is currently the
    active/foreground window.
    """

    try:
        return hwnd == win32gui.GetForegroundWindow()

    except Exception:
        return False


def activate_window(hwnd):
    """
    Restore and bring a window to the foreground.
    """

    try:

        if win32gui.IsIconic(hwnd):

            win32gui.ShowWindow(
                hwnd,
                win32con.SW_RESTORE
            )

        win32gui.SetForegroundWindow(hwnd)

        return True

    except Exception as e:

        print(
            "Could not activate window:",
            e
        )

        return False


def minimize_window(hwnd):
    """
    Minimize a window.
    """

    try:

        win32gui.ShowWindow(
            hwnd,
            win32con.SW_MINIMIZE
        )

        return True

    except Exception as e:

        print(
            "Could not minimize window:",
            e
        )

        return False


def toggle_window(hwnd, application_name):
    """
    Toggle an existing application window.

    If active:
        minimize it

    If not active:
        bring it to front
    """

    if is_window_active(hwnd):

        print(
            application_name
            + " is already active."
        )

        print(
            "Minimizing "
            + application_name
            + "..."
        )

        minimize_window(hwnd)

    else:

        print(
            application_name
            + " is open."
        )

        print(
            "Activating existing "
            + application_name
            + "..."
        )

        activate_window(hwnd)


# =========================================================
# FIND WINDOW BY PROCESS
# =========================================================

def find_window_by_process(process_name):

    found_windows = []

    def callback(hwnd, extra):

        try:

            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd)

            if not title:
                return

            _, pid = (
                win32process.GetWindowThreadProcessId(
                    hwnd
                )
            )

            process = psutil.Process(pid)

            if (
                process.name().lower()
                == process_name.lower()
            ):

                found_windows.append(hwnd)

        except Exception:

            pass


    win32gui.EnumWindows(
        callback,
        None
    )


    if found_windows:

        return found_windows[0]

    return None


# =========================================================
# FIND FILE EXPLORER
# =========================================================

def find_file_explorer_window():

    found_windows = []

    def callback(hwnd, extra):

        try:

            if not win32gui.IsWindowVisible(hwnd):
                return

            class_name = win32gui.GetClassName(hwnd)

            if class_name == "CabinetWClass":

                found_windows.append(hwnd)

        except Exception:

            pass


    win32gui.EnumWindows(
        callback,
        None
    )


    if found_windows:

        return found_windows[0]

    return None


# =========================================================
# FIND WHATSAPP
# =========================================================

def find_whatsapp_window():

    found_windows = []

    whatsapp_process_names = [
        "WhatsApp.exe",
        "WhatsApp.Root.exe"
    ]


    def callback(hwnd, extra):

        try:

            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd)

            if not title:
                return

            _, pid = (
                win32process.GetWindowThreadProcessId(
                    hwnd
                )
            )

            process = psutil.Process(pid)

            process_name = (
                process.name().lower()
            )


            for name in whatsapp_process_names:

                if (
                    process_name
                    == name.lower()
                ):

                    found_windows.append(hwnd)

                    return

        except Exception:

            pass


    win32gui.EnumWindows(
        callback,
        None
    )


    if found_windows:

        return found_windows[0]

    return None


# =========================================================
# EDGE
# =========================================================

def open_edge():

    print("\n================================")
    print("INDEX FINGER -> EDGE")
    print("================================")


    hwnd = find_window_by_process(
        "msedge.exe"
    )


    # -----------------------------------------
    # EDGE ALREADY OPEN
    # -----------------------------------------

    if hwnd:

        toggle_window(
            hwnd,
            "Microsoft Edge"
        )

        return


    # -----------------------------------------
    # EDGE CLOSED
    # -----------------------------------------

    print(
        "Edge is not running."
    )

    print(
        "Opening Edge..."
    )


    edge_paths = [

        os.path.join(
            os.environ.get(
                "PROGRAMFILES",
                ""
            ),
            "Microsoft",
            "Edge",
            "Application",
            "msedge.exe"
        ),

        os.path.join(
            os.environ.get(
                "PROGRAMFILES(X86)",
                ""
            ),
            "Microsoft",
            "Edge",
            "Application",
            "msedge.exe"
        )

    ]


    for path in edge_paths:

        if os.path.exists(path):

            subprocess.Popen(
                [path]
            )

            return


    subprocess.Popen(
        "start microsoft-edge:",
        shell=True
    )


# =========================================================
# BRAVE
# =========================================================

def open_brave():

    print("\n================================")
    print("TWO FINGERS -> BRAVE")
    print("================================")


    hwnd = find_window_by_process(
        "brave.exe"
    )


    # -----------------------------------------
    # BRAVE ALREADY OPEN
    # -----------------------------------------

    if hwnd:

        toggle_window(
            hwnd,
            "Brave"
        )

        return


    # -----------------------------------------
    # BRAVE CLOSED
    # -----------------------------------------

    print(
        "Brave is not running."
    )

    print(
        "Opening Brave..."
    )


    brave_paths = [

        os.path.join(
            os.environ.get(
                "PROGRAMFILES",
                ""
            ),
            "BraveSoftware",
            "Brave-Browser",
            "Application",
            "brave.exe"
        ),

        os.path.join(
            os.environ.get(
                "PROGRAMFILES(X86)",
                ""
            ),
            "BraveSoftware",
            "Brave-Browser",
            "Application",
            "brave.exe"
        ),

        os.path.join(
            os.environ.get(
                "LOCALAPPDATA",
                ""
            ),
            "BraveSoftware",
            "Brave-Browser",
            "Application",
            "brave.exe"
        )

    ]


    for path in brave_paths:

        if os.path.exists(path):

            subprocess.Popen(
                [path]
            )

            return


    print(
        "Brave executable was not found."
    )


# =========================================================
# FILE EXPLORER
# =========================================================

def open_file_explorer():

    print("\n================================")
    print("3 FINGERS -> FILE EXPLORER")
    print("================================")


    hwnd = find_file_explorer_window()


    # -----------------------------------------
    # EXPLORER ALREADY OPEN
    # -----------------------------------------

    if hwnd:

        toggle_window(
            hwnd,
            "File Explorer"
        )

        return


    # -----------------------------------------
    # EXPLORER CLOSED
    # -----------------------------------------

    print(
        "File Explorer is not open."
    )

    print(
        "Opening File Explorer..."
    )


    subprocess.Popen(
        "explorer.exe",
        shell=True
    )


# =========================================================
# WHATSAPP
# =========================================================

def open_whatsapp():

    print("\n================================")
    print("4 FINGERS -> WHATSAPP")
    print("================================")


    hwnd = find_whatsapp_window()


    # -----------------------------------------
    # WHATSAPP ALREADY OPEN
    # -----------------------------------------

    if hwnd:

        toggle_window(
            hwnd,
            "WhatsApp"
        )

        return


    # -----------------------------------------
    # WHATSAPP CLOSED
    # -----------------------------------------

    print(
        "WhatsApp is not open."
    )

    print(
        "Opening WhatsApp..."
    )


    try:

        subprocess.Popen(
            "start whatsapp:",
            shell=True
        )

    except Exception as e:

        print(
            "Could not open WhatsApp:",
            e
        )


# =========================================================
# DESKTOP
# =========================================================

def open_desktop():

    print("\n================================")
    print("5 FINGERS -> DESKTOP")
    print("================================")


    pyautogui.hotkey(
        "win",
        "d"
    )


# =========================================================
# THUMB -> BRACKETS
# =========================================================

def type_brackets():

    print("\n================================")
    print("THUMB -> ()")
    print("================================")


    pyautogui.write(
        "()"
    )


# =========================================================
# EXECUTE FINGER GESTURE
# =========================================================

def execute_finger_gesture(
    finger_count
):

    if finger_count == 1:

        open_edge()

        return "EDGE"


    elif finger_count == 2:

        open_brave()

        return "BRAVE"


    elif finger_count == 3:

        open_file_explorer()

        return "FILES"


    elif finger_count == 4:

        open_whatsapp()

        return "WHATSAPP"


    elif finger_count == 5:

        open_desktop()

        return "DESKTOP"


    return None


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    success, frame = camera.read()


    if not success:

        print(
            "Could not read camera frame."
        )

        break


    # Mirror camera
    frame = cv2.flip(
        frame,
        1
    )


    # BGR -> RGB
    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # Detect hand
    result = hands.process(
        rgb
    )


    current_gesture = None


    # =====================================================
    # HAND DETECTED
    # =====================================================

    if result.multi_hand_landmarks:

        hand = (
            result.multi_hand_landmarks[0]
        )


        # ---------------------------------------------
        # HANDEDNESS
        # ---------------------------------------------

        handedness = (
            result
            .multi_handedness[0]
            .classification[0]
            .label
        )


        # ---------------------------------------------
        # FINGER STATES
        # ---------------------------------------------

        fingers = finger_states(
            hand,
            handedness
        )


        thumb = fingers[0]
        index = fingers[1]
        middle = fingers[2]
        ring = fingers[3]
        pinky = fingers[4]


        # ---------------------------------------------
        # COUNT
        # ---------------------------------------------

        finger_count = count_fingers(
            hand,
            handedness
        )


        # ---------------------------------------------
        # DRAW HAND
        # ---------------------------------------------

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )


        # ---------------------------------------------
        # DEBUG INFO
        # ---------------------------------------------

        cv2.putText(
            frame,
            "Hand: " + handedness,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )


        cv2.putText(
            frame,
            "Fingers: " + str(finger_count),
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )


        # =================================================
        # THUMB ONLY -> ()
        # =================================================

        if (
            thumb
            and not index
            and not middle
            and not ring
            and not pinky
        ):

            current_gesture = "BRACKETS"


        # =================================================
        # INDEX ONLY -> EDGE
        # =================================================

        elif (
            index
            and not thumb
            and not middle
            and not ring
            and not pinky
        ):

            current_gesture = "1"


        # =================================================
        # TWO FINGERS -> BRAVE
        # =================================================

        elif (
            index
            and middle
            and not thumb
            and not ring
            and not pinky
        ):

            current_gesture = "2"


        # =================================================
        # THREE FINGERS -> FILE EXPLORER
        # =================================================

        elif (
            index
            and middle
            and ring
            and not thumb
            and not pinky
        ):

            current_gesture = "3"


        # =================================================
        # FOUR FINGERS -> WHATSAPP
        # =================================================

        elif (
            index
            and middle
            and ring
            and pinky
            and not thumb
        ):

            current_gesture = "4"


        # =================================================
        # FIVE FINGERS -> DESKTOP
        # =================================================

        elif (
            thumb
            and index
            and middle
            and ring
            and pinky
        ):

            current_gesture = "5"


    # =====================================================
    # DISPLAY GESTURE
    # =====================================================

    if current_gesture:

        if current_gesture == "BRACKETS":

            display_text = "THUMB -> ()"

        elif current_gesture == "1":

            display_text = "1 FINGER -> EDGE"

        elif current_gesture == "2":

            display_text = "2 FINGERS -> BRAVE"

        elif current_gesture == "3":

            display_text = "3 FINGERS -> FILES"

        elif current_gesture == "4":

            display_text = "4 FINGERS -> WHATSAPP"

        elif current_gesture == "5":

            display_text = "5 FINGERS -> DESKTOP"

        else:

            display_text = current_gesture


        cv2.putText(
            frame,
            display_text,
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


    # =====================================================
    # EXECUTE GESTURE
    # =====================================================

    current_time = time.time()


    if current_gesture:

        # Only trigger when gesture changes
        if current_gesture != last_gesture:

            # Cooldown
            if (
                current_time
                - last_action_time
                >= GESTURE_COOLDOWN
            ):

                # -----------------------------------------
                # THUMB
                # -----------------------------------------

                if (
                    current_gesture
                    == "BRACKETS"
                ):

                    type_brackets()


                # -----------------------------------------
                # APPLICATION GESTURES
                # -----------------------------------------

                elif current_gesture in [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5"
                ]:

                    execute_finger_gesture(
                        int(current_gesture)
                    )


                last_action_time = (
                    current_time
                )


        last_gesture = current_gesture


    else:

        last_gesture = None


    # =====================================================
    # CAMERA WINDOW
    # =====================================================

    cv2.imshow(
        "Gesture Assistant",
        frame
    )


    # =====================================================
    # QUIT
    # =====================================================

    if (
        cv2.waitKey(1)
        & 0xFF
        == ord("q")
    ):

        break


# =========================================================
# CLEANUP
# =========================================================

camera.release()

cv2.destroyAllWindows()