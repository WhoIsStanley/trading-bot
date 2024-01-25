import { createApp } from 'vue'
import { createPinia } from 'pinia'

export default () => {
    console.log('vite init')
    const vue = createApp({})
    const pinia = createPinia()

    vue.use(pinia)
}