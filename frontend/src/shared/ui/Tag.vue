<script setup lang="ts">
    interface Props {
        value: string;
        type?: "green" | "red" | "yellow"
    }

    const props = defineProps<Props>();
</script>

<template>
    <div class="tag" :class="props.type ? `tag_${props.type}` : ''">{{ props.value }}</div>
</template>

<style scoped>
.tag.tag_red {
    color: #bf0031;
    background-color: #ffecf1;
}

.tag.tag_green {
    color: #1e6d00;
    background-color: #e1f7d8;
}

.tag.tag_yellow {
    color: #9e3f00;
    background-color: #fff0cb;
}

.tag {
    padding: 4px 12px;
    background-color: #d5d6f8;
    color: #2b31b3;
    width: fit-content;
    border-radius: 100px;
    font-size: 14px;
    font-weight: 500;
    line-height: 21px;
    letter-spacing: 0.25px;
}
</style>