<!-- prettier-ignore -->
<template>
  <div @click="$emit('toggle')" class="cover">
    <svg
      id="Youtube"
      data-name="Layer 1"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 512 358.48"
    >
      <path class="cls-1"
        d="M501.45,133.09A64.12,64.12,0,0,0,456.33,88C416.26,77,256,77,256,77S95.73,77,55.67,87.55a65.46,65.46,0,0,0-45.13,45.54C0,173.16,0,256.24,0,256.24s0,83.51,10.54,123.15a64.18,64.18,0,0,0,45.13,45.13c40.49,11,200.33,11,200.33,11s160.26,0,200.33-10.55a64.16,64.16,0,0,0,45.13-45.13C512,339.75,512,256.66,512,256.66S512.42,173.16,501.45,133.09Z"
        transform="translate(0 -77)" />
      <path class="cls-2" d="M205,333l133.27-76.76L205,179.49Z" transform="translate(0 -77)" />
    </svg>
  </div>
</template>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

svg:hover
  background-color #f9f9f9
  cursor pointer

.cover
  width 25px
  height 25px
  margin 10px

.cls-1
  fill red

.cls-2
  fill #fff
</style>
