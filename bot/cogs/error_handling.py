from discord import Interaction
from discord.ext.commands import Bot, Cog, CommandError
from discord.app_commands import (
    AppCommandError,
    CheckFailure,
    MissingRole,
    MissingPermissions,
    CommandNotFound,
    CommandOnCooldown
)

error_map = {
    MissingRole: "You are missing the role {error.missing_role} to use this command.",
    MissingPermissions: "You are missing the required permissions to use this command.",
    CheckFailure: "You are not allowed to use this command.",
    CommandNotFound: "This command was not found.",
    CommandOnCooldown: "This command is on cooldown. Try again in {error.retry_after:.2f} seconds."
}  # note: some of these errors are not yet implemented in the bot


class ErrorHandler(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.error_message = "An error occurred."
        bot.tree.error(coro=self.__dispatch_to_app_command_handler)

    async def __dispatch_to_app_command_handler(self, interaction: Interaction, error: AppCommandError):
        self.bot.dispatch("app_command_error", interaction, error)

    @Cog.listener()
    async def on_app_command_error(self, interaction: Interaction, error: CommandError):
        """
        Handles all errors that occur in app commands and sends a response to the user.

        :param interaction: Interaction
        :param error: Error
        """
        # returns the error message if it exists, else returns the default error message
        error_message = error_map.get(type(error), self.error_message)
        error_message = error_message.format(error=error)  # formats the error message if it has a format string
        await interaction.response.send_message(error_message, ephemeral=True)


async def setup(bot: Bot):
    await bot.add_cog(ErrorHandler(bot))
