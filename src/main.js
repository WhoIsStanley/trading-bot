// Require the necessary discord.js classes
import { Client, Events, GatewayIntentBits } from 'discord.js'
import dotenv from 'dotenv'
import vueinit from '@/core/vue.js'
import { loadCommands, loadEvents } from '@/core/loader'
import { useAppStore } from '@/store/app'


// init dotenv, vue, pinia
dotenv.config()
vueinit()

loadCommands();

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds] });
const appStore = useAppStore()
appStore.client = client

loadEvents();

// Log in to Discord with your client's token
client.login(process.env.TOKEN);