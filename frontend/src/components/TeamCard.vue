<template>
    <li @click="propOnClick" class="list-group-item d-flex justify-content-between py-3" :class="{ selected: propSelected }">
        <h6 class="my-auto">{{ propTeam.name }}</h6>
        <p class="my-auto">{{ propTeam.ip }}</p>
    </li>
</template>

<style scoped>
li {
    cursor: pointer;
}

.selected {
    background-color: #352f85;
    color: white;
}

</style>

<script>
export default {
    props: {
        propTeam: Object,
        propSelected: Boolean,
        propOnClick: Function,
    },
};
</script>