<!-- prettier-ignore -->
<template>
  <div @click="$emit('toggle')" class="cover">
    <svg
      id="Instagram"
      data-name="Layer 1"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 512 512"
    >
    <defs>
      <linearGradient id="linear-gradient" x1="-727.04" y1="171.72" x2="-713.96" y2="158.65"
            gradientTransform="translate(23312 -5030) scale(32)" gradientUnits="userSpaceOnUse">
            <stop offset="0" stop-color="#ffc107" />
            <stop offset="0.51" stop-color="#f44336" />
            <stop offset="0.99" stop-color="#9c27b0" />
        </linearGradient>
        <linearGradient id="linear-gradient-2" x1="-723.33" y1="168.02" x2="-717.67" y2="162.36"
            xlink:href="#linear-gradient" />
        <linearGradient id="linear-gradient-3" x1="-716.58" y1="161.26" x2="-715.82" y2="160.51"
            xlink:href="#linear-gradient" />
    </defs>
    <title>instagram</title>
    <path class="cls-1"
        d="M352,0H160A160,160,0,0,0,0,160V352A160,160,0,0,0,160,512H352A160,160,0,0,0,512,352V160A160,160,0,0,0,352,0ZM464,352A112.12,112.12,0,0,1,352,464H160A112.12,112.12,0,0,1,48,352V160A112.12,112.12,0,0,1,160,48H352A112.12,112.12,0,0,1,464,160Z" />
    <path class="cls-2"
        d="M256,128A128,128,0,1,0,384,256,128,128,0,0,0,256,128Zm0,208a80,80,0,1,1,80-80A80.11,80.11,0,0,1,256,336Z" />
    <circle class="cls-3" cx="393.6" cy="118.4" r="17.06" />
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
  fill url(#linear-gradient)

.cls-2
  fill url(#linear-gradient-2)

.cls-3
  fill url(#linear-gradient-3)
</style>
