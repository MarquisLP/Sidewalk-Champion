class CharacterPreview(object):
    """A looped character animation with an accompanying shadow and
    name.

    Class Constants:
        NAME_COLOR: A tuple containing the RGB values for the name
            text's color.
        NAME_OUTLINE_COLOR: A tuple containing the RGB values for the
            color of the name text's outline.
        SHADOW_HEIGHT: An integer for the height of the shadow, in
            pixels.
        SHADOW_COLOR: A tuple containing the RGB values for the color
            of the shadow.
        OFFSET_FROM_SHADOW: An integer for the distance, in pixels,
            from the bottom edge of the character sprite to the vertical
            center of the shadow.

    Attributes:
        x: An integer for the x-coordinate of the sprite relative to the
            screen.
        y: An integer for the y-coordinate of the sprite relative to the
            screen.
        is_reversed: A Boolean indicating whether the character is
            facing to the left instead of to the right.
        name: A PyGame Surface with the character's name rendered onto
            it.
        spritesheet: A PyGame Surface containing all of the animation
            frames in order.
        shadow: A PyGame Surface with the character's shadow drawn onto
            it.
        frame_width: An integer for width, in pixels, of each frame in
            the animation.
        frame_durations: A tuple of integers containing the duration,
            in update cycles, of each animation frame in order.
        current_frame: An integer for the index of the animation frame
            currently being displayed.
        frame_timer: An integer for the number of update cycles elapsed
            since the current animation frame was shown.
    """
    NAME_COLOR = (255, 255, 255)
    NAME_OUTLINE_COLOR = (80, 80, 80)
    SHADOW_HEIGHT = 14
    SHADOW_COLOR = (0, 5, 90)
    OFFSET_FROM_SHADOW = 3
