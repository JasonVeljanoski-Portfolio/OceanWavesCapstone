<template>
  <div>{{ number }}{{ tag }}</div>
</template>

<script>
export default {
  name: 'BaseNumberAnimate',
  props: {
    number: {
      type: Number,
      required: true,
      default: 0,
      validator(value) {
        return typeof value === 'number'
      },
    },
    tag: {
      type: String,
      required: false,
      default: '',
      validator(value) {
        return typeof value === 'string'
      },
    }
  },
  data() {
    return {
      displayNumber: 0,
      interval: false,
    }
  },
  mounted() {
    this.displayNumber = this.number ? this.number : 0
  },
  watch: {
    number: function () {
      clearInterval(this.interval)
      if (this.number == this.displayNumber) {
        return
      }
      this.interval = window.setInterval(
        function () {
          if (this.displayNumber != this.number) {
            var change = (this.number - this.displayNumber) / 10
            // change = change >= 0 ? Math.ceil(change) : Math.floor(change)
            let res = this.displayNumber + Number(change)
            this.displayNumber = Number(res.toFixed(2))
          }
        }.bind(this),
        20
      )
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'
</style>
