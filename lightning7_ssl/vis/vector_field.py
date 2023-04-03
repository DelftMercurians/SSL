import base64
import io
from typing import Any, Callable

import numpy as np
from matplotlib import pyplot as plt

from lightning7_ssl.vecMath.vec_math import Vec2


def draw_vector_field(
    field_size: tuple[float, float],
    fun: Callable[[Any], Vec2],
    step: float = 500,
    margin: tuple[float, float] = (3750, 2850),  # magic numbers that line up that image with the field
    **kwargs,
) -> str:
    """Draw a vector field on the current axes.

    Args:
        field_size: The size of the field to draw the vector field on.
        fun: A function that takes a position and returns a vector.
        step: The step size to use when drawing the vector field.

    Returns:
        A base64 data url containing the image in PNG format.
    """
    field_size = (field_size[0] + margin[0], field_size[1] - margin[1])
    x = np.arange(-field_size[0] / 2, field_size[0] / 2, step)
    y = np.arange(-field_size[1] / 2, field_size[1] / 2, step)
    X, Y = np.meshgrid(x, y)
    U, V = np.zeros(X.shape), np.zeros(Y.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            U[i, j], V[i, j] = fun(Vec2(X[i, j], Y[i, j]))

    # Transform to bottom-left origin from center origin
    X = X + field_size[0] / 2
    Y = Y + field_size[1] / 2

    # Figure size in inchs using correct aspect ratio
    plt.figure()

    plt.quiver(X, Y, U, V, **kwargs)
    # no axes
    plt.axis("off")
    # no border
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    # no ticks
    plt.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        labelbottom=False,
        right=False,
        left=False,
        labelleft=False,
    )
    # no background
    plt.gca().set_facecolor("none")
    plt.gcf().set_facecolor("none")
    # no margins
    plt.margins(0, 0)
    # fill the whole figure
    plt.tight_layout(pad=0)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    plt.close()
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{img_data}"
