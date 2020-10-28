<template>
    <div class="tile flexbox">
      <section class="content">
        <span :style="_color" class="stat"><BaseNumberAnimate :number="number" :tag="tag"></BaseNumberAnimate></span>
        <div class="title">{{ title }}</div>
        <p class="description">{{ description }}</p>
      </section>
    </div>
</template>

<script>
export default {
  name: 'BaseBlogTile',
  // image should have 16:9 aspect ratio
  props: {
    title: {
      type: String,
      required: true,
      validator(value) {
        return typeof value === 'string'
      }
    },
    description: {
      type: String,
      required: true,
      validator(value) {
        return typeof value === 'string'
      }
    },
    number: {
      type: Number,
      required: true,
      validator(value) {
        return typeof value === 'number'
      }
    },
    tag: {
      type: String,
      required: true,
      validator(value) {
        return typeof value === 'string'
      }
    },
    gtThreshold: {
      type: Number,
      required: true,
      validator(value) {
        return typeof value === 'number'
      }
    },
    ltThreshold: {
      type: Number,
      required: true,
      validator(value) {
        return typeof value === 'number'
      }
    },
    flip: {
      type: Boolean,
      required: false,
      default: false,
      validator(value) {
        return typeof value === 'boolean'
      }
    }
  },
  computed: {
    _color() {
      let color = '#27c9b8'

      // FLIP INEQUALITY TO SWAP RED/GREEN COLOR
      if (this.flip) {

        if (this.number >= this.gtThreshold)
         color = '#ec6d5f'
        else if (this.number <= this.ltThreshold)
          color = '#27c9b8'
        else
          color = '#ffce00'

      } else {

        if (this.number >= this.gtThreshold)
         color = '#27c9b8'
        else if (this.number <= this.ltThreshold)
          color = '#ec6d5f'
        else
          color = '#ffce00'

      }

      return {
        'color': color
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'
@import '~static/css/transitions.styl'

$w = 300px
$h = 150px
$footer-txt-height = 50px

$footer-wrap-brkpnt = 313px     // mobile
mobile()
  @media (max-width: $footer-wrap-brkpnt)
    {block}

.nav-item
  text-decoration none
  color $grey

.tile
  margin 10px
  min-height $h
  max-width $w
  border solid 1px $border-color
  transition: transform 0.5s ease

.tile:hover
  transform scale(1.01, 1.01)
  span
    opacity 1 !important

.content
  width 100%

.title
  font-size 12pt
  font-style italic
  text-align center
  width 100%
  font-weight bold

.stat
  color $navy
  font-size 40pt
  font-weight 600
  padding 15px 15px 0 15px
  text-align center

.description
  text-align left
  line-height normal
  margin-top 10px
  font-size 11pt
  color $grey
  padding 15px 15px 0 15px

// .tile
//   position relative

// .content
//   padding-bottom "calc(2 * %s)" % $footer-txt-height

// +mobile()
//   .content
//     padding-bottom "calc(3 * %s)" % $footer-txt-height
</style>
