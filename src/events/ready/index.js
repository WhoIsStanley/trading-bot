import { Events } from "discord.js"

export const event = {
    name: Events.ClientReady,
    //client.once or client.on
    once: true
}

// 'c' = event parameter to keep it separate from the already defined 'client'
export const action = (c) => {
    console.log(`Bot Ready! Logged in as ${c.user.tag}`);
}