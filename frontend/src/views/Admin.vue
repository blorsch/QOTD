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
        <b-table style="margin-bottom: 10px" :loading="isLoading" :data="tableData" :columns="tableColumns" :selected.sync="selected"></b-table>
        <a style="margin-right: 30px" @click="isEditModalActive = true">Edit selection</a>
        <a style="margin-right: 30px; color: #f14668" @click="deleteQuote">Delete selection</a>
        <a @click="selected = null">Clear selection</a>
      </div>
    </section>
    <b-modal has-modal-card v-model="isEditModalActive">
      <EditQuoteModal v-on:close="isEditModalActive = false" v-on:updatedQuote="getQuotes()" :form-author="selected.author" :form-text="selected.text" :id="selected.id"/>
    </b-modal>
  </div>
</template>

<script>
import EditQuoteModal from "@/views/EditQuoteModal";

const axios = require('axios');

export default {
  name: 'App',
  components: {EditQuoteModal},
  data: function() {
    return {
      formText: "",
      formAuthor: "",
      isEditModalActive: false,
      isLoading: true,
      tableData: [],
      tableColumns: [
        {
          field: 'id',
          label: 'ID',
          centered: true
        },
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
      axios.get("/list-quotes").then(function (response) {
        const sorted = response.data.quotes.sort((a, b) => (a.id > b.id) ? 1 : -1) // https://flaviocopes.com/how-to-sort-array-of-objects-by-property-javascript/
        instance.tableData = sorted
        instance.isLoading = false
      }).catch(function(error) {
        console.log(error)
        instance.isLoading = false
      })
    },
    addQuote() {
      const instance = this
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
      const instance = this
      axios.post(`/delete-quote/${instance.selected.id}`).then(function () {
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
    }
  },
  mounted() {
    //setup axios
    axios.defaults.baseURL = process.env.VUE_APP_API_ROOT;
    axios.defaults.headers.common['Authorization'] = `Bearer ${this.$store.state.jwt.token}`;

    //get data
    this.getQuotes()
  }
}
</script>