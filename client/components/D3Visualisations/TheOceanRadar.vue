<template>
  <div>
    <div class="flexbox">
      <div id="radarChart"></div>
      <div class="flexbox">
        <svg id="legend-svg"></svg>
        <div class="time">Normalised Wave Energy</div>
      </div>
    </div>
    <div class="describe">Last Updateded: {{ data[data.length-1].DateTime }}</div>

    <div>
      <span>Time: {{ data[value].DateTime }}</span>
    </div>
    
    <div class="flexbox">
      <input type="range" min="0" :max="data.length-1" step="1" v-model="value">
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: 'TheOceanRadar',
  props: {
    data: {
      type: Array,
      required: true,
      validator(value) {
        return typeof value === 'object'
      },
    },
  },
  data() {
    return {
      value: 10,
      subsetData: this.data,
      cottStats: { max: 1, min: 0 }
    }
  },
  methods: {
      lastDay() {
        this.upperbound = 50
      },
      lastWeek() {
        this.upperbound = 350
      }
  },
  mounted() {
    // update data set
    d3.select('#radarChart *').remove()
    if (this.value - 20 < 0)
      this.subsetData = this.data.slice(0, this.value)
    else
      this.subsetData = this.data.slice(this.value-20, this.value)

    this.cottStats.max = d3.max(this.data, function(d) { return +d.CottHeight;} );
    this.cottStats.min = d3.min(this.data, function(d) { return +d.CottHeight;} );

    // duplicated code

    // [ SETUP CONSTANTS ] ---------------------------------------------------------------------
    const margin = { top: 10, right: 30, bottom: 30, left: 60 },
      size = 550,
      width = size - margin.left - margin.right,
      height = size - margin.top - margin.bottom,
      radius = Math.min(width, height) / 2 - 30,
      angleOffset = 90,
      domain = {min: 0, max: 25}

    const style = {fontsize: '12px', stroke: '1.5px', navy: '#285166' ,grey: '#515b6e'}
    const colour = {red: '#ec6d5f', green: '#27c9b8', blue: '#2caaca', navy: '#285166', dark: '#2d4051'}
    const stroke = {linewidth: 1.5, pointwidth: 6}

    const scales = {
      'puOr11': ['#7f3b08', '#b35806', '#e08214', '#fdb863', '#fee0b6', '#f7f7f7', '#d8daeb', '#b2abd2', '#8073ac', '#542788', '#2d004b'],
      'spectral8': ['#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd'],
      'redBlackGreen': ['#ff0000', '#AA0000', '#550000', '#005500', '#00AA00', '#00ff00'],
      'viridis': ["#440154","#440256","#450457","#450559","#46075a","#46085c","#460a5d","#460b5e","#470d60","#470e61","#471063","#471164","#471365","#481467","#481668","#481769","#48186a","#481a6c","#481b6d","#481c6e","#481d6f","#481f70","#482071","#482173","#482374","#482475","#482576","#482677","#482878","#482979","#472a7a","#472c7a","#472d7b","#472e7c","#472f7d","#46307e","#46327e","#46337f","#463480","#453581","#453781","#453882","#443983","#443a83","#443b84","#433d84","#433e85","#423f85","#424086","#424186","#414287","#414487","#404588","#404688","#3f4788","#3f4889","#3e4989","#3e4a89","#3e4c8a","#3d4d8a","#3d4e8a","#3c4f8a","#3c508b","#3b518b","#3b528b","#3a538b","#3a548c","#39558c","#39568c","#38588c","#38598c","#375a8c","#375b8d","#365c8d","#365d8d","#355e8d","#355f8d","#34608d","#34618d","#33628d","#33638d","#32648e","#32658e","#31668e","#31678e","#31688e","#30698e","#306a8e","#2f6b8e","#2f6c8e","#2e6d8e","#2e6e8e","#2e6f8e","#2d708e","#2d718e","#2c718e","#2c728e","#2c738e","#2b748e","#2b758e","#2a768e","#2a778e","#2a788e","#29798e","#297a8e","#297b8e","#287c8e","#287d8e","#277e8e","#277f8e","#27808e","#26818e","#26828e","#26828e","#25838e","#25848e","#25858e","#24868e","#24878e","#23888e","#23898e","#238a8d","#228b8d","#228c8d","#228d8d","#218e8d","#218f8d","#21908d","#21918c","#20928c","#20928c","#20938c","#1f948c","#1f958b","#1f968b","#1f978b","#1f988b","#1f998a","#1f9a8a","#1e9b8a","#1e9c89","#1e9d89","#1f9e89","#1f9f88","#1fa088","#1fa188","#1fa187","#1fa287","#20a386","#20a486","#21a585","#21a685","#22a785","#22a884","#23a983","#24aa83","#25ab82","#25ac82","#26ad81","#27ad81","#28ae80","#29af7f","#2ab07f","#2cb17e","#2db27d","#2eb37c","#2fb47c","#31b57b","#32b67a","#34b679","#35b779","#37b878","#38b977","#3aba76","#3bbb75","#3dbc74","#3fbc73","#40bd72","#42be71","#44bf70","#46c06f","#48c16e","#4ac16d","#4cc26c","#4ec36b","#50c46a","#52c569","#54c568","#56c667","#58c765","#5ac864","#5cc863","#5ec962","#60ca60","#63cb5f","#65cb5e","#67cc5c","#69cd5b","#6ccd5a","#6ece58","#70cf57","#73d056","#75d054","#77d153","#7ad151","#7cd250","#7fd34e","#81d34d","#84d44b","#86d549","#89d548","#8bd646","#8ed645","#90d743","#93d741","#95d840","#98d83e","#9bd93c","#9dd93b","#a0da39","#a2da37","#a5db36","#a8db34","#aadc32","#addc30","#b0dd2f","#b2dd2d","#b5de2b","#b8de29","#bade28","#bddf26","#c0df25","#c2df23","#c5e021","#c8e020","#cae11f","#cde11d","#d0e11c","#d2e21b","#d5e21a","#d8e219","#dae319","#dde318","#dfe318","#e2e418","#e5e419","#e7e419","#eae51a","#ece51b","#efe51c","#f1e51d","#f4e61e","#f6e620","#f8e621","#fbe723","#fde725"]
    }
    
    let colors = d3.scaleQuantize()
      .domain([0, 1])
      .range( scales.spectral8 )
    // -----------------------------------------------------------------------------------------


    // [ HELPER FUNCTIONS ] ---------------------------------------------------------------------
    function angleHelper(degree) {
      return (degree- angleOffset) * Math.PI / 180
    }

    function mapHelper(value) {
      return (value - domain.min) * (radius - 0) / (domain.max - domain.min) + 0
    }
    // -----------------------------------------------------------------------------------------

    // [ CALLBACKS FUNCTIONS ] ---------------------------------------------------------------------
    // MOUSEOVER CALLBACK
    const mouseoverCottPeriod = function (event, d) {
      // Use D3 to select element, change color and size
      d3.select(this)
        // .attr('stroke', colour.red)
        // .attr('fill', colour.red)
        .attr('cursor', 'pointer')
        .attr('r', stroke.pointwidth*1.5)

      // Specify where to put label of text
      svg
        .append('text')
        .attr('id', 'temp_text') // For later reference to remove from DOM
        .attr('x', () => {
          return mapHelper( d.CottPeakPeriod ) * Math.cos(angleHelper(d.CottDirection))
        })
        .attr('y', () => {
          return mapHelper( d.CottPeakPeriod ) * Math.sin(angleHelper(d.CottDirection))
        })
        .text(() => {
          return parseFloat(d.CottPeakPeriod).toFixed(2)
        }) // Value of the text
    }

    // MOUSELEAVE CALLBACK
    const mouseleave = function (event) {
      // Use D3 to select element, change color back to normal
      d3.select(this)
        // .attr('fill', colour.navy)
        // .attr('stroke', colour.navy)
        .attr('cursor', 'default')
        .attr('r', stroke.pointwidth)

      // Select text by id and then remove
      d3.select('#temp_text').remove()
    }
    // -----------------------------------------------------------------------------------------

    // [ CREATE GRAPHIC ] ----------------------------------------------------------------------
    let r = d3.scaleLinear().domain([domain.min, domain.max]).range([0, radius])

    let svg = d3
      .select('#radarChart')
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')')

    let gr = svg
      .append('g')
      .attr('class', 'r axis')
      .selectAll('g')
      .data(r.ticks(5).slice(1))
      .enter()
      .append('g')

    gr
      .append('circle')
      .attr('r', r)
      .style('fill', 'none')
      .style('stroke', style.navy)
      .style('stroke-dasharray', '1,4')

    // make the last circle solid
    d3.select(".axis :last-of-type circle").style('stroke', style.grey).style('stroke-dasharray', 'none')

    gr.append('text')
      .attr('y',  (d) => {
        return -r(d) - 4
      })
      .attr('transform', 'rotate(15)')
      .style('text-anchor', 'middle')
      .text( (d) => {
        return d + 's'
      })
      .style('font-size', style.fontsize)
      .style('fill', style.navy)
      

    let ga = svg
      .append('g')
      .attr('class', 'a axis')
      .selectAll('g')
      .data(d3.range(0, 360, 30))
      .enter()
      .append('g')
      .attr('transform',  (d) => {
        return 'rotate(' + `${d - 90}` +')'
      })
     

    ga
      .append('line')
      .attr('x2', radius)
      .style('fill', 'none')
      .style('stroke', style.navy)
      .style('stroke-dasharray', '1,4')

    ga.append('text')
      .attr('x', radius + 6)
      .attr('dy', '.35em')
      .style("text-anchor", function(d) { return d < 360 && d > 180 ? "end" : null; })
      .attr("transform", function(d) { return d < 360 && d > 180 ? "rotate(180 " + (radius + 6) + ",0)" : null; })
      .text( (d) => {
        return d + '°'
      })
      .style('font-size', style.fontsize)
      .style('fill', style.navy)

      

    // ADD INSTANCE POINTS
    svg
      .append('g')
      .selectAll('rottDots')
      .data(this.subsetData)
      .enter()
      .append('circle')
      .attr('class', 'rottPeakPeriod')
      .attr('cx', (d) => mapHelper( d.CottPeakPeriod ) * Math.cos(angleHelper(d.CottDirection)) )
      .attr('cy', (d) => mapHelper( d.CottPeakPeriod ) * Math.sin(angleHelper(d.CottDirection)) )
      .attr('r', 6)
      // .attr('fill', style.navy)
      .attr('fill', (d) => colors( (d.CottHeight - this.cottStats.min) / (this.cottStats.max - this.cottStats.min) ) )
      .attr('stroke', (d) => colors( (d.CottHeight - this.cottStats.min) / (this.cottStats.max - this.cottStats.min) ) )
      .attr('stroke-width', 0)
      .on('mouseover', mouseoverCottPeriod)
      .on('mouseleave', mouseleave)






 
  
    // [ LEGEND ] ------------------------------------------------------------------------
    var fullWidth = 600;
    var fullHeight = 400;

    // add the legend now
    var legendFullHeight = fullHeight;
    var legendFullWidth = 50;

    var legendMargin = { top: 20, bottom: 20, left: 5, right: 20 };

    // use same margins as main plot
    var legendWidth = legendFullWidth - legendMargin.left - legendMargin.right;
    var legendHeight = legendFullHeight - legendMargin.top - legendMargin.bottom;

    var legendSvg = d3.select('#legend-svg')
        .attr('width', legendFullWidth)
        .attr('height', legendFullHeight)
        .append('g')
        .attr('transform', 'translate(' + legendMargin.left + ',' +
        legendMargin.top + ')')

    updateColourScale(scales['spectral8'])


    // update the colour scale, restyle the plot points and legend
    function updateColourScale(scale) {
        // create colour scale
        // let colorScale = d3.scaleLinear()
        //     .domain(linspace(-3, 3, scale.length))
        //     .range(scale)


        // // style points
        // d3.selectAll('circle')
        //     .attr('fill', (d) => {
        //         if (d !== undefined)
        //           return colorScale(d.z)
        //     })


        // clear current legend
        legendSvg.selectAll('*').remove();

        // append gradient bar
        var gradient = legendSvg.append('defs')
            .append('linearGradient')
            .attr('id', 'gradient')
            .attr('x1', '0%') // bottom
            .attr('y1', '100%')
            .attr('x2', '0%') // to top
            .attr('y2', '0%')
            .attr('spreadMethod', 'pad');

        // programatically generate the gradient for the legend
        // this creates an array of [pct, colour] pairs as stop
        // values for legend
        var pct = linspace(0, 100, scale.length).map(function(d) {
            return Math.round(d) + '%'
        });

        var colourPct = d3.zip(pct, scale);

        colourPct.forEach(function(d) {
            gradient.append('stop')
                .attr('offset', d[0])
                .attr('stop-color', d[1])
                .attr('stop-opacity', 1);
        });

        legendSvg.append('rect')
            .attr('x1', 0)
            .attr('y1', 0)
            .attr('width', legendWidth - 10)
            .attr('height', legendHeight)
            .style('fill', 'url(#gradient)');

        // create a scale and axis for the legend
        // var legendScale = d3.scaleLinear()
        //     .domain([0, 1])
        //     .range([legendHeight, 0]);

        // var legendAxis = d3.axisRight(legendScale)
        //     .tickFormat((d, i) => { return i === 3 ? '12hr': 'now' })
        //     .tickValues(d3.range(-3, 4))

        // create a scale and axis for the legend
        var legendScale = d3.scaleLinear()
            .domain([0, 1])
            .range([legendHeight, 0]);

        var legendAxis = d3.axisRight(legendScale)
            .tickValues(d3.range(0, 5))
            .tickFormat(d3.format("d"));

        legendSvg.append("g")
            .attr("class", "legend axis")
            .attr("transform", "translate(" + (legendWidth-10) + ", 0)")
            .call(legendAxis);
    }

    function linspace(start, end, n) {
        var out = [];
        var delta = (end - start) / (n - 1);

        var i = 0;
        while(i < (n - 1)) {
            out.push(start + (i * delta));
            i++;
        }
        out.push(end);
        return out;
    }
    // ------------------------------------------------------------------------------






  },
  updated() {

    // update data set
    d3.select('#radarChart *').remove()
    if (this.value - 20 < 0)
      this.subsetData = this.data.slice(0, this.value)
    else
      this.subsetData = this.data.slice(this.value-20, this.value)


    // duplicated code

    // [ SETUP CONSTANTS ] ---------------------------------------------------------------------
    const margin = { top: 10, right: 30, bottom: 30, left: 60 },
      size = 550,
      width = size - margin.left - margin.right,
      height = size - margin.top - margin.bottom,
      radius = Math.min(width, height) / 2 - 30,
      angleOffset = 90,
      domain = {min: 0, max: 25}

    const style = {fontsize: '12px', stroke: '1.5px', navy: '#285166' ,grey: '#515b6e'}
    const colour = {red: '#ffce00', green: '#27c9b8', blue: '#87c7ff', navy: '#285166', dark: '#2d4051'}
    const stroke = {linewidth: 1.5, pointwidth: 6}

    const scales = {
      'puOr11': ['#7f3b08', '#b35806', '#e08214', '#fdb863', '#fee0b6', '#f7f7f7', '#d8daeb', '#b2abd2', '#8073ac', '#542788', '#2d004b'],
      'spectral8': ['#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd'],
      'redBlackGreen': ['#ff0000', '#AA0000', '#550000', '#005500', '#00AA00', '#00ff00'],
      'viridis': ["#440154","#440256","#450457","#450559","#46075a","#46085c","#460a5d","#460b5e","#470d60","#470e61","#471063","#471164","#471365","#481467","#481668","#481769","#48186a","#481a6c","#481b6d","#481c6e","#481d6f","#481f70","#482071","#482173","#482374","#482475","#482576","#482677","#482878","#482979","#472a7a","#472c7a","#472d7b","#472e7c","#472f7d","#46307e","#46327e","#46337f","#463480","#453581","#453781","#453882","#443983","#443a83","#443b84","#433d84","#433e85","#423f85","#424086","#424186","#414287","#414487","#404588","#404688","#3f4788","#3f4889","#3e4989","#3e4a89","#3e4c8a","#3d4d8a","#3d4e8a","#3c4f8a","#3c508b","#3b518b","#3b528b","#3a538b","#3a548c","#39558c","#39568c","#38588c","#38598c","#375a8c","#375b8d","#365c8d","#365d8d","#355e8d","#355f8d","#34608d","#34618d","#33628d","#33638d","#32648e","#32658e","#31668e","#31678e","#31688e","#30698e","#306a8e","#2f6b8e","#2f6c8e","#2e6d8e","#2e6e8e","#2e6f8e","#2d708e","#2d718e","#2c718e","#2c728e","#2c738e","#2b748e","#2b758e","#2a768e","#2a778e","#2a788e","#29798e","#297a8e","#297b8e","#287c8e","#287d8e","#277e8e","#277f8e","#27808e","#26818e","#26828e","#26828e","#25838e","#25848e","#25858e","#24868e","#24878e","#23888e","#23898e","#238a8d","#228b8d","#228c8d","#228d8d","#218e8d","#218f8d","#21908d","#21918c","#20928c","#20928c","#20938c","#1f948c","#1f958b","#1f968b","#1f978b","#1f988b","#1f998a","#1f9a8a","#1e9b8a","#1e9c89","#1e9d89","#1f9e89","#1f9f88","#1fa088","#1fa188","#1fa187","#1fa287","#20a386","#20a486","#21a585","#21a685","#22a785","#22a884","#23a983","#24aa83","#25ab82","#25ac82","#26ad81","#27ad81","#28ae80","#29af7f","#2ab07f","#2cb17e","#2db27d","#2eb37c","#2fb47c","#31b57b","#32b67a","#34b679","#35b779","#37b878","#38b977","#3aba76","#3bbb75","#3dbc74","#3fbc73","#40bd72","#42be71","#44bf70","#46c06f","#48c16e","#4ac16d","#4cc26c","#4ec36b","#50c46a","#52c569","#54c568","#56c667","#58c765","#5ac864","#5cc863","#5ec962","#60ca60","#63cb5f","#65cb5e","#67cc5c","#69cd5b","#6ccd5a","#6ece58","#70cf57","#73d056","#75d054","#77d153","#7ad151","#7cd250","#7fd34e","#81d34d","#84d44b","#86d549","#89d548","#8bd646","#8ed645","#90d743","#93d741","#95d840","#98d83e","#9bd93c","#9dd93b","#a0da39","#a2da37","#a5db36","#a8db34","#aadc32","#addc30","#b0dd2f","#b2dd2d","#b5de2b","#b8de29","#bade28","#bddf26","#c0df25","#c2df23","#c5e021","#c8e020","#cae11f","#cde11d","#d0e11c","#d2e21b","#d5e21a","#d8e219","#dae319","#dde318","#dfe318","#e2e418","#e5e419","#e7e419","#eae51a","#ece51b","#efe51c","#f1e51d","#f4e61e","#f6e620","#f8e621","#fbe723","#fde725"]
    }
    
    let colors = d3.scaleQuantize()
      .domain([0, 1])
      .range( scales.spectral8 )
    // -----------------------------------------------------------------------------------------


    // [ HELPER FUNCTIONS ] ---------------------------------------------------------------------
    function angleHelper(degree) {
      return (degree- angleOffset) * Math.PI / 180
    }

    function mapHelper(value) {
      return (value - domain.min) * (radius - 0) / (domain.max - domain.min) + 0
    }
    // -----------------------------------------------------------------------------------------

    // [ CALLBACKS FUNCTIONS ] ---------------------------------------------------------------------
    // MOUSEOVER CALLBACK
    const mouseoverCottPeriod = function (event, d) {
      // Use D3 to select element, change color and size
      d3.select(this)
        // .attr('stroke', colour.red)
        // .attr('fill', colour.red)
        .attr('cursor', 'pointer')
        .attr('r', stroke.pointwidth*1.5)

      // Specify where to put label of text
      svg
        .append('text')
        .attr('id', 'temp_text') // For later reference to remove from DOM
        .attr('x', () => {
          return mapHelper( d.CottPeakPeriod ) * Math.cos(angleHelper(d.CottDirection))
        })
        .attr('y', () => {
          return mapHelper( d.CottPeakPeriod ) * Math.sin(angleHelper(d.CottDirection))
        })
        .text(() => {
          return parseFloat(d.CottPeakPeriod).toFixed(2)
        }) // Value of the text
    }

    // MOUSELEAVE CALLBACK
    const mouseleave = function (event) {
      // Use D3 to select element, change color back to normal
      d3.select(this)
        // .attr('fill', colour.navy)
        // .attr('stroke', colour.navy)
        .attr('cursor', 'default')
        .attr('r', stroke.pointwidth)

      // Select text by id and then remove
      d3.select('#temp_text').remove()
    }
    // -----------------------------------------------------------------------------------------

    // [ CREATE GRAPHIC ] ----------------------------------------------------------------------
    let r = d3.scaleLinear().domain([domain.min, domain.max]).range([0, radius])

    let svg = d3
      .select('#radarChart')
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')')

    let gr = svg
      .append('g')
      .attr('class', 'r axis')
      .selectAll('g')
      .data(r.ticks(5).slice(1))
      .enter()
      .append('g')

    gr
      .append('circle')
      .attr('r', r)
      .style('fill', 'none')
      .style('stroke', style.navy)
      .style('stroke-dasharray', '1,4')

    // make the last circle solid
    d3.select(".axis :last-of-type circle").style('stroke', style.grey).style('stroke-dasharray', 'none')

    gr.append('text')
      .attr('y',  (d) => {
        return -r(d) - 4
      })
      .attr('transform', 'rotate(15)')
      .style('text-anchor', 'middle')
      .text( (d) => {
        return d + 's'
      })
      .style('font-size', style.fontsize)
      .style('fill', style.navy)
      

    let ga = svg
      .append('g')
      .attr('class', 'a axis')
      .selectAll('g')
      .data(d3.range(0, 360, 30))
      .enter()
      .append('g')
      .attr('transform',  (d) => {
        return 'rotate(' + `${d - 90}` +')'
      })
     

    ga
      .append('line')
      .attr('x2', radius)
      .style('fill', 'none')
      .style('stroke', style.navy)
      .style('stroke-dasharray', '1,4')

    ga.append('text')
      .attr('x', radius + 6)
      .attr('dy', '.35em')
      .style("text-anchor", function(d) { return d < 360 && d > 180 ? "end" : null; })
      .attr("transform", function(d) { return d < 360 && d > 180 ? "rotate(180 " + (radius + 6) + ",0)" : null; })
      .text( (d) => {
        return d + '°'
      })
      .style('font-size', style.fontsize)
      .style('fill', style.navy)

      

    // ADD INSTANCE POINTS
    svg
      .append('g')
      .selectAll('rottDots')
      .data(this.subsetData)
      .enter()
      .append('circle')
      .attr('class', 'rottPeakPeriod')
      .attr('cx', (d) => mapHelper( d.CottPeakPeriod ) * Math.cos(angleHelper(d.CottDirection)) )
      .attr('cy', (d) => mapHelper( d.CottPeakPeriod ) * Math.sin(angleHelper(d.CottDirection)) )
      .attr('r', 6)
      // .attr('fill', style.navy)
      .attr('stroke', (d) => colors( (d.CottHeight - this.cottStats.min) / (this.cottStats.max - this.cottStats.min) ) )
      .attr('fill', (d) => colors( (d.CottHeight - this.cottStats.min) / (this.cottStats.max - this.cottStats.min) ) )
      .attr('stroke-width', 0)
      .on('mouseover', mouseoverCottPeriod)
      .on('mouseleave', mouseleave)






 
  
    // [ LEGEND ] ------------------------------------------------------------------------
    var fullWidth = 600;
    var fullHeight = 400;

    // add the legend now
    var legendFullHeight = fullHeight;
    var legendFullWidth = 50;

    var legendMargin = { top: 20, bottom: 20, left: 5, right: 20 };

    // use same margins as main plot
    var legendWidth = legendFullWidth - legendMargin.left - legendMargin.right;
    var legendHeight = legendFullHeight - legendMargin.top - legendMargin.bottom;

    var legendSvg = d3.select('#legend-svg')
        .attr('width', legendFullWidth)
        .attr('height', legendFullHeight)
        .append('g')
        .attr('transform', 'translate(' + legendMargin.left + ',' +
        legendMargin.top + ')')

    updateColourScale(scales['spectral8'])


    // update the colour scale, restyle the plot points and legend
    function updateColourScale(scale) {
        // create colour scale
        // let colorScale = d3.scaleLinear()
        //     .domain(linspace(-3, 3, scale.length))
        //     .range(scale)


        // // style points
        // d3.selectAll('circle')
        //     .attr('fill', (d) => {
        //         if (d !== undefined)
        //           return colorScale(d.z)
        //     })


        // clear current legend
        legendSvg.selectAll('*').remove();

        // append gradient bar
        var gradient = legendSvg.append('defs')
            .append('linearGradient')
            .attr('id', 'gradient')
            .attr('x1', '0%') // bottom
            .attr('y1', '100%')
            .attr('x2', '0%') // to top
            .attr('y2', '0%')
            .attr('spreadMethod', 'pad');

        // programatically generate the gradient for the legend
        // this creates an array of [pct, colour] pairs as stop
        // values for legend
        var pct = linspace(0, 100, scale.length).map(function(d) {
            return Math.round(d) + '%'
        });

        var colourPct = d3.zip(pct, scale);

        colourPct.forEach(function(d) {
            gradient.append('stop')
                .attr('offset', d[0])
                .attr('stop-color', d[1])
                .attr('stop-opacity', 1);
        });

        legendSvg.append('rect')
            .attr('x1', 0)
            .attr('y1', 0)
            .attr('width', legendWidth - 10)
            .attr('height', legendHeight)
            .style('fill', 'url(#gradient)');

        // create a scale and axis for the legend
        // var legendScale = d3.scaleLinear()
        //     .domain([0, 1])
        //     .range([legendHeight, 0]);

        // var legendAxis = d3.axisRight(legendScale)
        //     .tickFormat((d, i) => { return i === 3 ? '12hr': 'now' })
        //     .tickValues(d3.range(-3, 4))

        // create a scale and axis for the legend
        var legendScale = d3.scaleLinear()
            .domain([0, 1])
            .range([legendHeight, 0]);

        var legendAxis = d3.axisRight(legendScale)
            .tickValues(d3.range(0, 5))
            .tickFormat(d3.format("d"));

        legendSvg.append("g")
            .attr("class", "legend axis")
            .attr("transform", "translate(" + (legendWidth-10) + ", 0)")
            .call(legendAxis);
    }

    function linspace(start, end, n) {
        var out = [];
        var delta = (end - start) / (n - 1);

        var i = 0;
        while(i < (n - 1)) {
            out.push(start + (i * delta));
            i++;
        }
        out.push(end);
        return out;
    }
    // ------------------------------------------------------------------------------




  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'

  input
    width 100%

  span
    padding 5px

  .time
    font-size 12px
    transform rotate(90deg)
    margin-left -70px
    font-weight bold

  .describe
    text-align center
    font-size 10px
    margin 0
    padding 0


  input[type=range] 
    width 100%
    margin 13.2px 0
    background-color transparent
    -webkit-appearance none
    border-radius 10px
  
  input[type=range]:focus 
    outline none
  
  input[type=range]::-webkit-slider-runnable-track 
    border 1px solid $border-color
    border-radius 6.2px
    width 100%
    height 12.6px
    cursor pointer
  
  input[type=range]::-webkit-slider-thumb 
    margin-top -5px
    width 20px
    height 20px
    background $navy
    border-radius 100%
    cursor pointer
    -webkit-appearance: none
  
  
  input[type=range]::-moz-range-track 
    border 1px solid $border-color
    border-radius 6.2px
    width 100%
    height 12.6px
    cursor pointer
  
  input[type=range]::-moz-range-thumb 
    margin-top -5px
    width 20px
    height 20px
    background $blue
    border-radius 100%
    cursor pointer
</style>
