"""
Created 20/7/2022 by goode_cheeseburgers.
"""
from quart import Blueprint, render_template

blueprint = Blueprint("auth", __name__)


@blueprint.route("/")
async def index():
    """
    Fix this docstring

    :return:
    """
    return await render_template("index.html")
