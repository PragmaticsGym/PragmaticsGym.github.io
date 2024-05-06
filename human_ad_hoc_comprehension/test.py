import jacinle
import argparse
from jaclearn.visualize.html_table import HTMLTableVisualizer, HTMLTableColumnDesc
import json
import random
import os

# parser = argparse.ArgumentParser()
# parser.add_argument('--start_idx', default=0)
# parser.add_argument('--type', default="cancel_direct_implicature")
# args = parser.parse_args()

def main():
    meta_list = []
    for item in os.listdir("./meta_data"):
        #print(type(item))
        if '.json' not in item:
            continue
        #print(item.rstrip(".jsonl").split("annotations_"))
        #print(item)
        temp_item = int(item.rstrip(".json").split("_")[1])#.strip("_")
        print(temp_item)
        #if int(temp_item) >= 0 and int(temp_item) <= 100 and "jsonl" in item:
        if int(temp_item) < 200:
            meta_list.append(item)
        #elif int(temp_item) >= 300 and int(temp_item) <= 400 and "jsonl" in item:
        #    meta_list.append(item)
    meta_list = list(set(meta_list))
    #print(meta_list[0])
        
    visualizer = HTMLTableVisualizer('./html_visualizer', f'Ad-hoc Implicature, 20')
    with visualizer.html(), visualizer.table('You are in a reference game. The speaker can only use one word (i.e., one property) to refer to the object, and he/ she will be rewarded if you can successfully pick the only target referent object in the image. So now, please select your answer by referencing the corresponding numerical index.', [
        HTMLTableColumnDesc('text', 'Text', 'raw'),
        HTMLTableColumnDesc('text1', 'ID', 'raw'),
        HTMLTableColumnDesc('Image1', 'Image', 'image'),
        HTMLTableColumnDesc('Image2', 'Image with Detection Overlay', 'image'),
        HTMLTableColumnDesc('answer', 'Answer', 'raw'),
        #HTMLTableColumnDesc('type', 'Implicature Type', 'raw'),
    ]):
        for k, file_name in enumerate(meta_list): #os.listdir("./meta_data/"):
            #image1_filename = f'./images/CLEVR_00000{int(start_idx)}.png'
            #image2_filename = f'./SoMs/CLEVR_00000{int(start_idx)}.png'
            json_filename = f'./meta_data/{file_name}'
            #index = int(file_name.split("_")[1])
            print(file_name)
            #index = file_name.strip(".json").split("_")[-1]
            #if start_idx >= 10:
            #    #image1_filename = f'./images/CLEVR_0000{int(start_idx)}.png'
            #    #image2_filename = f'./SoMs/CLEVR_0000{int(start_idx)}.png'
            #    json_filename = f'./meta_120/{file_name}'
            #if start_idx >= 100:
            #    #image1_filename = f'./images/CLEVR_000{int(start_idx)}.png'
            #    #image2_filename = f'./SoMs/CLEVR_000{int(start_idx)}.png'
            #    json_filename = f'./meta_120/{file_name}'
            #if start_idx >= 1000:
            #    json_filename = f'./meta_120/{file_name}'

            with open(json_filename, "r") as f:
                data = json.load(f)
            #data = [json.loads(_) for _ in data]
            #print(data.keys())
            image_som = f'./SoMs/{file_name.rstrip(".json")}.png'
            image_src = f'./images/{file_name.rstrip(".json")}.png'
            
            
            utterance = data['utterance']
            
            #images = []
            #for item in data:
            #    if "image_filename" in item:
            #        image_filename = item['image_filename']
            #        images.append(os.path.join("./human_ad_hoc_understand/SoMs", image_filename))
            #    if "utterance" in item:
            #        utterance = item["utterance"]#.replace("novel ", "")
            #        impli_type = item["type"]
                    
                    #referent_obj_id = data['referent'][0]
            #with open(json_filename, 'r') as f:
            #    ans = json.load(f)
            #data = jacinle.load(json_filename)
            
            text = f'<b>Utterance:</b> {utterance}'

            #referent1 = images[0]
            for j, obj in enumerate(data['objects']):
                #
                obj_name = obj['size'] + " " + obj['color'] + " " + obj['material'] + " "+ obj['shape']
                if obj_name == data['referent']:
                    referent_idx = j
            print(data['referent'])

            #referent1_id = images.index(referent1)
            #referent2_id = images.index(referent2)
            #if referent1_id > referent2_id:
            #    referent1_id, referent2_id = referent2_id, referent1_id

            answer = f'<b>Referent:</b> {data["referent"]}<br><b>Referent Object ID: </b> {referent_idx + 1}'
            
            #text = f'<b>Utterance:</b> {text1}'
            #answer = f'<b>Referents:</b> Image {ans_ids[0]+1}, {ans_ids[1]+1}<br><b>Type:</b> {implicature_type}'
            #type_ = f'<b>Type:</b> {implicature_type}'
            #print(images, json_filename)

            visualizer.row(text1=str(k), Image1=image_src, Image2=image_som, text=text, answer=answer)


if __name__ == '__main__':
    main()
