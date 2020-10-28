<!-- prettier-ignore -->
<template>
  <div @click="$emit('toggle')" class="cover">
    <svg
      id="Cross"
      version="1.1"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      x="0px"
      y="0px"
      viewBox="0 0 512.001 512.001"
      style="enable-background:new 0 0 512.001 512.001;"
      xml:space="preserve"
    >
      <rect class="cls-1" x="-85.96" y="243.33" width="692.11" height="31" rx="15.5"
        transform="translate(258.19 -108.2) rotate(45)" />
      <rect class="cls-1" x="-86.3" y="243.67" width="692.11" height="31" rx="15.5"
        transform="translate(-108.2 259.49) rotate(-45)" />
    </svg>
  </div>
</template>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

path
 fill #777

svg:hover
  background-color #f9f9f9
  cursor pointer

.cover
  width 20px
  margin 10px
  padding-top 5px

.cls-1
  stroke #777
  fill #777
  stroke-miterlimit 10
  stroke-width 19px
</style>
