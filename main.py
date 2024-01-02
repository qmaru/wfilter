import argparse
import glob
import json
import os
from datetime import datetime
from typing import Dict, List


def get_basic_info(file: str) -> List[Dict[str, str]]:
    x_info: List[Dict[str, str]] = []
    with open(file, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        links = data["links"]
        for link in links:
            if link.get("otherPropertiesMap"):
                otherPropertiesMap = link["otherPropertiesMap"]
                is_retweet = otherPropertiesMap["is_retweet"]
                is_reply_tweet = otherPropertiesMap["is_reply_tweet"]
                is_quoted_tweet = otherPropertiesMap["is_quoted_tweet"]
                if is_retweet == is_reply_tweet == is_quoted_tweet:
                    status_id = otherPropertiesMap["status_id"]
                    full_url = otherPropertiesMap["full_url"]
                    created_at = otherPropertiesMap["created_at"]
                    dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                    output_date = dt.strftime("%Y%m%d%H%M%S")
                    x_info.append(
                        {"date": output_date, "url": full_url, "id": status_id}
                    )
            else:
                print("file data error")
                exit()
    return x_info


def rename_files(save_folder: str, basic_info: List[Dict[str, str]]):
    files = glob.glob(f"{save_folder}/*")
    for file in files:
        dir_path, file_path = os.path.split(file)
        base_name, ext = os.path.splitext(file_path)
        s_id = base_name.split("_")[0]
        for info in basic_info:
            if s_id == info["id"]:
                date = info["date"]
                new_name = f"{date}_{base_name}{ext}"
                new_path = os.path.join(dir_path, new_name)
                try:
                    os.rename(file, new_path)
                except BaseException as e:
                    print(file, new_path, e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="basic_file", help="WFDownloader Export JSON")
    parser.add_argument("-i", dest="image_folder", help="X Media Folder")
    args = parser.parse_args()

    basic_file = args.basic_file
    image_folder = args.image_folder

    if basic_file and image_folder is None:
        basic_info = get_basic_info(basic_file)
        for info in basic_info:
            print(info["url"])
    elif basic_file and image_folder:
        basic_info = get_basic_info(basic_file)
        rename_files(image_folder, basic_info)


if __name__ == "__main__":
    main()
