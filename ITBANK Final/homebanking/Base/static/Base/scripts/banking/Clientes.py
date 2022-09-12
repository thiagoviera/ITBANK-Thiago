from abc import ABC, abstractmethod

from Cuentas import Cuenta


class Cliente(ABC):
    def __init__(self, nombre: str, apellido: str, numero: int, dni: str, direccion: dict):
        self._nombre = nombre
        self._apellido = apellido
        self._numero = numero
        self._dni = dni
        self._direccion = Cliente.Direccion(
            pais=direccion["pais"],
            provincia=direccion["provincia"],
            ciudad=direccion["ciudad"],
            calle=direccion["calle"],
            numero=direccion["numero"]
        )

        self._chequeras = 0
        self._tarjetas_credito = 0

        self._cuenta = None

    @abstractmethod
    def set_cuenta(self, limite_extraccion_diario: int, saldo_en_cuenta: int):
        pass

    @property
    @abstractmethod
    def puede_crear_chequera(self) -> bool:
        pass

    @property
    @abstractmethod
    def puede_crear_tarjeta_credito(self) -> bool:
        pass

    @property
    @abstractmethod
    def puede_comprar_dolar(self) -> bool:
        pass

    def set_chequeras(self, chequeras: int):
        self._chequeras = chequeras

    def set_tarjetas_credito(self, tarjetas_credito: int):
        self._tarjetas_credito = tarjetas_credito

    def dar_alta_chequera(self) -> None | str:
        if self.puede_crear_chequera:
            self._chequeras += 1
        else:
            return "No se pueden dar de alta mas Chequeras para esta Cuenta"

    def dar_alta_tarjeta_credito(self) -> None | str:
        if self.puede_crear_tarjeta_credito:
            self._tarjetas_credito += 1
        else:
            return "No se pueden dar de alta mas Tarjetas de Credito para esta Cuenta"

    def comprar_dolar(self, monto: int) -> None | str:
        if self.puede_comprar_dolar:
            razon = self._cuenta.retirar_saldo(monto)
            if razon == "LIMITE":
                return "No se cuenta con el Limite de Extraccion para esta Operacion"
            elif razon == "SALDO":
                return "No se cuenta con el Saldo para esta Operacion"
        else:
            return "No se cuenta con Caja de Ahorro en Dolares"

    def retirar_efectivo(self, monto) -> None | str:
        razon = self._cuenta.retirar_saldo(monto)
        if razon == "LIMITE":
            return "No se cuenta con el Limite de Extraccion para esta Operacion"
        elif razon == "SALDO":
            return "No se cuenta con el Saldo para esta Operacion"

    def enviar_transferencia(self, monto) -> None | str:
        razon = self._cuenta.enviar_transaccion(monto)
        if razon == "LIMITE":
            return "No se cuenta con el Limite de Extraccion para esta Operacion"
        elif razon == "SALDO":
            return "No se cuenta con el Saldo para esta Operacion"

    def recibir_transferencia(self, monto) -> None | str:
        if self._cuenta.retirar_saldo(monto) == "LIMITE":
            return "No se cuenta con la Autorizacion para recibir Transferencias de este volumen"

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def pais(self) -> str:
        return self._direccion.pais

    @property
    def provincia(self) -> str:
        return self._direccion.provincia

    @property
    def ciudad(self) -> str:
        return self._direccion.ciudad

    @property
    def calle(self) -> str:
        return f"{self._direccion.calle} {self._direccion.numero}"

    def __repr__(self):
        return f'Nombre: {self._nombre} || Apellido: {self._apellido} ||' \
               f' Numero: {self._numero} || DNI: {self._dni} || Direccion: [{self._direccion}] ||' \
               f' Tarjetas de Credito: {self._tarjetas_credito} || Chequeras: {self._chequeras}'

    class Direccion:
        def __init__(self, pais: str, provincia: str, ciudad: str, calle: str, numero: str):
            self._pais = pais
            self._provincia = provincia
            self._ciudad = ciudad
            self._calle = calle
            self._numero = numero

        @property
        def pais(self):
            return self._pais

        @property
        def provincia(self):
            return self._provincia

        @property
        def ciudad(self):
            return self._ciudad

        @property
        def calle(self):
            return self._calle

        @property
        def numero(self):
            return self._numero


