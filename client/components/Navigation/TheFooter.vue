<template>
  <footer>
    <!-- copyright -->
    <div>
      <nuxt-link to="/">
        <img class="logo" src="@/static/logos/safeharbour.svg" />
      </nuxt-link>
      <p>&#9400; SafeHarbour 2020. All rights reserved.</p>
    </div>
    <div class="spacer" />
    <!-- nav links -->
    <div>
      <nav class="navigation-items">
        <ul class="nav-list">
          <li class="nav-item">
            <nuxt-link class="link" to="/contact">Team</nuxt-link>
          </li>
          <li class="nav-item">
            <nuxt-link class="link" to="/privacy">Privacy Policy</nuxt-link>
          </li>
          <li class="nav-item">
            <nuxt-link class="link" to="/terms">
              Terms &amp; Conditions
            </nuxt-link>
          </li>
        </ul>
      </nav>
      <BaseSocialMedia
        :has-facebook="true"
        :has-instagram="false"
        :has-linkedin="true"
        :has-twitter="true"
        :has-youtube="false"
        link-linkedin="https://www.linkedin.com"
      />
    </div>
  </footer>
</template>

<script>
import BaseSocialMedia from '@/components/Utils/BaseSocialMedia'

export default {
  name: 'TheFooter',
  components: {
    BaseSocialMedia
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

footer
  background-color white
  width 100%
  padding 0 40px 0 20px
  border-top 1px solid $border-color
  padding-top 10px

  // To keep the footer where it belongs
  position absolute
  bottom 0
  height $footer-height-phone

+desktop()
  footer
    display flex
    flex-flow row wrap
    align-items center
    height $footer-height-desktop

p
  text-align left
  font-size 10pt

img
  max-width 250px
  width 100%

.logo
  padding 10px

.spacer
  flex 1 1 auto

+desktop()
  .nav-list
    display flex
  footer
    display flex
    flex-flow row wrap
    align-items center

.nav-list
  list-style none
  padding 0
  margin 0

.nav-item a
  text-decoration none
  color $dark

.nav-item
  margin 0 10px
  text-decoration none
  font-size 14pt

.nav-item:hover
  cursor pointer

.link:hover
  color $grey

.nuxt-link-exact-active
  font-weight 400
  color $blue !important
</style>
