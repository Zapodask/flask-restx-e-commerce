import base64


def isBase64(sb):
    try:
        sb_bytes = bytes(sb, "ascii")

        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except:
        return False
