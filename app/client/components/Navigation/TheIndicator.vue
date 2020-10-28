<template>
  <div :style="_color" class="indicator" />
</template>

<script>
export default {
  name: 'TheIndicator',
  props: {
    color: {
      type: String,
      required: false,
      default: '#4a98f7',
    },
  },
  computed: {
    _color() {
      let color = this.color

      switch (color) {
        case 'red':
          color = '#ec6d5f'
          break
        case 'green':
          color = '#27c9b8'
          break
        case 'blue':
          color = '#4a98f7'
          break
      }
      // const rgb = this.hexToRGB(color)

      return {
        'background-color': color,
        opacity: 1,
      }
    },
  },
  mounted() {
    window.addEventListener('scroll', this.progressBarCallback)
  },
  destroyed() {
    window.removeEventListener('scroll', this.progressBarCallback)
  },
  methods: {
    progressBarCallback() {
      const scrollPos = window.scrollY
      const winHeight = window.innerHeight
      const docHeight = document.documentElement.scrollHeight // instead document.body.clientHeight
      const perc = (100 * scrollPos) / (docHeight - winHeight)
      this.$el.style.width = perc + '%'
    },
    hexToRGB(hex) {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
      return result
        ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16),
          }
        : null
    },
  },
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.indicator
  position fixed
  top 0
  left 0
  margin-top $header-height
  height 5px
  z-index 3
</style>
