import json
import webbrowser
from pathlib import Path

import jsonschema
from jsonschema.validators import validate

from Clientes import *
from Transacciones import Transaccion

report_name = "report.html"


def is_valid_tps_json(client_json: list) -> bool:
    try:
        validate(client_json, {
            "type": "object",
            "properties": {
                "nombre": {"type": "string"},
                "apellido": {"type": "string"},
                "dni": {"type": "string"},
                "tipo": {
                    "type": "string",
                    "enum": [
                        "CLASSIC",
                        "GOLD",
                        "BLACK"
                    ]
                },
                "direccion": {
                    "type": "object",
                    "properties": {
                        "calle": {"type": "string"},
                        "numero": {"type": "string"},
                        "ciudad": {"type": "string"},
                        "provincia": {"type": "string"},
                        "pais": {"type": "string"},
                    }
                },
                "transacciones": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "estado": {"type": "string"},
                            "tipo": {"type": "string"},
                            "cuentaNumero": {"type": "number"},
                            "cupoDiarioRestante": {"type": "number"},
                            "cantidadExtraccionesHechas": {"type": "number"},
                            "monto": {"type": "number"},
                            "fecha": {"type": "string"},
                            "numero": {"type": "number"},
                            "saldoEnCuenta": {"type": "number"},
                            "totalTarjetasDeCreditoActualmente": {"type": "number"},
                            "totalChequerasActualmente": {"type": "number"}
                        }
                    }
                }
            },
            "required": ["nombre", "apellido", "dni", "tipo", "direccion", "transacciones"]
        })
    except jsonschema.exceptions.ValidationError:
        return False
    return True


def fetch_tps_data() -> dict:
    try:
        directorio = str(input("Ingrese el archivo JSON (sin la extension) a leer: "))
        file = open(f"../..//{directorio}.json")
        data = json.load(file)

        file.close()

        if not is_valid_tps_json(data):
            print("El JSON indicado no corresponde con el formato del TPS, elija otro")
        else:
            return data
    except IOError as error:
        print(f"No se pudo leer el archivo indicado: {error}")
    except ValueError as error:
        print(f"El archivo indicado no es un JSON: {error}")


