import requests

import xml.etree.ElementTree as ET


def calc_frete(
    nCdServico: str,
    sCepOrigem: str,
    sCepDestino: str,
    nVlPeso: float,
    nCdFormato: int,
    nVlComprimento: float,
    nVlAltura: float,
    nVlLargura: float,
    nVlDiametro: int = 0,
    sCdMaoPropria: str = "N",
    nVlValorDeclarado: int = 0,
    sCdAvisoRecebimento: str = "N",
    nCdEmpresa: str = "",
    sDsSenha: str = "",
):
    data = ""

    for k, v in locals().items():
        data += f"{k}={v}&"

    while True:
        try:
            res = requests.post(
                "https://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx/CalcPrecoPrazo",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            ).text

            break

        except:
            pass

    root = ET.fromstring(str(res))[0][0]

    ret = {
        "codigo": root[0].text,
        "valor": root[1].text,
        "prazo_entrega": root[2].text,
        "valor_mao_propria": root[3].text,
        "valor_aviso_recebimento": root[4].text,
        "valor_declarado": root[5].text,
        "entrega_domiciliar": root[6].text,
        "entrega_sabado": root[7].text,
        "erro": root[8].text,
        "valor_sem_adicionais": root[10].text,
    }

    return ret
