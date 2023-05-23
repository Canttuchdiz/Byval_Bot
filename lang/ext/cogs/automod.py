from discord import Interaction, AutoModRuleEventType, AutoModRuleTriggerType, \
    AutoModRuleActionType, AutoModTrigger, AutoModRuleAction, HTTPException, Embed, Color
from discord.app_commands import command, Group, autocomplete, Choice, describe
from discord.ext.commands import Cog, Bot
import traceback


class AutoModCog(Cog):

    group = Group(name="rule", description="The group behind all automod commands.")

    def __init__(self, bot: Bot) -> None:
        self.client = bot

    async def trigger_autocomplete(self, interaction: Interaction, current: str) -> list:

        try:

            return [Choice(name=t_type.name, value=str(t_type.value)) for t_type in AutoModRuleTriggerType if
                    current.lower() in t_type.name.lower()]

        except Exception as e:
            traceback.print_exc()

    async def rule_autocomplete(self, interaction: Interaction, current: str) -> list:
        rules = await interaction.guild.fetch_automod_rules()
        return [Choice(name=rule.name, value=str(rule.id)) for rule in rules if current.lower() in rule.name.lower()]

    @group.command(name="create", description="Creates an automod rule.")
    @describe(name="Name of rule", trigger="Automod trigger", enabled="If rule is enabled")
    @autocomplete(trigger=trigger_autocomplete)
    async def create_rule(self, interaction: Interaction, name: str, trigger: str, enabled: bool) -> None:
        try:
            am_trigger = AutoModRuleTriggerType(int(trigger))
        except ValueError as e:
            await interaction.response.send_message("Invalid trigger.", ephemeral=True)
            return
        try:
            await interaction.guild.create_automod_rule(name=name,
                                                        event_type=AutoModRuleEventType.message_send,
                                                        trigger=AutoModTrigger(type=am_trigger),
                                                        actions=[AutoModRuleAction()], enabled=enabled)
            await interaction.response.send_message("Rule successfully added!", ephemeral=True)
            self.client.total_rules += 1
        except HTTPException as e:
            await interaction.response.send_message("Rule already exists.", ephemeral=True)

    @group.command(name="delete", description="Deletes an automod rule.")
    @describe(rule="Name of rule")
    @autocomplete(rule=rule_autocomplete)
    async def delete_rule(self, interaction: Interaction, rule: str) -> None:
        try:
            am_rule = await interaction.guild.fetch_automod_rule(int(rule))
            await am_rule.delete()
            await interaction.response.send_message("Rule was deleted!", ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message("Invalid rule.", ephemeral=True)

    @group.command(name="list", description="Lists automod rules.")
    async def rule_list(self, interaction: Interaction) -> None:
        rules = await interaction.guild.fetch_automod_rules()
        rules_list = ', '.join([rule.name for rule in rules])
        embed = Embed(title="Automod Rules", description=rules_list, color=Color.blue())
        await interaction.response.send_message(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(AutoModCog(bot))
