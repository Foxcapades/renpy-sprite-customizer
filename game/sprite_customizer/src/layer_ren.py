from renpy.store import DynamicDisplayable, Attribute # type: ignore

from options.option_ren import SCOption
from options.list_option_ren import SCValueListOption

"""renpy
init -1 python:
"""

class SCLayer:
    """
    # Sprite Customization Layer

    Represents a single layer in a customizable sprite.

    This layer has zero or more customization options provided at
    construction time via named layer option keyword args.  The user's
    selections of those options are then passed to the given
    `layer_provider` to construct the underlying Displayable for the layer.

    ```python
    SCLayer("name", callback, option=("Option", [ "some", "choices" ]))

    # OR

    SCLayer("name", "my_image_{option}", option=("Option", [ "some", "choices" ]))
    ```
    """

    def __init__(self, name, layer_provider, transform=None, **options):
        """
        Initializes the new `SCLayer` instance with the given arguments.

        Arguments
        ---------

        name : str
            Internal name of the layer.  This value should be all lowercase
            and should only contain letters, numbers, and underscores.

        layer_provider : callable | str
            Either a Layer Callback used to create the displayable that
            backs this layer, or a template string containing `{var_name}`
            variables that will be injected based on the selected options.

        transform : callable | None
            Optional transform function.  This function takes a Displayable
            as a single argument and returns a Displayable.  Allows
            performing arbitrary transforms to the whole layer regardless of
            option selections.

        **options : kwargs
            Keyword arguments that define the options available to this
            layer. Keyword args must be one of the following types:

            * An <<sc-opt>> instance.
            * An <<sc-option>> instance.
            * A tuple of 2 values: `(display_name, value_list)`
            * A tuple of 3 values: `(display_name, group, value_list)`

            ```python
            option=SCOpt("Option", ["some", "choices"])

            option=SCOpt("Option", group="My Group", values=["some", "choices"])

            option=SCValueListOption("option", "Option", "My Group", ["some", "choices"])

            option=("Option", ["some", "choices"])

            option=("Option", "My Group", ["some", "choices"])
            ```
        """

        if not isinstance(name, str):
            raise Exception("SCLayer name must be a string.")

        if not (callable(layer_provider) or isinstance(layer_provider, str)):
            raise Exception("SCLayer layer_provider must be callable or a string.")

        self._name  = name
        self._provider = layer_provider
        self._state = None
        self._options = {}
        self._transform = transform

        for key, opt in options.items():
            if isinstance(opt, SCOption):
                if key != opt.key:
                    raise Exception("kwargs key and option key do not align! {} != {}".format(key, opt.key))
                self._options[key] = opt
            elif isinstance(opt, tuple):
                if len(opt) == 2:
                    self._options[key] = SCLayer._2_tuple_to_opt(key, opt)
                elif len(opt) == 3:
                    self._options[key] = SCLayer._3_tuple_to_opt(key, opt)
                else:
                    raise Exception("Unexpected {} value tuple for option {}".format(len(opt), key))
            else:
                raise Exception("SCLayer option \"{}\" was not a tuple or SCOption instance.".format(key))


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Properties
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def name(self):
        """
        Name of the layer.
        """
        return self._name

    @property
    def options(self):
        """
        List of options attached to this layer.
        """
        return self._options.values()

    @property
    def options_by_key(self):
        """
        """
        return self._options.copy()


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Internal Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    @staticmethod
    def _2_tuple_to_opt(key, tup):
        """
        Converts a two-tuple keyword arg from __init__ into an SCOption
        instance.

        Arguments
        ---------

        key : str
            Keyword for the option.

        tup : tuple
            Tuple containing a display name and a list of option values.
        """
        if not isinstance(tup[0], str):
            raise Exception("invalid 2 tuple passed as option {}, first value must be a string".format(key))

        if isinstance(tup[1], list) or isinstance(tup[1], set):
            return SCValueListOption(key, tup[0], tup[0], tup[1].copy())

        raise Exception("invalid 2 tuple passed as option {}, second value must be a list or set".format(key))

    @staticmethod
    def _3_tuple_to_opt(key, tup):
        """
        Converts a three-tuple keyword arg from __init__ into an SCOption
        instance.

        Arguments
        ---------

        key : str
            Keyword for the option.

        tup : tuple
            Tuple containing a display name, a group name, and a list of
            option values.
        """
        if not isinstance(tup[0], str):
            raise Exception("invalid 3 tuple passed as option {}, first value must be a string".format(key))

        if not isinstance(tup[1], str):
            raise Exception("invalid 3 tuple passed as option {}, second value must be a string".format(key))

        if isinstance(tup[2], list) or isinstance(tup[2], set):
            return SCValueListOption(key, tup[0], tup[1], tup[2].copy())

        raise Exception("invalid 3 tuple passed as option {}, third value must be a list or set".format(key))

    def _require_option(self, key):
        """
        Requires that the given option keyword is known to this layer, then
        returns the target option.

        Arguments
        ---------

        key : str
            Keyword for the option to require.
        """
        if key not in self._options:
            raise Exception("Unrecognized SCLayer option \"{}\"".format(key))

        return self._options[key]

    def _render(self, st, at, **kwargs):
        if callable(self._provider):
            return self._render_function(st, at, **kwargs)
        else:
            return self._render_string(st, at, **kwargs)

    def _render_string(self, st, at, **kwargs):
        out = self._provider
        vals = kwargs.copy()

        for key, value in self._state._user_state.items():
            vals[key] = value

        for key, option in self._options.items():
            vals[key] = option.selection_value

        for key, value in vals.items():
            out = out.replace("{" + key + "}", value)

        return (out, 0.0)

    def _render_function(self, st, at, **kwargs):
        kwargs["st"] = st
        kwargs["at"] = at

        # Go through user state first to prevent it from overwriting real
        # option selections.  TODO: Should we allow overriding selections?
        for key, value in self._state._user_state.items():
            kwargs[key] = value

        for key, option in self._options.items():
            kwargs[key] = option.selection_value

        out = self._provider(**kwargs)

        return out if isinstance(out, tuple) else (out, 0.0)

    def _set_state(self, state):
        self._state = state
        for opt in self._options.values():
            opt._set_state(state)

    def _append_options_to_dict(self, d):
        for key, opt in self._options.values():
            d[key] = opt

    def _clone(self):
        """
        Creates a clone of this layer instance sans user state.

        Returns
        -------

        SCLayer
            A new `SCLayer` instance containing the same values configured
            on this instance minus any user state.
        """
        options = {}

        for key, option in self._options.items():
            options[key] = option._clone()

        return SCLayer(self._name, self._provider, self._transform, **options)


    def _build_image(self):
        """
        Builds the DynamicDisplayable that represents this `SCLayer`
        instance.

        Returns
        -------

        DynamicDisplayable
            The DynamicDisplayable that represents this `SCLayer` instance.
        """
        if self._transform == None:
            return DynamicDisplayable(self._render)

        return self._transform(DynamicDisplayable(self._render))

    def _build_attribute(self):
        """
        Builds a LayeredImage Attribute instance to represent this `SCLayer`
        instance.

        Returns
        -------

        Attribute
            A LayeredImage Attribute instance to represent this `SCLayer`
            instance.
        """
        return Attribute(None, self._name, image=self._build_image(), default=True)
