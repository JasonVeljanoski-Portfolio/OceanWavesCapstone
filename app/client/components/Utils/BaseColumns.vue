<template>
  <div :style="style" class="columns">
    <slot />
  </div>
</template>

<script>
export default {
  name: 'BaseColumns',
  props: {
    width: {
      type: String,
      required: false,
      default: '100%'
    }
  },
  computed: {
    style() {
      return {
        'max-width': this.width
      }
    }
  }
}
</script>
<style scoped>
.columns {
  width: calc(100% + 20px);
  display: flex;
  flex-flow: row wrap;
  margin: 0 auto;
}

@media (max-width: 800px) {
  .column {
    min-width: 60%;
  }
}
</style>
