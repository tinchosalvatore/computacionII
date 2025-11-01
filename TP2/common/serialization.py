import json

def serialize_data(data: dict) -> bytes:
    """
    Serializa un diccionario a bytes usando JSON con codificación UTF-8.

    Args:
        data: El diccionario a serializar.

    Returns:
        Los datos serializados como bytes.
    """
    return json.dumps(data).encode('utf-8')

def deserialize_data(data_bytes: bytes) -> dict:
    """
    Deserializa bytes (codificados en UTF-8) a un diccionario usando JSON.

    Args:
        data_bytes: Los bytes a deserializar.

    Returns:
        El diccionario deserializado.
    """
    return json.loads(data_bytes.decode('utf-8'))
