"""
Basic example of a Mkdocs-macros module
"""

import math
import yaml
import os

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

    @env.macro
    def get_prediction_containers():
        data = []
        d = env.project_dir+"/docs/containers/prediction"
        for f in os.listdir(d):
            if f.endswith(".md"):
                y = get_front_matter(f"{d}/{f}")
                page_name = f.split("/")[-1].replace(".md","")
                y['url'] = f"[{y['title']}](/containers/prediction/{page_name})"
                y['drugs'] = ", ".join(y['drugs'])
                data.append(y)
        return data

    @env.macro
    def get_preprocessing_containers():
        data = []
        d = env.project_dir+"/docs/containers/preprocessing"
        for f in os.listdir(d):
            if f.endswith(".md"):
                y = get_front_matter(f"{d}/{f}")
                page_name = f.split("/")[-1].replace(".md","")
                y['url'] = f"[{y['title']}](/containers/preprocessing/{page_name})"
                data.append(y)
        return data

    @env.macro
    def get_front_matter(f):
        page_text = [x for x in open(f).readlines()]
        bounds = [i for i in range(len(page_text)) if page_text[i].strip()=="---"]
        data = yaml.safe_load("\n".join(page_text[bounds[0]+1:bounds[1]]))
        return data