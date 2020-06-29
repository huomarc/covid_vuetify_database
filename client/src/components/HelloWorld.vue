<template>
    <v-card>
        <v-card-title>
            COVID-19 Global Data
            <v-spacer></v-spacer> 
            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers" :items="countries" :search="search"></v-data-table>
    </v-card>
</template>
<script>
import axios from 'axios'
export default {
    name: "app",
    data() {
        return {
            search: '',
            headers: [{
                    text: 'Country ID',
                    align: 'start',
                    sortable: false,
                    value: 'id',
                },
                { text: 'Country', value: 'country' },
                { text: 'Country Code', value: 'code' },
                { text: 'Population', value: 'population' },
                { text: 'Last Updated', value: 'last_updated' },
                { text: 'Confirmed', value: 'confirmed' },
                { text: 'Deaths', value: 'deaths' },
                { text: 'Recovered', value: 'recovered' },
            ],
            countries: []
        }
    },
    mounted() {
        axios
            .get('http://localhost:8000/records/')
            .then(response => this.countries = response.data)
            .catch(error => {
                console.log(error)
            })
    }
}
</script>