def create_tps_report(cliente: Cliente, transacciones: list[Transaccion]):
    print(f"Procesando las transacciones del Cliente N°{cliente.numero}")

    document = [f"""<html>
        <head>
            <link rel="icon" href="./images/logos/ISOLOGO.png">
            <link href="./CSS/styles.css" rel="stylesheet"/>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">

            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap" rel="stylesheet">

            <title>Reporte ITBANK</title>
        </head>
        <body id="report-body">
            <section id="report-content" class="A4 position-relative">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.min.js" integrity="sha384-ODmDIVzN+pFdexxHEHFBQH3/9/vQ9uori45z4JjnFsRydbmQbmL5t1tQ0culUzyK" crossorigin="anonymous"></script>
                <nav class="navbar bg-light border-bottom container p-3">
                    <div class="row w-100 gx-5">
                        <div class="navbar-brand col-4">
                            <img src="./images/logos/logomarginado-08.png" class="img-fluid" alt="Logo ITBANK" width="336" height="115">
                        </div>
                        <div class="col">
                            <div class="row text-light rounded px-1" id="azulito">
                                <div class="col-7">
                                    <p class="fs-5 my-auto">{cliente.nombre} {cliente.apellido}</p>
                                </div>
                                <div class="col-5">
                                    <div class="row d-block border-bottom">
                                        Cliente:
                                        <span class="fs-5">{cliente.dni}</span>
                                    </div>
                                    <div class="row d-block">
                                        ID:
                                        <span class="fs-5">{cliente.numero}</span>
                                    </div>
                                </div>
                            </div>
                            <span class="d-block">{cliente.calle} {cliente.numero}</span>
                            <span class="d-block">{cliente.ciudad}</span>
                            <span class="d-block">{cliente.provincia}</span>
                        </div>
                    </div>
                </nav>
                <main class="container py-3">
                    <h1 class="text-center">REPORTE DE TRANSACCIONES</h1>
                    <hr>
                    <div class="container">
                        <table class="table table-bordered table-sm">
                            <thead>
                                <tr>
                                    <th scope="col" class="report-font">#</th>
                                    <th scope="col" class="report-font">Estado</th>
                                    <th scope="col" class="report-font">Tipo</th>
                                    <th scope="col" class="report-font">ID Cuenta</th>
                                    <th scope="col" class="report-font">Cupo Restante</th>
                                    <th scope="col" class="report-font">Monto</th>
                                    <th scope="col" class="report-font">Saldo en Cuenta</th>
                                    <th scope="col" class="report-font">Tarjetas de Credito</th>
                                    <th scope="col" class="report-font">Chequeras</th>
                                    <th scope="col" class="report-font">Fecha</th>
                                </tr>
                            </thead>
                            <tbody class="table-group-divider">"""]

    for transaccion in transacciones:
        document.append(f"""
                                <tr>
                                    <th scope="row"{' rowspan="2"' if transaccion.estado == "RECHAZADA" else ''}>
                                        {transaccion.numero}
                                    </th>
                                    <td class="report-font">{transaccion.estado}</td>
                                    <td class="report-font">{transaccion.tipo.replace('_', ' ')}</td>
                                    <td class="report-font">{transaccion.cuenta_numero}</td>
                                    <td class="report-font">{transaccion.cupo_diario_restante}</td>
                                    <td class="report-font">{transaccion.monto}</td>
                                    <td class="report-font">{transaccion.saldo_en_cuenta}</td>
                                    <td class="report-font">{transaccion.tarjetas_credito_actualmente}</td>
                                    <td class="report-font">{transaccion.chequeras_actualmente}</td>
                                    <td class="report-font">06/06/2022 12:30:55</td>
                                </tr>""")
        if transaccion.estado == "RECHAZADA":
            document.append(f"""
                                <tr class="table-danger">
                                    <td colspan="9" class="fw-semibold report-font">Razon: {transaccion.resolver(cliente)}</td>
                                </tr>""")

    document.append("""
                            </tbody>
                        </table>
                    </div>
                </main>
                <footer class="bg-light border-top position-absolute bottom-0 w-100">
                    <div class="container py-3 text-center">
                        © 2022 Full-Stack Developer, ITBA.
                    </div>
                </footer>
            </section>
        </body>
    </html>""")

    file = open(f"../../{report_name}", "w")
    file.write(''.join(document))

    webbrowser.open(str(Path(f"../../{report_name}").absolute()))
    file.close()


def main():
    while True:
        data = fetch_tps_data()
        cliente = None

        match data["tipo"]:
            case "CLASSIC":
                cliente = Classic(
                    nombre=data["nombre"],
                    apellido=data["apellido"],
                    numero=data["numero"],
                    dni=data["dni"],
                    direccion=data["direccion"]
                )
            case "GOLD":
                cliente = Gold(
                    nombre=data["nombre"],
                    apellido=data["apellido"],
                    numero=data["numero"],
                    dni=data["dni"],
                    direccion=data["direccion"]
                )
            case "BLACK":
                cliente = Black(
                    nombre=data["nombre"],
                    apellido=data["apellido"],
                    numero=data["numero"],
                    dni=data["dni"],
                    direccion=data["direccion"]
                )

        transacciones = []
        for transaccion in data["transacciones"]:
            transacciones.append(Transaccion(
                estado=transaccion["estado"],
                tipo=transaccion["tipo"],
                cuenta_numero=transaccion["cuentaNumero"],
                cupo_diario_restante=transaccion["cupoDiarioRestante"],
                monto=transaccion["monto"],
                fecha=transaccion["fecha"],
                numero=transaccion["numero"],
                saldo_en_cuenta=transaccion["saldoEnCuenta"],
                tarjetas_credito_actualmente=transaccion["totalTarjetasDeCreditoActualmente"],
                chequeras_actualmente=transaccion["totalChequerasActualmente"],
            ))

        create_tps_report(cliente, transacciones)

        continuar = input("Desea abrir otro archivo? [SI/NO]: ").upper().strip()
        if continuar != "SI":
            break


if __name__ == "__main__":
    main()
