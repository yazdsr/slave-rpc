from jsonrpcserver import Success, method, serve, Result, Error
import os
from messages import *


@method
def createUser(username, password) -> Result:
    try:
        out = os.system(f'net user "{username}" "{password}" /add')
        if out != 0:
            return Error(code=123, message=ErrUserCreationFailed)

        out = os.system(
            f'net localgroup "Remote Desktop Users" "{username}" /add')
        if out != 0:
            deleteUser(username)
            return Error(code=123, message=ErrUserCreationFailed)

        return Success(MsgUserCreated)
    except:
        return Error(code=123, message=ErrUserCreationFailed)


@method
def deleteUser(username) -> Result:
    try:
        out = os.system(f'net user "{username}" /delete')
        if out != 0:
            return Error(code=123, message=ErrUserDelete)
        return Success(MsgUserDeleted)
    except:
        return Error(code=123, message=ErrUserDelete)


@method
def activeUser(username) -> Result:
    try:
        out = os.system(f'net user "{username}" /active:YES')
        if out != 0:
            return Error(code=123, message=ErrActiveUser)
        return Success(MsgActiveUser)
    except:
        return Error(code=123, message=ErrActiveUser)


@method
def disableUser(username) -> Result:
    try:
        out = os.system(f'net user "{username}" /active:NO')
        if out != 0:
            return Error(code=123, message=ErrDisableUser)
        return Success(MsgDisableUser)
    except:
        return Error(code=123, message=ErrDisableUser)

@method
def updatePassword(username, password) -> Result:
    try:
        out = os.system(f'net user "{username}" "{password}"')
        if out != 0:
            return Error(code=123, message=ErrUpdatePassword)
        return Success(MsgUpatePassword)
    except:
        return Error(code=123, message=ErrUpdatePassword)

@method
def heartbeat() -> Result:
    return Success("I'm alive!")

if __name__ == "__main__":
    print("Server is running...")
    serve('0.0.0.0', 9000)
