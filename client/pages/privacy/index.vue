<template>
  <div>
    <ThePrivacyPolicy>
      <!-- prettier-ignore -->
      <div class="legal">
        <p>Our privacy policy is private. This should be updated.</p>
      </div>
    </ThePrivacyPolicy>
  </div>
</template>

<script>
import ThePrivacyPolicy from '@/components/Legal/ThePrivacyPolicy'

export default {
  name: 'PrivacyPage',
  components: {
    ThePrivacyPolicy
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.legal
  font-size 12pt

.legal p
  text-align left
</style>
