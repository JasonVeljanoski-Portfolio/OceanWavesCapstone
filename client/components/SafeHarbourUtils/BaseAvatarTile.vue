<template>
    <div class="tile flexbox">
      <section class="content">
        <slot />
        
        <div>
            <div class="title">{{ title }}</div>
            <p class="description">{{ description }}</p>
        </div>

        <BaseSocialMedia
            @togglewechat="$emit('togglewechat', linkWeChat)"
            :has-facebook="hasFacebook"
            :has-instagram="hasInstagram"
            :has-linkedin="hasLinkedin"
            :has-twitter="hasTwitter"
            :has-youtube="hasYoutube"
            :hasWeChat="hasWeChat"
            :link-linkedin="linkLinkedin"
            :link-facebook="linkFacebook"
            :link-instagram="linkInstagram"
            :link-youtube="linkYoutube"
            :link-twitter="linkTwitter"
            :linkWeChat="linkWeChat"
        />
      </section>
    </div>
</template>

<script>
import BaseSocialMedia from '@/components/Utils/BaseSocialMedia'

export default {
  name: 'BaseBlogTile',
  components: {
    BaseSocialMedia
  },
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
    hasFacebook: {
      type: Boolean,
      require: true,
      validator(value) {
        return typeof value === 'boolean'
      }
    },
    hasInstagram: {
      type: Boolean,
      require: true,
      validator(value) {
        return typeof value === 'boolean'
      }
    },
    hasLinkedin: {
      type: Boolean,
      require: true,
      validator(value) {
        return typeof value === 'boolean'
      }
    },
    hasTwitter: {
      type: Boolean,
      require: true,
      validator(value) {
        return typeof value === 'boolean'
      }
    },
    hasYoutube: {
      type: Boolean,
      require: true,
      validator(value) {
        return typeof value === 'boolean'
      }
    },
    hasWeChat: {
      type: Boolean,
      require: false,
      default: false,
      validator(value) {
        return typeof value === 'boolean'
      }
    },
    linkFacebook: {
      type: String,
      require: false,
      default: 'https://www.facebook.com',
      validator(value) {
        // value must match a web link or '/' (the default value)
        const web = /^https?:\/\/(.*)/gi
        const regex = new RegExp(web)
        return value.match(regex)
      }
    },
    linkInstagram: {
      type: String,
      require: false,
      default: 'https://www.instagram.com',
      validator(value) {
        // value must match a web link or '/' (the default value)
        const web = /^https?:\/\/(.*)/gi
        const regex = new RegExp(web)
        return value.match(regex)
      }
    },
    linkLinkedin: {
      type: String,
      require: false,
      default: 'https://www.linkedin.com',
      validator(value) {
        // value must match a web link with http or https or '/' (the default value)
        const web = /^https?:\/\/(.*)/gi
        const regex = new RegExp(web)
        return value.match(regex)
      }
    },
    linkTwitter: {
      type: String,
      require: false,
      default: 'https://www.twitter.com',
      validator(value) {
        // value must match a web link or '/' (the default value)
        const web = /^https?:\/\/(.*)/gi
        const regex = new RegExp(web)
        return value.match(regex)
      }
    },
    linkYoutube: {
      type: String,
      require: false,
      default: 'https://www.youtube.com',
      validator(value) {
        // value must match a web link or '/' (the default value)
        const web = /^https?:\/\/(.*)/gi
        const regex = new RegExp(web)
        return value.match(regex)
      }
    },
    linkWeChat: {
      type: String,
      require: false,
      default: 'sampleWeChatID',
      validator(value) {
        return typeof(value) === 'string'
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

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
  font-size 22pt
  text-align center
  width 100%
  font-weight bold

.stat
  color $navy
  font-size 40pt
  font-weight 600
  //   padding 15px 15px 0 15px
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
