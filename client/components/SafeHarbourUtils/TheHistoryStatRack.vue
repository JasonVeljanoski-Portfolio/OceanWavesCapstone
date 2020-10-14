<template>
  <div class="flexcontainer">
    <BaseStatTile
      :title="`stat 0`"
      :number="statConfidenceVal"
      :gtThreshold="90"
      :ltThreshold="89"
      description="Not sure what stats to add here [change later] ..."
      tag="%"
    />
    <BaseStatTile
      :title="`stat 1`"
      :number="statTimeObj.maxWaveHeight"
      :gtThreshold="1"
      :ltThreshold="0.94"
      :flip="true"
      description="Not sure what stats to add here [change later] ..."
      tag="m"
    />
    <BaseStatTile
      :title="`stat 2`"
      :number="statTimeObj.maxWavePeriod"
      :gtThreshold="24"
      :ltThreshold="20"
      :flip="true"
      description="Not sure what stats to add here [change later] ..."
      tag="s"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import BaseStatTile from '@/components/SafeHarbourUtils/BaseStatTile'

export default {
  name: 'CoursesPage',
  components: {
    BaseStatTile
  },
  props: {
    stats: {
        type: Object,
        required: true,
        default: 0,
        validator(value) {
            return typeof value === 'object'
        }
    },
    time: {
        type: String,
        required: true,
        validator(value) {
            return typeof value === 'string' && (value === 'Last Day' || value === 'Last Week' || value === 'Last Month')
        }
    },
    graph: {
        type: String,
        required: true,
        validator(value) {
            return typeof value === 'string' && (value === 'Wave Height' || value === 'Peak Period' || value === 'Direction')
        }
    }
  },
  data() {
      return {
          statTimeObj: this.stats.day,
          statConfidenceVal: this.stats.confidence.waveHeight
      }
  },
  mounted() {
      this.renderStats
  },
  computed: {
    renderStats() {
        // TIME VALUE
        if (this.time === 'Last Day')
            this.statTimeObj = this.stats.day
        else if (this.time === 'Last Week')
            this.statTimeObj = this.stats.week
        else if (this.time === 'Last Month')
            this.statTimeObj = this.stats.month    
        
        // CONFIDENCE SCORE
        if (this.graph === 'Wave Height')
            this.statConfidenceVal = this.stats.confidence.waveHeight
        else if (this.graph === 'Peak Period')
            this.statConfidenceVal = this.stats.confidence.peakPeriod
        else if (this.graph === 'Direction')
            this.statConfidenceVal = this.stats.confidence.direction
    }
  },
  watch: {
    time: function () {
      this.renderStats
    },
    graph: function() {
        this.renderStats
    }
  },
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.flexcontainer
   display flex
   align-items center
   justify-content center
   flex-flow row wrap
   align-content flex-end
</style>
