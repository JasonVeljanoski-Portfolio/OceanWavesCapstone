<template>
  <div class="flexbox">
      <div class="container">
        <BaseAmmarAvatar />
      </div>
      <div class="text">
         <h4>"Coming Soon..."</h4>
      </div>
  </div>
</template>

<script>
import BaseAmmarAvatar from '@/components/SafeHarbourUtils/BaseAmmarAvatar'

export default {
  name: 'ComingSoon',
  components: {
    BaseAmmarAvatar
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.container 
  width 100%

.text
  width 100%
  max-width 550px
</style>
