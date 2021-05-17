<template>
  <div class="admin">
    <section class="hero is-primary">
      <div class="hero-body">
        <p class="title">
          Admin dashboard
        </p>
        <p class="subtitle">
          Get deep
        </p>
      </div>
    </section>
    <section id="form" style="margin-top: 30px">
      <div class="container">
        <h1 class="subtitle">Add Quote</h1>
        <b-field label="Quote">
          <b-input v-model="formText" minlength="1" required validation-message="Make sure this field isn't empty"></b-input>
        </b-field>
        <b-field label="Author">
          <b-input v-model="formAuthor" minlength="1" required validation-message="Make sure this field isn't empty"></b-input>
        </b-field>
        <b-field>
          <b-button
              label="Add quote"
              type="is-primary"
              size="ismedium"
              @click="addQuote"
          />
        </b-field>
      </div>
    </section>
    <section>
      <div class="container" style="margin-top: 30px; margin-bottom: 30px">
        <b-table :loading="isLoading" :data="tableData" :columns="tableColumns" :selected.sync="selected"></b-table>
        <a style="margin-right: 30px; color: #f14668" @click="deleteQuote">Delete selection</a>
        <a @click="selected = null">Clear selection</a>
      </div>
    </section>
  </div>
</template>

<script>
const axios = require('axios');

export default {
  name: 'App',
  data: function() {
    return {
      formText: "",
      formAuthor: "",
      isLoading: true,
      tableData: [],
      tableColumns: [
        /*{
          field: 'id',
          label: 'ID',
          centered: true
        },*/
        {
          field: 'text',
          label: 'Quote',
          centered: true
        },
        {
          field: 'author',
          label: 'Author',
          centered: true
        }
      ],
      selected: {}
    };
  },
  methods: {
    getQuotes() {
      const instance = this
      axios.defaults.baseURL = 'http://localhost:5000';
      axios.get("/list-quotes").then(function (response) {
        instance.tableData = response.data.quotes
        instance.isLoading = false
      }).catch(function(error) {
        console.log(error)
        instance.isLoading = false
      })
    },
    addQuote() {
      const instance = this
      axios.defaults.baseURL = 'http://localhost:5000';
      axios.post("/add-quote", {
        text: instance.formText,
        author: instance.formAuthor
      }).then(function () {
        instance.formText = ""
        instance.formAuthor = ""

        instance.isLoading = true
        const sleep = (milliseconds) => {
          return new Promise(resolve => setTimeout(resolve, milliseconds))
        }
        sleep(100).then(function() {
          instance.getQuotes()
        })
      }).catch(function(error) {
        console.log(error)
      })
    },
    deleteQuote() {

    }
  },
  mounted() {
    this.getQuotes()
  }
}
</script>