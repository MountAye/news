import pandas as pd
import yaml
from pathlib import Path
from batch_apply import batch_apply

def translate(path_old, path_new):
    with open(str(path_old),'rb') as yml:
        old = yaml.load(yml,Loader=yaml.BaseLoader)
    new = {}
    new['title']    = old['title']
    new['abstract'] = old['abstract'] if 'abstract' in old.keys() else None
    new['sections'] = []
    for old_section in old['sections']:
        new_section = {}
        new_section['subtitle'] = old_section['subtitle']
        if 'abstract' in old_section.keys():
            new_section['abstract'] =  old_section['abstract']
        new_section['entries'] = []
        for subsection in old_section['subsections']:
            new_entry = {}
            new_entry['paragraph'] = subsection['subsubtitle']
            if 'abstract' in subsection.keys():
                new_entry['paragraph'] = new_entry['paragraph'] + ' | ' + subsection['abstract'] 
            new_entry['multimedia'] = []
            new_entry['reports']    = []
            new_entry['opinions']   = []
            for old_entry in subsection['entries']:
                if 'media' in old_entry.keys():
                    for old_media in old_entry['media']:
                        new_media = {}
                        new_media['alt']  = old_media['text']
                        new_media['link'] = old_media['link']
                        if 'backup' in old_media.keys():
                            new_media['backup'] = old_media['backup']
                        new_entry['multimedia'].append(new_media)
                if 'hearfrom' in old_entry.keys():
                    for old_hearfrom in old_entry['hearfrom']:
                        if not 'link' in old_hearfrom.keys():
                            continue
                        new_hearfrom = {}
                        new_hearfrom['author'] = old_hearfrom['text']
                        new_hearfrom['main'] = "新闻报道"
                        new_hearfrom['link'] = old_hearfrom['link']
                        if 'backup' in old_hearfrom.keys():
                            new_hearfrom['backup'] = old_hearfrom['backup']
                        new_entry['reports'].append(new_hearfrom)
                if 'facts' in old_entry.keys():
                    new_fact = {}
                    new_fact['main'] = "新闻报道"
                    if 'author' in old_entry.keys():
                        new_fact['author'] = old_entry['author']
                    if 'published' in old_entry.keys():
                        new_fact['date'] = old_entry['published']
                    if 'link' in old_entry.keys():
                        new_fact['link'] = old_entry['link']
                    if 'backup' in old_entry.keys():
                        new_fact['backup'] = old_entry['backup']
                    new_fact['details'] = []
                    for detail in old_entry['facts']:
                        new_fact['details'].append(detail['text'])
                    new_entry['reports'].append(new_fact)                
                if 'opinions' in old_entry.keys():
                    new_opinion = {}
                    new_opinion['main'] = "新闻评论"
                    if 'author' in old_entry.keys():
                        new_opinion['author'] = old_entry['author']
                    if 'published' in old_entry.keys():
                        new_opinion['date'] = old_entry['published']
                    if 'link' in old_entry.keys():
                        new_opinion['link'] = old_entry['link']
                    if 'backup' in old_entry.keys():
                        new_opinion['backup'] = old_entry['backup']
                    new_opinion['details'] = []
                    for detail in old_entry['opinions']:
                        new_opinion['details'].append(detail['text'])
                    new_entry['opinions'].append(new_opinion)             
            new_section['entries'].append(new_entry)
        new['sections'].append(new_section)

    yaml.dump(
        new,
        open(str(path_new),'w'),
        encoding='UTF-8', allow_unicode=True,
        sort_keys=False
    )


files = list(Path("data/").glob("*/*.yml"))
args = pd.DataFrame({
    'path_old': files,
    'path_new': [f.name for f in files]
})

batch_apply(translate,args)