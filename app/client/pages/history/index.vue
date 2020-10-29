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
          <TheHistoryForecastWaveHeight :width="chartWidth" :outcome="historyData.forecastOutcome" :data="historyData.forecast" v-show="activeGraphItem === graphitmes[0]" />
          
          <BaseComingSoon v-show="activeGraphItem === graphitmes[1]" />
          <!-- <TheHistoryForecastPeakPeriod :width="chartWidth" :outcome="historyData.forecastOutcome" :data="historyData.forecast" v-show="activeGraphItem === graphitmes[1]" /> -->

          <BaseComingSoon v-show="activeGraphItem === graphitmes[2]" />
          <!-- <TheHistoryForecastDirection :width="chartWidth" :outcome="historyData.forecastOutcome" :data="historyData.forecast" v-show="activeGraphItem === graphitmes[2]" /> -->
        </div>
        <div v-else>
          <TheHistoryWaveHeight :width="chartWidth" v-show="activeGraphItem === graphitmes[0]" :data="historyData.history.slice(historyData.history.length-upperbound-1, historyData.history.length-1)" />
          <TheHistoryPeakPeriod :width="chartWidth" v-show="activeGraphItem === graphitmes[1]" :data="historyData.history.slice(historyData.history.length-upperbound-1, historyData.history.length-1)" />
          <TheHistoryDirection :width="chartWidth" v-show="activeGraphItem === graphitmes[2]" :data="historyData.history.slice(historyData.history.length-upperbound-1, historyData.history.length-1)" />
        </div>

      </div>

    </div>
    </BaseContainer>

    <div v-if=" ! (showForecast && (activeGraphItem === graphitmes[1] || activeGraphItem === graphitmes[2]) )">
      <TheStatsRack :confidence="confidence" :height="height" :period="period" :time="time" :graph="activeGraphItem" />
    </div>

  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import BaseContainer from '@/components/Utils/BaseContainer'
import BaseToggleRack from '@/components/Utils/BaseToggleRack'
import TheHistoryForecastWaveHeight from '@/components/D3Visualisations/TheHistoryForecastWaveHeight'
import TheHistoryForecastPeakPeriod from '@/components/D3Visualisations/TheHistoryForecastPeakPeriod'
import TheHistoryForecastDirection from '@/components/D3Visualisations/TheHistoryForecastDirection'
import TheForecastPeakPeriod from '@/components/D3Visualisations/TheForecastPeakPeriod'
import TheForecastDirection from '@/components/D3Visualisations/TheForecastDirection'
import TheHistoryWaveHeight from '@/components/D3Visualisations/TheHistoryWaveHeight'
import TheHistoryPeakPeriod from '@/components/D3Visualisations/TheHistoryPeakPeriod'
import TheHistoryDirection from '@/components/D3Visualisations/TheHistoryDirection'
import TheStatsRack from '@/components/SafeHarbourUtils/TheStatsRack'
import BaseComingSoon from '@/components/SafeHarbourUtils/BaseComingSoon'

export default {
  name: 'D3Demos',
  components: {
    BaseContainer,
    BaseToggleRack,
    TheHistoryForecastWaveHeight,
    TheHistoryForecastPeakPeriod,
    TheHistoryForecastDirection,
    TheForecastPeakPeriod,
    TheForecastDirection,
    TheHistoryWaveHeight,
    TheHistoryPeakPeriod,
    TheHistoryDirection,
    TheStatsRack,
    BaseComingSoon
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
          period: 2,
          chartWidth: 950,
          radarWidth: 550,
          windowWidth: window.innerWidth
      }
  },
  mounted() {
    this.confidence = this.historyData.summary_history.forecast.confidence.waveHeight
    this.height = this.historyData.summary_history.forecast.height
    this.period = this.historyData.summary_history.forecast.period

    // get window width
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    })
  },
  beforeDestroy() { 
    window.removeEventListener('resize', this.onResize); 
  },
  computed: {
    ...mapGetters({
      historyData: 'oceandata/getHistoryData'
    }),
  },
  methods: {
    onResize() {
      this.windowWidth = window.innerWidth
    },
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
            this.confidence = this.historyData.summary_history.forecast.confidence.waveHeight
          }
          else if ( this.activeGraphItem === 'Peak Period' ) {
            this.confidence = this.historyData.summary_history.forecast.confidence.peakPeriod
          }
          else if ( this.activeGraphItem === 'Direction' ) {
            this.confidence = this.historyData.summary_history.forecast.confidence.direction
          }
          
          this.height = this.historyData.summary_history.forecast.height
          this.period = this.historyData.summary_history.forecast.period

        }
        else if ( event === 'Last Day' ) {  // LAST DAY

          this.showForecast = false
          this.upperbound = 50  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence = this.historyData.summary_history.waveHeight.confidence
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = this.historyData.summary_history.peakPeriod.confidence
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = this.historyData.summary_history.direction.confidence
          }

          this.height = this.historyData.summary_history.waveHeight.day
          this. period = this.historyData.summary_history.peakPeriod.day

        }
        else if ( event === 'Last Week' ) {

          this.showForecast = false
          this.upperbound = 350  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence = this.historyData.summary_history.waveHeight.confidence
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = this.historyData.summary_history.peakPeriod.confidence
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = this.historyData.summary_history.direction.confidence
          }
          
          this.height = this.historyData.summary_history.waveHeight.week
          this. period = this.historyData.summary_history.peakPeriod.week

        }
        else if ( event === 'Last Month' ) {

          this.showForecast = false
          this.upperbound = 1400  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence = this.historyData.summary_history.waveHeight.confidence
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = this.historyData.summary_history.peakPeriod.confidence
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = this.historyData.summary_history.direction.confidence
          }

          this.height = this.historyData.summary_history.waveHeight.month
          this. period = this.historyData.summary_history.peakPeriod.month

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
  watch: {
    windowWidth(newWidth, oldWidth) {

      // IF WINDOW WIDTH IS SMALLER THAN THRESHOLD
      if ( this.windowWidth < 950 ) {
        this.chartWidth = this.windowWidth * 0.85  // 0.85 of window width tested to be a good value
        this.forceRerender()
      }
      // RESET WIDTH IF GREATER THAN THRESHOLD
      else {
        this.chartWidth = 950  // tested to be a good default
        this.forceRerender()
      }

      // RESIZE RADAR CHARTS DIFFERENTLY
      if ( this.windowWidth < 630 ) {
        this.radarWidth = this.windowWidth * 0.85  // 0.85 of window width tested to be a good value
        this.forceRerender()
      }
      else {
        this.radarWidth = 550  // tested to be a good default
        this.forceRerender()
      }
         
    }
  },
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

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
