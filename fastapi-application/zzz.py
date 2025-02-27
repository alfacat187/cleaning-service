from typing import Any

from sqlalchemy.ext.asyncio import AsyncAttrs

# def chunk_generator(iterable, chunk_size: int):
#     obj = iter(iterable)
#     for run in range(chunk_size):
#
#
#


# print(next(g))
# print(next(g))
# def chunk_generator(iterable, chunk_size):
#     it = iter(iterable)
#     new = []
#     while True:
#         try:
#             new = []
#             for _ in range(chunk_size):
#                 new.append(next(it))
#             yield new
#         except StopIteration:
#             if new:
#                 yield new
#
#
# g = chunk_generator([1, 6, 8, 9, 0], 2)
# for chunk in g:
#     print(chunk)
# class Stack:
#     def __init__(self):
#         self.lst = []
#
#     def push(self, x: int):
#         self.lst.append(x)
#
#     def pop(self):
#         return self.lst.pop()
#
#     def pick(self):
#         try:
#             return self.lst[-1]
#         except IndexError:
#             print("Out of range")
#         return None
#
#     def empty(self) -> bool:
#         return not self.lst
#
#
# stack = Stack()
# stack.push(1)
# stack.push(3)
# print(stack.pop())
# print(stack.pop())
# print(stack.pick())
# print(stack.empty())
# stack1 = []
# stack2 = []
#
#
# class Queue:
#     def __init__(self):
#         self.st1 = stack1
#         self.st2 = stack2
#
#     def push(self, x):
#         self.st1.append(x)
#
#     def pop(self) -> int:
#         if not self.st2:
#             for run in range(len(self.st1)):
#                 self.st2.append(self.st1.pop())
#         try:
#             return self.st2.pop()
#         except IndexError:
#             pass
#
#     def peek(self):
#         return self.st2[-1]
#
#     def empty(self):
#         return not self.st2
#
#
# qu = Queue()
# qu.push(1)
# qu.push(2)
# print(qu.pop())
# print(qu.pop())
# print(qu.pop())
# print(qu.pop())
# print(qu.empty())
# p: dict[str, int] = {"a": 1}
import jwt
from jwt.exceptions import InvalidTokenError

from core.config import settings


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict[str, Any]:

    return jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )


l = None
try:
    k = decode_jwt(l)
except InvalidTokenError as e:
    print(e)
