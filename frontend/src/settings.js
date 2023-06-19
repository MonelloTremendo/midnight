import default_py from "@/assets/code_templates/default.py";
import randomFlags_py from "@/assets/code_templates/random_flags.py";

export default {
    api_url: "http://100.90.164.60:8000",
    websocket_url: "ws://100.90.164.60:8000/ws/",
    templates: [
        {
            "name": "Default",
            "source": default_py
        },
        {
            "name": "Random Flags",
            "source": randomFlags_py
        }
    ],
    services: [
        "capp",
        "tickkricket",
        "fixme",
        "ccmanager"
    ]
};