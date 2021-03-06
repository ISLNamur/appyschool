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
        <div
            class="loading"
            v-if="!loaded"
        />
        <app-menu
            v-if="loaded"
            :menu-info="menuInfo"
        />
        <b-container v-if="loaded">
            <b-row>
                <h2>Demandes de sanction</h2>
            </b-row>
            <b-row>
                <b-tabs>
                    <template slot="tabs">
                        <b-nav-item href="/dossier_eleve/">
                            Dossier des élèves
                        </b-nav-item>
                        <b-nav-item
                            active
                            href="/dossier_eleve/ask_sanctions"
                        >
                            Demandes de sanction
                        </b-nav-item>
                    </template>
                </b-tabs>
            </b-row>
            <b-row>
                <b-col
                    cols="12"
                    lg="3"
                >
                    <b-form-group>
                        <div>
                            <b-btn
                                variant="primary"
                                @click="openDynamicModal('ask-modal')"
                                class="w-100"
                            >
                                <icon
                                    name="plus"
                                    scale="1"
                                    class="align-middle"
                                />
                                Nouvelle demande
                            </b-btn>
                            <b-btn
                                variant="secondary"
                                @click="openDynamicModal('ask-export-modal')"
                                class="w-100 mt-1"
                            >
                                <icon
                                    name="file"
                                    scale="1"
                                />
                                Export
                            </b-btn>
                        </div>
                    </b-form-group>
                </b-col>
                <b-col
                    cols="12"
                    lg="9"
                >
                    <filters
                        app="dossier_eleve"
                        model="ask_sanctions"
                        ref="filters"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggleSearch="showFilters = !showFilters"
                        class="mb-1"
                    />
                </b-col>
            </b-row>
            <b-row v-if="$store.state.canSetSanction">
                <b-col>
                    <b-list-group>
                        <b-list-group-item>Demandes de sanction en attente : <b-badge>{{ entriesCount }}</b-badge></b-list-group-item>
                        <b-list-group-item
                            button
                            @click="addFilter('activate_not_done', 'Activer', true)"
                        >
                            Sanctions non faites <strong>à traiter</strong> : <b-badge variant="danger">
                                {{ entriesNotDone }}
                            </b-badge>
                        </b-list-group-item>
                        <b-list-group-item
                            button
                            v-if="entriesWaiting > 0"
                            @click="addFilter('activate_waiting', 'Activer', true)"
                        >
                            En attentes de validations : <b-badge variant="warning">
                                {{ entriesWaiting }}
                            </b-badge>
                        </b-list-group-item>
                    </b-list-group>
                </b-col>
            </b-row>
            <b-pagination
                class="mt-1"
                :total-rows="entriesCount"
                v-model="currentPage"
                @change="changePage"
                :per-page="20"
            />
            <b-card
                no-body
                class="current-card d-none d-md-block d-lg-block d-xl-block"
            >
                <b-row class="text-center">
                    <b-col cols="2">
                        <strong>Type de sanctions</strong>
                    </b-col>
                    <b-col
                        v-if="$store.state.settings.enable_disciplinary_council"
                        cols="2"
                    >
                        <strong>Conseil de discipline</strong>
                    </b-col>
                    <b-col cols="2">
                        <strong>Date de la sanction</strong>
                    </b-col>
                    <b-col><strong>Commentaire(s)</strong></b-col>
                </b-row>
            </b-card>
            <ask-sanctions-entry
                v-for="(entry, index) in entries"
                :key="entry.id"
                :row-data="entry"
                @delete="askDelete(entry)"
                @edit="editEntry(index)"
                @filterStudent="filterStudent($event)"
                @showInfo="showInfo(entry)"
                @done="loadEntries"
                @update-sanction="updateSanction(entry, $event)"
            />
            <b-modal
                ref="deleteModal"
                cancel-title="Annuler"
                hide-header
                centered
                @ok="deleteEntry"
                @cancel="currentEntry = null"
                :no-close-on-backdrop="true"
                :no-close-on-esc="true"
            >
                Êtes-vous sûr de vouloir supprimer définitivement cette entrée ?
            </b-modal>
            <b-modal
                :title="currentName"
                size="xl"
                ref="infoModal"
                centered
                ok-only
                @hidden="currentEntry = null"
            >
                <info
                    v-if="currentEntry"
                    :matricule="currentEntry.matricule_id"
                    type="student"
                />
            </b-modal>
            <component
                :is="currentModal"
                ref="dynamicModal"
                @update="loadEntries"
                @reset="currentEntry = null"
                :entry="currentEntry"
            />
        </b-container>
    </div>
