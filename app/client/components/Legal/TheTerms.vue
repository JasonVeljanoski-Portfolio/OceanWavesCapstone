<template>
  <div class="container flexbox">
    <div class="letter">
      <!-- Header -->
      <div class="header">
        <div class="title">TERMS OF USE</div>
        <div class="updated">Last Updated 23 October, 2020</div>
      </div>
      <!-- Slot - Add legal HTLM/ CSS in component -->
      <div class="legal">
        <slot />
      </div>
      <!-- Footer  -->
      <div class="footer">
        <div class="updated">
          SafeHarbour pty ltd <br />
          support@safeharbour.com
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Privacy'
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.container
  width 100vw

.letter
  max-width 800px
  width 100%
  margin 20px 40px 20px 40px
  padding 20px 40px 20px 40px
  box-shadow 0 0 10px rgba(0, 0, 0, 0.05)
  background-color white

.title
  text-align left
  font-weight 400
  font-size 20pt
  text-transform uppercase
  font-style italic

.updated
  text-align left
  font-style italic
  font-size 12pt

.legal
  margin-top 20px
  margin-bottom 20px
</style>
