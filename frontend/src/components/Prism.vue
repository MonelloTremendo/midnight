<template>
    <div>
        <prism language="bash" :plugins="['command-line']" :code="code"></prism>
    </div>
</template>

<style lang="css" scoped src="prismjs/themes/prism.css"></style>

<script>
import Prism from 'vue-prismjs';
import 'prismjs/themes/prism.css';

export default {
    components: {
    Prism
    },
    data () {
        return {
            code: 'npm install vue-prismjs --save'
        }
    }
}
</script>