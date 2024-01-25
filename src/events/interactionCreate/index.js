//interaction with users in discord
import { Events } from 'discord.js'
import { useAppStore } from '@/store/app'

export const event = {
    name: Events.InteractionCreate,
}

export const action = async(interaction) => {
    if(!interaction.isChatInputCommand())return
    const appStore = useAppStore();
    const action = appStore.commandActionMap.get(interaction.commandName)
    
    await action(interaction)
}


