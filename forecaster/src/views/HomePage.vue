<template>
    <h1>Disaster Forecaster</h1>

    <div class="options">
        <div>
            <label for="continent">Continent:</label>
            <select v-model="selectedContinent" id="continent" @change="onContinentChange">
                <option disabled value="">Please select one</option>
                <option v-for="continent in continents" :key="continent" :value="continent">{{ continent }}</option>
            </select>
        </div>

        <div>
            <label for="country">Country:</label>
            <select v-model="selectedCountry" id="country" @change="onCountryChange" :disabled="!selectedContinent">
                <option disabled value="">Please select one</option>
                <option v-for="country in countries" :key="country" :value="country">{{ country }}</option>
            </select>
        </div>

        <div>
            <label for="city">City:</label>
            <select v-model="selectedCity" id="city" :disabled="!selectedCountry">
                <option disabled value="">Please select one</option>
                <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
        </div>

        <div>
            <label for="startDate">Start Date:</label>
            <input type="date" id="startDate" v-model="startDate">
        </div>

        <div>
            <label for="endDate">End Date:</label>
            <input type="date" id="endDate" v-model="endDate">
        </div>

        <button @click="forecast">Forecast</button>
    </div>

    <div v-if="showInformation" class="information">
        <p>{{ selectedStartDate }} - {{ selectedEndDate }}</p>
        <p>
            <span :class="getArrowClass(67)">➤</span> 67% chance of floods
        </p>
        <p>
            <span :class="getArrowClass(13)">➤</span> 13% chance of hurricanes
        </p>
        <p>
            <span :class="getArrowClass(2)">➤</span> 2% chance of wildfires
        </p>
    </div>

    <div class="chart-area">
        <div class="tabs">
            <button v-for="disaster in disasters" :key="disaster" @click="selectedDisaster = disaster">
                {{ disaster }}
            </button>
        </div>
        <line-chart :chart-data="chartData"></line-chart>
    </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import { LineChart } from 'vue-chart-3';
Chart.register(...registerables);

export default {
    name: 'HomePage',
    data() {
        return {
            selectedDisaster: 'Floods',
            disasters: ['Floods', 'Hurricanes', 'Wildfires'],
            chartData: {},
            showInformation: false,
            continents: ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Australia', 'Antarctica'],
            countries: [],
            cities: [],
            data: {
                'Europe': ['Germany', 'Slovakia', 'Czech Republic'],
                'Germany': ['Berlin', 'Munich', 'Hamburg', 'Cologne'],
                'Slovakia': ['Bratislava', 'Košice', 'Prešov', 'Nitra'],
                'Czech Republic': ['Prague', 'Brno', 'Ostrava', 'Pilsen'],
            },
            selectedContinent: '',
            selectedCountry: '',
            selectedCity: '',
            startDate: '',
            endDate: '',
        };
    },

    components: {
        'line-chart': LineChart, // Register the LineChart component with the tag you will use in the template
    },
    watch: {
        selectedDisaster() {
            this.updateChartData();
        }
    },
    mounted() {
        this.selectedContinent = 'Europe';
        this.onContinentChange();
        this.selectedCountry = 'Germany';
        this.onCountryChange();
        this.selectedCity = 'Berlin';
        this.startDate = '2024-04-05';
        this.endDate = '2024-04-06';
    },
    methods: {
        async updateChartData() {
            if (!this.selectedCity || !this.startDate || !this.endDate) return;

            let cityDisasters;
            try {
                cityDisasters = await import(`../data/${this.selectedCity.toLowerCase()}.js`);
            } catch (error) {
                console.error(`Could not load disaster data for ${this.selectedCity}:`, error);
                return;
            }

            const disasterData = cityDisasters.default; // The imported data is available here

            const labels = [];
            const data = [];

            let currentDate = new Date(this.startDate);
            const endDate = new Date(this.endDate);

            while (currentDate <= endDate) {
                const dateString = currentDate.toISOString().split('T')[0];
                labels.push(this.formatDateForDisplay(dateString)); // Add the date to the labels array

                const percentage = disasterData[this.selectedDisaster.toLowerCase()][dateString] || 0;
                data.push(percentage); // Add the disaster chance to the data array

                // Increment the date by one day
                currentDate = new Date(currentDate.setDate(currentDate.getDate() + 1));
            }

            // Update the chartData reactive property
            this.chartData = {
                labels,
                datasets: [
                    {
                        label: this.selectedDisaster,
                        data: data,
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }
                ]
            };
        },
        onContinentChange() {
            this.countries = this.data[this.selectedContinent] || [];
            this.selectedCountry = this.countries.length > 0 ? this.countries[0] : '';
            this.onCountryChange(); // Update cities when the countries are updated
        },

        onCountryChange() {
            this.cities = this.data[this.selectedCountry] || [];
            this.selectedCity = this.cities.length > 0 ? this.cities[0] : '';
        },
        forecast() {
            if (this.selectedCity && this.startDate && this.endDate) {
                this.showInformation = true;
                this.selectedStartDate = this.formatDateForDisplay(this.startDate);
                this.selectedEndDate = this.formatDateForDisplay(this.endDate);
                this.updateChartData();
            } else {
                this.showInformation = false;
            }
        },
        formatDateForDisplay(dateString) {
            const [year, month, day] = dateString.split('-');
            const idx = Number(month);
            const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            return `${day} ${months[idx]} ${year}`;
        },
        getArrowClass(percentage) {
            if (percentage > 50) {
                return 'high-risk';
            } else if (percentage > 20) {
                return 'medium-risk';
            } else {
                return 'low-risk';
            }
        }
    }
}
</script>

<style scoped>
.options {
    display: flex;
    /* flex-direction: column; */
    align-items: center;
    justify-content: center;
    gap: 30px;
}

.high-risk {
    color: red;
}

.medium-risk {
    color: blue;
}

.low-risk {
    color: green;
}

.information {
    /* Styling for your information div */
}
</style>