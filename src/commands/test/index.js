import { SlashCommandBuilder } from "discord.js";

export const command = new SlashCommandBuilder()
    .setName('test')
    .setDescription('reply a testing message');

export const action = async(ctx) => {
    ctx.reply('Bot is ready to use!');
}