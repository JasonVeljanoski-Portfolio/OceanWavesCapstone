<template>
  <div class="flexcontainer">
    <BaseStatTile
      :title="`${this.graph} Confidence Score`"
      :number="confidence"
      :gtThreshold="0"
      :ltThreshold="0"
      :description="`Root mean square error of ${this.time}.`"
      tag=""
    />
    <BaseStatTile
      :title="`Max Cott Wave Height in ${this.time}`"
      :number="height"
      :gtThreshold="2.0"
      :ltThreshold="1.7"
      :flip="true"
      description="We recommend you stay on land where it is safer."
      tag="m"
    />
    <BaseStatTile
      :title="`Max Cott Wave Period in ${this.time}`"
      :number="period"
      :gtThreshold="15"
      :ltThreshold="13"
      :flip="true"
      :description="period==0?'The model to forecast peak wave period is coming soon.' : 'We recommend you stay on land where it is safer.'"
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
    confidence: {
        type: Number,
        required: true,
        validator(value) {
            return typeof value === 'number'
        }
    },
    height: {
        type: Number,
        required: true,
        validator(value) {
            return typeof value === 'number'
        }
    },
    period: {
        type: Number,
        required: true,
        validator(value) {
            return typeof value === 'number'
        }
    },
    time: {
        type: String,
        required: true,
        validator(value) {
            return typeof value === 'string' && (value === 'Forecast' || value === 'Last Day' || value === 'Last Week' || value === 'Last Month')
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
  // data() {
  //     return {
  //         statTimeObj: this.stats.day,
  //         statConfidenceVal: this.stats.confidence.waveHeight
  //     }
  // },
  // mounted() {
  //     this.renderStats
  // },
  // computed: {
  //   renderStats() {
  //       // TIME VALUE
  //       if (this.time === '12hr Forecast')
  //           this.statTimeObj = this.stats.twelveHrForecast
  //       else if (this.time === 'Last Day')
  //           this.statTimeObj = this.stats.day
  //       else if (this.time === 'Last Week')
  //           this.statTimeObj = this.stats.week
  //       else if (this.time === 'Last Month')
  //           this.statTimeObj = this.stats.month  
        
  //       // CONFIDENCE SCORE
  //       // if (this.time === '12hr Forecast')
  //       //     this.statConfidenceVal = this.stats.confidence.twelveHrForecast
  //       if (this.graph === 'Wave Height')
  //           this.statConfidenceVal = this.stats.confidence.waveHeight
  //       else if (this.graph === 'Peak Period')
  //           this.statConfidenceVal = this.stats.confidence.peakPeriod
  //       else if (this.graph === 'Direction')
  //           this.statConfidenceVal = this.stats.confidence.direction
  //   }
  // },
  // watch: {
  //   time: function () {
  //     this.renderStats
  //   },
  //   graph: function() {
  //       this.renderStats
  //   }
  // },
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
