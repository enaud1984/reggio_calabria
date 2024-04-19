start_request_validator_responses = {
    201: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Normal": {"value": {
                                  "esito": "Processo di ESEGUI_TUTTO_CON_REPORT RUNNING",
                                  "validator_request": {
                                    "Request": {
                                      "ID": "1",
                                      "SHAPEFILE": "Shape_flat.zip",
                                      "STATO": "uploaded",
                                      "STATUS": "RUNNING",
                                      "USER_ID": "giu",
                                      "GROUP_ID": "tim",
                                      "DATA_CARICAMENTO": "2024-02-21 09:39:38.940966",
                                      "DATA_ELABORAZIONE": None,
                                      "DATA_VALIDAZIONE": None,
                                      "PATH_SHAPEFILE": "to_upload/Shape_flat20240221_0939/Shape_flat",
                                      "MD5": "da3a0981a7cfe5fb25ffc921823568ce",
                                      "HOST_WORKER": "test",
                                      "RUNNING": None,
                                      "QUEUED": None,
                                      "ESITO": None,
                                      "STACK_TRACE_JAVA": None,
                                      "RESULTS": None,
                                      "USERFILE": None,
                                      "SINFI_PLUS": None
                                    }
                                  }
                                }
                   },
                   "Queued": {"value": {
                              "esito": "Processo di ESEGUI_TUTTO_CON_REPORT RUNNING",
                              "validator_request": {
                                "Request": {
                                  "ID": "2",
                                  "SHAPEFILE": "Shape_flat.zip",
                                  "STATO": "uploaded",
                                  "STATUS": "QUEUED",
                                  "USER_ID": "giu",
                                  "GROUP_ID": "tim",
                                  "DATA_CARICAMENTO": "2024-02-15 14:24:29.873938",
                                  "PATH_SHAPEFILE": "to_upload/Shape_flat20240215_1424/Shape_flat",
                                  "MD5": "da3a0981a7cfe5fb25ffc921823568ce",
                                  "HOST_WORKER": "test",
                                  "RUNNING": None,
                                  "QUEUED": None,
                                  "ESITO": None,
                                  "STACK_TRACE_JAVA": None,
                                  "RESULTS": None,
                                  "USERFILE": None,
                                  "DATA_ELABORAZIONE": None
                                }
                              }
                            }
                },
            }
        },}
    },
    501 : {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {
                        "error": "[WinError 1225] Il computer remoto ha rifiutato la connessione di rete",
                      "group_id": "tim",
                      "path": None
                }
            }
        },
    }
}
get_request_director_response = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                "RequestValidatorSinfi": {
                  "DATA_VALIDAZIONE": None,
                  "DATE_UPDATE": None,
                  "SINFI_PLUS": {
                    "message": "Processo completato",
                    "title": "ESEGUI_TUTTO_CON_REPORT",
                    "messageType": 9,
                    "process_detail":[
                          "Processo di Importazione: ENDED",
                          "Processo di Normalizzazione: ENDED",
                          "Controllo Vincoli strutturali: ENDED",
                          "Controllo Vincoli GeoUML: ENDED",
                          "Durata validazione: PT17.051S",
                          "Esportazione: ENDED",
                          "Generazione Report DB DERBY_TYPE: to_upload\\Shape_flat20240224_1126\\report",
                          "Generazione Report DB POSTGIS_TYPE: to_upload\\Shape_flat20240224_1126\\report",
                          "Processo di validazione terminato in PT23.157S"
                    ],
                    "validation_detail": {
                      "attributestructure": 43,
                      "structuralconstraintviolationsin": 5,
                      "parameterstep": 2,
                      "elementstatedbf": 39,
                      "geoumlconstraintnotverified": 58,
                      "elementstatedbn": 33,
                      "geometryerrorsin": 1,
                      "fkconstraintviolation": 15,
                      "geometricconstraintviolation": 60,
                      "elementstate": 37,
                      "fkconstraintviolationsin": 4,
                      "processstep": 4,
                      "geometryerror": 1,
                      "structuralconstraintviolation": 352
                    },
                    "report_sinfi": [
                      {
                        "checks": [
                          {
                            "role": "elementstate",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbn",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbf",
                            "count": 1
                          }
                        ],
                        "sfphystructname": "ab_cda"
                      },
                      {
                        "checks": [
                          {
                            "role": "elementstatedbf",
                            "count": 1
                          },
                          {
                            "role": "elementstate",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbn",
                            "count": 1
                          }
                        ],
                        "sfphystructname": "ac_ped"
                      },
                      {
                        "checks": [
                          {
                            "role": "elementstate",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbf",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbn",
                            "count": 1
                          }
                        ],
                        "sfphystructname": "ac_ped_ac_ped_sup_sr"
                      },
                      {
                        "checks": [
                          {
                            "role": "elementstatedbf",
                            "count": 1
                          },
                          {
                            "role": "elementstate",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbn",
                            "count": 1
                          }
                        ],
                        "sfphystructname": "ac_vei"
                      },
                      {
                        "checks": [
                          {
                            "role": "geometricconstraintviolation",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbn",
                            "count": 1
                          },
                          {
                            "role": "elementstate",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbf",
                            "count": 1
                          },
                          {
                            "role": "attributestructure",
                            "count": 5
                          }
                        ],
                        "sfphystructname": "ac_vei_ac_vei_sup_sr"
                      },
                      {
                        "checks": [
                          {
                            "role": "geometricconstraintviolation",
                            "count": 4
                          },
                          {
                            "role": "elementstatedbn",
                            "count": 1
                          },
                          {
                            "role": "elementstatedbf",
                            "count": 1
                          },
                          {
                            "role": "elementstate",
                            "count": 1
                          }
                        ],
                        "sfphystructname": "acc_pc"
                      },
                  
                    ],
                    "report_sinfiplus": [
                      {
                        "id": 1,
                        "date_execution": "2024-02-20T16:17:37",
                        "countnotinconstruction": [
                          252
                        ],
                        "errors": ""
                      }
                    ],
                    "validation_id": 32,
                    "local_validation_id": 1
                  },
                  "ID": 32,
                  "USER_ID": "imir",
                  "RUNNING": None,
                  "SHAPEFILE": "Shape_flat.zip",
                  "GROUP_ID": "tre",
                  "QUEUED": None,
                  "STATO": "uploaded",
                  "PATH_SHAPEFILE": "",
                  "ESITO": None,
                  "STATUS": "RUNNING",
                  "MD5": "da3a0981a7cfe5fb25ffc921823568ce",
                  "RESULTS": None,
                  "DATA_CARICAMENTO": "2024-02-20T16:17:15.815592",
                  "USERFILE": None,
                  "DBCONNECTION_STRING": None,
                  "DATA_ELABORAZIONE": "2024-02-20T16:17:37.983746",
                  "LOAD_TYPE": "strict",
                  "STACK_TRACE_JAVA": None,
                  "HOST_WORKER": "test"
                }
              }
          }
      },
    },
    501 : {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {"error": "Error","group_id":"group_id","id":"id"}
            }
        },
    }
}


