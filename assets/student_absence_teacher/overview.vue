<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <div>
        <b-row>
            <b-col>
                <b-form-group
                    label="Date"
                >
                    <b-overlay
                        :show="loading"
                        rounded="sm"
                    >
                        <b-input
                            type="date"
                            v-model="date"
                            @input="get_absence_count"
                        />
                    </b-overlay>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-table
                    hover
                    bordered
                    :items="absence_count"
                    :fields="fields"
                    :filter="filter"
                    :filter-included-fields="['classe']"
                >
                    <template v-slot:head(classe)="">
                        <b-form-group
                            label-for="filterInput"
                        >
                            <b-form-input
                                v-model="filter"
                                type="search"
                                id="filterInput"
                                placeholder="Filtrer par classe"
                            />
                        </b-form-group>
                    </template>
                    <template v-slot:cell(classe)="data">
                        {{ data.value }}
                    </template>
                    <template v-slot:cell()="data">
                        <span
                            v-if="data.value.teacher_count >= 0"
                            class="btn-link btn"
                            @click="toList(data)"
                        >
                            {{ data.value.teacher_count }}
                        </span>
                        <span v-else>-</span>
                        <span v-if="'not_teacher_count' in data.value">
                            /
                            <span v-if="data.value.not_teacher_count >= 0">
                                {{ data.value.not_teacher_count }}
                            </span>
                            <span v-else>-</span>
                        </span>
                    </template>
                </b-table>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

export default {
    data: function () {
        return {
            date: Moment().format("YYYY-MM-DD"),
            absence_count: [],
            fields: [
                {key: "classe", }
            ],
            filter: "",
            loading: true,
        };
    },
    methods: {
        get_absence_count: function () {
            this.loading = true;
            axios.get(`/student_absence_teacher/api/count_absence/${this.date}/`)
                .then(resp => {
                    this.absence_count = JSON.parse(resp.data).map(row => {
                        const periods = Object.entries(row).filter(c => c[0].startsWith("period"));
                        const emptyPeriods = periods.filter(p => p[1]["teacher_count"] < 0);
                        row._cellVariants = emptyPeriods.reduce((acc, v) => {
                            acc[v[0]] = "warning";
                            return acc;
                        }, {});
                        if (periods.length > 0 && "not_teacher_count" in periods[0][1]) {
                            const mismatchPeriods = periods.filter(p => {
                                if (p[1]["not_teacher_count"] < 0 || p[1]["teacher_count"] < 0) {
                                    return false;
                                }
                                if (p[1]["not_teacher_count"] != p[1]["teacher_count"]) {
                                    return true;
                                }
                                return false;
                            });
                            mismatchPeriods.forEach(p => {
                                row._cellVariants[p[0]] = "danger";
                            });
                        }
                        return row;
                    });
                    this.loading = false;
                });
        },
        toList: function (data) {
            this.$store.commit("removeFilter", "period__name");
            this.$store.commit("addFilter", {"tag": data.field.name, "filterType":"period__name", "value": data.field.name});

            this.$store.commit("removeFilter", "classe");
            this.$store.commit("addFilter", {"tag": data.item.classe, "filterType": "classe", "value": data.item.classe});

            this.$router.push("list");
        }
    },
    mounted: function () {
        axios.get("/student_absence_teacher/api/period/")
            .then(resp => {
                this.fields = this.fields.concat(
                    resp.data.results.map(p => {
                        return {
                            key: `period-${p.id}`,
                            label: `${p.start.slice(0, 5)} ${p.end.slice(0, 5)}`,
                            name: p.name
                        };
                    })
                );
            });
        this.get_absence_count();
    }
};
</script>
