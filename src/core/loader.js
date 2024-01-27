import { REST, Routes, Collection } from "discord.js";
import fg from 'fast-glob'
import { useAppStore } from '@/store/app'
import { readSync } from "fs";

//settingup url to DC sever
const updateSlashCommands = async(commands) => {
    const rest = new REST({
        version: 10
    }).setToken(process.env.TOKEN)
    
    const result = await rest.put(
        Routes.applicationCommands(
            /*application ID*/
            process.env.APPLICATION_ID, 
        ),
        {
            body: commands
        },
    )
    // console.log(result)
}

// Upload 'commands/**/index.js' (commands & action) to updateSlashCommands
export const loadCommands = async() => {
    const appStore = useAppStore()
    const commands = []
    const actions = new Collection();

    const files = await fg('./src/commands/**/index.js')

    for(const file of files){
        const cmd = await import(file)
        commands.push(cmd.command)
        actions.set(cmd.command.name, cmd.action)
        console.log(cmd.command)
    }

    await updateSlashCommands(commands)
    appStore.commandActionMap = actions
    //console.log(commands)
    console.log('\nAction map:')
    console.log(appStore.commandActionMap)
}

// Upload 'events/**/index.js' (events & action) to updateSlashCommands
export const loadEvents = async() => {
    const appStore = useAppStore()
    const client = appStore.client
    const files = await fg('./src/events/**/index.js')

    for(const file of files){
        const eventObj = await import(file)

        if (eventObj.event.once){
            client.once(
                eventObj.event.name,
                eventObj.action
            )
        }else{
            client.on(
                eventObj.event.name,
                eventObj.action
                )
        }
    }
    // console.log(appStore.commandActionMap)
}





