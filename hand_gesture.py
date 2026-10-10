def finger_states(hand_landmarks, handedness):
    """
    Detect the state of all five fingers.

    Returns:
        [
            thumb,
            index,
            middle,
            ring,
            pinky
        ]

    True  = finger is open
    False = finger is closed
    """

    lm = hand_landmarks.landmark

    # -----------------------------------------
    # INDEX FINGER
    # -----------------------------------------

    index = lm[8].y < lm[6].y

    # -----------------------------------------
    # MIDDLE FINGER
    # -----------------------------------------

    middle = lm[12].y < lm[10].y

    # -----------------------------------------
    # RING FINGER
    # -----------------------------------------

    ring = lm[16].y < lm[14].y

    # -----------------------------------------
    # PINKY
    # -----------------------------------------

    pinky = lm[20].y < lm[18].y

    # -----------------------------------------
    # THUMB
    # -----------------------------------------

    if handedness == "Right":

        thumb = lm[4].x < lm[3].x

    else:

        thumb = lm[4].x > lm[3].x

    return [
        thumb,
        index,
        middle,
        ring,
        pinky
    ]


# =====================================================
# COUNT FINGERS
# =====================================================

def count_fingers(
    hand_landmarks,
    handedness
):

    fingers = finger_states(
        hand_landmarks,
        handedness
    )

    return sum(fingers)


# =====================================================
# THUMB ONLY
# =====================================================

def thumb_only(
    hand_landmarks,
    handedness
):

    fingers = finger_states(
        hand_landmarks,
        handedness
    )

    thumb = fingers[0]
    index = fingers[1]
    middle = fingers[2]
    ring = fingers[3]
    pinky = fingers[4]

    return (
        thumb
        and not index
        and not middle
        and not ring
        and not pinky
    )