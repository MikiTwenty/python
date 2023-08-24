### imgdt
### v0.0.2
### MikiTwenty

import os
from pathlib import Path
from .tools import History, Transformer
from .utils import log, stdoformat

def run(dataset_folder, target_folder='', history_file='', dataset_name='', scaling_size=1080, remove_originals=False):
    dataset_folder = Path(dataset_folder)
    log(f"Dataset folder path     : \"{dataset_folder}\"", stdoformat.INFO)
    if dataset_name != '':
        log(f"Dataset name            : \'{dataset_name.lower()}\'", stdoformat.INFO)
        dataset_name = dataset_name.lower()+'_'

    if history_file == '':
        history_file = os.path.join(dataset_folder.parent.absolute(), f"{dataset_name.replace('_', '.')}history")
        if os.path.exists(history_file):
            log(f"History file path       : \"{history_file}\"", stdoformat.INFO)
        else:
            log(f"History file path       : -", stdoformat.INFO)
    else:
        log(f"History file path       : \"{history_file}\"", stdoformat.INFO)

    if target_folder == '' or not os.path.isdir(target_folder):
        target_folder = os.path.join(dataset_folder.parent.absolute(), f"{dataset_name.replace('_', '.')}processed")
        if os.path.isdir(target_folder):
            log(f"Target folder path      : \"{target_folder}\"", stdoformat.INFO)
        else:
            log(f"Target folder path      : -", stdoformat.INFO)
    else:
        log(f"Target folder path      : \"{target_folder}\"", stdoformat.INFO)
    log(f"Scaling size            : {scaling_size}px", stdoformat.INFO)
    log(f"Remove original images  : {remove_originals}", stdoformat.INFO)

    if not os.path.exists(history_file):
        log(f"Generating new history...", stdoformat.TEXT)
        stored_new_labels = set()
        with open(history_file, 'w') as f:
            pass
        log(f"History generated at \"{history_file}\"", stdoformat.SUCCESS)

    if not os.path.isdir(target_folder):
        log(f"Generating target folder...", stdoformat.TEXT)
        os.mkdir(target_folder)
        log(f"Target folder generated at \"{target_folder}\"", stdoformat.SUCCESS)

    transformer = Transformer(dataset_folder, target_folder, scaling_size)

    history = History(history_file)

    old_labels, new_labels = transformer.get_labels()

    stored_new_labels = history.read(old_labels, new_labels)

    old_labels, new_labels = transformer.convert(old_labels, dataset_name.replace('.', '_'), remove_originals, stored_new_labels)

    history.update(old_labels, new_labels)

    old_labels, new_labels = transformer.get_labels()

    transformer.scale(new_labels)

    transformer.crop(new_labels)

    print(f"{stdoformat.TEXT}")