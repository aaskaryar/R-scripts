import pandas as pd
from sqlalchemy import create_engine

eng = create_engine('postgresql://readonly:3535Harbor@geodbinstance.cottkh4djef2.us-west-2.rds.amazonaws.com/empa2021')

SYSTEM_FIELD = [
        "objectid",
        "original_objectid",
        "globalid",
        "created_date",
        "created_user",
        "last_edited_date",
        "last_edited_user",
        "submissionid",
        "warnings",
        "login_email",
        "gdb_geomattr_data",
        "shape",
        "login_agency",
        "login_siteid",
        "login_data_entry_year",
        "login_protocol_version",
        "login_sensortype",
        "login_stationno",
        "login_protocol_name",
        "login_notes",
        "login_data_entry_day",
        "login_sensorid",
        "login_contact_email_address",
        "login_data_entry_month",
        "login_contact_person",
        "login_projectid",
        "login_estuaryname",
        "login_filetype",
        "login_phone_number",
        "login_start",
        "login_project",
        "login_end",
        "samplecollectiontimestamp_utc",
        "raw_depth_qcflag_robot",
        "raw_pressure_qcflag_robot",
        "raw_h2otemp_qcflag_robot",
        "raw_ph_qcflag_robot",
        "raw_conductivity_qcflag_robot",
        "raw_turbidity_qcflag_robot",
        "raw_do_qcflag_robot",
        "raw_do_pct_qcflag_robot",
        "raw_salinity_qcflag_robot",
        "raw_chlorophyll_qcflag_robot",
        "raw_orp_qcflag_robot",
        "raw_qvalue_qcflag_robot",
        "qaqc_comment"
    ]


dtypes = {
    'discretewq': ["tbl_protocol_metadata","tbl_waterquality_metadata","tbl_waterquality_data"]
}

with pd.ExcelWriter('discretewq_clean.xlsx') as writer:
    for datatype in dtypes.keys():
        for tbl in dtypes[datatype]:
            if tbl == 'tbl_protocol_metadata':
                df = pd.read_sql(f'SELECT * FROM {tbl}', eng)
                df[[col for col in df.columns if col not in SYSTEM_FIELD]].to_excel(writer, sheet_name=tbl, index=False)
            else:
                estuaryname = pd.read_sql(f"SELECT DISTINCT estuaryname FROM {tbl} LIMIT 1", eng).iloc[0,0]
                df = pd.read_sql(f"SELECT * FROM {tbl} WHERE estuaryname = '{estuaryname}'", eng)
                for col in df.columns:
                    if 'date' in col:
                        df[col] = pd.Timestamp('1950-01-01 00:00:00')
                df[[col for col in df.columns if col not in SYSTEM_FIELD]].to_excel(writer, sheet_name=tbl, index=False)


