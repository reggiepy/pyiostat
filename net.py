# *_*coding:utf-8 *_*
import subprocess
from typing import List

from pydantic import BaseModel
from pydantic import Field


class Netnfo(BaseModel):
    NicNumNics: int = Field(default=0)  # 网卡数量
    Nics: List = Field(default=[])  # 每个网卡的状态信息


class NicInfo(BaseModel):
    Name: str = Field(default="")

    RBytes: int = Field(default=0)
    RPackets: int = Field(default=0)
    RErrs: int = Field(default=0)
    RDrop: int = Field(default=0)
    RFifo: int = Field(default=0)
    RFrame: int = Field(default=0)
    RComporessed: int = Field(default=0)
    RMulticast: int = Field(default=0)


class Net:
    @classmethod
    def get_net_info(cls):
        net_info = Netnfo()
        # cmd: = fmt.Sprintf("cat %s/net/dev | tail -n +3 | sed 's/^\\s*//g' | sed 's/\\s\\+/|/g'", Ctx.Procfs)
        p1 = subprocess.Popen("cat /proc/net/dev".split(), shell=False, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("tail -n +3".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/^\\s*//g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/\\s\\+/|/g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p1.communicate()
        rc = p1.returncode
        if rc != 0:
            raise Exception(err)
        out = out.decode()
        for v in out.split("\n"):
            if v == "":
                continue
            NicStrs = v.split(":")
            infos = NicStrs[1].split("|")
            if len(infos) < 17:
                return net_info
            net_info.Nics.append(
                NicInfo(
                    Name=NicStrs[0],
                    RBytes=infos[1],
                    RPackets=infos[2],
                    RErrs=infos[3],
                    RDrop=infos[4],
                    RFifo=infos[5],
                    RFrame=infos[6],
                    RComporessed=infos[7],
                    RMulticast=infos[8],
                    TBytes=infos[9],
                    TPackets=infos[10],
                    TErrs=infos[11],
                    TDrop=infos[12],
                    TFifo=infos[13],
                    TFrame=infos[14],
                    TComporessed=infos[15],
                    TMulticast=infos[16],
                )
            )
        return net_info.dict()


if __name__ == '__main__':
    out = Net.get_net_info()
    print(out)
