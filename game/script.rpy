# Create new SCState objects to hold the state of our customizable sprite's
# settings.  This is necessary to persist the customization selections in
# the game's save data.
#
# One SCState object is needed for every customized character sprite in use.
default player_sprite_state = SCState()
default antagonist_sprite_state = SCState()

# Define our characters like normal.
define pc = Character("Player", image="player")
define an = Character("Antagonist", image="antagonist")

label after_load:
    # !!IMPORTANT!!
    # Recall the saved state for all our custom sprites.
    $ cc_player_sprite.set_state(player_sprite_state)
    $ cc_antagonist_sprite.set_state(antagonist_sprite_state)
    return

label start:

    # !!IMPORTANT!!
    # Set the state for all our custom sprites.
    $ cc_player_sprite.set_state(player_sprite_state)
    $ cc_antagonist_sprite.set_state(antagonist_sprite_state)

    show player at left
    show antagonist relaxed smile at right:
        xzoom -1.0

    pc "Customize my sprite!"

    $ quick_menu = False
    call screen sprite_creator("player", cc_player_sprite)
    $ quick_menu = True

    show player relaxed smile
    show antagonist -relaxed -smile

    an "Now customize {i}my{/i} sprite!"

    $ quick_menu = False
    call screen sprite_creator("antagonist", cc_antagonist_sprite)
    $ quick_menu = True

    show antagonist angry_brows grin

    pc "Now both characters are customized separately!"

    an "Use this for whatever evil purposes you will."

    return

