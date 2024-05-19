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
            .setRequired(true));

export const action = async(interaction) => {
    const name = interaction.options.get('stockname').value
    const appStore = useAppStore()

    await interaction.deferReply();
    await webclawer(name);
    try{
        const files = await fg(`./screenshot/*${name}.png`)
    
        const stockEmbed = await new EmbedBuilder()
        .setColor(0x0099FF)
        .setAuthor({ name: `${appStore.ChartName} - ${ChartTime}`, iconURL: `attachment://icon${name}.png`, url: `https://www.tradingview.com/chart/?symbol=${name}` })
        .addFields(
            { name: 'Regular field title', value: 'Some value here' },
            { name: '\u200B', value: '\u200B' },
            { name: 'Inline field title', value: 'Some value here', inline: true },
            { name: 'Inline field title', value: 'Some value here', inline: true },
        )
        .setFooter({ text: 'Source by tradingview'});

        console.log('\nFile:')
        console.log(files)
        console.log('\nEmbed:')
        console.log(stockEmbed)
    
        await interaction.editReply({ embeds: [stockEmbed], files: files });
    } 
    catch (e) {await interaction.editReply('Wrong Command');}

}
