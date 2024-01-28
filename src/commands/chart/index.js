import webclawer from "./webclawer";
import { SlashCommandBuilder, EmbedBuilder } from "discord.js";
import fg from 'fast-glob'
import { useAppStore } from '@/store/app'

export const command = new SlashCommandBuilder()
    .setName('chart')
    .setDescription('Stock chart detail')
    .addStringOption(option =>
		option.setName('stockname')
			.setDescription('Input Stock Name')
            .setRequired(true))
	.addStringOption(option =>
		option.setName('timeinterval')
			.setDescription('Input chart timeinterval')
			.setRequired(true)
			.addChoices(
				{ name: '1min', value: '1 min' },
				{ name: '5min', value: '5 min' },
				{ name: '15min', value: '15 min' },
                { name: '1hour', value: '1 hr' },
				{ name: '4hour', value: '4 hr' },
				{ name: '1day', value: '1 D' },
                { name: '1week', value: '1 Wk' },
				{ name: '1month', value: '1 M' },
				{ name: '3month', value: '3 M' },
                { name: '1year', value: '1 yr' },
			));

export const action = async(interaction) => {
    const name = interaction.options.get('stockname').value
    const appStore = useAppStore()
    const ChartTime = interaction.options.get('timeinterval').value

    await interaction.deferReply();
    await webclawer(name, ChartTime);
    try{
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
    catch (e) {await interaction.editReply('Wrong Command');}

}
