class PrimitiveIdlTypes:
    """
    Описывает страндартные типы переменных IDL
    """
    # Basic types as defined by the IDL specification
    # 7.4.1.4.4.2 Basic Types
    SIGNED_NONEXPLICIT_INTEGER_TYPES = (  # rules (26)
        'short',  # rule (27)
        'long',  # rule (28)
        'long long',  # rule (29)
    )
    UNSIGNED_NONEXPLICIT_INTEGER_TYPES = (  # rules (30)
        'unsigned short',  # rule (31)
        'unsigned long',  # rule (32)
        'unsigned long long',  # rule (33)
    )
    FLOATING_POINT_TYPES = (  # rule (24)
        'float',
        'double',
        # TODO: шо это???
        'double[36]',
        'long double',
    )
    CHARACTER_TYPES = (
        'char',  # rule (34)
        'wchar',  # rule (35)
    )
    BOOLEAN_TYPE = (
        'boolean',  # rule (36)
    )
    OCTET_TYPE = (
        'octet',  # rule (37)
    )
    # 7.4.13.4.4 Integers restricted to holding 8-bits of information
    # 7.4.13.4.5 Explicitly-named Integer Types
    SIGNED_EXPLICIT_INTEGER_TYPES = (
        'int8',  # rule (208)
        'int16',  # rule (210)
        'int32',  # rule (211)
        'int64',  # rule (212)
    )
    UNSIGNED_EXPLICIT_INTEGER_TYPES = (
        'uint8',  # rule (209)
        'uint16',  # rule (213)
        'uint32',  # rule (214)
        'uint64',  # rule (215)
    )
    STRING = (
        'string',
    )


def get_common_types_list():
    types_list = list()

    for var_type in PrimitiveIdlTypes.SIGNED_NONEXPLICIT_INTEGER_TYPES:
        types_list.append(var_type)
    for var_type in PrimitiveIdlTypes.UNSIGNED_NONEXPLICIT_INTEGER_TYPES:
        types_list.append(var_type)
    for var_type in PrimitiveIdlTypes.SIGNED_EXPLICIT_INTEGER_TYPES:
        types_list.append(var_type)
    for var_type in PrimitiveIdlTypes.UNSIGNED_EXPLICIT_INTEGER_TYPES:
        types_list.append(var_type)
    for var_type in PrimitiveIdlTypes.FLOATING_POINT_TYPES:
        types_list.append(var_type)
    for var_type in PrimitiveIdlTypes.CHARACTER_TYPES:
        types_list.append(var_type)
    for var_type in PrimitiveIdlTypes.OCTET_TYPE:
        types_list.append(var_type)
    for var_type in PrimitiveIdlTypes.STRING:
        types_list.append(var_type)
    for var_type in PrimitiveIdlTypes.BOOLEAN_TYPE:
        types_list.append(var_type)

    return types_list
