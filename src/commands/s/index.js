import webclawer from "./webclawer";
import { SlashCommandBuilder, EmbedBuilder } from "discord.js";
import fg from 'fast-glob'
import { useAppStore } from '@/store/app'

export const command = new SlashCommandBuilder()
    .setName('chart')
    .setDescription('Stock chart detail')
    .addStringOption(option =>
		option.setName('stockname')
			.setDescription('The input Stock Name')
            .setRequired(true));
    /*
    .addSubcommand(subcommand => subcommand.setName('Name').setDescription('Stock Name')
        .addStringOption(option => option.setName('Name').setDescription('Stock Name').setRequired(true)));
*/
export const action = async(interaction) => {
    /*
    const name = interaction.options.get('Name');
    const num = interaction.user.id.get()
    console.log(interaction)
    */
    const name = interaction.options.get('stockname').value
    const appStore = useAppStore()

    await interaction.deferReply();
    await webclawer(name);
    const ChartTime = '1D'
    const files = await fg(`./screenshot/*${name}.png`)
    
    const stockEmbed = await new EmbedBuilder()
    .setColor(0x0099FF)
    .setAuthor({ name: `${appStore.ChartName} - ${ChartTime}`, iconURL: `attachment://icon${name}.png`, url: `https://www.tradingview.com/chart/?symbol=${name}` })
	.setImage(`attachment://${name}.png`);

    console.log('\nFile:')
    console.log(files)
    console.log('\nEmbed:')
    console.log(stockEmbed)

    await interaction.editReply({ embeds: [stockEmbed], files: files });
}
