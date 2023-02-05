#!/usr/bin/env python3
import asyncio
from typing import AsyncIterable

from yapapi import Golem, Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm
import datetime
import shlex
import uuid
import json

import apprise
apobj = apprise.Apprise()
env = json.load(open("../env.json"))
apobj.add(env["webhook"])


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    script = context.new_script(timeout=datetime.timedelta(hours=1))
    
    async for task in tasks:
        apobj.notify(body="starting job", title=f"task: {task.data} is starting")
        script.run(*shlex.split(f"/usr/local/bin/python3 /txt2img.py '{task.data}' '/golem/output/output.png' --offline"))
        output_file = f"output/image-{uuid.uuid1()}.png"
        script.download_file("/golem/output/output.png", output_file)
        
        yield script
        
        task.accept_result(result=output_file)
        apobj.notify(body="finished job", title=f"task: {task.data} is finished")


async def main():
    package = await vm.repo(
        image_hash="bf0bfedb65309eccab85ee6e93517d0bf66f7d00057a52cb45c299ef",
        image_url="http://auto-editor.online/images/dog.gvmi",
        min_mem_gib=6,
        min_storage_gib=8,
        min_cpu_threads=2
    )

    tasks = [Task(data=t) for t in ["hello world", "happy golem"]]

    async with Golem(budget=10.0, subnet_tag="public") as golem:
        async for completed in golem.execute_tasks(worker, tasks, payload=package, timeout=datetime.timedelta(hours=1)):
            print(completed.result.stdout)


if __name__ == "__main__":
    
    enable_default_logger(log_file=f"logs/log_{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log")

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)


