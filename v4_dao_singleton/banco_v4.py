from v4_dao_singleton.cuenta_dao import CuentaDAO

# 1. Instanciamos el traductor (DAO)
banco_service = CuentaDAO()

# 2. Consultamos de forma limpia
cuenta_info = banco_service.consultar_cuenta("111")
if cuenta_info:
    print(f"Titular: {cuenta_info[0]}, Saldo: {cuenta_info[1]}€")

# 3. Operación compleja desacoplada
tranf_ok = banco_service.transferencia_bancaria("111", "222", 50.0)