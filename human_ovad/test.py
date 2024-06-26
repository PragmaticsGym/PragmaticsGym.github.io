import jacinle
import shutil
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
    implicature_type = "Direct Implicature"
    #indx_list = [4, 11, 17, 23, 26, 28, 31, 32, 50, 89, 91, 92, 102, 105, 107, 110, 135, 137, 149, 153, 158, 159, 161, 183, 204, 205, 209, 217, 218, 221, 225, 233, 234, 237, 238,254, 262, 270, 284,291, 293, 296, 299, 275, 48, 163, 172, 193]
    json_list = []
    #indx_list = [3, 17, 18, 30, 34, 38, 47,  50, 70, 75, 76, 79, 93, 97, 101, 107, 119, 131, 137, 141, 145, 168, 230, 240, 245, 310, 335, 344, 369, 371, 373, 399, 405, 412, 467]
    #for i, json_ind in enumerate(json_list):
    #    json_list[i] = 'MSCOCO_%%0%dd.jsonl' % 6 % (json_ind-1)
    #    print(json_list[i])
    count = 0
    visualizer = HTMLTableVisualizer('./html_visualizer', f'Connective Implicature Visualization, Natural Domain, 100')
    with visualizer.html(), visualizer.table('In this reference game, the speaker will generate a statement to describe two images, and both the speaker and you will be rewarded if you can correctly identify both referent images. Please proceed by selecting your answers based on the corresponding numerical image index.', [
        HTMLTableColumnDesc('text', 'Text', 'raw'),
        HTMLTableColumnDesc('idx', 'Idx', 'raw'),
        HTMLTableColumnDesc('image1', 'Image 1', 'image'),
        HTMLTableColumnDesc('image2', 'Image 2', 'image'),
        HTMLTableColumnDesc('image3', 'Image 3', 'image'),
        HTMLTableColumnDesc('image4', 'Image 4', 'image'),
        HTMLTableColumnDesc('image5', 'Image 5', 'image'),
        HTMLTableColumnDesc('answer', 'Answer', 'raw'),
        #HTMLTableColumnDesc('type', 'Implicature Type', 'raw'),
    ]):
        for k, file_name in enumerate(os.listdir("./meta_data/")):
            #if k+1 not in indx_list:
            #    continue #json_list.append(f"{file_name}")
            #if not os.path.exists("./good_meta_data"):
            #    os.mkdir("./good_meta_data")
            #if not os.path.exists("./good_images"):
            #    os.mkdir("./good_images")
            #else:
            #    continue
            #image1_filename = f'./images/CLEVR_00000{int(start_idx)}.png'
            #image2_filename = f'./SoMs/CLEVR_00000{int(start_idx)}.png'
            json_filename = f'./meta_data/{file_name}'
            #shutil.copy(json_filename, f'./good_meta_data/%03d.jsonl' % count)
            #if file_name not in json_list:
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
                data = list(f)
            data = [json.loads(_) for _ in data]
            game_type = data[0]['type']

            images = []
            utterance = ""
            game_setup = 'In this reference game, the speaker will generate a statement to describe two images, and both the speaker and you will be rewarded if you can correctly identify both referent images. Please proceed by selecting your answers based on the corresponding numerical image index.'
            for item in data:
                if "image" in item:
                    image_filename = item['image']
                    images.append(os.path.join("./images", image_filename.split("/")[-1]))
                    #shutil.copy(os.path.join("./images_new", image_filename.split("/")[-1]), os.path.join("./good_images", image_filename.split("/")[-1]))

                if "utterance" in item:
                    if "persons" in item['utterance']:
                        utterance = item['utterance'].replace("persons", "people").replace("skiss", "skis")
                    else:
                        utterance = item['utterance']
                    #utterance = " shows ".join(item["utterance"].split("shows"))

            
            #for image in images:
            #    shutil.copy(image, os.path.join('./updated_images/', image.split('/')[-1]))
            #shutil.copy(json_filename, os.path.join('./updated_meta_data/', json_filename.split('/')[-1]))
            #with open(json_filename, 'r') as f:
            #    ans = json.load(f)
            #data = jacinle.load(json_filename)
            
            
            text = f'<b>Game:</b> {game_setup}<br><b>Speaker:</b> {utterance}'

            referent1, referent2 = images[0], images[1]
            random.shuffle(images)
            referent1_id = images.index(referent1)
            referent2_id = images.index(referent2)
            if referent1_id > referent2_id:
                referent1_id, referent2_id = referent2_id, referent1_id
            
            answer = f'<b>Referent Image ID:</b> {referent1_id+1}, {referent2_id+1}'
            
            #text = f'<b>Utterance:</b> {text1}'
            answer = f'<b>Referents:</b> Image {referent1_id+1}, {referent2_id+1}<br><b>Type:</b> {game_type}'
            #type_ = f'<b>Type:</b> {implicature_type}'
            count += 1

            visualizer.row(idx=k+1, image1=images[0], image2=images[1], image3=images[2], image4=images[3], image5=images[4], text=text, answer=answer)


if __name__ == '__main__':
    main()
