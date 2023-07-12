# Create new CCState objects to hold the state of our customizable sprite's
# settings.  This is necessary to persist the customization selections in
# the game's save data.
#
# One CCState object is needed for every customized character sprite in use.
default player_sprite_state = CCState()
default antagnoist_sprite_state = CCState()

# Define our characters like normal.
define pc = Character("Player", image="player")
define an = Character("Antagonist", image="antagonist")

# You can even use our custom sprites in image proxies:
image side player = LayeredImageProxy("player", Transform(yoffset=350, xoffset=-50, zoom=0.7))
image side antagonist = LayeredImageProxy("antagonist", Transform(yoffset=350, xoffset=-50, zoom=0.7))


label after_load:
    # !!IMPORTANT!!
    # Recall the saved state for all our custom sprites.
    $ cc_player_sprite.set_state(player_sprite_state)
    $ cc_antagonist_sprite.set_state(antagnoist_sprite_state)
    return

label start:

    # !!IMPORTANT!!
    # Set the state for all our custom sprites.
    $ cc_player_sprite.set_state(player_sprite_state)
    $ cc_antagonist_sprite.set_state(antagnoist_sprite_state)

    show player at left
    show antagonist at right:
        xzoom -1.0

    pc "Customize my sprite!"

    call screen character_creator("player", cc_player_sprite)

    an "Now customize {i}my{/i} sprite!"

    call screen character_creator("antagonist", cc_antagonist_sprite)

    pc "Now both characters are customized separately!"

    an "Use this for whatever evil purposes you will."

    return

