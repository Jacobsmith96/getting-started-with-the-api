# OAuth2 settings for communicating with clinical server
CLINICAL = {
    'client_id': '',
    'redirect_uri': 'localhost:2048/',
    'scopes': [
    'launch',
    'launch/patient',
    'launch/encounter',
    'patient/*.read',
    'user/*.*',
    'openid',
    'profile']
}
# OAuth2 settings for communicating with genomic server
GENOMICS = {
    'client_id': '',
    'redirect_uri': 'google.genomics.com:8005/',
    'scopes': ['user/Sequence.read', 'user/Patient.read','user/Sequence.write'],
    'oauth_base': 'google.genomics.com/auth',
    'api_base': 'google.genomics.com/api'
}


# choose a secret key here:
GOOGLE_API_KEY="AIzaSyApqOknh5j8-_aJAItLbU439b3O8KvLOIc"
SECRET_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCNddNLFcxhIgsT\ntbOWNEe6hSGuCciKPyvy63DHRn84Zxq8tjKeP9kJwakc5PKO3be7PpMHJLaZCx1g\nhdgCtcebglzx+p8/j2bp25ITh9e4EVRZJiJi/U56+i9z8jv/o5liKrzQ9OJXmM1Y\nH2/5aNX+0z/HiKCDSYUvO/IHuRp7Z0vi37vjg725M6DIkkPojqZ0EWRXFJRv2Qqb\n+UVPlLWVhlWoEca4Nn6WV2swE90pMsrbx05QEYuAy8r4tVfskBiPmhuO57iYrTts\nXWuqQI7mkMLnUBpfi6SVvGpH7ePi2GUKSK4Z/CtpfyPW6lPHtV4l9xxBUtgSsevo\nQBKnQAZnAgMBAAECggEAC7N8V9CkyEAVpHq6MSl/6WjLwWajxPO2wfBBsuoc6eB1\ncLitdTOY01rGj1JM0g56/S0O4l9iD0TBGFPZ61d3/GALKiTt+Ub2X0+/RIhPCrW8\nQWeLHp8PV9LMDA40ck/pBxq75ZjsBAzqp2hqTbojQWHd+7ZMeK+jKaYOvh7Mlvpz\n4qrJYjC00T/S/n37eigKzwFuGhNWRiS/da89KqHHcABk2LxubBXFmaTjfMYKQbqA\nxemXET6RjWcarYEPe9uFoCiRmDDmmiun4GyzOyh5A9VONbdDsEuhwC6Z03znL3IM\nlThsEmKc7mIraGZaJOXyXLb6FBNMugE6jKanh52+WQKBgQDHsW1FwGgal9LDBxBW\nEDnx620DoIV14Q3WSn7NUV1TeeneUDEA+h37D3HxSnaH3F9r2TZisRTrnHRM7kTj\nnoEMF/l9YVIZ2Ed4jmut4MIRvIzLIXe/SWVP/jR/P4kWTQ80FJbh//vnYxyfyHZh\nri8gviL6sQexZPJ2rIB5yKIwPQKBgQC1WPEQ4/cuHKxFZaiPP9IiFzMJIuq3ikJe\nX80qIIzzDEV8uHwVeqasEo+qFMQmUsmGYAE4LbbWY7hwXUg4YcA1nUFtK9BUOqXL\nXQsd5OXagtQIoXXgCs0HM3J6ZmG/u2mDuvKrPjB3W3ovT2WceKD0yprPrNiYeTy3\nZkmTkVh3cwKBgEi6wT6fRgsxcoyffP6raD9I7Gpew1zce8qpVSd4U9I8W8YhVMez\nUMoIpQopgaQXyhUghmNJdYIeeGkwepygNQXvkWlt0ZYiJF2vGV65tlT5ZBnzdYaQ\nt7p7rikOPeKGbFweh5mGPvvWKC21uA/5faaiOWEuqsucJYa9awlv3kpNAoGBAIqW\nYgPqc2gF+ZE/U0XGHCx5VkNRL9b8DiRZSk07evvzENdzlUBE70LpHGl6XTx8YA4V\nKFlqdiP5KWaVoy+TZHSUrP9lUFxORY3YmTpLR21qNegynAaPuogaRQ5NV75S1xwY\nroM3j4pnmkS1hI3Dkh4BB7ZV/WDopgHyZaAkn1sJAoGAaA02wgtIyygMpZO3M52P\nqDtgoeJghgkbvjl9k7CF5FB/YhOJ++XiEt5g+j7419qpf/nckywvRi9iy7YOfhG1\ntF6CzJbWWcDY7ecR/ufRVYjp9obHB8YRzra9mgseFdyG+3wwODoWqRngaTJX7wOe\nF6MN1DqR2T09EUbOKMY1/2o=\n-----END PRIVATE KEY-----\n"
