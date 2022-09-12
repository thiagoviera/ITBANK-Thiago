from Clientes import Cliente


class Transaccion:
    def __init__(self, estado: str, tipo: str, cuenta_numero: int, cupo_diario_restante: int,
                 monto: int, fecha: str, numero: int, saldo_en_cuenta: int,
                 tarjetas_credito_actualmente: int, chequeras_actualmente: int):
        self._estado = estado
        self._tipo = tipo
        self._cuenta_numero = cuenta_numero
        self._cupo_diario_restante = cupo_diario_restante
        self._monto = monto
        self._fecha = fecha
        self._numero = numero
        self._saldo_en_cuenta = saldo_en_cuenta
        self._tarjetas_credito_actualmente = tarjetas_credito_actualmente
        self._chequeras_actualmente = chequeras_actualmente

    def resolver(self, cliente: Cliente) -> str:
        cliente.set_cuenta(self._cupo_diario_restante, self._saldo_en_cuenta)

        match self._tipo:
            case "ALTA_CHEQUERA":
                cliente.set_chequeras(self._chequeras_actualmente)
                return cliente.dar_alta_chequera()
            case "ALTA_TARJETA_CREDITO":
                cliente.set_tarjetas_credito(self._tarjetas_credito_actualmente)
                return cliente.dar_alta_tarjeta_credito()
            case "COMPRA_DOLAR":
                return cliente.comprar_dolar(self._monto)
            case "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                return cliente.retirar_efectivo(self._monto)
            case "TRANSFERENCIA_ENVIADA":
                return cliente.enviar_transferencia(self._monto)
            case "TRANSFERENCIA_RECIBIDA":
                return cliente.recibir_transferencia(self._monto)

    @property
    def estado(self):
        return self._estado

    @property
    def tipo(self):
        return self._tipo

    @property
    def cuenta_numero(self):
        return self._cuenta_numero

    @property
    def cupo_diario_restante(self):
        return self._cupo_diario_restante

    @property
    def monto(self):
        return self._monto

    @property
    def saldo_en_cuenta(self):
        return self._saldo_en_cuenta

    @property
    def tarjetas_credito_actualmente(self):
        return self._tarjetas_credito_actualmente

    @property
    def chequeras_actualmente(self):
        return self._chequeras_actualmente

    @property
    def numero(self):
        return self._numero
