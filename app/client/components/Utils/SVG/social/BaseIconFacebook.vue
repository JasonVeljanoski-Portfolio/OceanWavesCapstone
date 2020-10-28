<!-- prettier-ignore -->
<template>
  <div @click="$emit('toggle')" class="cover">
    <svg
      id="Facebook"
      data-name="Layer 1"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 512 512"
    >
      <path class="cls-1"
        d="M483.74,0H28.24A28.26,28.26,0,0,0,0,28.26v455.5A28.26,28.26,0,0,0,28.26,512H483.74A28.25,28.25,0,0,0,512,483.75h0V28.24A28.26,28.26,0,0,0,483.74,0Z"
        transform="translate(0 0)" />
      <path class="cls-2"
        d="M353.5,512V314h66.75l10-77.5H353.5V187.14c0-22.39,6.21-37.64,38.32-37.64H432.5V80.37c-7.08-.94-31.36-3.05-59.62-3.05-59,0-99.38,36-99.38,102.14v57H207V314h66.5V512Z"
        transform="translate(0 0)" />
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
  fill #4267b2

.cls-2
  fill #fff
</style>
