import renpy  # type: ignore

"""renpy
init python:
"""

renpy.register_shader(
    "fxcpds.color_block",
    variables="""
        uniform   vec3  u_top_right_rgb;
        uniform   vec2  u_model_size;
        varying   float v_gradient_x_done;
        varying   float v_gradient_y_done;
        attribute vec4  a_position;
    """,
    vertex_300="""
        v_gradient_x_done = a_position.x / u_model_size.x;
        v_gradient_y_done = a_position.y / u_model_size.y;
    """,
    fragment_300="""
        vec3 top = mix(vec3(1.0, 1.0, 1.0), u_top_right_rgb, v_gradient_x_done);
        gl_FragColor = vec4(mix(vec3(0, 0, 0), top, 1.0 - v_gradient_y_done), 1.0);
    """,
)

renpy.register_shader(
    "fxcpds.slider",
    variables="""
        uniform   vec2  u_model_size;
        varying   float v_gradient_y_done;
        attribute vec4  a_position;
    """,
    fragment_functions="""
        vec3 hue2rgb(float hue) {
            vec3 rgb = clamp(abs(mod(hue * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0);
            return 0.5 + (rgb - 0.5);
        }
    """,
    vertex_300="""
        v_gradient_y_done = a_position.y / u_model_size.y;
    """,
    fragment_300="""
        gl_FragColor = vec4(hue2rgb(1.0 - v_gradient_y_done), 1.0);
    """,
)

