# *_*coding:utf-8 *_*
from typing import List

from pydantic import BaseModel
from pydantic import Field
import subprocess


# asyncio.create_subprocess_exec

class MemInfo(BaseModel):
    MemTotal: int = Field(default=0)
    MemFree: int = Field(default=0)
    MemAvailable: int = Field(default=0)
    Buffers: int = Field(default=0)
    Cached: int = Field(default=0)
    SwapCached: int = Field(default=0)
    Active: int = Field(default=0)
    Inactive: int = Field(default=0)
    ActiveAnon: int = Field(default=0)
    InactiveAnon: int = Field(default=0)
    ActiveFile: int = Field(default=0)
    InactiveFile: int = Field(default=0)
    Unevictable: int = Field(default=0)
    Mlocked: int = Field(default=0)
    SwapTotal: int = Field(default=0)
    SwapFree: int = Field(default=0)
    Dirty: int = Field(default=0)
    Writeback: int = Field(default=0)
    AnonPages: int = Field(default=0)
    Mapped: int = Field(default=0)
    Shmem: int = Field(default=0)
    Slab: int = Field(default=0)
    SReclaimable: int = Field(default=0)
    SUnreclaim: int = Field(default=0)
    KernelStack: int = Field(default=0)
    PageTables: int = Field(default=0)
    NfsUnstable: int = Field(default=0)
    Bounce: int = Field(default=0)
    WritebackTmp: int = Field(default=0)
    CommitLimit: int = Field(default=0)
    CommittedAS: int = Field(default=0)
    VmallocTotal: int = Field(default=0)
    VmallocUsed: int = Field(default=0)
    VmallocChunk: int = Field(default=0)
    HardwareCorrupted: int = Field(default=0)
    AnonHugePages: int = Field(default=0)
    CmaTotal: int = Field(default=0)
    CmaFree: int = Field(default=0)
    HugePagesTotal: int = Field(default=0)
    HugePagesFree: int = Field(default=0)
    HugePagesRsvd: int = Field(default=0)
    HugePagesSurp: int = Field(default=0)
    Hugepagesize: int = Field(default=0)
    DirectMap4k: int = Field(default=0)
    DirectMap2M: int = Field(default=0)
    DirectMap1G: int = Field(default=0)

    UsedMem: int = Field(default=0)


class Memory(object):
    @classmethod
    def get_all(cls):
        mem_info = MemInfo()
        p1 = subprocess.Popen("cat /proc/meminfo".split(), shell=False, stdout=subprocess.PIPE)
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
            if attrs[0] == "MemTotal":
                mem_info.MemTotal = attrs[1]
            elif attrs[0] == "MemFree":
                mem_info.MemFree = attrs[1]
            elif attrs[0] == "MemAvailable":
                mem_info.MemAvailable = attrs[1]
            elif attrs[0] == "Buffers":
                mem_info.Buffers = attrs[1]
            elif attrs[0] == "Cached":
                mem_info.Cached = attrs[1]
            elif attrs[0] == "SwapCached":
                mem_info.SwapCached = attrs[1]
            elif attrs[0] == "Active":
                mem_info.Active = attrs[1]
            elif attrs[0] == "Inactive":
                mem_info.Inactive = attrs[1]
            elif attrs[0] == "Active(anon)":
                mem_info.ActiveAnon = attrs[1]
            elif attrs[0] == "Inactive(anon)":
                mem_info.InactiveAnon = attrs[1]
            elif attrs[0] == "Active(file)":
                mem_info.ActiveFile = attrs[1]
            elif attrs[0] == "Inactive(file)":
                mem_info.InactiveFile = attrs[1]
            elif attrs[0] == "Unevictable":
                mem_info.Unevictable = attrs[1]
            elif attrs[0] == "Mlocked":
                mem_info.Mlocked = attrs[1]
            elif attrs[0] == "SwapTotal":
                mem_info.SwapTotal = attrs[1]
            elif attrs[0] == "SwapFree":
                mem_info.SwapFree = attrs[1]
            elif attrs[0] == "Dirty":
                mem_info.Dirty = attrs[1]
            elif attrs[0] == "Writeback":
                mem_info.Writeback = attrs[1]
            elif attrs[0] == "AnonPages":
                mem_info.AnonPages = attrs[1]
            elif attrs[0] == "Mapped":
                mem_info.Mapped = attrs[1]
            elif attrs[0] == "Shmem":
                mem_info.Shmem = attrs[1]
            elif attrs[0] == "Slab":
                mem_info.Slab = attrs[1]
            elif attrs[0] == "SReclaimable":
                mem_info.SReclaimable = attrs[1]
            elif attrs[0] == "SUnreclaim":
                mem_info.SUnreclaim = attrs[1]
            elif attrs[0] == "KernelStack":
                mem_info.KernelStack = attrs[1]
            elif attrs[0] == "PageTables":
                mem_info.PageTables = attrs[1]
            elif attrs[0] == "NFS_Unstable":
                mem_info.NfsUnstable = attrs[1]
            elif attrs[0] == "Bounce":
                mem_info.Bounce = attrs[1]
            elif attrs[0] == "WritebackTmp":
                mem_info.WritebackTmp = attrs[1]
            elif attrs[0] == "CommitLimit":
                mem_info.CommitLimit = attrs[1]
            elif attrs[0] == "Committed_AS":
                mem_info.CommittedAS = attrs[1]
            elif attrs[0] == "VmallocTotal":
                mem_info.VmallocTotal = attrs[1]
            elif attrs[0] == "VmallocUsed":
                mem_info.VmallocUsed = attrs[1]
            elif attrs[0] == "VmallocChunk":
                mem_info.VmallocChunk = attrs[1]
            elif attrs[0] == "HardwareCorrupted":
                mem_info.HardwareCorrupted = attrs[1]
            elif attrs[0] == "AnonHugePages":
                mem_info.AnonHugePages = attrs[1]
            elif attrs[0] == "CmaTotal":
                mem_info.CmaTotal = attrs[1]
            elif attrs[0] == "CmaFree":
                mem_info.CmaFree = attrs[1]
            elif attrs[0] == "HugePages_Total":
                mem_info.HugePagesTotal = attrs[1]
            elif attrs[0] == "HugePages_Free":
                mem_info.HugePagesFree = attrs[1]
            elif attrs[0] == "HugePages_Rsvd":
                mem_info.HugePagesRsvd = attrs[1]
            elif attrs[0] == "HugePages_Surp":
                mem_info.HugePagesSurp = attrs[1]
            elif attrs[0] == "Hugepagesize":
                mem_info.Hugepagesize = attrs[1]
            elif attrs[0] == "DirectMap4k":
                mem_info.DirectMap4k = attrs[1]
            elif attrs[0] == "DirectMap2M":
                mem_info.DirectMap2M = attrs[1]
            elif attrs[0] == "DirectMap1G":
                mem_info.DirectMap1G = attrs[1]
        mem_info.UsedMem = cls.get_used_mem()
        return mem_info.dict()

    @classmethod
    def get_used_mem(cls):
        p1 = subprocess.Popen("free".split(), shell=False, stdout=subprocess.PIPE)
        p1 = subprocess.Popen(["awk", "NR==2 {print $3}"], shell=False, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p1.communicate()
        rc = p1.returncode
        if rc != 0:
            raise Exception(err)
        out = out.decode().strip()

        return out


if __name__ == '__main__':
    out = Memory.get_all()
    print(out)
    out = Memory.get_used_mem()
    print(out)
