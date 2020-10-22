# *_*coding:utf-8 *_*
import subprocess
from typing import List

from pydantic import BaseModel
from pydantic import Field


class NumaNode(BaseModel):
    Name: str = Field(default="")
    Cpus: str = Field(default="")


class Core(BaseModel):
    Name: str = Field(default="")
    User: int = Field(default=0)
    Nice: int = Field(default=0)
    System: int = Field(default=0)
    Idle: int = Field(default=0)
    Iowait: int = Field(default=0)
    Irq: int = Field(default=0)
    Softirq: int = Field(default=0)
    Steal: int = Field(default=0)
    Guest: int = Field(default=0)
    GuestNice: int = Field(default=0)


class CpuInfo(BaseModel):
    CoreNum: str = Field(default="")
    OnlineCore: str = Field(default="")
    Arch: str = Field(default="")
    CpuOpMode: str = Field(default="")
    ByteOrder: str = Field(default="")
    ThreadPerCore: int = Field(default=0)
    CorePerSocket: int = Field(default=0)
    Socket: int = Field(default=0)
    NumaNodeNum: int = Field(default=0)
    VendorId: str = Field(default="")
    CpuFamily: str = Field(default="")
    ModelName: str = Field(default="")
    Freq: str = Field(default="")
    HypervisorVendor: str = Field(default="")
    Virtualization: str = Field(default="")
    L1dCache: str = Field(default="")
    L1iCache: str = Field(default="")
    L2Cache: str = Field(default="")
    L3Cache: str = Field(default="")
    NumaNodes: List[NumaNode] = Field(default=[])
    Cores: List[Core] = Field(default=[])


class Cpu(object):
    @classmethod
    def get_core_info(cls):
        cores = []
        p1 = subprocess.Popen("cat /proc/stat".split(), shell=False, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("grep ^cpu[0-9]".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/\s\+/|/g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p1.communicate()
        rc = p1.returncode
        if rc != 0:
            raise Exception(err)
        out = out.decode()
        for v in out.split("\n"):
            if v == "":
                continue
            attrs = v.split("|")
            a = attrs
            core = Core()
            core.Name = attrs[0]
            core.User = attrs[0]
            core.Nice = attrs[1]
            core.System = attrs[2]
            core.Idle = attrs[3]
            core.Iowait = attrs[4]
            core.Irq = attrs[5]
            core.Softirq = attrs[6]
            if len(a) >= 8:
                core.Steal = a[7]
            if len(a) >= 9:
                core.Guest = a[8]
            if len(a) >= 10:
                core.GuestNice = a[9]
            cores.append(core.dict())

        return cores

    @classmethod
    def get_cpu_info(cls):
        cpu_info = CpuInfo()
        p1 = subprocess.Popen("lscpu".split(), shell=False, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("sed s/:\s*/:/g".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p1.communicate()
        rc = p1.returncode
        if rc != 0:
            raise Exception(err)
        out = out.decode()
        for v in out.split("\n"):
            if v == "":
                continue
            attrs = v.split(":")
            if attrs[0] == "Architecture":
                cpu_info.Arch = attrs[1]
            elif attrs[0] == "CPU op-mode(s)":
                cpu_info.CpuOpMode = attrs[1]
            elif attrs[0] == "Byte Order":
                cpu_info.ByteOrder = attrs[1]
            elif attrs[0] == "On-line CPU(s) list":
                cpu_info.OnlineCore = attrs[1]
            elif attrs[0] == "Thread(s) per core":
                cpu_info.ThreadPerCore = attrs[1]
            elif attrs[0] == "Core(s) per socket":
                cpu_info.CorePerSocket = attrs[1]
            elif attrs[0] == "Socket(s)":
                cpu_info.Socket = attrs[1]
            elif attrs[0] == "NUMA node(s)":
                cpu_info.NumaNodeNum = attrs[1]
            elif attrs[0] == "Vendor ID":
                cpu_info.VendorId = attrs[1]
            elif attrs[0] == "CPU family":
                cpu_info.CpuFamily = attrs[1]
            elif attrs[0] == "CPU MHz":
                cpu_info.Freq = attrs[1]
            elif attrs[0] == "Hypervisor vendor":
                cpu_info.HypervisorVendor = attrs[1]
            elif attrs[0] == "Virtualization type":
                cpu_info.Virtualization = attrs[1]
            elif attrs[0] == "L1d cache":
                cpu_info.L1dCache = attrs[1]
            elif attrs[0] == "L1i cache":
                cpu_info.L1iCache = attrs[1]
            elif attrs[0] == "L2 cache":
                cpu_info.L2Cache = attrs[1]
            elif attrs[0] == "L3 cache":
                cpu_info.L3Cache = attrs[1]
            if attrs[0] in ["NUMA node0 CPU(s)", "NUMA node1 CPU(s)", "NUMA node2 CPU(s)", "NUMA node3 CPU(s)"]:
                cpu_info.NumaNodes.append(NumaNode(Name=attrs[0], Cpus=attrs[1]))
        cpu_info.ModelName = cls.get_mode_name()
        cpu_info.Cores = cls.get_core_info()
        return cpu_info.dict()

    @classmethod
    def get_mode_name(cls):
        p1 = subprocess.Popen("cat /proc/cpuinfo".split(), shell=False, stdout=subprocess.PIPE)
        p1 = subprocess.Popen(["grep", "model name"], shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen("head -n1".split(), shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1 = subprocess.Popen(["sed", "s/^.*: //"], shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p1.communicate()
        rc = p1.returncode
        if rc != 0:
            raise Exception(err)
        return out.decode()


if __name__ == '__main__':
    out = Cpu.get_core_info()
    print(out)
    out = Cpu.get_cpu_info()
    print(out)
    out = Cpu.get_mode_name()
    print(out)
