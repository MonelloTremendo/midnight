import default_py from "@/assets/code_templates/default.py";
import randomFlags_py from "@/assets/code_templates/random_flags.py";
import web_py from "@/assets/code_templates/web.py";

export default {
    api_url: "http://100.90.164.60:8000",
    websocket_url: "ws://100.90.164.60:8000/ws/",
    // api_url: "",
    // websocket_url: "",
    templates: [
        {
            "name": "Empty",
            "source": default_py
        },
        {
            "name": "Random",
            "source": randomFlags_py
        },
        {
            "name": "Web - Faker - Flagids",
            "source": web_py
        }
    ],
};