get_all_requests_responses={
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "filter group_id='tim'": {"value":[
                              {
                                "ID": 1,
                                "SHAPEFILE": "Shape_flat.zip",
                                "GROUP_ID": "tim",
                                "QUEUED": None,
                                "STATO": "uploaded",
                                "PATH_SHAPEFILE": "to_upload\\Shape_flat20240209_1646\\Shape_flat",
                                "ESITO": None,
                                "STATUS": None,
                                "MD5": "da3a0981a7cfe5fb25ffc921823568ce",
                                "RESULTS": None,
                                "DATA_CARICAMENTO": "2024-02-09T16:46:04.838101",
                                "USERFILE": None,
                                "DBCONNECTION_STRING": None,
                                "DATA_ELABORAZIONE": None,
                                "LOAD_TYPE": None,
                                "STACK_TRACE_JAVA": None,
                                "DATA_VALIDAZIONE": "2024-02-09T16:46:04.881000",
                                "HOST_WORKER": "test",
                                "USER_ID": "giu",
                                "DATE_UPDATE": "2024-02-09T16:46:27.125000",
                                "RUNNING": True
                              },
                              {
                                "ID": 3,
                                "SHAPEFILE": "Shape_flat.zip",
                                "GROUP_ID": "tim",
                                "QUEUED": None,
                                "STATO": "uploaded",
                                "PATH_SHAPEFILE": "to_upload\\Shape_flat20240209_1946\\Shape_flat",
                                "ESITO": None,
                                "STATUS": "QUEUED",
                                "MD5": "da3a0981a7cfe5fb25ffc921823568ce",
                                "RESULTS": None,
                                "DATA_CARICAMENTO": None,
                                "USERFILE": None,
                                "DBCONNECTION_STRING": None,
                                "DATA_ELABORAZIONE": None,
                                "LOAD_TYPE": None,
                                "STACK_TRACE_JAVA": None,
                                "DATA_VALIDAZIONE": "2024-02-09T16:46:04.881000",
                                "HOST_WORKER": "test",
                                "USER_ID": "imir",
                                "DATE_UPDATE": "2024-02-09T16:46:27.125000",
                                "RUNNING": False
                              }
                            ]
                    },
                     "status=uploaded": {"value":[
                              {
                                "ID": 3,
                                "SHAPEFILE": "Shape_flat.zip",
                                "GROUP_ID": "tim",
                                "QUEUED": None,
                                "STATO": "uploaded",
                                "PATH_SHAPEFILE": "to_upload\\Shape_flat20240209_1946\\Shape_flat",
                                "ESITO": None,
                                "STATUS": "QUEUED",
                                "MD5": "da3a0981a7cfe5fb25ffc921899568ce",
                                "RESULTS": None,
                                "DATA_CARICAMENTO": None,
                                "USERFILE": None,
                                "DBCONNECTION_STRING": None,
                                "DATA_ELABORAZIONE": None,
                                "LOAD_TYPE": None,
                                "STACK_TRACE_JAVA": None,
                                "DATA_VALIDAZIONE": None,
                                "HOST_WORKER": "test",
                                "USER_ID": "imir",
                                "DATE_UPDATE": "2024-02-09T16:46:27.125000",
                                "RUNNING": False
                              }
                            ]
                    }
                }
            }
        },
    },
    501 : {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {"error": "Error","group_id":"group_id","id":"id"}
            }
        },
    }
}


