from Funciones import *
import os

while True:
    print("\n--- MENU PRINCIPAL  ---")
    print("1. Cargar archivo HL7 (Admision)")
    print("2. Cargar archivo XML Signos Vitales ")
    print("3. Cargar archivo XML Diagnostico ")
    print("4. Cargar archivo TXT Telemetria ")
    print("5. Consolidar y Exportar Historias Clinicas")
    print("6. Salir")
    opt = input("Seleccione una opcion (1-6): ").strip()
    if opt == "1":
        ruta = input("Ingrese la ruta del archivo HL7: ").strip()
        if os.path.exists(ruta):
            admision_datos = extraer_hl7(ruta)
            paciente_id = admision_datos.get("id")
            if paciente_id:
                if paciente_id not in GLOBAL_CLINICAL_DB:
                    GLOBAL_CLINICAL_DB[paciente_id] = {}
                GLOBAL_CLINICAL_DB[paciente_id]["admision"] = admision_datos
                print(f"Datos cargados para el paciente: {paciente_id}")
        else:
            print("La ruta ingresada no existe")
    elif opt == "2":
        ruta = input("Ingrese la ruta del archivo XML de Signos Vitales: ").strip()
        if os.path.exists(ruta):
            pac_id, signos_datos = extraer_signos_vitales(ruta)
            if pac_id not in GLOBAL_CLINICAL_DB:
                GLOBAL_CLINICAL_DB[pac_id] = {}
            GLOBAL_CLINICAL_DB[pac_id]["signos_vitales"] = signos_datos
            print(f"Signos vitales cargados para el paciente: {pac_id}")
        else:
            print("La ruta ingresada no existe")
    elif opt == "3":
        ruta = input("Ingrese la ruta del archivo XML de Diagnostico: ").strip()
        if os.path.exists(ruta):
            pac_id, diag_datos = extraer_diagnostico(ruta)
            if pac_id not in GLOBAL_CLINICAL_DB:
                GLOBAL_CLINICAL_DB[pac_id] = {}
            GLOBAL_CLINICAL_DB[pac_id]["diagnostico"] = diag_datos
            print(f"Diagnostico cargado para el paciente: {pac_id}")
        else:
            print("La ruta ingresada no existe")
    elif opt == "4":
        ruta = input("Ingrese la ruta del archivo TXT de Telemetria: ").strip()
        if os.path.exists(ruta):
            pac_id, telemetria_datos = extraer_telemetria(ruta)
            if pac_id not in GLOBAL_CLINICAL_DB:
                GLOBAL_CLINICAL_DB[pac_id] = {}
            GLOBAL_CLINICAL_DB[pac_id]["telemetria"] = telemetria_datos
            print(f"Telemetria cargada para el paciente: {pac_id}")
        else:
            print("La ruta ingresada no existe")
    elif opt == "5":
        if GLOBAL_CLINICAL_DB:
            exportar_informacion()
        else:
            print("No hay informacion almacenada")
    elif opt == "6":
        print("Cerrando modulo")
        break
    else:
        print("Opcion invalida")