class Classic(Cliente):
    # Tiene una sola tarjeta de debito, creada junto al cliente
    # Tiene una caja de ahorro en pesos, pero no una en dolares, por ende no puede comprar USD
    # Solo puede retirar $10.000 por dia
    # No tiene acceso a tarjetas de credito, ni chequeras
    # La comision por transferencia es del 1%
    # No puede recibir transferencias mayores a $150.000 sin previo aviso

    def __init__(self, nombre: str, apellido: str, numero: int, dni: str, direccion: dict):
        super().__init__(nombre, apellido, numero, dni, direccion)

        self._cajaAhorroDolares = True
        self._cuentaCorriente = True

    @property
    def puede_crear_chequera(self) -> bool:
        return False

    @property
    def puede_crear_tarjeta_credito(self) -> bool:
        return False

    @property
    def puede_comprar_dolar(self) -> bool:
        return False

    def set_cuenta(self, limite_extraccion_diario: int = 10000, saldo_en_cuenta: int = 0):
        self._cuenta = Cuenta(
            limite_extraccion_diario=limite_extraccion_diario,
            limite_transferencia_recibida=150000,
            saldo_en_cuenta=saldo_en_cuenta,
            costo_transferencias=1.0,
            saldo_descubierto_disponible=0
        )


class Gold(Cliente):
    # Tiene una tarjeta de debito, creada junto al cliente
    # Tiene una cuenta corriente con un descubierto de $10.000, es decir, puede tener hasta -$10.000
    # Tiene caja de ahorro en dolares
    # Solo puede retirar $20.000 por dia
    # Puede tener una sola tarjeta de credito
    # Puede tener una sola chequera
    # La comision por transferencia es del 0,5%
    # No puede recibir transferencias mayores a $500.000 sin previo aviso

    def __init__(self, nombre: str, apellido: str, numero: int, dni: str, direccion: dict):
        super().__init__(nombre, apellido, numero, dni, direccion)

    @property
    def puede_crear_chequera(self) -> bool:
        return self._chequeras < 1

    @property
    def puede_crear_tarjeta_credito(self) -> bool:
        return self._tarjetas_credito < 1

    @property
    def puede_comprar_dolar(self) -> bool:
        return True

    def set_cuenta(self, limite_extraccion_diario: int = 20000, saldo_en_cuenta: int = 0):
        self._cuenta = Cuenta(
            limite_extraccion_diario=limite_extraccion_diario,
            limite_transferencia_recibida=500000,
            saldo_en_cuenta=saldo_en_cuenta,
            costo_transferencias=0.5,
            saldo_descubierto_disponible=10000
        )


class Black(Cliente):
    # Tiene una caja de ahorro en pesos, cuenta corriente en pesos, y una caja de ahorro en dolares
    # Su cuenta corriente tiene un descubierto de $10.000, es decir, puede tener hasta -$10.000
    # Solo puede retirar $100.000 por dia
    # Puede tener hasta 5 tarjetas de credito
    # Puede tener hasta dos chequeras
    # No aplican comisiones por transferencia
    # No aplican restricciones para recibir transferencias

    def __init__(self, nombre: str, apellido: str, numero: int, dni: str, direccion: dict):
        super().__init__(nombre, apellido, numero, dni, direccion)

    @property
    def puede_crear_chequera(self) -> bool:
        return self._chequeras < 2

    @property
    def puede_crear_tarjeta_credito(self) -> bool:
        return self._tarjetas_credito < 5

    @property
    def puede_comprar_dolar(self) -> bool:
        return True

    def set_cuenta(self, limite_extraccion_diario: int = 100000, monto: int = 0):
        self._cuenta = Cuenta(
            limite_extraccion_diario=limite_extraccion_diario,
            limite_transferencia_recibida=0,
            saldo_en_cuenta=monto,
            costo_transferencias=0.0,
            saldo_descubierto_disponible=10000
        )