</template>

<script>
import Vue from "vue";
import {BootstrapVue, BootstrapVueIcons} from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";
Vue.component("icon", Icon);

import axios from "axios";
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import Moment from "moment";

import Info from "../annuaire/info.vue";

import AskSanctionsEntry from "./askSanctionsEntry.vue";
import AskModal from "./askModal.vue";
import AskExportModal from "./askExportModal.vue";
import Filters from "../common/filters.vue";
import Menu from "../common/menu.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    data: function () {
        return {
            menuInfo: {},
            showFilters: false,
            filter: "",
            ordering: "&ordering=datetime_sanction",
            entriesCount: 0,
            currentPage: 1,
            entries: [],
            entriesNotDone: 0,
            entriesWaiting: 0,
            currentEntry: null,
            currentModal: "ask-modal",
            retenues_mode: false,
            loaded: false,
        };
    },
    computed: {
        currentName: function () {
            if (this.currentEntry) {
                return this.currentEntry.matricule.display;
            }
            return "";
        }
    },
    watch: {
        retenues_mode: function (mode) {
            if (mode) {
                this.addFilter("activate_all_retenues", "Activer", true);
            } else {
                this.$store.commit("removeFilter", "activate_all_retenues");
                this.applyFilter();
            }
        }
    },
    methods: {
        updateSanction: function (entry, newDate) {
            entry.datetime_sanction = newDate + Moment(entry.datetime_sanction).format(" HH:MM");
            axios.put(`/dossier_eleve/api/ask_sanctions/${entry.id}/`, entry, token);
        },
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            return;
        },
        openDynamicModal: function (modal) {
            this.currentModal = modal;
            this.$refs.dynamicModal.show();
        },
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.$store.commit("addFilter",
                {filterType: "matricule_id", tag: matricule, value: matricule}
            );
            this.applyFilter();
        },
        showInfo: function (entry) {
            this.currentEntry = entry;
            this.$refs.infoModal.show();
        },
        applyFilter: function () {
            this.filter = "";
            let storeFilters = this.$store.state.filters;
            for (let f in storeFilters) {
                if (storeFilters[f].filterType.startsWith("date")
                    || storeFilters[f].filterType.startsWith("time")) {
                    let ranges = storeFilters[f].value.split("_");
                    this.filter += "&" + storeFilters[f].filterType + "__gt=" + ranges[0];
                    this.filter += "&" + storeFilters[f].filterType + "__lt=" + ranges[1];
                } else {
                    this.filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
                }
            }
            this.currentPage = 1;
            this.loadEntries();
        },
        askDelete: function (entry) {
            this.currentEntry = entry;
            this.$refs.deleteModal.show();
        },
        editEntry: function(index) {
            this.currentEntry = this.entries[index];
            this.openDynamicModal("ask-modal");
        },
        deleteEntry: function () {
            axios.delete("/dossier_eleve/api/ask_sanctions/" + this.currentEntry.id + "/", token)
                .then(() => {
                    this.loadEntries();
                });

            this.currentEntry = null;
        },
        addFilter: function(filterType, tag, value) {
            this.showFilters = true;
            this.$store.commit("addFilter",
                {"filterType": filterType, "tag": tag, "value": value}
            );
            this.applyFilter();
        },
        loadEntries: function () {
            axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering)
                .then(response => {
                    this.entriesCount = response.data.count;
                    this.entries = response.data.results;
                    this.loaded = true;

                    // Get other counts.
                    this.getEntriesNotDone();
                    this.getEntriesWaiting();
                });
        },
        getEntriesNotDone: function () {
            axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering + "&activate_not_done=true")
                .then(response => {
                    this.entriesNotDone = response.data.count;
                });
        },
        getEntriesWaiting: function () {
            axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering + "&activate_waiting=true")
                .then(response => {
                    this.entriesWaiting = response.data.count;
                });
        }
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;

        this.applyFilter();
        this.loadEntries();
    },
    components: {
        "filters": Filters,
        "ask-sanctions-entry": AskSanctionsEntry,
        "ask-modal": AskModal,
        "ask-export-modal": AskExportModal,
        "info": Info,
        "app-menu": Menu,
    }
};
</script>

<style>
</style>
