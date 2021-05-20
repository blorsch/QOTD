<template>
  <div class="modal-card" style="width: auto">
    <header class="modal-card-head">
      <p class="subtitle">
        Update quote
      </p>
    </header>
    <section class="modal-card-body">
      <b-field label="Quote">
        <b-input v-model="formText" minlength="1" required
                 validation-message="Make sure this field isn't empty"></b-input>
      </b-field>
      <b-field label="Author">
        <b-input v-model="formAuthor" minlength="1" required
                 validation-message="Make sure this field isn't empty"></b-input>
      </b-field>
    </section>
    <footer class="modal-card-foot">
      <b-field>
        <b-button
            label="Done"
            type="is-primary"
            size="ismedium"
            :loading="isLoading"
            @click="updateQuote"
        />
      </b-field>
    </footer>
  </div>
</template>
<script>
const axios = require('axios');

export default {
  name: 'EditQuoteModal',
  props: {
    formAuthor: {},
    formText: {},
    id: {}
  },
  data: function() {
    return {
      isLoading: false
    }
  },
  mounted() {
    //setup axios
    axios.defaults.baseURL = process.env.VUE_APP_API_ROOT;
    axios.defaults.headers.common['Authorization'] = `Bearer ${this.$store.state.jwt.token}`;
  },
  methods: {
    updateQuote: function() {
      const instance = this
      instance.isLoading = true
      axios.post(`/update-quote/${instance.id}`, {
        text: instance.formText,
        author: instance.formAuthor
      }).then(function () {
        instance.isLoading = false
        instance.$emit('updatedQuote')
        instance.$emit('close')
      }).catch(function(error) {
        instance.isLoading = false
        console.log(error)
      })
    }
  }
}
</script>