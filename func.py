import discord
import json
import global_value as g_value
import global_value as g_path

class CounterView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="カウントする！", style=discord.ButtonStyle.success, custom_id="counter")
    async def count(self,  interaction: discord.Interaction, button: discord.ui.Button):
        g_value.count += 1
        await interaction.response.edit_message(content=f"現在のカウント数：{g_value.count}", view=CounterView())
        with open(g_path.path, "w") as file:
            json.dump(g_value.count, file, indent=4)

    @discord.ui.button(label="リセットする！", style=discord.ButtonStyle.red, custom_id="counter_reset")
    async def count_reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        g_value.count = 0
        await interaction.response.edit_message(content=f"現在のカウント数：{g_value.count}", view=CounterView())
        with open(g_path.path, "w") as file:
            json.dump(g_value.count, file, indent=4)