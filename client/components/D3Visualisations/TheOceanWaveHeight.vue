<template>
  <div>
    <div id="TheOceanWaveHeight"></div>
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: 'TheOceanWaveHeight',
  props: {
    data: {
      type: Array,
      required: true,
      validator(value) {
        return typeof value === 'object'
      },
    },
  },
  mounted() {
    // [ SETUP CONSTANTS ] ---------------------------------------------------------------------
    const margin = { top: 10, right: 30, bottom: 30, left: 60 },
      width = 1000 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom

    const colour = {red: '#ffce00', green: '#27c9b8', blue: '#87c7ff', navy: '#285166', dark: '#2d4051'}
    const legend = {xpos: 20, ypos: 0}
    const stroke = {linewidth: 1.5, pointwidth: 1}

    const parseDateTime = d3.timeParse('%Y-%m-%d %H:%M:%S')
    // --------------------------------------------------------------------------------------


    // [ CALLBACKS ] ------------------------------------------------------------------------
    // MOUSEOVER CALLBACK
    const mouseoverCott = function (event, d) {
      // Use D3 to select element, change color and size
      d3.select(this)
        .attr('stroke', colour.blue)
        .attr('fill', colour.blue)
        .attr('cursor', 'pointer')
        .attr('r', 2)

      // Specify where to put label of text
      svg
        .append('text')
        .attr('id', 'temp_text') // For later reference to remove from DOM
        .attr('x', () => {
          return x(parseDateTime(d.DateTime)) - 30
        })
        .attr('y', () => {
          return y(d.CottHeight) - 15
        })
        .text(() => {
          return parseFloat(d.CottHeight).toFixed(2)
        }) // Value of the text
    }

    // MOUSEOVER CALLBACK
    const mouseoverRott = function (event, d) {
      // Use D3 to select element, change color and size
      d3.select(this)
        .attr('stroke', colour.red)
        .attr('fill', colour.red)
        .attr('cursor', 'pointer')
        .attr('r', stroke.pointwidth*1.5)

      // Specify where to put label of text
      svg
        .append('text')
        .attr('id', 'temp_text') // For later reference to remove from DOM
        .attr('x', () => {
          return x(parseDateTime(d.DateTime)) - 30
        })
        .attr('y', () => {
          return y(d.RottHeight) - 15
        })
        .text(() => {
          return parseFloat(d.RottHeight).toFixed(2)
        }) // Value of the text
    }

    // MOUSELEAVE CALLBACK
    const mouseleave = function (event) {
      // Use D3 to select element, change color back to normal
      d3.select(this)
        .attr('fill', colour.navy)
        .attr('stroke', colour.navy)
        .attr('cursor', 'default')
        .attr('r', stroke.pointwidth)

      // Select text by id and then remove
      d3.select('#temp_text').remove()
    }

        // TOGGLE ROTTNEST GRAPH
    const toggleRott = function(d) {
        // is the element currently visible ?
        let currentOpacity = d3.selectAll(".rottHeight").style("opacity")
        // Change the opacity: from 0 to 1 or from 1 to 0
        d3.selectAll(".rottHeight").transition().style("opacity", currentOpacity == 0 ? 1:0)
    }

    // TOGGLE COTTESLOE GRAPH
    const toggleCott = function(d) {
        // is the element currently visible ?
        let currentOpacity = d3.selectAll(".cottHeight").style("opacity")
        // Change the opacity: from 0 to 1 or from 1 to 0
        d3.selectAll(".cottHeight").transition().style("opacity", currentOpacity == 0 ? 1:0)
    }

    // MOUSEOVER LEGEND ROTTNEST
    const mouseoverLegendRott = function(d) {
        // is the element currently visible ?
        let currentOpacity = d3.selectAll(".rottHeight").style("opacity")

        if (currentOpacity == 1)
            // Change the opacity: from 0 to 1 or from 1 to 0
            d3.selectAll(".rottHeight").transition().style("opacity", 0.3)
    }

    // MOUSEOVER LEGEND COTTESLOE
    const mouseoverLegendCott = function(d) {
        // is the element currently visible ?
        let currentOpacity = d3.selectAll(".cottHeight").style("opacity")

        if (currentOpacity == 1)
            // Change the opacity: from 0 to 1 or from 1 to 0
            d3.selectAll(".cottHeight").transition().style("opacity", 0.3)
    }

    // MOUSELEAVE LEGEND COTTESLOE
    const mouseleaveLegendCott = function(d) {
        // is the element currently visible ?
        let currentOpacity = d3.selectAll(".cottHeight").style("opacity")

        if (currentOpacity != 0)
            // Change the opacity: from 0 to 1 or from 1 to 0
            d3.selectAll(".cottHeight").transition().style("opacity", 1)
    }

    // MOUSELEAVE LEGEND ROTTNEST
    const mouseleaveLegendRott = function(d) {
        // is the element currently visible ?
        let currentOpacity = d3.selectAll(".rottHeight").style("opacity")

        if (currentOpacity != 0)
            // Change the opacity: from 0 to 1 or from 1 to 0
            d3.selectAll(".rottHeight").transition().style("opacity", 1)
    }
    // --------------------------------------------------------------------------------------


    // [ BUILD D3 GRAPHIC ] -----------------------------------------------------------------
    // CONSTRUCT <svg> CONTAINER
    let svg = d3
      .select('#TheOceanWaveHeight')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)


    // ADD X AXIS --> DATE FORMAT
    const x = d3
      .scaleTime()
      .domain(d3.extent(this.data, (d) => { return parseDateTime(d.DateTime) }))
      .range([0, width])
    svg
      .append('g')
      .attr('transform', `translate(0, ${height})`)
      .call(d3.axisBottom(x))
      .attr('color', colour.navy)

    
    // ADD Y AXIS
    const y = d3
      .scaleLinear()
      .domain([ 0, d3.max(this.data, (d) => { return d.RottHeight }), ]) // bound Y by RottHeight as Rott >> Cott
      .range([height, 0])
    svg
      .append('g')
      .call(d3.axisLeft(y))
      .attr('color', colour.navy)

    
    // [ Construct Cottesloe Data ]
    // ADD LINE PATH
    svg
      .append('path')
      .datum(this.data)
      .attr('fill', 'none')
      .attr('stroke', colour.blue)
      .attr('stroke-width', stroke.linewidth)
      .attr('class', 'cottHeight')
      .attr('d',
        d3.line()
          .x((d) => { return x(parseDateTime(d.DateTime)) })
          .y((d) => { return y(d.CottHeight) })
      )

    // ADD INSTANCE POINTS
    svg
      .append('g')
      .selectAll('dot')
      .data(this.data)
      .enter()
      .append('circle')
      .attr('class', 'cottHeight')
      .attr('cx', (d) => { return x(parseDateTime(d.DateTime)) })
      .attr('cy', (d) => {  return y(d.CottHeight) })
      .attr('r', 1)
      .attr('fill', colour.navy)
      .attr('stroke', colour.navy)
      .attr('stroke-width', stroke.pointwidth)
      .on('mouseover', mouseoverCott)
      .on('mouseleave', mouseleave)



    // [ Construct Rottnest Data ]
    // ADD LINE PATH
    svg
      .append('path')
      .datum(this.data)
      .attr('fill', 'none')
      .attr('stroke', colour.red)
      .attr('stroke-width', stroke.linewidth)
      .attr('class', 'rottHeight')
      .attr('d',
        d3.line()
          .x((d) => { return x(parseDateTime(d.DateTime)) })
          .y((d) => { return y(d.RottHeight) })
      )

    // ADD INSTANCE POINTS
    svg
      .append('g')
      .selectAll('dot')
      .data(this.data)
      .enter()
      .append('circle')
      .attr('class', 'rottHeight')
      .attr('cx', (d) => { return x(parseDateTime(d.DateTime)) })
      .attr('cy', (d) => { return y(d.RottHeight) })
      .attr('r', 1)
      .attr('fill', colour.navy)
      .attr('stroke', colour.navy)
      .attr('stroke-width', stroke.pointwidth)
      .on('mouseover', mouseoverRott)
      .on('mouseleave', mouseleave)
    // --------------------------------------------------------------------------------------


    // [ Create Legend ] --------------------------------------------------------------------
    svg.append("circle").attr("cx", legend.xpos).attr("cy", legend.ypos).attr("r", 6).style("fill", colour.red).style("cursor", "pointer").on("click", toggleRott).on("mouseover", mouseoverLegendRott).on("mouseleave", mouseleaveLegendRott)
    svg.append("circle").attr("cx",legend.xpos).attr("cy",legend.ypos + 24).attr("r", 6).style("fill", colour.blue).style("cursor", "pointer").on("click", toggleCott).on("mouseover", mouseoverLegendCott).on("mouseleave", mouseleaveLegendCott)
    svg.append("text").attr("x", legend.xpos + 18).attr("y", legend.ypos + 1).text("Recorded Rottnest Wave Height").style("cursor", "pointer").style("font-size", "15px").attr("alignment-baseline","middle").on("click", toggleRott).on("mouseover", mouseoverLegendRott).on("mouseleave", mouseleaveLegendRott)
    svg.append("text").attr("x", legend.xpos + 18).attr("y", legend.ypos + 25).text("Predicted Cottesloe Wave Height").style("cursor", "pointer").style("font-size", "15px").attr("alignment-baseline","middle").on("click", toggleCott).on("mouseover", mouseoverLegendCott).on("mouseleave", mouseleaveLegendCott)
    // --------------------------------------------------------------------------------------

  }
}
</script>

<style lang="stylus" scoped>
@import '~static/css/main.styl'
</style>
