<template>
  <div :style="style" class="column">
    <slot />
  </div>
</template>

<script>
export default {
  name: 'BaseColumn',
  props: {
    align: {
      type: String,
      required: false,
      default: 'center'
    },
    width: {
      type: String,
      required: false,
      default: '200px'
    }
  },
  computed: {
    style() {
      let align = this.align
      if (align === 'start') align = 'flex-start'
      if (align === 'end') align = 'flex-end'
      return {
        'align-self': align,
        'flex-basis': this.minWidth
      }
    }
  }
}
</script>

<style scoped>
.column {
  flex: 1 1;
  margin: 0 10px;
  flex-wrap: wrap;
}
</style>
