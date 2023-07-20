"""renpy
init -1 python:
"""

class SCState:
    """
    # Sprite Customizer State

    This class defines an object that is used to hold sprite customization
    option selections. This is used to persist the selected options as part
    of the game saves and reload those selections when loading the game from
    a save.

    ```python
    my_sprite_state = SCState()
    my_sprite.set_state(my_sprite_state)
    ```
    """
    def __init__(self, selections: dict = {}, user_state: dict = {}):
        """
        Initializes the new, blank SCState instance.

        Arguments
        ---------

        selection : dict
            Initial selection state for the SCState instance.

        user_state : dict
            Initial user variable state for the SCState instance.
        """
        if not isinstance(selections, dict):
            raise Exception("SCState selections argument must be a dict value.")
        if not isinstance(user_state, dict):
            raise Exception("SCState user_state argument must be a dict value.")

        self._selections = selections.copy()
        self._user_state = user_state.copy()

    def set_variable(self, key: str, value: any):
        """
        Store arbitrary user variable that will be passed to all layer
        callbacks.

        **NOTE**: This method cannot be used to override option selections.
        If a user state item key conflicts with a sprite customization
        option, the sprite customization option will take priority.

        ```python
        default sprite_state = SCState()

        label start:
            $ sprite_state.set_variable("mood", "happy")
            $ sprite.set_state(my_state)
            ...
            ...
            ...
            $ sprite_state.set_variable("mood", "angry")
        ```

        Arguments
        ---------

        key : str
            Key for the user state item.

        value : any
            Value to store.
        """
        self._user_state[key] = value

    def get_variable(self, key: str) -> any:
        """
        Retrieve user variable from the SCState store by key.

        Arguments
        ---------

        key : str
            Key for the user state item.

        Returns
        -------

        any
            User state value.
        """
        return self._user_state[key]

    def get_selection(self, key: str) -> any:
        """
        Looks up the target selection value.

        Arguments
        ---------

        key : str
            Key of the selection to look up.

        Returns
        -------

        any
            Target selection value (or `None` if no such value is set).
        """
        return self._selections[key]

    def set_selection(self, key: str, value: any):
        """
        Sets the target selection value.

        Arguments
        ---------

        key : str
            Key of the selection to set.

        value : any
            Value to set.
        """
        self._selections[key] = value

    def has_selection(self, key: str) -> bool:
        """
        Tests whether the state contains a selection value with the given
        key.

        Arguments
        ---------

        key : str
            Key of the selection value to test for.

        Returns
        -------

        boolean
            Whether the state contains the target selection value.
        """
        return key in self._selections

    def has_variable(self, key: str) -> bool:
        """
        Tests whether the state contains a user variable value with the
        given key.

        Arguments
        ---------

        key : str
            Key of the user variable to test for.

        Returns
        -------

        boolean
            Whether the state contains the target user variable.
        """
        return key in self._user_state
