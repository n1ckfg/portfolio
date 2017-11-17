#!/usr/bin/env python3

import os, sys, yaml, markdown, shutil, jinja2, re, subprocess, time, datetime, json
from PIL import Image

def process_images():
    try:
        subprocess.check_call("exiftool -all= images/*", shell=True)      # security / helps opengraph
    except Exception as e:
        print(e)
        exit()
    try:
        subprocess.check_call("rm images/*_original &> /dev/null", shell=True)        
    except Exception:
        pass
    images = {}
    for filename in os.listdir("images"):
        if ".jpg" not in filename:
            continue
        slug = filename.split(".")[0].replace("@2x", "")
        tag = slug.split("_")[-1]
        try:
            int(tag)
            slug = slug[:-(len(tag) + 1)]
        except ValueError:
            pass
        if slug not in images:
            images[slug] = []
        if "@2x" in filename:
            images[slug][-1][1] = filename
        else:
            images[slug].append([filename, None])
    # print(json.dumps(images, indent=4))
    return images
images = process_images()

def build(structure, root):
    if structure is not None:
        pages = structure.keys() if type(structure) is dict else structure
        for page in pages:
            path = os.path.abspath(os.path.join(root, page))
            if not os.path.isdir(path):
                os.mkdir(path)
            content = os.path.abspath("content/%s.yaml" % page.split('.')[0])
            if type(structure) is dict:
                template = "templates/%s.html" % page
            else:
                template = "templates/%s.html" % root.split("/")[-1][:-1]
            html_path = os.path.join(path, "index.html")      
            print("PAGE: %s" % page)
            data = {'page': page, 'path': path}
            if os.path.isfile(content):
                with open(content) as f:
                    data.update(yaml.load(f))
                if 'text' in data:
                    data['text'] = markdown.markdown(data['text'].strip())   
            update = False
            work_images = []
            if page in images:
                for (image, hires) in images[page]:
                    image_source_path = os.path.abspath(os.path.join("images", image))
                    image_destination_path = os.path.join(path, image_source_path.split("/")[-1])                    
                    if not os.path.isfile(image_destination_path) or os.path.getmtime(image_source_path) > os.path.getmtime(image_destination_path):
                        shutil.copy(image_source_path, path)                    
                        print("\t--> copying %s..." % image)
                        update = True
                    if hires is not None:
                        hires_source_path = os.path.abspath(os.path.join("images", hires))
                        hires_destination_path = os.path.join(path, hires_source_path.split("/")[-1])                    
                        if not os.path.isfile(hires_destination_path) or os.path.getmtime(hires_source_path) > os.path.getmtime(hires_destination_path):
                            shutil.copy(hires_source_path, path)                    
                            print("\t--> copying %s hires..." % hires)                        
                            update = True
                    width, height = Image.open(image_source_path).size                        
                    work_images.append((image, width, height, hires))
            data.update({'images': work_images, 'image_structure': images})
            if os.path.isfile(template) and os.path.isfile(content) and (not os.path.isfile(html_path) or (os.path.getmtime(template) > os.path.getmtime(html_path)) or (os.path.getmtime(content) > os.path.getmtime(html_path))):           
                print("\t--> updating content: %s\twith template: %s" % (content, template))                
                update = True
            elif os.path.isfile(template) and (not os.path.isfile(html_path) or (os.path.getmtime(template) > os.path.getmtime(html_path))):           
                print("\t--> updating template: %s" % template)
                update = True
            if update:
                html = render(template, data, structure=(structure[page] if type(structure) is dict else None))
                with open(html_path, 'w') as f:
                    f.write(html)
            if type(structure) is dict:           
                build(structure[page], path)

def render(template_name, template_values=None, **kwargs):
    if type(template_values) == dict:
        template_values.update(kwargs)
    else:
        template_values = kwargs
    renderer = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    renderer.filters.update({'slugify': slugify, 'unslugify': unslugify, 'strip_html': strip_html, 'strip_quotes': strip_quotes, 'strslice': strslice})
    output = renderer.get_template(template_name).render(template_values)
    return output

def slugify(value):
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[\s]+', '_', value)

def unslugify(s):
    s = s.replace('_', ' ')
    s = re.sub("([a-z])'([A-Z])", lambda m: m.group(0).lower(), s.title()).split()
    s = ' '.join([(s.lower() if s.lower() in ['for', 'in', 'to', 'a', 'of', 'the', 'or'] and i != 0 else s) for (i, s) in enumerate(s)])
    return s

def strip_html(s, keep_links=False):
    if keep_links:
        s = re.sub(r'</[^aA].*?>', '', s) 
        s = re.sub(r'<[^/aA].*?>', '', s)        
        return s
    else:    
        return re.sub(r'<.*?>', '', s)    

def strip_quotes(s):
    return s.replace('"', '')    

def strslice(s, length):
    if not type(s) == str:
        s = str(s)
    return s[:length]        

def copy_static():
    for filename in os.listdir("."):
        if filename[-3:] == "css":
            shutil.copy(filename, "www/")
        elif filename == ".htaccess":
            shutil.copy(filename, "www/")
    for filename in os.listdir("js"):
        if filename[-2:] == "js":
            shutil.copy(os.path.join("js", filename), "www/")
    for filename in os.listdir("img"):
        if filename[-3:] == "png":
            shutil.copy(os.path.join("img", filename), "www/")

if __name__ == "__main__":
    with open("structure.yaml") as f:
        structure = yaml.load(f)
    build(structure, ".")
    copy_static()
    shutil.copy("www/works/index.html", "www/index.html")       # this should be a rewrite rule

