// libaray
import { Client, Events, GatewayIntentBits } from 'discord.js';
import vueinit from '@/core/vue';
import dotenv from 'dotenv';
import { loadCommands, loadEvents } from '@/core/loader';
import { useAppStore } from '@/store/app';

vueinit();
dotenv.config();

//start loader1
loadCommands();

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const appStore = useAppStore();
appStore.client = client;

//start loader2
loadEvents();

// Log in to Discord with your client's token
client.login(process.env.TOKEN);