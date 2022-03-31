from jinja2 import Environment
from jinja2 import FileSystemLoader
import os
import json
import pandas as pd

aci_csv_df = pd.read_csv("data_aci.csv")
aci_attr = aci_csv_df.to_dict('records')

def save_file(file_name, data):
    print(f"***** working on file: {file_name}")
    save_dir_name = "ACI_JSON"
    if not os.path.exists(save_dir_name):
        os.makedirs(save_dir_name)
    with open(f"{save_dir_name}/{file_name}", 'w') as file:
        data_rep = data.replace("'", '"')
        try:
            data_rep = data_rep[data_rep.index("{"):]
            item_count = json.loads(data_rep)
            print(f' {file_name} ---> {len(item_count["resource"])} items to deploy ...\n')
        except ValueError:
            print(f"Empty Data on {file_name} ... \n")
        finally:
            file.write(data_rep)
    print("-"*50)


def temp_generator(jinja_file):
    try:
        jinja_template = JINJA2_TEMPLATES.get_template(jinja_file)
        payload_aci = jinja_template.render(aci_attr=aci_attr)
        save_file(f"{jinja_file.split('.')[0]}.json", payload_aci)
    except exceptions.TemplateNotFound:
        print(f"Check for the file: {jinja_file}")


if __name__ == "__main__":
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    JINJA2_TEMPLATES = Environment(loader=FileSystemLoader(DIR_PATH + '/ACI_Service'))

    bd = "bd.jinja2"
    bind_int_epg = "bind_int_epg.jinja2"
    bind_sel = "bind_sel.jinja2"
    dom_epg = "dom_epg.jinja2"
    encap = "encap.jinja2"
    epg = "epg.jinja2"
    vpc_bind = "vpc_bind.jinja2"
    vpc_ipg = "vpc_ipg.jinja2"
    vpc_sel = "vpc_sel.jinja2"
    descr = "descr.jinja2"

    # ___________________________ bd _________________________________
    temp_generator(bd)
    # ___________________________ bind_int_epg _________________________________
    temp_generator(bind_int_epg)
    # ___________________________ bind_sel _________________________________
    temp_generator(bind_sel)
    # ___________________________ dom_epg _________________________________
    temp_generator(dom_epg)
    # ___________________________ encap _________________________________
    temp_generator(encap)
    # ___________________________ epg _________________________________
    temp_generator(epg)
    # ___________________________ vpc_bind _________________________________
    temp_generator(vpc_bind)
    # ___________________________ vpc_ipg _________________________________
    temp_generator(vpc_ipg)
    # ___________________________ vpc_sel _________________________________.
    temp_generator(vpc_sel)
    # ___________________________ descr _________________________________.
    temp_generator(descr)

