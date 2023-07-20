# Create new SCState objects to hold the state of our customizable sprite's
# settings.  This is necessary to persist the customization selections in
# the game's save data.
#
# One SCState object is needed for every customized character sprite in use.
default player_sprite_state = SCState()

# For the antagonist, set some different defaults than the player.
default antagonist_sprite_state = SCState({
    "skin_color": 3,
    "clothes": 1,
    "hair_style": 2,
    "hair_color": "#526f48",
    "accessories": 3,
    "eye_color": 2
})

# Define our characters like normal.
define pc = Character("Player", image="player")
define an = Character("Antagonist", image="antagonist", color="#a174b0")


label after_load:
    # !!IMPORTANT!!
    # Recall the saved state for all our custom sprites.
    $ sc_player_sprite.set_state(player_sprite_state)
    $ sc_antagonist_sprite.set_state(antagonist_sprite_state)
    return


label start:

    # !!IMPORTANT!!
    # Set the state for all our custom sprites.
    $ sc_player_sprite.set_state(player_sprite_state)
    $ sc_antagonist_sprite.set_state(antagonist_sprite_state)

    scene classroom

    show player at left
    show antagonist relaxed smile at right:
        xzoom -1.0

    pc "Customize my sprite!"

    $ quick_menu = False
    call screen sprite_creator("player", sc_player_sprite)
    $ quick_menu = True

    show player relaxed smile
    show antagonist -relaxed -smile

    an "Now customize {i}my{/i} sprite!"

    $ quick_menu = False
    call screen sprite_creator("antagonist", sc_antagonist_sprite)
    $ quick_menu = True

    show antagonist angry_brows grin

    pc "Now both characters are customized separately!"

    an "Use this for whatever evil purposes you will."

    return

