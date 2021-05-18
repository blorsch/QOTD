<template>
  <div id="app">
    <button id="edit" class="button">Edit</button>
    <div id="quote">
      <h1 class="title is-1 has-text-white" style="z-index: 1; position: relative">"{{quoteText}}"</h1>
      <h4 class="subtitle has-text-white" style="z-index: 1; position: relative">{{quoteAuthor}}</h4>
    </div>
    <v-vanta v-if="showVanta" effect="fog" :options=vantaOptions></v-vanta>
  </div>
</template>

<script>
const axios = require('axios');
import VVanta from 'vue-vanta';

export default {
  name: 'App',
  components: {
    VVanta
  },
  data: function() {
    return {
      quoteText: "",
      quoteAuthor: "",
      showVanta: true, //for performance
      vantaOptions: {
        mouseControls: false,
        touchControls: false,
        minHeight: 500.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00
      }
    };
  },
  mounted() {
    this.showVanta = true

    const instance = this
    axios.defaults.baseURL = 'http://localhost:5000';
    axios.get("/random-quote").then(function (response) {
      const quote = response.data.quotes[0]
      instance.quoteText = quote.text
      instance.quoteAuthor = quote.author
    }).catch(function(error) {
      console.log(error)
    })
  },
  beforeDestroy() {
    this.showVanta = false
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #FFFFFF;
  margin-top: 0px;
}

.vanta-container {
  position: absolute;
  z-index: 0;
  top: 0px;
  left: 0px;
  bottom: 0px;
  height: 100%;
  width: 100%;
}

#quote {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  top: 0px;
  left: 0px;
  bottom: 0px;
  height: 100%;
  width: 100%;
}

#edit {
  position: fixed;
  right: 10px;
  bottom: 10px;
  height: 20px;
  width: 50px;
  padding: 20px 50px;
  z-index: 1;
}

</style>

<style scoped>
.button {
  display: none !important;
}

.button:hover {
  display: inline-flex !important;
}
</style>
