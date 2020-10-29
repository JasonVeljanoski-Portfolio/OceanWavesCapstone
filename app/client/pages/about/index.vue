<template>
  <div class="container">

    
    <div class="flexcontainer">
      <div @click="toggle('Matlab-to-JSON')" class="button">
        <div class="button">Matlab to JSON</div>
      </div>
      <div @click="toggle('Data-Alignment')" class="button">
        <div class="button">Data Alignment</div>
      </div>
      <div @click="toggle('height')" class="button">
        <div class="button">Cott Height Notebook</div>
      </div>
      <div @click="toggle('period')" class="button">
        <div class="button">Cott Peak Period Notebook</div>
      </div>
      <div @click="toggle('direction')" class="button">
        <div class="button">Cott Direction Notebook</div>
      </div>
      <div @click="toggle('forecast')" class="button">
        <div class="button">Forecast Notebook</div>
      </div>
    </div>



    <div class="pdf">
      <embed v-show="isMtJSON" src="/data-transform-align.pdf" type="application/pdf" width="100%" height="800px" />
      <embed v-show="isDataAlign" src="/mat-to-json.pdf" type="application/pdf" width="100%" height="800px" />
      <embed v-show="isHeight" src="/height.pdf" type="application/pdf" width="100%" height="800px" />
      <embed v-show="isPeriod" src="/period.pdf" type="application/pdf" width="100%" height="800px" />
      <embed v-show="isDirection" src="/direction.pdf" type="application/pdf" width="100%" height="800px" />
      <embed v-show="isForecast" src="/forecast.pdf" type="application/pdf" width="100%" height="800px" />
    </div>
   




  </div>
</template>

<script>
import TheTeam from '@/components/SafeHarbourUtils/TheTeam'

export default {
  name: 'ContactPage',
  components: {
    TheTeam
  },
  data() {
    return {
        isMtJSON: true,
        isDataAlign: false,
        isHeight: false,
        isPeriod: false,
        isDirection: false,
        isForecast: false
    }
  },
  methods: {
    toggle(event) {
        if (event == 'Matlab-to-JSON') {

          this.isMtJSON = true
          this.isDataAlign = false
          this.isHeight = false
          this.isPeriod = false
          this.isDirection = false
          this.isForecast = false

        } else if (event == 'Data-Alignment') {

          this.isMtJSON = false
          this.isDataAlign = true
          this.isHeight = false
          this.isPeriod = false
          this.isDirection = false
          this.isForecast = false

        } else if (event == 'height') {

          this.isMtJSON = false
          this.isDataAlign = false
          this.isHeight = true
          this.isPeriod = false
          this.isDirection = false
          this.isForecast = false

        } else if (event == 'period') {

          this.isMtJSON = false
          this.isDataAlign = false
          this.isHeight = false
          this.isPeriod = true
          this.isDirection = false
          this.isForecast = false
          
        } else if (event == 'direction') {

          this.isMtJSON = false
          this.isDataAlign = false
          this.isHeight = false
          this.isPeriod = false
          this.isDirection = true
          this.isForecast = false
          
        } else if (event == 'forecast') {

          this.isMtJSON = false
          this.isDataAlign = false
          this.isHeight = false
          this.isPeriod = false
          this.isDirection = false
          this.isForecast = true

        }
    }
  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

.button
  background #efefef
  font-weight bold
  cursor pointer
  padding 0px 3px 0px 3px
  margin 2px
  font-size 10pt

.button:hover
  opacity 0.8

.active
  background #d3d3d3

.flexcontainer
   display flex
   align-items center
   justify-content center
   flex-flow row wrap
   align-content flex-end

  .pdf
    margin 10px

  .container
    margin 20px
</style>