validator_status_responses= {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                  "start thread":{"value":[
                        {
                          "id": 10,
                          "name": "tim",
                          "state": "RUNNABLE",
                          "is_alive": True,
                          "is_interrupted": False,
                          "activeCount": 3,
                          "status": {
                            "available": "true",
                            "found_error": "false",
                            "endThread": "false",
                            "readyToExecute": "false",
                            "internal_status": ""
                          }
                        }
                      ]
                    },
                  "starting validation":{"value":[
                      {
                        "id": 10,
                        "name": "tim",
                        "state": "TIMED_WAITING",
                        "is_alive": True,
                        "is_interrupted": False,
                        "activeCount": 13,
                        "status": {
                          "available": "true",
                          "found_error": "false",
                          "endThread": "false",
                          "readyToExecute": "false",
                          "internal_status": "Avvio Validatore...libsfolder:lib"
                        }
                      }
                    ]
                  },
                  "end validation":{
                      "value":[
                                {
                                  "thread_id": 19,
                                  "name": "tre",
                                  "state": "WAITING",
                                  "is_alive": True,
                                  "is_interrupted": False,
                                  "activeCount": 11,
                                  "status": {
                                    "available": "false",
                                    "found_error": "false",
                                    "endThread": "false",
                                    "readyToExecute": "false",
                                    "internal_status": "generated report sinfi_plus PT0.094S",
                                    "resultProcess": {
                                      "message": "Processo completato",
                                      "title": "ESEGUI_TUTTO_CON_REPORT",
                                      "messageType": 9,
                                      "process_detail": [
                                        "Processo di Importazione: ENDED",
                                        "Processo di Normalizzazione: ENDED",
                                        "Controllo Vincoli strutturali: ENDED",
                                        "Controllo Vincoli GeoUML: ENDED",
                                        "Durata validazione: PT17.307S",
                                        "Esportazione: ENDED",
                                        "Generazione Report DB DERBY_TYPE: to_upload\\Shape_flat20240224_1329\\report",
                                        "Generazione Report DB POSTGIS_TYPE: to_upload\\Shape_flat20240224_1329\\report",
                                        "Processo di validazione terminato in PT24.022S"
                                      ],
                                      "validation_detail": {
                                        "attributestructure": 43,
                                        "structuralconstraintviolationsin": 5,
                                        "parameterstep": 2,
                                        "elementstatedbf": 39,
                                        "geoumlconstraintnotverified": 58,
                                        "elementstatedbn": 33,
                                        "geometryerrorsin": 1,
                                        "fkconstraintviolation": 15,
                                        "geometricconstraintviolation": 60,
                                        "elementstate": 37,
                                        "fkconstraintviolationsin": 4,
                                        "processstep": 4,
                                        "geometryerror": 1,
                                        "structuralconstraintviolation": 352
                                      },
                                      "report_sinfi": [
                                        {
                                          "checks": [
                                            {
                                              "role": "elementstate",
                                              "count": 1
                                            },
                                            {
                                              "role": "elementstatedbn",
                                              "count": 1
                                            },
                                            {
                                              "role": "elementstatedbf",
                                              "count": 1
                                            }
                                          ],
                                          "sfphystructname": "ab_cda"
                                        },
                                        {
                                          "checks": [
                                            {
                                              "role": "elementstate",
                                              "count": 1
                                            },
                                            {
                                              "role": "geometricconstraintviolation",
                                              "count": 3
                                            },
                                            {
                                              "role": "elementstatedbf",
                                              "count": 1
                                            },
                                            {
                                              "role": "elementstatedbn",
                                              "count": 1
                                            }
                                          ],
                                          "sfphystructname": "comune"
                                        },
                                        {
                                          "checks": [
                                            {
                                              "role": "elementstate",
                                              "count": 1
                                            },
                                            {
                                              "role": "elementstatedbf",
                                              "count": 1
                                            },
                                            {
                                              "role": "elementstatedbn",
                                              "count": 1
                                            }
                                          ],
                                          "sfphystructname": "comune_comune_ext_sg"
                                        },
                                        {
                                          "checks": [
                                            {
                                              "role": "elementstatedbn",
                                              "count": 1
                                            },
                                            {
                                              "role": "geometricconstraintviolation",
                                              "count": 5
                                            }
                                          ],
                                          "sfphystructname": "cr_edf"
                                        },
                                      
                                      ],
                                      "report_sinfiplus": [
                                        {
                                          "id": 1,
                                          "date_execution": "2024-02-24T13:29:47",
                                          "countnotinconstruction": [
                                            252
                                          ],
                                          "errors": ""
                                        }
                                      ],
                                      "validation_id": 34,
                                      "local_validation_id": 34
                                    }
                                  },
                                  "validation_id": 34,
                                  "metrics": {
                                    "CUSPMINANGLE": 0,
                                    "MINIMUMDISTANCE": 0,
                                    "MAXIMUMVERTICES": 10000,
                                    "LINESMINIMUMLENGTH": 0,
                                    "MINIMUMPERIMETER": 0,
                                    "SEGMENTSMINIMUMLENGTH": 0,
                                    "POLYGONSMINIMUMAREA": 0
                                  }
                                }
                          ]
                    },
                   "end reports_3.1.2":{
                      "value":[
                                {
                                  "thread_id": 19,
                                  "name": "acantho",
                                  "state": "WAITING",
                                  "is_alive": True,
                                  "is_interrupted": False,
                                  "activeCount": 13,
                                  "status": {
                                    "available": "false",
                                    "found_error": "false",
                                    "endThread": "false",
                                    "readyToExecute": "false",
                                    "internal_status": "generated report sinfi_plus PT0.094S",
                                    "resultProcess": {
                                      "message": "Processo completato",
                                      "title": "ESEGUI_TUTTO_CON_REPORT",
                                      "messageType": 9,
                                      "process_detail": [
                                        "Processo di Importazione: ENDED",
                                        "Processo di Normalizzazione: ENDED",
                                        "Controllo Vincoli strutturali: ENDED",
                                        "Controllo Vincoli GeoUML: ENDED",
                                        "Durata validazione: PT2M4.36S",
                                        "Esportazione: ENDED",
                                        "Generazione Report DB DERBY_TYPE: to_upload\\#281_ACANTHO_2024022620240302_2011\\report",
                                        "Generazione Report durata PT9.037S DB POSTGIS_TYPE: to_upload\\#281_ACANTHO_2024022620240302_2011\\report",
                                        "Processo di validazione terminato in PT3M17.178S",
                                        "Generate Detail ended terminato in PT0.166S",
                                        "SinfiPlus ended terminato in PT0.094S",
                                        "Processo di report terminato in PT0S"
                                      ],
                                      "validation_detail": {
                                        "attributestructure": 52,
                                        "geometryerrorsin": 3,
                                        "structuralconstraintviolationsin": 2,
                                        "parameterstep": 2,
                                        "geometricconstraintviolation": 2598,
                                        "elementstatedbf": 86,
                                        "elementstate": 57,
                                        "geoumlconstraintnotverified": 76,
                                        "processstep": 4,
                                        "geometryerror": 23,
                                        "structuralconstraintviolation": 107826,
                                        "elementstatedbn": 47
                                      },
                                      "report_sinfi": [
                                        {
                                          "sfphystructname": "comune"
                                        },
                                        {
                                          "sfphystructname": "comune_comune_nom_t"
                                        },
                                        {
                                          "sfphystructname": "comune_ni"
                                        },
                                        {
                                          "sfphystructname": "cr_edf"
                                        },
                                        {
                                          "sfphystructname": "edi_min"
                                        },
                                        {
                                          "sfphystructname": "edi_min_cr_edf_is"
                                        },
                                        {
                                          "sfphystructname": "edi_min_cr_edf_me"
                                        },
                                        {
                                          "sfphystructname": "edi_min_ni"
                                        },
                                        {
                                          "sfphystructname": "edifc"
                                        },
                                        {
                                          "sfphystructname": "edifc_cr_edf_is"
                                        },
                                        {
                                          "sfphystructname": "edifc_cr_edf_me"
                                        },
                                        {
                                          "sfphystructname": "edifc_edifc_uso"
                                        },
                                        {
                                          "sfphystructname": "edifc_ni"
                                        },
                                        {
                                          "sfphystructname": "infr_rt"
                                        },
                                        {
                                          "sfphystructname": "infr_rt_estensione"
                                        },
                                        {
                                          "sfphystructname": "infr_rt_estensione_l"
                                        },
                                        {
                                          "sfphystructname": "infr_rt_estensione_p"
                                        },
                                        {
                                          "sfphystructname": "infr_rt_infr_rt_tr"
                                        },
                                        {
                                          "sfphystructname": "infr_rt_infr_rt_ty"
                                        },
                                        {
                                          "sfphystructname": "meta",
                                          "count_caricamento": 1,
                                          "count_normalizzazione": 1
                                        },
                                        {
                                          "sfphystructname": "mn_ind"
                                        },
                                        {
                                          "sfphystructname": "mn_ind_mn_ind_sup"
                                        },
                                        {
                                          "sfphystructname": "mn_ind_mn_ind_sup_p"
                                        },
                                        {
                                          "sfphystructname": "mn_ind_ni"
                                        },
                                        {
                                          "sfphystructname": "nd_aac"
                                        },
                                        {
                                          "sfphystructname": "nd_aac_nd_aac_ty"
                                        },
                                        {
                                          "sfphystructname": "nd_aac_nd_aac_ty_ni"
                                        },
                                        {
                                          "sfphystructname": "nd_aac_ni"
                                        },
                                        {
                                          "checks": [
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 53583
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 53583
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 53583
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 53583
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 53583
                                            }
                                          ],
                                          "sfphystructname": "nd_com",
                                          "count_caricamento": 53583,
                                          "count_normalizzazione": 53583
                                        },
                                        {
                                          "sfphystructname": "nd_com_nd_com_ty",
                                          "count_caricamento": 53583,
                                          "count_normalizzazione": 53583
                                        },
                                        {
                                          "sfphystructname": "nd_com_ni"
                                        },
                                        {
                                          "sfphystructname": "nd_ele"
                                        },
                                        {
                                          "sfphystructname": "nd_ele_nd_ele_ty"
                                        },
                                        {
                                          "sfphystructname": "nd_ele_ni"
                                        },
                                        {
                                          "sfphystructname": "nd_gas"
                                        },
                                        {
                                          "sfphystructname": "nd_gas_nd_gas_ty"
                                        },
                                        {
                                          "sfphystructname": "nd_gas_ni"
                                        },
                                        {
                                          "sfphystructname": "nd_ole"
                                        },
                                        {
                                          "sfphystructname": "nd_ole_nd_ole_ty"
                                        },
                                        {
                                          "sfphystructname": "nd_ole_nd_ole_ty_ni"
                                        },
                                        {
                                          "sfphystructname": "nd_ole_ni"
                                        },
                                        {
                                          "sfphystructname": "nd_sac"
                                        },
                                        {
                                          "sfphystructname": "nd_sac_nd_sac_ty"
                                        },
                                        {
                                          "sfphystructname": "nd_sac_ni"
                                        },
                                        {
                                          "sfphystructname": "nd_tlr"
                                        },
                                        {
                                          "sfphystructname": "nd_tlr_nd_tlr_ty"
                                        },
                                        {
                                          "sfphystructname": "nd_tlr_ni"
                                        },
                                        {
                                          "sfphystructname": "palo"
                                        },
                                        {
                                          "sfphystructname": "palo_ni"
                                        },
                                        {
                                          "sfphystructname": "provin"
                                        },
                                        {
                                          "sfphystructname": "provin_provin_nom_t"
                                        },
                                        {
                                          "sfphystructname": "region"
                                        },
                                        {
                                          "sfphystructname": "region_region_nom_t"
                                        },
                                        {
                                          "sfphystructname": "stato"
                                        },
                                        {
                                          "sfphystructname": "stato_stato_nom_t"
                                        },
                                        {
                                          "sfphystructname": "tr_aac"
                                        },
                                        {
                                          "sfphystructname": "tr_aac_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_aac_tr_aac_tra_sg"
                                        },
                                        {
                                          "sfphystructname": "tr_aac_tr_aac_tra_sg_ni"
                                        },
                                        {
                                          "checks": [
                                            {
                                              "role": "geometricconstraintviolation",
                                              "count": 2598
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 54243
                                            },
                                            {
                                              "role": "geometricconstraintviolation",
                                              "count": 2598
                                            },
                                            {
                                              "role": "geometricconstraintviolation",
                                              "count": 2598
                                            },
                                            {
                                              "role": "geometricconstraintviolation",
                                              "count": 2598
                                            },
                                            {
                                              "role": "geometricconstraintviolation",
                                              "count": 2598
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 21
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 21
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 21
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 21
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 21
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 54243
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 54243
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 54243
                                            },
                                            {
                                              "role": "structuralconstraintviolation",
                                              "count": 54243
                                            }
                                          ],
                                          "sfphystructname": "tr_com",
                                          "count_caricamento": 54243,
                                          "count_normalizzazione": 54243
                                        },
                                        {
                                          "sfphystructname": "tr_com_ni"
                                        },
                                        {
                                          "checks": [
                                            {
                                              "role": "geometryerror",
                                              "count": 2
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 2
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 2
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 2
                                            },
                                            {
                                              "role": "geometryerror",
                                              "count": 2
                                            }
                                          ],
                                          "sfphystructname": "tr_com_tr_com_tra_sg",
                                          "count_caricamento": 54243,
                                          "count_normalizzazione": 54243
                                        },
                                        {
                                          "sfphystructname": "tr_com_tr_com_tra_sg_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_ele"
                                        },
                                        {
                                          "sfphystructname": "tr_ele_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_ele_tr_ele_tra_sg"
                                        },
                                        {
                                          "sfphystructname": "tr_ele_tr_ele_tra_sg_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_gas"
                                        },
                                        {
                                          "sfphystructname": "tr_gas_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_gas_tr_gas_tra_sg"
                                        },
                                        {
                                          "sfphystructname": "tr_gas_tr_gas_tra_sg_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_ole"
                                        },
                                        {
                                          "sfphystructname": "tr_ole_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_ole_tr_ole_tra_sg"
                                        },
                                        {
                                          "sfphystructname": "tr_ole_tr_ole_tra_sg_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_sac"
                                        },
                                        {
                                          "sfphystructname": "tr_sac_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_sac_tr_sac_tra_sg"
                                        },
                                        {
                                          "sfphystructname": "tr_sac_tr_sac_tra_sg_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_tlr"
                                        },
                                        {
                                          "sfphystructname": "tr_tlr_ni"
                                        },
                                        {
                                          "sfphystructname": "tr_tlr_tr_tlr_tra_sg"
                                        },
                                        {
                                          "sfphystructname": "tr_tlr_tr_tlr_tra_sg_ni"
                                        },
                                        {
                                          "sfphystructname": "tralic"
                                        },
                                        {
                                          "sfphystructname": "tralic_ni"
                                        },
                                        {
                                          "sfphystructname": "tralic_tral_bas"
                                        },
                                        {
                                          "sfphystructname": "tralic_tral_bas_p"
                                        }
                                      ],
                                      "report_sinfiplus": [],
                                      "validation_id": 97,
                                      "local_validation_id": 97
                                    }
                                  },
                                  "validation_id": 97,
                                  "metrics": {
                                    "LINESMINIMUMLENGTH": 0,
                                    "POLYGONSMINIMUMAREA": 0,
                                    "SEGMENTSMINIMUMLENGTH": 0,
                                    "MINIMUMPERIMETER": 0,
                                    "MAXIMUMVERTICES": 10000,
                                    "MINIMUMDISTANCE": 0,
                                    "CUSPMINANGLE": 0
                                  }
                                }
                          ]
                    },

                }
            }
       }
    },
    501 : {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {"error": "Error ","group_id":"TIM","id":"2"}
            }
        },
    }
}


