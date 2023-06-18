<template>
    <li class="list-group-item d-flex justify-content-between py-3">
        <h6 class="my-auto">{{ propTeam.name }}</h6>
        <p class="my-auto">{{ propTeam.ip }}</p>
    </li>
</template>

<script>
export default {
    props: ['propTeam'],
};
</script>