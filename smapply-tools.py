from util import get_smapply_instance
import logging
import traceback
from datetime import datetime
import sys
import json
import pandas as pd
import numpy as np
import textwrap

smapply = get_smapply_instance()
DEFAULT_PROGRAM_ID = smapply.default_program_id   
apps=[]

def concat_labels(li):
    s=""
    for l in li:
        if s :
            s+=" "
        s+=l['name'].replace("Track:","")
    return s

def get_application(**kwargs):
    kwargs =  {k.lower(): v for k, v in kwargs.items()}
    
    id = kwargs['id']

    logging.debug(f"Looking up app id {id}")

    global smapply
    
    app = smapply.call_api(f"applications/{id}/tasks/1609224",
                            method="GET", all_pages=False)

    df = pd.DataFrame(app["data"])

    for d in df:
        print("{}\n{}".format(df[d]['label'], 
            textwrap.indent(
                textwrap.fill(
                    str(df[d]['response']).replace("\r\n","\n").replace("\n\n","\n")
                    ,
                    width=70 
                )
            ,
            '    ' 
            )
        ))

    # csv_filename="output/"+"detail-application-"+id+datetime.now().strftime('-%Y%m%d-%H%M%S.csv')
    # df.to_csv(csv_filename)        

def list_applications(**kwargs):
    kwargs =  {k.lower(): v for k, v in kwargs.items()}

    global smapply
    logging.debug(f"Listing applications")
    
    applications = smapply.call_api(f"applications",
                            method="GET")

    df = pd.DataFrame(applications)

    csv_filename="output/"+datetime.now().strftime('list-applications-%Y%m%d-%H%M%S.csv')
    df.to_csv(csv_filename)        

    df_result = (
        df
        [df.current_stage.apply(lambda x: x["title"]=="KCD Review")]
        .rename(columns={"id": "application_id"})
        .assign(
            applicant_id=df.applicant.map(lambda x:x.get("id")),
            first_name=df.applicant.map(lambda x:x.get("first_name")),
            last_name=df.applicant.map(lambda x:x.get("last_name")),
            email=df.applicant.map(lambda x:x.get("email")),
            track=df.labels.map(lambda x: concat_labels(x))
        )
        .drop(columns="applicant")
        .drop(columns="current_stage")
        .drop(columns="collaborators")
        .drop(columns="custom_fields")
        .drop(columns="decision")
        .drop(columns="labels")
        .drop(columns="organization")
        .drop(columns="program")
        .drop(columns="state")
        .drop(columns="status")
        .drop(columns="created_at")
        .drop(columns="updated_at")
        .drop(columns="last_submitted_at")
        .drop(columns="average_score")
        .drop(columns="notes")
        .drop(columns="overall_score")
        .drop(columns="weighted_score")
        .drop(columns="title")
        .reset_index(drop=True)
    )

    purged_csv_filename="output/"+datetime.now().strftime('purged-list-applications-%Y%m%d-%H%M%S.csv')
    df_result.to_csv(purged_csv_filename)        

    print(df_result.to_string(index=False,header=False))

if __name__ == "__main__":
    try: 
        if len(sys.argv) > 1:
            if sys.argv[1] == "list":
                logging.debug("list")
                list_applications()
            elif sys.argv[1] == "get":
                logging.debug("get")
                if len(sys.argv) > 2:
                    row={"id": sys.argv[2]}
                    logging.debug(f"look for app id {sys.argv[2]}")
                    get_application(**row)
                else:
                    logging.error("need to specify an application id")
            else:
                logging.error("unknown command")
        else:
            logging.error("need to specify a command")

        exit()

    except KeyError as e:
        logging.error("Missing input value: {}".format(e))
    except Exception as e:
        traceback.print_exc()
        logging.error("Unexpected error occured: {}:{}".format(type(e).__name__, e))

