// vuex data
export const state = () => ({
    oceanData: [],
    oceanDataReady: false,
    historyData: [],
    historyDataReady: false
  })
 
// synchronous way to update the state in our vuex store (synchronous setter)
export const mutations = {
    SET_OCEANDATA(state, payload) {
        state.oceanData = payload
        state.oceanDataReady = true
    },
    SET_HISTORYDATA(state, payload) {
      state.historyData = payload
      state.historyDataReady = true
    }
}
  
// get item from state (getter)
export const getters = {
  getOceanData(state) {
    return state.oceanData
  },
  getOceanDataReady(state) {
    return state.oceanDataReady
  },
  getHistoryData(state) {
    return state.historyData
  },
  getHistoryDataReady(state) {
    return state.historyDataReady
  }
}

// asynchronous way to update state (asynchronous setter)
export const actions = {

    async loadItems ( { commit } ) {
      const { data } = await this.$axios.$get('/oceanwaves')
      commit( 'SET_OCEANDATA', data )
    },

    async loadHistoryItems ( { commit } ) {
      const { data } = await this.$axios.$get('/historywaves')
      commit( 'SET_HISTORYDATA', data )
    }

}