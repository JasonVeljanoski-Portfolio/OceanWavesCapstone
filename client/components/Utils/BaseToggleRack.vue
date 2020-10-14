<template>
  <div class="flexcontainer">
    <div v-for="(item, i ) in items" :key="i" :class="{ active: i === activeItem}" class="button">
      <div class="button" :class="{ active: i === activeItem}" @click="selectItem(i, item)">{{ item }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseToggleRack',
  props: {
    items: {
      type: Array,
      required: false,
      default: null,
      validator(value) {
        return typeof value === 'object'
      }
    }
  },
  data() {
    return {
      activeItem: 0
    }
  },
  methods: {
    selectItem(i, item) {
      this.$emit('toggle', item)
      this.activeItem = i
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.button
  background #efefef
  font-weight bold
  cursor pointer
  padding 0px 3px 0px 3px
  margin 2px

.button:hover
  opacity 0.8

.active
  background #d3d3d3

.flexcontainer
   display flex
   align-items center
   justify-content center
   flex-flow row wrap
   align-content flex-end
</style>
