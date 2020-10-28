<template>
  <div :style="_color" class="block-quote">
    <slot />
  </div>
</template>

<script>
export default {
  name: 'BaseBlockQuote',
  props: {
    color: {
      type: String,
      required: false,
      default: '#ccc',
      validator(value) {
        // hex, rgb(a) and red | green | blue
        const color = /red|green|blue|(#([\da-f]{3}){1,2}|(rgb|hsl)a\((\d{1,3}%?,\s?){3}(1|0?\.\d+)\)|(rgb|hsl)\(\d{1,3}%?(,\s?\d{1,3}%?){2}\))/gi
        const regex = new RegExp(color)
        return value.match(regex)
      }
    }
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
          color = '#2caaca'
          break
      }

      const rgb = this.hexToRGB(color)

      return {
        'border-left-color': color,
        'background-color':
          'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ', 0.2)'
      }
    }
  },
  methods: {
    hexToRGB(hex) {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
      return result
        ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
          }
        : null
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.block-quote
  overflow scroll
  padding 10px 10px 10px 20px
  border-left 5px solid
  opacity 1
  margin-bottom 10px
</style>
