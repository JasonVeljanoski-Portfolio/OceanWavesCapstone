<template>
  <div>
    <BaseContainer @itemtoggle="graphToggleHandler($event)" :rackitems="graphitmes" :description="activeGraphItem" logo-file-name="safeharbourMini.svg" width="100%">
    <div>

      <div class="flexbox queue">

        <h3>Forecast Reports</h3>
        <div class="spacer" />
        <BaseToggleRack @toggle="reScale($event)" :items="scaleitems" />

      </div>


      <div :key="componentKey">

        <div v-if="showForecast">
          <TheForecastWaveHeight :data="oceanData.forecast" v-show="activeGraphItem === graphitmes[0]" />
          <TheForecastPeakPeriod :data="oceanData.forecast" v-show="activeGraphItem === graphitmes[1]" />
          <TheForecastDirection :data="oceanData.forecast" v-show="activeGraphItem === graphitmes[2]" />
        </div>
        <div v-else>
          <TheOceanWaveHeight v-show="activeGraphItem === graphitmes[0]" :data="oceanData.data.slice(oceanData.data.length-upperbound-1, oceanData.data.length-1)" />
          <TheOceanPeakPeriod v-show="activeGraphItem === graphitmes[1]" :data="oceanData.data.slice(oceanData.data.length-upperbound-1, oceanData.data.length-1)" />
          <TheOceanRadar v-show="activeGraphItem === graphitmes[2]" :data="oceanData.data.slice(oceanData.data.length-upperbound-1, oceanData.data.length-1)"/>
        </div>
  
      </div>

    </div>
    </BaseContainer>
    <TheStatsRack :confidence="confidence" :height="height" :period="period" :time="time" :graph="activeGraphItem" />

  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import BaseContainer from '@/components/Utils/BaseContainer'
import BaseToggleRack from '@/components/Utils/BaseToggleRack'
import TheForecastWaveHeight from '@/components/D3Visualisations/TheForecastWaveHeight'
import TheForecastPeakPeriod from '@/components/D3Visualisations/TheForecastPeakPeriod'
import TheForecastDirection from '@/components/D3Visualisations/TheForecastDirection'
import TheOceanWaveHeight from '@/components/D3Visualisations/TheOceanWaveHeight'
import TheOceanPeakPeriod from '@/components/D3Visualisations/TheOceanPeakPeriod'
import TheOceanRadar from '@/components/D3Visualisations/TheOceanRadar'
import TheStatsRack from '@/components/SafeHarbourUtils/TheStatsRack'

export default {
  name: 'D3Demos',
  components: {
    BaseContainer,
    BaseToggleRack,
    TheForecastWaveHeight,
    TheForecastPeakPeriod,
    TheForecastDirection,
    TheOceanWaveHeight,
    TheOceanPeakPeriod,
    TheOceanRadar,
    TheStatsRack
  },
  data() {
      return {
          showForecast: true,
          activeGraphItem: 'Wave Height',
          activeTime: 'Forecast',
          graphitmes: ['Wave Height', 'Peak Period', 'Direction'],
          scaleitems: ['Forecast', 'Last Day', 'Last Week', 'Last Month'],
          upperbound: 50,
          componentKey: 0,
          time: 'Forecast',
          confidence: 0,
          height: 1,
          period: 2
      }
  },
  mounted() {
    this.confidence = this.oceanData.summary.forecast.confidence.waveHeight
    this.height = this.oceanData.summary.forecast.height
    this.period = this.oceanData.summary.forecast.period
  },
  methods: {
      forceRerender() {
        this.componentKey += 1
      },
      graphToggleHandler(event) {
          this.activeGraphItem = event
          this.reScale(this.activeTime)
      },
      reScale(event) {
        this.activeTime = event
        // FORECAST
        if ( event === 'Forecast' ) {

          this.showForecast = true

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem === 'Wave Height' ) {
            this.confidence = this.oceanData.summary.forecast.confidence.waveHeight
          }
          else if ( this.activeGraphItem === 'Peak Period' ) {
            this.confidence = this.oceanData.summary.forecast.confidence.peakPeriod
          }
          else if ( this.activeGraphItem === 'Direction' ) {
            this.confidence = this.oceanData.summary.forecast.confidence.direction
          }
          
          this.height = this.oceanData.summary.forecast.height
          this.period = this.oceanData.summary.forecast.period

        }
        else if ( event === 'Last Day' ) {  // LAST DAY

          this.showForecast = false
          this.upperbound = 50  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence = this.oceanData.summary.waveHeight.confidence
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = this.oceanData.summary.peakPeriod.confidence
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = this.oceanData.summary.direction.confidence
          }

          this.height = this.oceanData.summary.waveHeight.day
          this. period = this.oceanData.summary.peakPeriod.day

        }
        else if ( event === 'Last Week' ) {

          this.showForecast = false
          this.upperbound = 350  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence = this.oceanData.summary.waveHeight.confidence
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = this.oceanData.summary.peakPeriod.confidence
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = this.oceanData.summary.direction.confidence
          }
          
          this.height = this.oceanData.summary.waveHeight.week
          this. period = this.oceanData.summary.peakPeriod.week

        }
        else if ( event === 'Last Month' ) {

          this.showForecast = false
          this.upperbound = 1400  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence = this.oceanData.summary.waveHeight.confidence
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = this.oceanData.summary.peakPeriod.confidence
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = this.oceanData.summary.direction.confidence
          }

          this.height = this.oceanData.summary.waveHeight.month
          this. period = this.oceanData.summary.peakPeriod.month

        }


        // if (event === this.scaleitems[0]) {
        //     this.showForecast = true
        //     return
        // }
        // else if (event === this.scaleitems[1]) {
        //     this.upperbound = 50  // rescale graph
        //     this.showForecast = false // reset
        // }
        // else if (event === this.scaleitems[2]) {
        //     this.upperbound = 350
        //     this.showForecast = false // reset
        // }
        // else if (event === this.scaleitems[3]) {
        //     this.upperbound = 1400
        //     this.showForecast = false // reset
        // }

        this.time = event     // update time for summary stats
        this.forceRerender()

      }
  },
//   methods: {
//     ...mapActions({
//       setDemoData: 'd3Demo/setDemoData', // map `this.setDemoData()` to `this.$store.dispatch('setDemoData')`
//       setOceanData: 'oceandata/setOceanData'
//     })
//   },
  computed: {
    ...mapGetters({
      oceanData: 'oceandata/getOceanData'
    }),
  },
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'
@import '~static/css/transitions.styl'

h3
  margin 0

.spacer
  flex 1 1 auto

.queue
  padding 5px

.flexcontainer
   display flex
   align-items center
   justify-content center
   flex-flow row wrap
   align-content flex-end
</style>
