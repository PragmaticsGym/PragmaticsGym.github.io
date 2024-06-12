import jacinle
import shutil
import argparse
from jaclearn.visualize.html_table import HTMLTableVisualizer, HTMLTableColumnDesc
import json
import random
import os
import re

# parser = argparse.ArgumentParser()
# parser.add_argument('--start_idx', default=0)
# parser.add_argument('--type', default="cancel_direct_implicature")
# args = parser.parse_args()

def main():
    implicature_type = "Direct Implicature"
    temp_files = os.listdir("./meta_data/")
    # process file_names
    impli_files = ['CLEVR_000000.json'] #zl']
    cancel_files = []
    for file in temp_files:
        
        if 'json' not in file:
            continue
        print(file)
        if 'CLEVR_000000.json' == file:
            continue
        if int(file.strip('.jsonl').split('_')[1]) < 100:#int(file.replace(re.search('CLEVR_0+', file).group(), "").replace(".jsonl", "")) < 400:
            impli_files.append(file)
        else:
            cancel_files.append(file)
    all_files = impli_files + cancel_files[:100]#random.sample(impli_files, 100) + random.sample(cancel_files, 100)
    random.shuffle(all_files)
        
    visualizer = HTMLTableVisualizer('./html_visualizer_all', f'Connective Implicature Visualization, CLEVR Domain, 200')
    with visualizer.html(), visualizer.table('In this reference game, the speaker will generate a statement to describe two images, and both the speaker and you will be rewarded if you can correctly identify both referent images. Please proceed by selecting your answers based on the corresponding numerical image index.', [
        HTMLTableColumnDesc('text', 'Text', 'raw'),
        HTMLTableColumnDesc('idx', 'Index', 'raw'),
        HTMLTableColumnDesc('image1', 'Image 1', 'image'),
        HTMLTableColumnDesc('image2', 'Image 2', 'image'),
        HTMLTableColumnDesc('image3', 'Image 3', 'image'),
        HTMLTableColumnDesc('image4', 'Image 4', 'image'),
        HTMLTableColumnDesc('image5', 'Image 5', 'image'),
        HTMLTableColumnDesc('answer', 'Answer', 'raw'),
        #HTMLTableColumnDesc('type', 'Implicature Type', 'raw'),
    ]):
        
        for k, file_name in enumerate(all_files):
            # process filenames
                
            
            #image1_filename = f'./images/CLEVR_00000{int(start_idx)}.png'
            #image2_filename = f'./SoMs/CLEVR_00000{int(start_idx)}.png'
            json_filename = f'./meta_data/{file_name}'
            #print(json_filename)
            #if ".jsonl" not in json_filename[:-10]:
            #    print(1)
            #    continue
            
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
                data = json.load(f)#list(f)
            #data = [json.loads(_) for _ in data]
            images = []
            utterance = ""
            impli_type = ""
            game_setup = 'In this reference game, the speaker will generate a statement to describe two images, and both the speaker and you will be rewarded if you can correctly identify both referent images. Please proceed by selecting your answers based on the corresponding numerical image index.'
            for item in data:
                if "image_filename" in item:
                    image_filename = item['image_filename']

                    images.append(os.path.join("./SoMs", image_filename))
                if "utterance" in item:
                    utterance = " shows ".join(item["utterance"].split("shows"))
                    impli_type = item["type"]
                    
            #if not os.path.exists('./updated_SoMs/'):
            #    os.mkdir('./updated_SoMs/')
            #if not os.path.exists('./updated_meta_data/'):
            #    os.mkdir('./updated_meta_data/')
            #for image in images:
            #    shutil.copy(image, os.path.join('./updated_SoMs/', image.split('/')[-1]))
            #shutil.copy(json_filename, os.path.join('./updated_meta_data/', json_filename.split('/')[-1]))
            #with open(json_filename, 'r') as f:
            #    ans = json.load(f)
            #data = jacinle.load(json_filename)
            utterance = utterance#.replace("It contains", "There are").replace("The image shows", "There are").replace("The image  shows", "There are").replace(" in the images", "").replace(".", "")+" in the images."
            
            
            text = f'<b>Game:</b> {game_setup}<br><b>Speaker:</b> {utterance}'

            referent1, referent2 = images[0], images[1]
            random.shuffle(images)
            referent1_id = images.index(referent1)
            referent2_id = images.index(referent2)
            if referent1_id > referent2_id:
                referent1_id, referent2_id = referent2_id, referent1_id
            
            answer = f'<b>Referent Image ID:</b> {referent1_id+1}, {referent2_id+1}'
            
            #text = f'<b>Utterance:</b> {text1}'
            answer = f'<b>Referents:</b> Image {referent1_id+1}, {referent2_id+1}<br><b>Type:</b> {impli_type}'
            #type_ = f'<b>Type:</b> {implicature_type}'

            visualizer.row(idx=k+1, image1=images[0], image2=images[1], image3=images[2], image4=images[3], image5=images[4], text=text, answer=answer)


if __name__ == '__main__':
    main()
