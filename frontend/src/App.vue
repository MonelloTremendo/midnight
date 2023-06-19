<script>
import NavBar from './components/NavBar.vue';

export default {
    name: 'App',
    components: { NavBar },
    data(){
        return {
        }
    },
    mounted() {

    }
}
</script>

<template>
  <NavBar/>
  <router-view/>
</template>

<style>
.scroll, * {
    scrollbar-color: var(--scroll-thumb-color, grey) var(--scroll-track, transparent);
    scrollbar-width: thin;
}
.scroll::-webkit-scrollbar, *::-webkit-scrollbar {
    width: var(--scroll-size, 10px);
    height: var(--scroll-size, 10px);
}
.scroll::-webkit-scrollbar-track, *::-webkit-scrollbar-track {
    background-color: var(--scroll-track, transparent);
    border-radius: var(--scroll-track-radius, var(--scroll-radius));
}
.scroll::-webkit-scrollbar-thumb, *::-webkit-scrollbar-thumb {
    background-color: var(--scroll-thumb-color, grey);
    background-image: var(--scroll-thumb, none);
    border-radius: var(--scroll-thumb-radius, var(--scroll-radius));
}
* {
    --scroll-size: 5px;
    --scroll-radius: 10px;
    --scroll-track: rgb(255 255 255 / 10%);
    --scroll-thumb-color: #9c9c9c;
}
</style>
