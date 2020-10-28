<template>
  <h2 class="anchor">
    <slot />
  </h2>
</template>

<script>
export default {
  name: 'BaseTitle',
  mounted() {
    this.setHeaderID()
  },
  updated() {
    this.setHeaderID()
  },
  methods: {
    createForgivingID(str) {
      if (str === undefined || str === null) return

      return str
        .trim()
        .toLowerCase()
        .split(' ')
        .join('_')
    },
    /* Set header ID to match navs a.href */
    setHeaderID() {
      const _header = this.$el
      const _forgivingID = this.createForgivingID(_header.innerHTML)
      _header.setAttribute('id', _forgivingID) // set id for _header element. This links to anchors href
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

h2
  margin 0
  padding-top $header-height
  color $navy
  font-size calc(1.25em + 1.5vw)
</style>
