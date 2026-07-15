import hashlib


def function_hash(source):

    """
    Retorna um hash SHA256 da função.
    """

    return hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()


def compare_files(file1, file2):

    dict1 = {
        f.name: f
        for f in file1.functions
    }

    dict2 = {
        f.name: f
        for f in file2.functions
    }

    names = sorted(
        set(dict1.keys()) | set(dict2.keys())
    )

    result = []

    for name in names:

        if name not in dict1:

            status = "Somente Arquivo 2"

        elif name not in dict2:

            status = "Somente Arquivo 1"

        else:

            h1 = function_hash(dict1[name].source)
            h2 = function_hash(dict2[name].source)

            if h1 == h2:

                status = "Idêntica"

            else:

                status = "Modificada"

        result.append((name, status))

    return result