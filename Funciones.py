import os
import json
import csv
import xml.etree.ElementTree as ET

os.makedirs("sistema_uci/exportaciones_json", exist_ok=True)
os.makedirs("sistema_uci/exportaciones_csv", exist_ok=True)

GLOBAL_CLINICAL_DB = {}

def extraer_hl7(ruta_archivo):
    with open(ruta_archivo, "r", encoding = "utf-8") as f:
        lineas = f.readlines()
    datos = {}
    for linea in lineas:
        if linea.startswith("PID"):
            campos = linea.split("|")
            datos["id"] = campos[3].strip()
            nombre_completo = campos[5].replace("^", " ").strip()
            datos["nombre"] = nombre_completo
        elif linea.startswith("PV1"):
            campos = linea.split("|")
            datos["ubicacion"] = campos[3].strip()
    return datos

def extraer_signos_vitales(ruta_archivo):
    tree = ET.parse(ruta_archivo)
    root = tree.getroot()
    paciente_id = "na"
    paciente_ref = root.find(".//Observation/subject/reference")
    if paciente_ref is not None and paciente_ref.text:
        partes_ref = paciente_ref.text
        if len(partes_ref) > 1:
            paciente_id = partes_ref[1].strip()
    datos = []
    for obs in root.findall(".//Observation/vitalSigns"):
        nombre = obs.find(".//code/coding/display")
        valor = obs.find(".//valueQuantity/value")
        unidad = obs.find(".//valueQuantity/unit")
        if nombre is not None and valor is not None and unidad is not None:
            datos.append({
                "nombre": nombre.text.strip(),
                "valor": float(valor.text.strip()),
                "unidad": unidad.text.strip()
            })
    return paciente_id, datos

def extraer_diagnostico(ruta_archivo):
    tree = ET.parse(ruta_archivo)
    root = tree.getroot()
    paciente_id = "na"
    paciente_ref = root.find(".//DiagnosticReport/patientId")
    if paciente_ref is not None and paciente_ref.text:
        partes_ref = paciente_ref.text
        paciente_id = partes_ref.strip()
    datos = {}
    categoria = root.find(".//DiagnosticReport/category")
    conclusion = root.find(".//DiagnosticReport/conclusion")
    medico = root.find(".//DiagnosticReport/physician")
    datos["Categoria"] = categoria.text.strip() if categoria is not None else "Dato no registrado"
    datos["Conclusion"] = conclusion.text.strip() if conclusion is not None else "Dato no registrado"
    datos["Medico"] = medico.text.strip() if medico is not None else "Dato no registrado"
    return paciente_id, datos

def extraer_telemetria(ruta_archivo):
    with open(r"C:\Users\hnnas\Downloads\pacientes_p3\log_telemetria_3.txt", "r", encoding = "utf-8") as file:
    linea = file.readlines()
    datos = {}
    for lineas in linea:
        if lineas.strip():
            fecha_hora, id, sensor, valor, estado = lineas.strip().split("|")
            fecha, hora = fecha_hora.split(" ")
            inf = {
                "Fecha": fecha.strip(),
                "Hora": hora.strip(),
                "Sensor": sensor.strip(),
                "Valor": valor.strip(),
                "Estado": estado.strip()
            }
        if id not in datos:
            datos[id] = []
        datos[id].append(inf)
    return datos

def exportar_informacion():
    csv_path = "sistema_uci/exportaciones_csv/signos_vitales_consolidados.csv"
    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ID_Paciente", "Nombre_Paciente", "Signo_Vital", "Valor", "Unidad"])
        for pid, hitoria in GLOBAL_CLINICAL_DB.items():
            json_path = f"sistema_uci/exportaciones_json/historia_paciente_{pid}.json"
            with open(json_path, "w") as json_file:
                json.dump(hitoria, json_file, indent=4)
            nombre_pac = hitoria.get("admision", {}).get("nombre", "Desconocido")
            signos = hitoria.get("signos_vitales", [])
            for sig in signos:
                writer.writerow([pid, nombre_pac, sig.get("nombre"), sig.get("valor"), sig.get("unidad")])
    print("\nInformacion exportada exitosamente")
