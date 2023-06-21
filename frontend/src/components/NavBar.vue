<template>
    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid px-3">
            <a class="navbar-brand d-flex flex-row-reverse" href="/">
                <img :src="logo_svg" class="d-inline-block mx-2" alt="" height="32">
                Mezzanotte
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <router-link to="/" class="nav-link">Dashboard</router-link>
                <router-link to="/exploits" class="nav-link">Exploits</router-link>
            </div>
            </div>
        </div>
    </nav>
</template>

<style>
nav {
    background-color: var(--bs-tertiary-bg);
}

.router-link-active {
    color: #42b983 !important;
    /*color: var(--bs-primary) !important;*/
}

</style>

<script>
import logo_svg from "../assets/images/noun-midnight.svg";

export default {
  name: 'NavBar',
  props: {
    propCurrentTab: String
  },
  data() {
    return {
        logo_svg
    };
  },  
}
</script>