requests_id={
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {}
            }
       }
    },
    404 :{
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {"descr": "Job not trovato",
                            "validation_id":1,
                            "group_id":"tim"}
            }
        },
    }
}

stop_validator={}

java_thread_status_responses= {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                  "1": {
                    "Thread_Name": "main",
                    "Thread_id": "1",
                    "CPU_time": "734 s",
                    "User_time": "593 s"
                  },
                  "2": {
                    "Thread_Name": "Reference Handler",
                    "Thread_id": "2",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "3": {
                    "Thread_Name": "Finalizer",
                    "Thread_id": "3",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "4": {
                    "Thread_Name": "Signal Dispatcher",
                    "Thread_id": "4",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "5": {
                    "Thread_Name": "Attach Listener",
                    "Thread_id": "5",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "19": {
                    "Thread_Name": "tim",
                    "Thread_id": "19",
                    "CPU_time": "515 s",
                    "User_time": "171 s"
                  },
                  "20": {
                    "Thread_Name": "Timer-0",
                    "Thread_id": "20",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "22": {
                    "Thread_Name": "PoolManagerCleanup-1009667867",
                    "Thread_id": "22",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "23": {
                    "Thread_Name": "cayenne-edt-671789269-0",
                    "Thread_id": "23",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "24": {
                    "Thread_Name": "cayenne-edt-671789269-1",
                    "Thread_id": "24",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "25": {
                    "Thread_Name": "cayenne-edt-671789269-2",
                    "Thread_id": "25",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "26": {
                    "Thread_Name": "cayenne-edt-671789269-3",
                    "Thread_id": "26",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "27": {
                    "Thread_Name": "cayenne-edt-671789269-4",
                    "Thread_id": "27",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "28": {
                    "Thread_Name": "derby.rawStoreDaemon",
                    "Thread_id": "28",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "29": {
                    "Thread_Name": "Java2D Disposer",
                    "Thread_id": "29",
                    "CPU_time": "0 ns",
                    "User_time": "0 ns"
                  },
                  "cpu": {
                  "cpuUsage": "0.009843906567715645",
                  "maxMemory": "7592738816",
                  "freeMemory": "433515376",
                  "allocatedMemory": "497549312"
                }
                }
              }
          }
    },
    501 : {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {"error": "Error "}
            }
        },
    }
} 

fill_report_responses= {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                      "group_id": "tim",
                      "reports_results": [
                        {
                          "activeCount": "3",
                          "subreportTempDir": "C:\\Users\\Imir\\Desktop\\sinfi_phys\\to_upload\\#281_ACANTHO_2024022620240302_1345\\report\\tempreportMasterAnalitico\\subreports",
                          "is_interrupted": "false",
                          "paramPath": "report\\analitici\\subreport",
                          "reportFile": "report\\analitici\\reportMasterAnalitico.jrxml",
                          "validation_id": "83",
                          "swapFile": "null",
                          "outputFile": "to_upload\\#281_ACANTHO_2024022620240302_1345\\report\\tim_reportMasterAnalitico.html",
                          "param": "SUBREPORT_DIR",
                          "is_alive": "false",
                          "tempDir": "to_upload\\#281_ACANTHO_2024022620240302_1345\\report\\tempreportMasterAnalitico",
                          "state": "TERMINATED",
                          "resultProcess": "it.nophys.Result@5387f9e0"
                        },
                        {
                          "activeCount": "3",
                          "subreportTempDir": "C:\\Users\\Imir\\Desktop\\sinfi_phys\\to_upload\\#281_ACANTHO_2024022620240302_1345\\report\\tempreportMasterSintetico\\subreports",
                          "is_interrupted": "false",
                          "paramPath": "report\\sintetici\\subreport",
                          "reportFile": "report\\sintetici\\reportMasterSintetico.jrxml",
                          "validation_id": "83",
                          "swapFile": "null",
                          "outputFile": "to_upload\\#281_ACANTHO_2024022620240302_1345\\report\\tim_reportMasterSintetico.html",
                          "param": "SUBREPORT_DIR",
                          "is_alive": "false",
                          "tempDir": "to_upload\\#281_ACANTHO_2024022620240302_1345\\report\\tempreportMasterSintetico",
                          "state": "TERMINATED",
                          "resultProcess": "it.nophys.Result@7cef4e59"
                        },
                        {
                          "19": {
                            "Thread_Name": "reportMasterAnalitico.jrxml_tim",
                            "CPU_time": "0 ns",
                            "User_time": "0 ns"
                          },
                          "20": {
                            "Thread_Name": "reportMasterSintetico.jrxml_tim",
                            "CPU_time": "0 ns",
                            "User_time": "0 ns"
                          }
                        }
                      ]
                    }  
                 }
          }
    },
    501 : {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {"error": "Error "}
            }
        },
    }
}        