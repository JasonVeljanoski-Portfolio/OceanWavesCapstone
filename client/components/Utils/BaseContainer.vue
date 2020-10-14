<template>
  <div class="flexbox">
    <div :style="{ width: width }" class="interactive-box">
      <div class="center">
        <slot />
      </div>
      <div class="description">
        <p>{{ description }}</p>
        <BaseToggleRack @toggle="$emit('itemtoggle',$event)" :items="rackitems" />
        <img :src="imagePath()" :alt="logoAlt" />
      </div>
    </div>
  </div>
</template>

<script>
import BaseToggleRack from '@/components/Utils/BaseToggleRack'

export default {
  name: 'BaseContainer',
  components: {
    BaseToggleRack
  },
  props: {
    description: {
      type: String,
      required: true,
      validator(value) {
        return typeof value === 'string'
      }
    },
    width: {
      type: String,
      required: false,
      default: '100%',
      validator(value) {
        return typeof value === 'string'
      }
    },
    logoFileName: {
      type: String,
      required: true,
      validator(value) {
        // value must end with an image file extention
        // file must be located in ~/static/logos/ dir
        const img = /\.(gif|jpg|jpeg|tiff|png|svg|bmp)$/i
        const regex = new RegExp(img)
        return value.match(regex)
      }
    },
    rackitems: {
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
      logoAlt: this.getFileName()
    }
  },
  methods: {
    imagePath() {
      return require(`~/static/logos/${this.logoFileName}`)
    },
    getFileName() {
      return this.logoFileName.split('.')[0]
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.interactive-box
  border solid 1px $border-color
  border-radius 5px
  overflow scroll
  margin 5px
  padding 5px

.center
  display flex
  justify-content center
  align-items center
  padding 10px

.description
  height 50px
  display flex
  justify-content space-between

.description img
  max-width 30px
  width 100%
  margin 10px

.description p
  margin 5px
  padding 5px
  font-style italic
  white-space nowrap
  overflow hidden
  position sticky
  text-overflow ellipsis
</style>
