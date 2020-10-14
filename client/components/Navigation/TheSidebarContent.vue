<template>
  <aside class="sidbar">
    <!-- header -->
    <header>
      <nuxt-link class="logo" to="/">
        <img @click="toggle" src="@/static/logos/safeharbour.svg" />
      </nuxt-link>
      <div class="spacer" />
      <div>
        <BaseIconCross @toggle="toggle" />
      </div>
    </header>

    <!-- navs -->
    <nav @click="toggle" class="navigation-items">
      <ul class="nav-list">
        <nuxt-link class="link" to="/">
          <li class="nav-item">Dashboard</li>
        </nuxt-link>
        <nuxt-link class="link" to="/history">
          <li class="nav-item">History</li>
        </nuxt-link>
        <nuxt-link class="link" to="/contact">
          <li class="nav-item">Team</li>
        </nuxt-link>
      </ul>
    </nav>

    <!-- social media -->
    <BaseSocialMedia
      :has-facebook="true"
      :has-instagram="false"
      :has-linkedin="true"
      :has-twitter="true"
      :has-youtube="false"
      link-linkedin="https://www.linkedin.com"
    />
  </aside>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import BaseIconCross from '@/components/Utils/SVG/navigation/BaseIconCross'
import BaseSocialMedia from '@/components/Utils/BaseSocialMedia'

export default {
  name: 'TheSidebarContent',
  components: {
    BaseIconCross,
    BaseSocialMedia
  },
  computed: {
    ...mapGetters({ auth: 'account/getAuthenticationState' })
  },
  methods: {
    ...mapMutations({ toggle: 'drawer/toggle' }),
    ...mapMutations({ toggleFormLogin: 'account.forms/toggleLogin' }),
    ...mapMutations({ toggleFormRegister: 'account.forms/toggleRegister' })
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

aside
  height 100%
  width 100%
  z-index 9

header
  background-color white
  display flex
  flex-flow row nowrap
  align-items center
  height $header-height
  padding 0 10px
  border-bottom 1px solid $border-color

.spacer
  flex 1 1 auto

.logo
  max-width 150px
  width 100%

// nav links
.nav-list
  list-style none
  padding 0
  margin 0

a
  text-decoration none
  color $dark

.nav-item
  padding 10px 10px
  font-size 14pt
  color $dark
  border-bottom solid 1px $border-color

.nav-item:hover
  cursor pointer
  background-color #efefef

.link:hover
  color $grey

.nuxt-link-exact-active
  font-weight 400
  color $blue !important
</style>
