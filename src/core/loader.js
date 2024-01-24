import { REST, Routes, Collection } from "discord.js";
import fg from 'fast-glob'
import { useAppStore } from '@/store/app'

//settingup url to DC sever
const updateSlashCommands = async(commands) => {
    const rest = new REST({version: 10})
        .setToken(process.env.TOKEN)
    
    const result = await rest.put(
        Routes.applicationGuildCommands(/*application ID*/process.env.APPLICATION_ID, /*guild ID*/process.env.GULID_ID),
        {
            body: commands,
        },
    )
}

//loader1
//search commands files and upload index.js command & event to updateSlashCommands
export const loadCommands = async() => {
    const appStore = useAppStore()
    const commands = []
    const actions = new Collection()
    const files = await fg('./src/commands/**/index.js')

    for(const file of files){
        const cmd = await import(file)
        commands.push(cmd.command)
        actions.set(cmd.command.name, cmd.action)
    }

   await updateSlashCommands(commands)
   appStore.commandsActionMap = actions

   console.log(appStore.commandsActionMap)
}

//loader 2
export const loadEvents = async() => {
    const appStore = useAppStore()
    const client = appStore.client
    const files = await fg('./src/events/**/index.js')

    for(const file of files){
        const eventFile = await import(file)

        if(eventFile.event.once){
            client.once(
                eventFile.event.name, 
                eventFile.action
            );
        }
        else{
            client.on(
                eventFile.event.name, 
                eventFile.action
            );
        }
        
    }
}