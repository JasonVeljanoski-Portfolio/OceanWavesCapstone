<template>
  <header>
    <nuxt-link to="/">
      <img class="logo" src="@/static/logos/safeharbour.svg" />
    </nuxt-link>
    <div class="spacer" />
    <!-- Nav Links -->
    <nav class="navigation-items">
      <ul class="nav-list">
        <li class="nav-item">
          <nuxt-link class="link" to="/">Dashboard</nuxt-link>
        </li>
        <li class="nav-item">
          <nuxt-link class="link" to="/history">History</nuxt-link>
        </li>
        <li class="nav-item">
          <nuxt-link class="link" to="/contact">Team</nuxt-link>
        </li>
      </ul>
    </nav>
    <div class="menu">
      <BaseIconBurger @toggle="toggle" />
    </div>
    <TheIndicator color="blue" />
  </header>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import TheIndicator from '@/components/Navigation/TheIndicator'
import BaseIconBurger from '@/components/Utils/SVG/navigation/BaseIconBurger'
import BaseIconAccount from '@/components/Utils/SVG/navigation/BaseIconAccount'

export default {
  name: 'TheHeader',
  components: {
    TheIndicator,
    BaseIconBurger,
    BaseIconAccount,
  },
  data() {
    return {
      activeAccount: false,
    }
  },
  computed: {
    ...mapGetters({ auth: 'account/getAuthenticationState' }),
  },
  methods: {
    ...mapMutations({ toggle: 'drawer/toggle' }),
    ...mapMutations({ toggleFormLogin: 'account.forms/toggleLogin' }),
    ...mapMutations({ toggleFormRegister: 'account.forms/toggleRegister' }),
    toggleActiveAccount() {
      this.activeAccount = !this.activeAccount
    },
  },
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'
@import '~static/css/transitions.styl'

header
  background-color white
  width 100%
  display flex
  flex-flow row nowrap
  align-items center
  height $header-height
  top 0
  position fixed
  z-index 1
  padding 0 40px 0 20px
  border-bottom 1px solid $border-color

img
  max-width 200px
  width 100%

.logo
  padding 10px

.spacer
  flex 1 1 auto

.attention
  padding 0 10px
  background-color $blue
  border-radius 5px
  .link
    color white !important

.attention:hover
  background-color $blue
  opacity 0.96

// nav links
.navigation-items
  display none

.menu
  display block

+desktop()
  .navigation-items
    display block
  .menu
    display none

.nav-list
  list-style none
  padding 0
  margin 0
  display flex
  align-items center

.nav-item a
  text-decoration none
  color $dark

.nav-item
  margin 0 10px
  display inline-block
  font-size 14pt
  color $dark

.nav-item:hover
  cursor pointer

.link:hover
  color $grey

.nuxt-link-exact-active
  font-weight 400
  color $blue !important
/*           */
.account
  position absolute
  z-index 9999
  list-style none
  padding 0
  margin 5px 0 0 0
  border solid 1px $border-color
  background-color white
  li
    padding 8px

.account li:hover
  cursor pointer
  background-color $border-color
</style>
