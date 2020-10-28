<!-- prettier-ignore -->
<template>
  <div @click="$emit('toggle')" class="cover">
    <svg
      id="Burger"
      data-name="Layer 1"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 512 355.12"
    >
      <path d="M491.32,0H20.68a20.68,20.68,0,0,0,0,41.36H491.32a20.68,20.68,0,1,0,0-41.36Z" />
      <path class="paddy" d="M491.32,156.88H20.68a20.68,20.68,0,0,0,0,41.36H491.32a20.68,20.68,0,0,0,0-41.36Z" />
      <path d="M491.32,313.76H20.68a20.68,20.68,0,1,0,0,41.36H491.32a20.68,20.68,0,0,0,0-41.36Z" />
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
  .paddy
    transform scaleX(1.0)

.cover
  width 25px
  margin 10px

.paddy
  transform scaleX(0.8)
  transition: transform 0.2s ease
</style>
