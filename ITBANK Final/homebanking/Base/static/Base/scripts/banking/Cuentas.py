class Cuenta:
    def __init__(self, limite_extraccion_diario: int, limite_transferencia_recibida: int,
                 saldo_en_cuenta: int, costo_transferencias: float, saldo_descubierto_disponible: int):
        self.__limite_extraccion_diario = limite_extraccion_diario
        self.__limite_transferencia_recibida = limite_transferencia_recibida
        self.__saldo_en_cuenta = saldo_en_cuenta
        self.__costo_transferencias = costo_transferencias
        self.__saldo_descubierto_disponible = saldo_descubierto_disponible

    def enviar_transaccion(self, monto: int) -> None | str:
        monto *= (1.0 + self.__costo_transferencias)
        return self.retirar_saldo(monto)

    def recibir_transaccion(self, monto: int) -> None | str:
        if self.__limite_transferencia_recibida == 0:
            self.__saldo_en_cuenta += monto
        elif self.__limite_transferencia_recibida < monto:
            return "LIMITE"
        else:
            self.__saldo_en_cuenta += monto

    def retirar_saldo(self, monto: int) -> None | str:
        if self.__limite_extraccion_diario < monto:
            return "LIMITE"
        elif self.__saldo_en_cuenta < monto:
            if self.__saldo_descubierto_disponible < monto - self.__saldo_en_cuenta:
                return "SALDO"
            else:
                self.__saldo_en_cuenta -= monto
        else:
            self.__saldo_en_cuenta -= monto
