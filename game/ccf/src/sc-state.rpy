init -1 python:

    class SCState:
        """
        # Sprite Customizer State

        This class defines an object that is used to hold sprite customization
        option selections. This is used to persist the selected options as part
        of the game saves and reload those selections when loading the game from
        a save.

        The state is a dict of 1 based indexes of option values.

        ```python
        my_sprite_state = SCState()
        my_sprite.set_state(my_sprite_state)
        ```
        """
        def __init__(self):
            """
            Initializes the new, blank SCState instance.
            """
            self._state = {}

        def get_selection(self, key):
            """
            Looks up the target selection value.  If the target selection value
            is unknown to the SCState object, the value `1` will be recorded in
            the state and returned from this method.

            Arguments:

            key (str): Selection key.

            Returns:

            int: Current selection state for the given option selection.
            """
            if not key in self._state:
                self._state[key] = 1

            return self._state[key]

        def inc_selection(self, key, max):
            """
            Increment the selection value for the given option to a maximum of
            `max`, rolling back over to `1` if it would exceed that maximum.

            Arguments:

            key (str): Key of the selection option whose value should be
            incremented.

            max (int): Max value the selection option can possibly be.
            """
            if not key in self._state:
                self._state[key] = 2
            elif self._state[key] >= max:
                self._state[key] = 1
            else:
                self._state[key] += 1

        def dec_selection(self, key, max):
            """
            Decrement the selection value for the given option to a minimum of
            `1`, rolling over to `max` if it would go below `1`.

            Arguments:

            key (str): Key of the selection option whose value should be
            decremented.

            max (int): Max value the selection option can possibly be.
            """
            if not key in self._state:
                self._state[key] = max
            elif self._state[key] == 1:
                self._state[key] = max
            else:
                self._state[key] -= 1
