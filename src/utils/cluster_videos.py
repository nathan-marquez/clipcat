import os
import json
import requests
from openai import OpenAI


def cluster_videos(category: str, cluster_size = 5):
    # given a category, such as "mood"

    # 1. perform a pass through the video_documents folder. retrieve all summarries from video jsons. 
    #    -  from this, we get a dictionary called summaryDict, which has keys as the video id, and values as the summary

    folder_path = "data/video_documents"
    summaryDict = {}
    categoryDict = {}

    # 1. Retrieve summaries from video JSONs
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                data = json.load(file)
                video_id = filename.replace('.json', '')
                summary = data.get("summary", "")
                if summary:
                    summaryDict[video_id] = summary
    print("retrieved summaries from jsons")



    # 2. now that we have a dictionary with all the summaries, we can generate 3-5 subcategories (ex "sad", "happy", "boring") for the documents
    #      - to do this, group the first 20 summaries
    #      - then call the chatgpt3.5 turbo api to generate cluster_size clsubcategoriesusters for these 20 seummaries. 
    #      - continue doing this for the next 20 summaries, until we've gone through all summaries
    #      - we should now have a list of list of subcategories
    #      - give this list of list of subcategories to chatgpt3.5 turbo api, and compress these subcategories into a list of 3-5 subcategories
    #      - we should now have a final list of 3-5 subcategories
     


    # Assuming function to interact with ChatGPT API
    def get_subcategories(texts):
        # Implement API call to ChatGPT 3.5 Turbo to get subcategories
        client = OpenAI(api_key="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")

        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Return {cluster_size} ONE WORD subcategories that fall under the category: {category}. Your answer should be in the format 'subcategory1, subcategory2, subcategory3, ..., subcategory4' "},
            {"role": "user", "content": texts}
        ]
        )

        response = completion.choices[0].message.content.lower()

        return response
    
    def flatten_and_format_subcategories(subcategory_lists):
        """
        Flatten a list of lists and format it into a string.
        """
        # Flatten the list of lists into a single list
        all_subcategories_flat = [subcategory for sublist in subcategory_lists for subcategory in sublist]
        
        # Convert the list into a string, separated by a unique separator if needed
        subcategories_string = ", ".join(all_subcategories_flat).lower()

        return subcategories_string
    
    # 2. Generate subcategories
    summaries_list = list(summaryDict.values())
    all_subcategories = []

    # Define a marker to indicate a new summary starts. This can be a simple string like "NEW SUMMARY:"
    # or something more unique if your summaries might contain similar text.
    summary_separator = " NEW SUMMARY: "

    step = 20
    i = 0
    while i < len(summaries_list):
        # Concatenate summaries in the chunk with the separator
        chunk_text = summary_separator.join(summaries_list[i:min(i+20,len(summaries_list)-1)])
        
        # Now, `chunk_text` is a large string with summaries separated by `summary_separator`
        # You can pass this string to the ChatGPT API or any function that processes it to generate subcategories
        subcategories = get_subcategories(chunk_text)

        subcategoryList = subcategories.split(', ')

        all_subcategories.append(subcategoryList)
        i+=20


    print("initial subcategories: ", all_subcategories)

    # Compress subcategories into 3-5 subcategories
    final_subcategories = get_subcategories(flatten_and_format_subcategories(all_subcategories))
    
    print("got final subcategories", final_subcategories)



    # 3. perform a final pass through each json in the video_documents folder.
    #    - use chatgpt3 turbo api to assign each document to a pre-determined cluster (determined from step 2), by adding the id to categoryDict[assigned_category]
    
    # return categoryDict, a dictonary of each category to their doc ids


    def determine_cluster(summary, clusters):
        # Implement API call to ChatGPT 3.5 Turbo to get clusters
        client = OpenAI(api_key="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")

        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Given the summary, categorize it as part of one of these clusters: {clusters}. Answer with one word, which is the cluster chosen."},
            {"role": "user", "content": summary}
        ]
        )

        response = completion.choices[0].message.content.lower()

        return response

    # 3. Assign documents to clusters
    for video_id, summary in summaryDict.items():
        # Placeholder for cluster assignment logic
        # You would call ChatGPT 3.5 Turbo API to determine the cluster for each summary
        assigned_cluster = determine_cluster(summary, final_subcategories)
        # print("assigned cluster for " + str(video_id) + ": assigned_cluster")

        if assigned_cluster not in categoryDict:
            categoryDict[assigned_cluster] = []
        categoryDict[assigned_cluster].append(video_id)

    return categoryDict

    
# print(cluster_videos("excitement level", 10))