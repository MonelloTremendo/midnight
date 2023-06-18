<template>
    <div class="container mt-4">
        <h1>Dashboard</h1>
        <div class="row mt-3">
            <div class="col-8">
                <h4 class="text-center">Flags retrieved per tick</h4>
                <div class="mt-3" style="height: 300px">
                    <Line v-if="flagsTick" :data="flagsTick" :options="flagsTickOptions" />
                </div>
            </div>
            <div class="col-4">
                <h4 class="text-center">Submit stats</h4>
                <div class="mt-3" style="height: 300px">
                    <Pie v-if="flagsAccepted" :data="flagsAccepted" :options="flagsAcceptedOptions" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
'use strict';

import * as _ from "lodash";
import { api, colors } from '../utils.js'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Line, Pie } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, ArcElement, Tooltip, Legend)

export default {
    name: 'Plots',
    components: { Line, Pie },
    data() {
        return {
            flagsTick: undefined,
            flagsAccepted: undefined,
            flagsTickOptions: {
                responsive: true,
                maintainAspectRatio: false,
                scales:
                {
                    x: {
                        grid: { color: "#3f3f3f", borderColor: "#8b8b8b" },
                    },
                    y: {
                        grid: { color: "#3f3f3f", borderColor: "#8b8b8b" },
                    },
                }
            },
            flagsAcceptedOptions: {
                responsive: true,
                maintainAspectRatio: false,
            },
        };
    },
    methods: {
        async getFlagsTick() {
            let res = await api.get('/stats/flags/tick');
            res = await res.json();
            res = _.reverse(res)

            console.log(res)

            this.flagsTick = {
                labels: res.map(el => el.tick_start),
                datasets: [{
                    label: "Flags",
                    data: res.map(el => el.total),
                    fill: true,
                    backgroundColor: '#7a4fbf',
                    borderColor: '#673ab7',
                }],
            };
        },
        async getFlagsAccepted() {
            let res = await api.get('/stats/flags/all');
            res = await res.json();
            console.log(res)

            this.flagsAccepted = {
                labels: ["Queued", "Accepted", "Rejected"],
                datasets: [{
                    data: [res.queued, res.accepted, res.rejected],
                    backgroundColor: colors.green1,
                    backgroundColor: ['#717171', '#4caf50', '#f44336'],
                }],
            };
        }
    },
    mounted() {
        this.getFlagsTick();
        this.getFlagsAccepted();
    },
}
</script>