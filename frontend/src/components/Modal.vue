<template>
    <!-- Modal -->
    <div class="modal" :id="propId" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" :class="{ 'modal-dialog-centered':propCenter }">
        <div class="modal-content">
        <div class="modal-header">
            <h4 class="modal-title" id="exampleModalLabel">{{ propTitle }}</h4>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            <slot></slot>
        </div>
        <div class="modal-footer">
            <button v-if="propNopFunc !== undefined" @click="propNopFunc" type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                {{ propNopText }}
            </button>
            <button v-if="propYepFunc !== undefined" @click="propYepFunc" type="button" class="btn btn-primary" data-bs-dismiss="modal">
                {{ propYepText }}
            </button>
        </div>
        </div>
    </div>
    </div>
</template>

<script>
export default {
    props: {
        propTitle: String,
        propId: String,
        propYepText: String,
        propYepFunc: Function,
        propNopText: String,
        propNopFunc: Function,
        propCenter: Boolean,
    },
    data() {
        return {
            
        };
    },
};
</script>