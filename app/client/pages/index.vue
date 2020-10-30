<template>
  <div>
    <BaseContainer @itemtoggle="graphToggleHandler($event)" :rackitems="graphitmes" :description="activeGraphItem" logo-file-name="safeharbourMini.svg" width="100%">
    <div>

      <div class="flexbox queue">

        <h3>Reports</h3>
        <div class="spacer" />
        <BaseToggleRack @toggle="reScale($event)" :items="scaleitems" />

      </div>

      <div :key="componentKey">

        <div v-if="showForecast">
          <TheForecastWaveHeight :width="chartWidth" :data="oceanData.forecast" v-show="activeGraphItem === graphitmes[0]" />
          <!-- <TheForecastPeakPeriod :width="chartWidth" :data="oceanData.forecast" v-show="activeGraphItem === graphitmes[1]" /> -->
          <BaseComingSoon v-show="activeGraphItem === graphitmes[1]" />
          <!-- <TheForecastDirection :width="radarWidth" :data="oceanData.forecast" v-show="activeGraphItem === graphitmes[2]" /> -->
          <BaseComingSoon v-show="activeGraphItem === graphitmes[2]" />
        </div>
        <div v-else>
          <TheOceanWaveHeight :width="chartWidth" v-show="activeGraphItem === graphitmes[0]" :data="oceanData.data.slice(oceanData.data.length-upperbound-1, oceanData.data.length-1)" />
          <TheOceanPeakPeriod :width="chartWidth" v-show="activeGraphItem === graphitmes[1]" :data="oceanData.data.slice(oceanData.data.length-upperbound-1, oceanData.data.length-1)" />
          <TheOceanRadar :width="radarWidth" v-show="activeGraphItem === graphitmes[2]" :data="oceanData.data.slice(oceanData.data.length-upperbound-1, oceanData.data.length-1)"/>
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
import TheForecastWaveHeight from '@/components/D3Visualisations/TheForecastWaveHeight'
import TheForecastPeakPeriod from '@/components/D3Visualisations/TheForecastPeakPeriod'
import TheForecastDirection from '@/components/D3Visualisations/TheForecastDirection'
import TheOceanWaveHeight from '@/components/D3Visualisations/TheOceanWaveHeight'
import TheOceanPeakPeriod from '@/components/D3Visualisations/TheOceanPeakPeriod'
import TheOceanRadar from '@/components/D3Visualisations/TheOceanRadar'
import TheStatsRack from '@/components/SafeHarbourUtils/TheStatsRack'
import TheDemoResponsiveD3 from '@/components/D3Visualisations/TheDemoResponsiveD3'
import BaseComingSoon from '@/components/SafeHarbourUtils/BaseComingSoon'

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
    TheStatsRack,
    TheDemoResponsiveD3,
    BaseComingSoon
  },
  data() {
      return {
          showForecast: false,
          activeGraphItem: 'Wave Height',
          activeTime: 'Last Day',
          graphitmes: ['Wave Height', 'Peak Period', 'Direction'],
          scaleitems: ['Last Day', 'Last Week', 'Last Month', 'Forecast'],
          upperbound: 50,
          componentKey: 0,
          time: 'Last Day',
          confidence: 0,
          height: 1,
          period: 2,
          chartWidth: 950,
          radarWidth: 550,
          windowWidth: window.innerWidth
      }
  },
  mounted() {
    this.confidence = 0.3064
    this.height = 2.52
    this.period = this.oceanData.summary.forecast.period

    // get window width
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    })
  },
  beforeDestroy() { 
    window.removeEventListener('resize', this.onResize); 
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


        // ERROR STATS - HARD CODED (Whooops!)
        // # MONTH.
        // rmse_height_mnth = 0.1752
        // rmse_period_mnth = 11.83
        // rmse_dir_mnth = 19.99

        // # WEEK.
        // rmse_height_week = 0.1462
        // rmse_period_week = 13.01
        // rmse_dir_week = 16.77

        // # DAY.
        // rmse_height_day = 0.3064
        // rmse_period_day = 9.148
        // rmse_dir_day = 20.71


        this.activeTime = event
        // FORECAST
        if ( event === 'Forecast' ) {

          this.showForecast = true

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem === 'Wave Height' ) {
            this.confidence = 0.1987
          }
          else if ( this.activeGraphItem === 'Peak Period' ) {
            this.confidence = this.oceanData.summary.forecast.confidence.peakPeriod
          }
          else if ( this.activeGraphItem === 'Direction' ) {
            this.confidence = this.oceanData.summary.forecast.confidence.direction
          }
          
          this.height = 2.52 // this.oceanData.summary.forecast.height
          this.period = this.oceanData.summary.forecast.period

        }
        else if ( event === 'Last Day' ) {  // LAST DAY

          this.showForecast = false
          this.upperbound = 50  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence =  0.3064 // this.oceanData.summary.waveHeight.confidence
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = 9.148
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = 20.71
          }

          this.height = this.oceanData.summary.waveHeight.day
          this. period = this.oceanData.summary.peakPeriod.day

        }
        else if ( event === 'Last Week' ) {

          this.showForecast = false
          this.upperbound = 350  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence = 0.1462
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = 13.01
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = 16.77
          }
          
          this.height = this.oceanData.summary.waveHeight.week
          this. period = this.oceanData.summary.peakPeriod.week

        }
        else if ( event === 'Last Month' ) {

          this.showForecast = false
          this.upperbound = 1400  // rescale graph

          // check which models confidence to display ('Wave Height', 'Peak Period', 'Direction' models)
          if ( this.activeGraphItem == 'Wave Height' ) {
            this.confidence = 0.1752
          }
          else if ( this.activeGraphItem == 'Peak Period' ) {
            this.confidence = 11.83
          }
          else if ( this.activeGraphItem == 'Direction' ) {
            this.confidence = 19.99
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
  computed: {
    ...mapGetters({
      oceanData: 'oceandata/getOceanData'
    }),
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
