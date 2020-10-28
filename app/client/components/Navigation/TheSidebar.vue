<template>
  <div>
    <!-- dark overlay -->
    <transition name="fade">
      <div v-if="drawer" class="focus" />
    </transition>
    <!-- sidebar -->
    <transition name="slide">
      <div v-if="drawer" class="background" @click="toggle">
        <div class="sidebar" @click.stop>
          <slot />
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  name: 'TheSidebar',
  computed: {
    ...mapGetters({ drawer: 'drawer/getDrawerState' }),
  },
  methods: {
    ...mapMutations({ toggle: 'drawer/toggle' }),
  },
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'
@import '~static/css/transitions.styl'

.sidebar
  float right
  max-width $sidebar-width
  width 100%
  height 100%
  border-right 1px solid #e5e5e5
  background-color white
  overflow-y scroll
  z-index 2000

+desktop()
  .sidebar,
  .focus
    display none

.background
  position fixed
  z-index 998
  top 0
  width 100%
  height 100%

.focus
  position fixed
  z-index 998
  top 0
  width 100%
  height 100%
  background-color rgba(0, 0, 0, 0.25)
</style>
