<template>
  <div
    class="container d-flex flex-column"
    style="height: calc(100vh - 58px - 4.5rem)"
  >
    <div class="d-flex flex-column" style="flex: 1; min-height: 100%">
      <h1>Dashboard</h1>
      <div class="row mt-4" style="flex: 1">
        <div class="col-8 d-flex flex-column">
          <h4 class="text-center">Flags retrieved</h4>
          <div class="mt-3 flex-fill">
            <Line
              v-if="flagsTick"
              :data="flagsTick"
              :options="flagsTickOptions"
            />
          </div>
        </div>
        <div class="col-4 d-flex flex-column">
          <h4 class="text-center">Submit stats</h4>
          <div class="mt-3 flex-fill">
            <Pie
              v-if="flagsAccepted"
              :data="flagsAccepted"
              :options="flagsAcceptedOptions"
            />
          </div>
        </div>
      </div>
      <div class="row mt-4" style="flex: 1">
        <div class="col-12 d-flex flex-column">
          <h4 class="text-center">Flags retrieved by exploit</h4>
          <div class="mt-3 flex-fill">
            <Pie
              v-if="flagsAcceptedPerExploit"
              :data="flagsAcceptedPerExploit"
              :options="flagsAcceptedPerExploitOptions"
            />
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
} from "chart.js";
import { Line, Pie } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ArcElement,
  Tooltip,
  Legend
);

export default {
  name: "Dashboard",
  components: { Line, Pie },
  data() {
    return {
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
      },
    };
  },
  methods: {
    async getFlagsTick() {
      let res = await api.get("/stats/flags/tick");
      res = await res.json();

      res = _.reverse(res);
      console.log(res);

      this.flagsTick = {
        labels: res.map((el) => {
          return new Date(new Date(el.tick_start * 1000).toUTCString())
            .toLocaleString()
            .split(", ")[1]
            .slice(0, -3);
        }),
        datasets: [
          {
            label: "Flags",
            data: res.map((el) => el.total),
            fill: true,
            backgroundColor: "#6f42c1",
            borderColor: "#6f42c1",
          },
        ],
      };
    },
    async getFlagsAccepted() {
      let res = await api.get("/stats/flags/all");
      res = await res.json();
      console.log(res);

      this.flagsAccepted = {
        labels: ["Queued", "Accepted", "Rejected"],
        datasets: [
          {
            data: [res.queued, res.accepted, res.rejected],
            backgroundColor: colors.green1,
            backgroundColor: ["#adb5bd", "#198754", "#dc3545"],
          },
        ],
      };
    },
    async getFlagsAcceptedPerExploit() {
      let res = await api.get("/stats/flags/scripts/all");
      res = await res.json();
      console.log(res);

      this.flagsAcceptedPerExploit = {
        labels: [res.map((item) => item.name)],
        datasets: [
          {
            label: "Data One",
            backgroundColor: "#f87979",
            data: [
              _.flatten(res.map((item) => {
                return {
                  label: "Dataset 2",
                  data: 0,
                  backgroundColor: "#f87979",
                  stack: "Stack 0",
                };
              })),
            ],
          },
        ],
      };
    },
  },
  async mounted() {
    await this.getFlagsTick();
    await this.getFlagsAccepted();
    await this.getFlagsAcceptedPerExploit();
  },
};
</script>
