import os, json
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

load_dotenv()

openai_key = os.getenv("OPENAI_APIKEY")

graph_config = {
    "llm": {
        "api_key": openai_key,
        "model": "gpt-4o",
    },
    "verbose": True,
    "headless": False,
}

def scrapeGraph(url):
    # Create the SmartScraperGraph instance and run it

    smart_scraper_graph = SmartScraperGraph(
        prompt="Summarize the text on the website, making sure to capture only the key points and using only 3 sentences.",
        # also accepts a string with the already downloaded HTML code
        source="{}".format(url),
        config=graph_config,
    )

    result = smart_scraper_graph.run()
    print(json.dumps(result, indent=4))
    print("this is the summary\n")
    print(result["summary"])

    # Get graph execution info
    graph_exec_info = smart_scraper_graph.get_execution_info()
    print(prettify_exec_info(graph_exec_info))

    return result["summary"]

# scrapeGraph("https://x.com/kylejeong21/status/1807661811854127510") 