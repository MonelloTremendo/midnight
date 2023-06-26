<template>
    <div class="container d-flex flex-column" style="height: calc(100vh - 58px - 4.5rem)">
        <div class="d-flex flex-column" style="flex: 1; min-height: 100%">
            <h1>Dashboard</h1>
            <div class="row mt-4" style="flex: 1">
                <div class="col-8 d-flex flex-column">
                    <h4 class="text-center">Flags retrieved</h4>
                    <div class="mt-3 flex-fill">
                        <Line v-if="flagsTick" :data="flagsTick" :options="flagsTickOptions" />
                    </div>
                </div>
                <div class="col-4 d-flex flex-column">
                    <h4 class="text-center">Submit stats</h4>
                    <div class="mt-3 flex-fill">
                        <Pie v-if="flagsAccepted" :data="flagsAccepted" :options="flagsAcceptedOptions" />
                    </div>
                </div>
            </div>
            <div class="row mt-4" style="flex: 1">
                <div class="col-12 d-flex flex-column">
                    <h4 class="text-center">Flags retrieved by exploit</h4>
                    <div class="mt-3 flex-fill">
                        <Bar v-if="flagsAcceptedPerExploit" :data="flagsAcceptedPerExploit"
                            :options="flagsAcceptedPerExploitOptions" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
"use strict";

import * as _ from "lodash";
import { api, colors } from "../utils.js";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    BarElement,
} from "chart.js";
import { Line, Pie, Bar } from "vue-chartjs";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    ArcElement,
    BarElement,
    Tooltip,
    Legend
);

export default {
    name: "Dashboard",
    components: { Line, Pie, Bar },
    data() {
        return {
            timer: undefined,
            flagsTick: undefined,
            flagsAccepted: undefined,
            flagsAcceptedPerExploit: undefined,
            flagsTickOptions: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { color: "#3f3f3f", borderColor: "#8b8b8b" },
                    },
                    y: {
                        grid: { color: "#3f3f3f", borderColor: "#8b8b8b" },
                        min: 0,
                    },
                },
            },
            flagsAcceptedOptions: {
                responsive: true,
                maintainAspectRatio: false,
            },
            flagsAcceptedPerExploitOptions: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                },
                scales: {
                    x: {
                        stacked: true,
                    },
                    y: {
                        stacked: true,
                    },
                },
            },
        };
    },
    methods: {
        async getFlagsTick() {
            let res = [];
            try {
                let req = await api.get("/stats/flags/tick");
                if (req.status == 200)
                    res = await req.json();
            } catch (exception) {
                console.log(exception);
            }
            const stamp_now = Date.now() / 1000;
            const tick_now = stamp_now - (stamp_now % 120);
            //console.log(tick_now);

            let out = [];

            for (let i = 0; i < 15; i++) {
                let tick = tick_now - 120 * i;
                let found = res.find((el, i) => el.tick_start === tick)

                if (found) {
                    out[i] = found
                } else {
                    out[i] = {
                        "total": 0,
                        "queued": 0,
                        "accepted": 0,
                        "rejected": 0,
                        "tick_start": tick
                    }
                }
            }

            let labels = out.reverse().map((el) => {
                return new Date(new Date(el.tick_start * 1000).toUTCString())
                    .toLocaleString()
                    .split(", ")[1]
                    .slice(0, -3);
            });

            this.flagsTick = {
                labels,
                datasets: [
                    {
                        label: "Flags",
                        data: out.map(item => item.total),
                        fill: true,
                        backgroundColor: "#6f42c1",
                        borderColor: "#6f42c1",
                    },
                ],
            };
        },
        async getFlagsAccepted() {
            let res = { queued: 0, accepted: 0, rejected: 0 }
            try {
                let req = await api.get("/stats/flags/all");
                if (req.status == 200)
                    res = await req.json();
            } catch (exception) {
                console.log(exception);
            }

            this.flagsAccepted = {
                labels: ["Queued", "Accepted", "Rejected"],
                datasets: [
                    {
                        data: [res.queued, res.accepted, res.rejected],
                        backgroundColor: colors.green1,
                        backgroundColor: ["#a7acb1", "#198754", "#dc3545"],
                    },
                ],
            };
        },
        async getFlagsAcceptedPerExploit() {
            let res = []
            try {
                let req = await api.get("/stats/flags/scripts");
                if (req.status == 200)
                    res = await req.json();
            } catch (exception) {
                console.log(exception);
            }

            let data = [
                {
                    label: "Accepted",
                    data: res.map((item) => (item.accepted / item.total) * 100),
                    backgroundColor: "#198754",
                    stack: 0,
                },
                {
                    label: "Rejected",
                    data: res.map((item) => (item.rejected / item.total) * 100),
                    backgroundColor: "#dc3545",
                    stack: 0,
                },
                {
                    label: "Queued",
                    data: res.map((item) => (item.queued / item.total) * 100),
                    backgroundColor: "#a7acb1",
                    stack: 0,
                },
            ];

            this.flagsAcceptedPerExploit = {
                labels: res.map((item) => item.name),
                datasets: data,
            };
        },
    },
    async mounted() {
        await this.getFlagsTick();
        await this.getFlagsAccepted();
        await this.getFlagsAcceptedPerExploit();

        this.timer = setInterval(async () => {
            await this.getFlagsTick();
            await this.getFlagsAccepted();
            await this.getFlagsAcceptedPerExploit();
        }, 20 * 1000);
    },
    async unmounted() {
        clearInterval(this.timer);
    },
};
</script>
