import { SlashCommandBuilder } from "discord.js";

export const command = new SlashCommandBuilder()
    .setName('ping')
    .setDescription('reply ping value');


//fixing about ping value reaction
export const action = async(interaction) => {
    interaction.reply('Bot ready to use!');
}