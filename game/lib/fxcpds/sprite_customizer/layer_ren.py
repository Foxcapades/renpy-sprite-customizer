from renpy.store import DynamicDisplayable, Attribute # type: ignore

from options.option_ren import SCOption
from options.list_option_ren import SCListOption
from .state_ren import SCState


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

    def __init__(
        self,
        name: str,
        layer_provider: str | function,
        options: SCOption | list[SCOption] = None,
        transform: function = None,
    ):
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

        options : list[SCOption]
            A list of 1 or more SCOption instances for all the options available
            to this layer.

        transform : callable | None
            Optional transform function.  This function takes a Displayable
            as a single argument and returns a Displayable.  Allows
            performing arbitrary transforms to the whole layer regardless of
            option selections.
        """

        if not isinstance(name, str):
            raise Exception("SCLayer name must be a string.")

        if not (callable(layer_provider) or isinstance(layer_provider, str)):
            raise Exception("SCLayer layer_provider must be callable or a string.")

        self._name: str = name
        self._provider: str|function = layer_provider
        self._state: SCState | None = None
        self._options: dict[str, SCOption] = {}
        self._transform: function = transform

        if options is None:
            pass
        elif isinstance(options, SCOption):
            self._options[options.key] = options
        elif isinstance(options, list):
            for i in range(len(options)):
                opt = options[i]
                if isinstance(opt, SCOption):
                    if opt.key in self._options:
                        raise Exception(f'More than one option defined with the key "{opt.key}"')
                    self._options[opt.key] = opt
                else:
                    raise Exception(f"SCLayer option {i+1} was not an SCOption instance.")
        else:
            raise Exception('"options" must be an SCOption or a list of SCOptions')

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Properties
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def name(self) -> str:
        """
        Name of the layer.
        """
        return self._name

    @property
    def options(self) -> list[SCOption]:
        """
        List of options attached to this layer.
        """
        return self._options.values()

    @property
    def options_by_key(self) -> dict[str, SCOption]:
        """
        """
        return self._options.copy()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Internal Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _render(self, st: float, at: float, **kwargs: any) -> tuple[any, float]:
        if callable(self._provider):
            return self._render_function(st, at, **kwargs)
        else:
            return self._render_string(**kwargs)

    def _render_string(self, **kwargs: any) -> tuple[str, float]:
        out = self._provider
        vals = kwargs.copy()

        for key, value in self._state._user_state.items():
            vals[key] = value

        for key, option in self._options.items():
            vals[key] = option.selection_value

        for key, value in vals.items():
            out = out.replace("{" + key + "}", value)

        return (out, 0.0)

    def _render_function(self, st: float, at: float, **kwargs: any) -> tuple[any, float]:
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

    def _set_state(self, state: SCState):
        self._state = state
        for opt in self._options.values():
            opt._set_state(state)

    def _append_options_to_dict(self, d: dict[str, SCOption]):
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
        options: list[SCOption] = []

        for option in self._options.values():
            tmp = option._clone()
            tmp._post_clone()
            options.append(tmp)

        return SCLayer(self._name, self._provider, options, self._transform)

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
