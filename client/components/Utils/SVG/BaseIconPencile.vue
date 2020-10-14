<!-- prettier-ignore -->
<template>
  <div class="cover">
    <svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 292.95 292.98">
    <title>pencil</title>
    <path
        d="M268.09,13.16a45,45,0,0,0-63.56,0L26.36,191.34a10.08,10.08,0,0,0-2.57,4.39L.36,280.32a10,10,0,0,0,12.29,12.3l84.59-23.44a10,10,0,0,0,4.4-2.56L279.81,88.44a45,45,0,0,0,0-63.56Zm-220,184.67L193.94,52l47,47L95.14,244.86Zm-9.4,18.85L76.3,254.26l-52,14.39Zm227-142.36-10.6,10.59-47-47,10.6-10.59a25,25,0,0,1,35.3,0L265.69,39A25,25,0,0,1,265.69,74.32Z" />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'BaseIconPenciles'
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.cover
  width 20px
  height 20px
  margin 10px

path
  fill $grey

.focus
  fill $blue

span
  font-weight 400
  font-size 12pt
</style>
