import { Events } from "discord.js"

export const event = {
    name: Events.ClientReady,
    // client.once = 1 or client.on = 0
    once: true
}

// 'c' = event parameter to keep it separate from the already defined 'client'
export const action = (c) => {
    console.log(`Bot Ready! Logged in as ${c.user.tag}`);
}