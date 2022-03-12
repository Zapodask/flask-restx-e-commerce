import requests

import xml.etree.ElementTree as ET


def calc_portage(
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
    """Calculate portage

    Args:
        nCdServico (str): service code
        sCepOrigem (str): origin zip code
        sCepDestino (str): destination zip code
        nVlPeso (float): weight
        nCdFormato (int): package format
        nVlComprimento (float): package length
        nVlAltura (float): package height
        nVlLargura (float): packet width
        nVlDiametro (int, optional): package diameter. Defaults to 0.
        sCdMaoPropria (str, optional): hand delivery. Defaults to "N".
        nVlValorDeclarado (int, optional): declared value. Defaults to 0.
        sCdAvisoRecebimento (str, optional): receipt notification. Defaults to "N".
        nCdEmpresa (str, optional): company email. Defaults to "".
        sDsSenha (str, optional): company password. Defaults to "".

    Returns:
        dict: calculus answer
    """
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
