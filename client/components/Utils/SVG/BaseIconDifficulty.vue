<!-- prettier-ignore -->
<template>
  <div class="flexbox">
      <div class="cover">
        <svg id="difficulty" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 294 293">
          <title>difficulty</title>
          <rect :class="{ active: isBeginner }" class="cls-1" y="162" width="35" height="131" rx="20" />
          <rect :class="{ active: isBeginner && isIntermediate }" class="cls-1" x="90" y="87" width="35" height="206" rx="20" />
          <rect :class="{ active: isBeginner && isIntermediate && isAdvanced }" class="cls-1" x="180" width="35" height="293" rx="20" />
        </svg>
      </div>
      <span>{{ difficulty }}</span>
  </div>
</template>

<script>
export default {
  name: 'BaseIconDifficulty',
  props: {
    difficulty: {
      type: String,
      require: true,
      default: 'Beginner',
      validator(value) {
        value = value.toUpperCase()
        // The value must match one of these strings
        return ['BEGINNER', 'INTERMEDIATE', 'ADVANCED'].includes(value)
      }
    }
  },
  data() {
    return {
      isBeginner: false,
      isIntermediate: false,
      isAdvanced: false
    }
  },
  mounted() {
    this._getDifficulty()
  },
  // update live in dev mode
  beforeUpdate() {
    this._getDifficulty()
  },
  methods: {
    _getDifficulty() {
      switch (this.difficulty.toUpperCase()) {
        case 'BEGINNER':
          this.isBeginner = true
          this.isIntermediate = false
          this.isAdvanced = false
          break
        case 'INTERMEDIATE':
          this.isBeginner = true
          this.isIntermediate = true
          this.isAdvanced = false
          break
        case 'ADVANCED':
          this.isBeginner = true
          this.isIntermediate = true
          this.isAdvanced = true
          break
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.cover
  width 20px
  height 20px
  margin 10px

.cls-1
  fill #a8a8a8

.active
  fill $blue

span
  font-weight 400
  font-size 12pt
  color $grey
</style>
