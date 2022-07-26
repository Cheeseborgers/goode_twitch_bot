"""
Created 18/7/2022 by goode_cheeseburgers.
"""

import os
from dataclasses import asdict

import quart
from quart import render_template, ResponseReturnValue, url_for
from quart_auth import (
    AuthManager,
    Unauthorized,
    logout_user,
)
from werkzeug.utils import redirect

from goode_bot_twitch.channel_cache import ChannelCache


class WebServer(quart.Quart):
    """
    A Quart webserver class for the twitch bot instance.

    """

    def __init__(self, channels: ChannelCache, logger, import_name):

        super().__init__(
            import_name=import_name,
            static_folder="webserver/static",
            template_folder="webserver/templates",
        )

        self.log = logger
        self.channels = channels
        self.quart_secret = os.environ.get("QUART_SECRET")
        self.auth_manager = AuthManager(self)

        # Register routes.
        self.route("/")(self.home)
        self.route("/login", methods=["GET", "POST"])(self.login)
        self.route("/logout")(self.logout)
        self.route("/channels")(self.all_channels)

        # Register error handlers.
        self.errorhandler(Unauthorized)(self.redirect_to_login)

    async def home(self) -> str:
        """
        Route to handle the site root (/)

        :return: str
        """
        return await render_template("index.html")

    async def login(self):
        """

        :return:
        """
        return await render_template("login.html")

    async def logout(self):
        """

        :return:
        """
        logout_user()

    # @login_required
    async def all_channels(self):
        """

        :return:
        """
        cache_copy = self.channels.cache.copy()
        channels = {}
        for key, value in cache_copy.items():
            channels[key] = asdict(value)

        return await render_template("channels.html", channels=channels)

    async def redirect_to_login(self, *_: Exception) -> ResponseReturnValue:
        """

        :param _:
        :return:
        """
        return redirect(url_for("login"))
