# # -*- coding: utf-8 -*-
import secrets
token = secrets.token_hex(4)  # 16 байт дадут строку из 32 символов

print(token)