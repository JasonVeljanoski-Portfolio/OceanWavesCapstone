// vuex data
export const state = () => ({
    demoData: []
  })
 
// synchronous way to update the state in our vuex store (synchronous setter)
export const mutations = {
    setDemoData(state, payload) {
        state.demoData = payload
    }
}
  
// get item from state (getter)
export const getters = {
  getDemoData(state) {
    return state.demoData
  }
}

// asynchronous way to update state (asynchronous setter)
export const actions = {

    async setDemoData(state, payload) {
        const { data } = await this.$axios.$get('/d3')
        state.commit('setDemoData', data)   // commit is to use the setter in mutations called 'setDemoData'
    }

}