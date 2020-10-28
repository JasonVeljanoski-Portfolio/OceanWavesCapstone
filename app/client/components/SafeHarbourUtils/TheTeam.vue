<template>
  <div>
    <div class="flexcontainer">
      <BaseAvatarTile
        title="Jason Veljanoski"
        description="21980294 - A proud UWA student."
        :has-facebook="false"
        :has-instagram="false"
        :has-linkedin="true"
        :has-twitter="false"
        :has-youtube="true"
        link-linkedin="https://www.linkedin.com/in/jason-veljanoski"
        link-youtube="https://www.youtube.com/channel/UCQiAdzUeiuYTaVRe_rwAP7A/featured?view_as=subscriber"
      >
        <BaseSampleAvatar />
      </BaseAvatarTile>

      <BaseAvatarTile
        title="Teggs Lou"
        description="22839079 - A proud UWA student."
        :has-facebook="false"
        :has-instagram="false"
        :has-linkedin="true"
        :has-twitter="false"
        :has-youtube="false"
        :has-we-chat="true"
        @togglewechat="showwechat('Teggs wechat id')"
      >
        <BaseSampleAvatar />
      </BaseAvatarTile>

      <BaseAvatarTile
        title="Johnny Barrett"
        description="22683565 - A proud UWA student."
        :has-facebook="false"
        :has-instagram="true"
        :has-linkedin="true"
        :has-twitter="true"
        :has-youtube="false"
      >
        <BaseSampleAvatar />
      </BaseAvatarTile>
    </div>
    <div class="flexcontainer">
      <BaseAvatarTile
        title="Ammar Pervez"
        description="22660382 - A proud UWA student."
        :has-facebook="true"
        :has-instagram="false"
        :has-linkedin="true"
        :has-twitter="false"
        :has-youtube="false"
        link-linkedin="https://www.linkedin.com"
      >
        <BaseSampleAvatar />
      </BaseAvatarTile>
      <BaseAvatarTile
        title="Yajun Zhou"
        description="22600288 - A proud UWA student."
        :has-facebook="false"
        :has-instagram="false"
        :has-linkedin="true"
        :has-twitter="false"
        :has-youtube="false"
        :has-we-chat="true"
        link-linkedin="https://www.linkedin.com"
        @togglewechat="showwechat('Yajuns wechat id')"
      >
        <BaseSampleAvatar />
      </BaseAvatarTile>
    </div>


    <transition name="fade">
      <div v-if="isWechat" class="wechatbox flexbox">
        <div>id: <span style="font-style: italic">{{ wechatid }}</span></div>
        <div class="spacer" />
        <BaseIconCross @toggle="isWechat=false" />
      </div>
    </transition>


  </div>
</template>

<script>
import BaseAvatarTile from '@/components/SafeHarbourUtils/BaseAvatarTile'
import BaseSampleAvatar from '@/components/Utils/SVG/BaseSampleAvatar'
import BaseIconCross from '@/components/Utils/SVG/navigation/BaseIconCross'

export default {
  name: 'CoursesPage',
  components: {
    BaseAvatarTile,
    BaseSampleAvatar,
    BaseIconCross
  },
  data() {
    return {
      wechatid: '',
      isWechat: false
    }
  },
  methods: {
    showwechat(event) {
      this.wechatid = event
      this.isWechat = true
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.flexcontainer 
  display flex
  align-items center
  justify-content center
  flex-flow row wrap
  align-content flex-end

.wechatbox 
  z-index 10000000 !important
  position fixed
  bottom 0
  right 0
  padding-left 10px
  margin 10px
  width 350px
  background-color white
  border solid 1px $border-color

.spacer
  flex 1 1 auto

</style>
