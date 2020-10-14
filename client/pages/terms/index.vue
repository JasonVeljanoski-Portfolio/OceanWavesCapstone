<template>
  <div>
    <TheTerms>
      <!-- prettier-ignore -->
      <div class="legal">
        <p>We are innocent. This should be updated.</p>
      </div>
    </TheTerms>
  </div>
</template>

<script>
import TheTerms from '@/components/Legal/TheTerms'

export default {
  name: 'TermsPage',
  components: {
    TheTerms
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'
.legal
  font-size 12pt
</style>
