<template>
    <div class="container mt-4">
        <div class="row mb-4">
            <div class="col">
                <!-- tests -->
                <div class="card border-light mt-4">
                    <div class="card-body">
                        <h4 class="card-title">Test configuration</h4>
                        <div class="d-flex">
                            <form action="/submit-random" method="get">
                                <button type="submit" class="btn btn-secondary" id="button-submit-random">Submit some
                                    random flags</button>
                            </form>
                            <button type="submit" class="ml-4 btn btn-secondary" id="button-ping-checksystem">Ping
                                checksystem</button>
                            <button type="submit" class="ml-4 btn btn-secondary" id="button-ping-vulnbox">Ping your
                                vulnbox</button>
                        </div>
                    </div>
                </div>
                <!-- config -->
                <div class="card border-light mt-4">
                    <div class="card-body">
                        <h4 class="card-title">Configuration</h4>
                        <form action="/config" method="post" class="mt-4">
                            <!-- TEAMS -->
                            <div class="form-group">
                                <label for="TEAMS_IP_FORMAT">Teams' IP format string </label>
                                <input class="form-control" type="text" id="TEAMS_IP_FORMAT" name="TEAMS_IP_FORMAT"
                                    placeholder="config['TEAMS_IP_FORMAT']"
                                    value="config['TEAMS_IP_FORMAT']" />
                            </div>
                            <div class="form-group">
                                <label for="MIN_TEAM_ID">ID of the first team</label>
                                <input class="form-control" type="number" min="0" id="MIN_TEAM_ID" name="MIN_TEAM_ID"
                                    placeholder="config['MIN_TEAM_ID']" value="{{config['MIN_TEAM_ID']}}"/>
                            </div>
                            <div class="form-group">
                                <label for="MAX_TEAM_ID">ID of the last team</label>
                                <input class="form-control" type="number" min="0" id="MAX_TEAM_ID" name="MAX_TEAM_ID"
                                    placeholder="config['MAX_TEAM_ID']" value="config['MAX_TEAM_ID']"/>
                            </div>
                            <div class="form-group">
                                <label for="YOUR_TEAM_ID">ID of your team</label>
                                <input class="form-control" type="number" min="0" id="YOUR_TEAM_ID" name="YOUR_TEAM_ID"
                                    placeholder="config['YOUR_TEAM_ID']" value="config['YOUR_TEAM_ID']"/>
                            </div>
                            <div class="form-group">
                                <label for="NOP_TEAM_EXISTS">NOP team exists</label>
                                <select class="form-control" id="NOP_TEAM_EXISTS" name="NOP_TEAM_EXISTS">
                                    <option selected>config["NOP_TEAM_EXISTS"]</option>
                                    <option>not config["NOP_TEAM_EXISTS"]</option>
                                </select>
                            </div>
                            <div class="row">
                                <div class="col-8"></div>
                                <div class="col-4 text-right form-group" id="nop-team-field">
                                    <label for="NOP_TEAM_ID">ID of the NOP team</label>
                                    <input class="form-control" type="number" min="0" id="NOP_TEAM_ID"
                                        name="NOP_TEAM_ID" placeholder="config['NOP_TEAM_ID']"
                                        value="config['NOP_TEAM_ID']"/>
                                </div>
                            </div>
                            <!-- SYSTEM -->
                            <div class="form-group">
                                <label for="CTF_START">CTF start (in UNIX Epoch format)</label>
                                <p class="small">really got no time to make this usable so use <a class="small" href="https://www.epochconverter.com/" target="_blank">this</a></p>
                                <input class="form-control" type="number" id="CTF_START" name="CTF_START"
                                    placeholder="{{config['CTF_START']}}" value="{{config['CTF_START']}}"/>
                            </div>
                            <div class="form-group">
                                <label for="CTF_END">CTF end (in UNIX Epoch format)</label>
                                <input class="form-control" type="number" id="CTF_END" name="CTF_END"
                                    placeholder="{{config['CTF_END']}}" value="{{config['CTF_END']}}"/>
                            </div>
                            <div class="form-group">
                                <label for="ROUND_LENGTH">Round length (in seconds)</label>
                                <input class="form-control" type="number" id="ROUND_LENGTH" name="ROUND_LENGTH"
                                    placeholder="{{config['ROUND_LENGTH']}}" value="{{config['ROUND_LENGTH']}}"/>
                            </div>
                            <div class="form-group">
                                <label for="SYSTEM_PROTOCOL">System protocol</label>
                                <select class="form-control" id="SYSTEM_PROTOCOL" name="SYSTEM_PROTOCOL">
                                    <!--
                                    {% for protocol in protocols %}
                                    {% if protocol == config["SYSTEM_PROTOCOL"]%}
                                    -->
                                    <option selected>{ {protocol} }</option>
                                    <!--
                                    {% else %}
                                    -->
                                    <option>{ {protocol} }</option>
                                </select>
                            </div>
                            <!-- PROTOCOL SPECIFIC -->
                            <!-- ructf_tcp -->
                            <div class="row">
                                <div class="col-8"></div>
                                <div class="col-4 text-right" id="specific-ructf_tcp">
                                    <div class="form-group">
                                        <label for="SYSTEM_HOST-ructf_tcp">System host</label>
                                        <input class="form-control" type="text" id="SYSTEM_HOST-ructf_tcp"
                                            name="specific-SYSTEM_HOST-ructf_tcp"
                                            placeholder="{{config['SYSTEM_HOST']}}"
                                            value="{{config['SYSTEM_HOST']}}"/>
                                    </div>
                                    <div class="form-group">
                                        <label for="SYSTEM_PORT-ructf_tcp">System port</label>
                                        <input class="form-control" type="text" id="SYSTEM_PORT-ructf_tcp"
                                            name="specific-SYSTEM_PORT-ructf_tcp"
                                            placeholder="{{config['SYSTEM_PORT']}}"
                                            value="{{config['SYSTEM_PORT']}}"/>
                                    </div>
                                </div>
                            </div>
                            <!-- ructf_http -->
                            <div class="row">
                                <div class="col-8"></div>
                                <div class="col-4 text-right" id="specific-ructf_http">
                                    <div class="form-group">
                                        <label for="SYSTEM_URL-ructf_http">System URL</label>
                                        <input class="form-control" type="text" id="SYSTEM_URL-ructf_http"
                                            name="specific-SYSTEM_URL-ructf_http" placeholder="{{config['SYSTEM_URL']}}"
                                            value="{{config['SYSTEM_URL']}}"/>
                                    </div>
                                    <div class="form-group">
                                        <label for="SYSTEM_TOKEN-ructf_http">System token</label>
                                        <input class="form-control" type="text" id="SYSTEM_TOKEN-ructf_http"
                                            name="specific-SYSTEM_TOKEN-ructf_http"
                                            placeholder="{{config['SYSTEM_TOKEN']}}"
                                            value="{{config['SYSTEM_TOKEN']}}"/>
                                    </div>
                                </div>
                            </div>
                            <!-- volgactf -->
                            <div class="row">
                                <div class="col-8"></div>
                                <div class="col-4 text-right" id="specific-volgactf">
                                    <div class="form-group">
                                        <label for="SYSTEM_HOST-volgactf">System host</label>
                                        <input class="form-control" type="text" id="SYSTEM_HOST-volgactf"
                                            name="specific-SYSTEM_HOST-volgactf" placeholder="{{config['SYSTEM_HOST']}}"
                                            value="{{config['SYSTEM_HOST']}}"/>
                                    </div>
                                </div>
                            </div>
                            <!-- forcad_tcp -->
                            <div class="row">
                                <div class="col-8"></div>
                                <div class="col-4 text-right" id="specific-forcad_tcp">
                                    <div class="form-group">
                                        <label for="SYSTEM_HOST-forcad_tcp">System host</label>
                                        <input class="form-control" type="text" id="SYSTEM_HOST-forcad_tcp"
                                            name="specific-SYSTEM_HOST-forcad_tcp"
                                            placeholder="{{config['SYSTEM_HOST']}}"
                                            value="{{config['SYSTEM_HOST']}}"/>
                                    </div>
                                    <div class="form-group">
                                        <label for="specific-SYSTEM_PORT-forcad_tcp">System port</label>
                                        <input class="form-control" type="text" id="SYSTEM_PORT-forcad_tcp"
                                            name="specific-SYSTEM_PORT-forcad_tcp"
                                            placeholder="{{config['SYSTEM_PORT']}}"
                                            value="{{config['SYSTEM_PORT']}}"/>
                                    </div>
                                    <div class="form-group">
                                        <label for="specific-TEAM_TOKEN-forcad_tcp">Team token</label>
                                        <input class="form-control" type="text" id="TEAM_TOKEN-forcad_tcp"
                                            name="specific-TEAM_TOKEN-forcad_tcp" placeholder="{{config['TEAM_TOKEN']}}"
                                            value="{{config['TEAM_TOKEN']}}"/>
                                    </div>
                                </div>
                            </div>
                            <!-- FLAGS -->
                            <div class="form-group">
                                <label for="FLAG_FORMAT">Flag format string</label>
                                <input class="form-control" type="text" id="FLAG_FORMAT" name="FLAG_FORMAT"
                                    placeholder="{{config['FLAG_FORMAT']}}" value="{{config['FLAG_FORMAT']}}"/>
                            </div>
                            <div class="form-group">
                                <label for="SUBMIT_FLAG_LIMIT">Submit flag limit</label>
                                <p class="small">The server will submit not more than SUBMIT_FLAG_LIMIT flags
                                    every SUBMIT_PERIOD seconds. Flags received more than
                                    FLAG_LIFETIME seconds ago will be skipped.</p>
                                <input class="form-control" type="number" id="SUBMIT_FLAG_LIMIT"
                                    name="SUBMIT_FLAG_LIMIT" placeholder="{{config['SUBMIT_FLAG_LIMIT']}}"
                                    value="{{config['SUBMIT_FLAG_LIMIT']}}"/>
                            </div>
                            <div class="form-group">
                                <label for="SUBMIT_PERIOD">Submit period</label>
                                <input class="form-control" type="number" id="SUBMIT_PERIOD" name="SUBMIT_PERIOD"
                                    placeholder="{{config['SUBMIT_PERIOD']}}"
                                    value="{{config['SUBMIT_PERIOD']}}"/>
                            </div>
                            <div class="form-group">
                                <label for="FLAG_LIFETIME">Flag lifetime</label>
                                <input class="form-control" type="number" id="FLAG_LIFETIME" name="FLAG_LIFETIME"
                                    placeholder="{{config['FLAG_LIFETIME']}}"
                                    value="{{config['FLAG_LIFETIME']}}"/>
                            </div>
                            <!-- OTHER -->
                            <div class="form-group">
                                <label for="SERVER_PASSWORD">Server password</label>
                                <p class="small">Password for the web interface. You can use it with any login.<br>
                                    This value will be excluded from the config before sending it to farm clients.</p>
                                <input class="form-control" type="text" id="SERVER_PASSWORD" name="SERVER_PASSWORD"
                                    placeholder="{{config['SERVER_PASSWORD']}}"
                                    value="{{config['SERVER_PASSWORD']}}"/>
                            </div>
                            <div class="form-group">
                                <label for="ENABLE_API_AUTH">Enable API auth</label>
                                <p class="small">Use authorization for API requests</p>
                                <select class="form-control" id="ENABLE_API_AUTH" name="ENABLE_API_AUTH">
                                    <option selected>{ {config["ENABLE_API_AUTH"]} }</option>
                                    <option>{ {not config["ENABLE_API_AUTH"]} }</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="API_TOKEN">API token</label>
                                <input class="form-control" type="text" id="API_TOKEN" name="API_TOKEN"
                                    placeholder="{{config['API_TOKEN']}}" value="{{config['API_TOKEN']}}"/>
                            </div>
                            <div class="text-right pt-3">
                                <button type="submit" class="btn btn-lg btn-primary">Apply</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Settings",
    data() {
        return {};
    },
    created() {
        // console.log(this.$router.currentRoute._value.name);
    }
}

/*
const a = {
    labels: ["a", "a", "a", "a", "a"],
    datasets: [{
        label: "data one",
        data: [0,1,2,3,4],
        backgroundColor: '#42b983',
    }],
};
*/
</script>