<template>
  <div class="login">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Login</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <b-field label="Email">
          <b-input v-model="email" type="email" minlength="1" required validation-message="Make sure this field isn't empty"></b-input>
        </b-field>
        <b-field label="Password">
          <b-input v-model="password" type="password" minlength="1" required validation-message="Make sure this field isn't empty"></b-input>
        </b-field>
        <b-field>
          <b-button
              label="Login"
              type="is-primary"
              size="ismedium"
              @click="authenticate"
          />
        </b-field>
      </div>
    </section>
  </div>
</template>

<script>
import {EventBus} from '@/utils'

export default {
  name: "Login",
  data: function () {
    return {
      email: '',
      password: '',
      errorMsg: ''
    }
  },
  // https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/
  methods: {
    authenticate () {
      this.$store.dispatch('login', { email: this.email, password: this.password })
          .then(() => this.$router.push('/admin'))
    }
  },
  mounted() {
    EventBus.$on('failedRegistering', (msg) => {
      this.errorMsg = msg
    })
    EventBus.$on('failedAuthentication', (msg) => {
      this.errorMsg = msg
    })
  },
  beforeDestroy () {
    EventBus.$off('failedRegistering')
    EventBus.$off('failedAuthentication')
  }
}
</script>

<style scoped>

</style>